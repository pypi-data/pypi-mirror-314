import os


def initializeFolderStructure(
    project_path: str,
) -> None:

    folders = ["templates", "mappings", "srcdata", "other"]
    for folder in folders:
        os.makedirs(os.path.join(project_path, folder), exist_ok=True)


def getMappingFilePath(projectname: str, local_project_path: str) -> str:
    return os.path.join(local_project_path, "mappings", f"{projectname}.csv")
