'''
# Idea behind this script
Some media files such as pictures or videos capture their original date in
metadata within the file. 
In order to organise these files by that datetime, which may differ from the
file creation datetime, the idea is to automatically rename them including 
their datetime info at the begining of the file name.

# Limitations
* It doesn't check if a file with the new name already exists, so it could
  potentially overwrite existing files.
* It doesn't check if the file already contains datetime info at the begining
  of its name.  
* It only renames images with EXIF data. It could be extended for video files.
* It doesn't produce any log file with the summary of the operations performed.
* It doesn't explore paths recursively.

# How to use this script
1. From the terminal:
>>> python prepend_datetime.py -f path_to_folder_with_files_to_rename

2. From other Python script:
>>> from prepend_datetime import prepend_datetime_to_filname
>>> # do your thing to retrive the path to the files to rename
>>> # then use the preprend_datetime_to_filename function for each of them
'''

import exifread  # to extract metadata from picture files
import os

def prepend_datetime_to_filename(filepath: os.path) -> None:
    '''Given a file, it tries to retrieve its creation datetime data, and
       it prepends that information to the file name.'''
    file_datetime = get_original_datetime(filepath)
    if file_datetime is None:
        return

    folderpath = os.path.dirname(filepath)
    filename = os.path.basename(filepath)

    new_filename = "{} {}".format(file_datetime, filename)
    new_filepath = os.path.join(folderpath, new_filename)

    os.rename(filepath, new_filepath)

def apply_function_to_files_in_folder(folderpath, function):
    '''Given a path and a function, 
       the function is applied to all files in the folder.'''
    for (dirpath, dirnames, filenames) in os.walk(folderpath):
        for filename in filenames:
            function(os.path.join(dirpath, filename))

def get_original_datetime(filepath):
    '''Given a file path, it tries to retrieve the date when the file was
       originally created.'''
    # this could be generalised for other file types like videos with this:
    # https://stackoverflow.com/questions/31507038/python-how-to-read-windows-media-created-date-not-file-creation-date
    try:
        with open(filepath, 'rb') as file:
            tags = exifread.process_file(file, stop_tag='EXIF DateTimeOriginal')
        
        # When converted to str, EXIF datetime looks like "YYYY:MM:DD hh:mm:ss",
        # and I want it like "YYYY-MM-DD hh.mm.ss"
        file_datetime = str(tags['EXIF DateTimeOriginal'])
        file_datetime = file_datetime.replace(':', '-', 2).replace(':', '.', 2)

        return file_datetime

    except:
        return None

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    arg_help = "Relative or absolute path to folder with files to rename"
    parser.add_argument('-f', '--folderpath', help=arg_help, 
                        default=os.path.dirname(__file__))
    arguments = parser.parse_args()
    folderpath = arguments.folderpath

    apply_function_to_files_in_folder(folderpath, prepend_datetime_to_filename)