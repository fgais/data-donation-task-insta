
import os
import zipfile

def read_file_from_zip(zip_file, target_filename):
    """
    Reads the content of a file within a ZIP archive, 
    searching through subdirectories.

    Args:
        zip_filename: The name of the ZIP file.
        target_filename: The name of the file to read.

    Returns:
        The file content as bytes, or None if the file is not found.
    """
    for info in zip_file.infolist():
        #print(info.filename, target_filename)

        if info.filename.endswith(target_filename):  # Match filename at the end
            #print("ENDFILENAME MATCH")
            path = info.filename
            return path  # Read and return file content
    return None  # File not found in the ZIP
