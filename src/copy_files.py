import os
import shutil


# delete all the contents of the destination directory first
# recursively copy all the files and subdirectories, nested files, etc
# from source to destination
def copy_files(source, destination):
    print(
        f"copying contents of source directory {source} into destination directory {destination}..."
    )

    if not os.path.exists(source):
        raise Exception(f"source path does not exist: {source}")

    if os.path.exists(destination):
        print(f"deleting and re-creating destination directory: {destination}")
        shutil.rmtree(destination)
        print(f"destination directory {destination} is deleted!")
    os.mkdir(destination)
    print(f"destination directory {destination} is created!")

    source_files = os.listdir(source)
    print(f"contents of source directory {source} are as follows: {source_files}")

    for source_file in source_files:
        source_file_path = os.path.join(source, source_file)
        if os.path.isfile(source_file_path):
            print(f"copying file from {source_file_path}")
            destination_file_path = shutil.copy(source_file_path, destination)
            print(f"copied file to {destination_file_path}")
        else:
            print(f"{source_file_path} is a directory")
            destination_dir = os.path.join(destination, source_file)
            copy_files(source_file_path, destination_dir)
