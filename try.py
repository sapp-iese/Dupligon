import hashlib
import os
from pathlib import Path
from collections import defaultdict

def get_directory_from_user():
    while True:
        directory = input("Enter the directory you wish to scan: ").strip()
        
        dir_path=Path(directory)
        
        if not dir_path.exists():
            print("doobara naam dekh!")
            continue
        if not dir_path.is_dir():
            print("Error: Paghal Samjha hua hai?")
            continue
        return dir_path
try:
    directory = get_directory_from_user()
    print(f"\n Scanning directory: {directory}")
    files = os.listdir(directory)    
except KeyboardInterrupt:
    print("\nOperation Cancelled by User")
except Exception as e:
    print(f"Error: {e} ")

# default dictionary is used coz it creates an empty list for new keys
file_hash_dict = defaultdict(list)




def get_file_hash(filepath):  # Changed parameter name to filepath for clarity
    hash_calculator = hashlib.sha256()
    if filepath.is_file():  # Check if it's a file
        try:
            with open(filepath, "rb") as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    hash_calculator.update(chunk)  
                return hash_calculator.hexdigest()
        except Exception as e:
            print(f"Error with file {filepath} : {e}")
            return None  
    return None  
def identify_duplicates_to_delete():
    duplicates_to_remove=[]
    for hash_value, filepath_list in file_hash_dict.items():
        if len(filepath_list) > 1:
            duplicates_to_remove.extend(filepath_list[1:])
    return duplicates_to_remove
# Process each file
for file in files:
    filepath = Path(directory) / file
    file_hash = get_file_hash(filepath)
    if file_hash:  # Only add to dictionary if we got a valid hash
        file_hash_dict[file_hash].append(filepath)

# Only prints duplicate files
for hash_value, filepath_list in file_hash_dict.items():  # Changed directory to filepath
    if len(filepath_list) > 1:
        print(f"\n The following files are identical: ")
        for filepath in filepath_list:
            print(f" {filepath}")
files_to_delete = identify_duplicates_to_delete()


def confirm_files_for_deletion(files_to_delete):
    print("\nFiles that would be deleted:")
    for file in files_to_delete:
        print(f"{file}")
    response = input("\nAre you sure you want to delete these files? (y/n)")
    return response.lower() == "y"



def delete_duplicate_files(files_to_delete):
    files_deleted=0
    for filepath in files_to_delete:
        try:
            os.remove(filepath)
            print(f"Deleted: {filepath}")
            files_deleted += 1
        except Exception as e:
            print(f"Error deleting {filepath}: {e}")
    return files_deleted

files_to_delete = identify_duplicates_to_delete()
if files_to_delete:
    if confirm_files_for_deletion(files_to_delete):
        deleted_count = delete_duplicate_files(files_to_delete)
        print(f"\nSuccessfully deleted {deleted_count} duplicate_files")
    else:
        print("Deletion Cancelled")
else:
    print("No duplicate files found")