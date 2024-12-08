import shutil
import os

directory_path = os.path.join('dist')
if os.path.exists(directory_path):
    shutil.rmtree(directory_path)
    print(f"The directory {directory_path} has been deleted.")
else:
    print(f"Cannot find the directory {directory_path} ")
