import logging
import os
import re
import tempfile
import pandas as pd
from nemo_library.features.config import Config
from nemo_library.features.fileingestion import ReUploadFile
from nemo_library.features.projects import (
    LoadReport,
    createImportedColumn,
    createOrUpdateReport,
    createProject,
    getImportedColumns,
    getProjectList,
)
from nemo_library.utils.utils import display_name, import_name, internal_name

__all__ = ["updateMappingForMigman"]


def updateMappingForMigman(
    config: Config,
    fields: list[str],
    folderForMappingFiles: str,
    additionalfields: dict[str, str] = None,
):

    for field in fields:

        additionalFields = (
            additionalfields[field] if field in additionalfields else None
        )

        # create project if needed
        projectList = getProjectList(config=config)["displayName"].to_list()
        projectame = f"Mapping {field}"

        newProject = False
        if not projectame in projectList:
            newProject = True
            createMappingProject(config=config, field=field, projectname=projectame)

            # update list of fields
            createMappingImportedColumnns(
                config=config,
                projectname=projectame,
                field=field,
                additionalFields=additionalFields,
            )

            # we need to ensure that the table in the database is created. Either we have data,
            # then we upload it. Or we have to create dummy data
            loadData(
                config=config,
                projectname=projectame,
                field=field,
                additionalFields=additionalFields,
                folderForMappingFiles=folderForMappingFiles,
                newProject=newProject,
            )

        # collect data
        collectData(
            config=config,
            projectname=projectame,
            field=field,
            additionalFields=additionalFields,
            folderForMappingFiles=folderForMappingFiles,
        )


def createMappingProject(
    config: Config,
    projectname: str,
    field: str,
) -> str:
    """
    Creates a mapping project for a specific field if it does not already exist.

    This function checks if a project with the name "Mapping {field}" exists in the system.
    If it does not exist, it creates the project with a description. The function then
    returns the name of the project.

    Args:
        config (Config): Configuration object containing authentication and system settings.
        field (str): The name of the field for which the mapping project is to be created.

    Returns:
        str: The name of the mapping project.
    """

    logging.info(f"'{projectname}' not found, create it")
    createProject(
        config=config,
        projectname=projectname,
        description=f"Mapping for field '{field}'",
    )


def createMappingImportedColumnns(
    config: Config,
    projectname: str,
    field: str,
    additionalFields: list[str],
) -> dict[str, str]:

    fields = []
    fields.append(display_name(f"source {field}"))
    fields.append(display_name(f"target {field}"))

    if additionalFields:
        for additionalField in additionalFields:
            fields.append(display_name(f"source {additionalField}"))
            fields.append(display_name(f"target {additionalField}"))

    importedColumnsList = getImportedColumns(config=config, projectname=projectname)
    importedColumnsList = (
        importedColumnsList["displayName"].to_list()
        if not importedColumnsList.empty
        else []
    )

    for fld in fields:
        if not fld in importedColumnsList:
            createImportedColumn(
                config=config,
                projectname=projectname,
                displayName=fld,
                internalName=internal_name(fld),
                importName=import_name(fld),
                dataType="string",
                description="",
            )


def loadData(
    config: Config,
    projectname: str,
    field: str,
    additionalFields: list[str],
    folderForMappingFiles,
    newProject: bool,
) -> None:

    # project is new and table does not exist. We have to upload dummy-data to enforce creation of database table

    # "real" data given? let's take this instead of the dummy file
    file_path = os.path.join(folderForMappingFiles, f"{projectname}.csv")
    logging.info(f"checking for data file {file_path}")

    if os.path.exists(file_path):
        ReUploadFile(
            config=config,
            projectname=projectname,
            filename=file_path,
            update_project_settings=False,
        )
        logging.info(f"upload to project {projectname} completed")
    else:
        if newProject:
            logging.info(
                f"file {file_path} for project {file_path} not found. Uploading dummy data"
            )
            fields = getImportedColumns(config=config, projectname=projectname)[
                "importName"
            ]
            data = {field: ["xxx"] * 5 for field in fields}
            df = pd.DataFrame(data)

            # Write to a temporary file and upload
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, "tempfile.csv")

                df.to_csv(
                    temp_file_path,
                    index=False,
                    sep=";",
                    na_rep="",
                )
                logging.info(
                    f"dummy file {temp_file_path} written for project '{projectname}'. Uploading data to NEMO now..."
                )

                ReUploadFile(
                    config=config,
                    projectname=projectname,
                    filename=temp_file_path,
                    update_project_settings=False,
                )
                logging.info(f"upload to project {projectname} completed")


