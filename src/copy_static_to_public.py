import os
import shutil


def copy_files(
    src_path: str = "./static", target_path: str = "./public", empty_target=True
):
    """
    Method to copy files from within src_path (source) into target_path (target)
    param:
        src_path: str repr of source path (path having the files to copy)
        target_path: str repr of target path (path having the files to copy into)
        empty_target: empty the contents of the target path every run for idempotency;
            DEFAULT: True
    """
    # if src dir does not exist
    if not os.path.exists(src_path):
        raise ValueError(f"Source path does not exist: {src_path}")

    # If we need to empty the target path
    if empty_target:
        if os.path.exists(target_path):
            shutil.rmtree(target_path)

    # create target path if it does not exist
    if not os.path.exists(target_path):
        os.mkdir(target_path)

    # iterate over the files in the source
    for file_folder in os.listdir(src_path):
        file_source = os.path.join(src_path, file_folder)
        file_target = os.path.join(target_path, file_folder)

        # if file_folder is a file
        if os.path.isfile(file_source):
            print(f"""Copying {file_folder} from {file_source} to {file_target}""")
            shutil.copyfile(
                src=file_source,
                dst=file_target,
            )
        # if file_folder is a folder
        else:
            copy_files(file_source, file_target)

# to test
if __name__ == "__main__":
    copy_files()