def collectData(
    config: Config,
    projectname: str,
    field: str,
    additionalFields: list[str],
    folderForMappingFiles: None,
):

    projectList = getProjectList(config=config)["displayName"].to_list()
    ctefields = {}
    for project in projectList:
        fields = collectDataFieldsForProject(
            config=config,
            project=project,
            field=field,
            additionalFields=additionalFields,
        )
        if fields:
            ctefields[project] = fields

    if len(ctefields) > 0:
        queryforreport = sqlQuery(project=projectname, ctefields=ctefields)
        createOrUpdateReport(
            config=config,
            projectname=projectname,
            displayName="source mapping",
            querySyntax=queryforreport,
            description="load all source values and map them"            
        )


def collectDataFieldsForProject(
    config: Config,
    project: str,
    field: str,
    additionalFields: list[str],
) -> list[str]:

    fieldList = None
    if project in ["Business Processes", "Master Data"] or project.startswith(
        "Mapping "
    ):
        return None

    imported_columns = getImportedColumns(config=config, projectname=project)[
        "displayName"
    ].to_list()
    result = next(
        (
            entry
            for entry in imported_columns
            if re.match(rf"^{re.escape(field)} \(\d{{3}}\)$", entry)
        ),
        None,
    )
    if result:
        logging.info(f"Found field '{result}' in project '{project}'")

        fieldList = {field: internal_name(result)}

        # check for additional fields now
        if additionalFields:
            for additionalField in additionalFields:
                result = next(
                    (
                        entry
                        for entry in imported_columns
                        if re.match(
                            rf"^{re.escape(additionalField)} \(\d{{3}}\)$", entry
                        )
                    ),
                    None,
                )
                if not result:
                    logging.info(
                        f"Field '{additionalField}' not found in project '{project}'. Skip this project"
                    )

                fieldList[additionalField] = internal_name(result)

    # we have found all relevant fields in project. Now we are going to collect data
    return fieldList


def sqlQuery(project: str, ctefields: dict[str, str]) -> str:

    # setup CTEs to load data from source projects
    ctes = []
    for ctekey, ctevalue in ctefields.items():

        subselect = [
            f'{fldvalue} AS "{fldkey}"' for fldkey, fldvalue in ctevalue.items()
        ]

        ctes.append(
            f"""CTE_{internal_name(ctekey)} AS (
    SELECT DISTINCT
        {"\n\t,".join(subselect)}
    FROM 
        $schema.PROJECT_{internal_name(ctekey)}
)"""
        )

    # create a union for all CTEs
    globfrags = []
    for ctekey, ctevalue in ctefields.items():

        subselect = [f'"{fldkey}"' for fldkey, fldvalue in ctevalue.items()]

        globfrags.append(
            f"""\tSELECT
    {"\n\t,".join(subselect)}
    FROM 
        CTE_{internal_name(ctekey)}"""
        )
    ctes.append(
        f"""CTE_ALL AS (
{"\nUNION ALL\n".join(globfrags)})"""
    )

    # and finally one for distinct value and join it with potentially existing data

    # we need to get a list of the fields itself. We assume they are the same in every CTE
    first_key = next(iter(ctefields))
    first_value = ctefields[first_key]
    subselect = [f'"{fldkey}"' for fldkey, fldvalue in first_value.items()]

    queryctes = f"""WITH {"\n,".join(ctes)}
,CTE_ALL_DISTINCT AS (
    SELECT DISTINCT
        {'\n\t,'.join(subselect)}
    FROM 
        CTE_ALL
)"""

    subselectsrc = [
        f'cte."{fldkey}" as "source {fldkey}"'
        for fldkey, fldvalue in first_value.items()
    ]
    subselecttgt = [
        f'mapping.TARGET_{internal_name(fldkey)} as "target {fldkey}"'
        for fldkey, fldvalue in first_value.items()
    ]
    subselectjoin = [
        f'mapping.SOURCE_{internal_name(fldkey)} = cte."{fldkey}"'
        for fldkey, fldvalue in first_value.items()
    ]
    finalquery = f"""{queryctes}
SELECT
    {'\n\t,'.join(subselectsrc)}
    , {'\n\t,'.join(subselecttgt)}
FROM
    CTE_ALL_DISTINCT cte
LEFT JOIN
    $schema.$table mapping
ON  
    {'\n\t AND '.join(subselectjoin)}
"""
    return finalquery
