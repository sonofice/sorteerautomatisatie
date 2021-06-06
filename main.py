import os, sys, time, requests, datetime, shutil, platform
from pathlib import Path
from zipfile import ZipFile
from datetime import datetime

#Dictionary (Add more if you want)
#In this dictionary I added some extra extensions and changed the name of an entry (python --> Code)
DIRECTORIES = {
    "HTML": [".html5", ".html", ".htm", ".xhtml"],
    "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
               ".heif", ".psd"],
    "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng",
               ".qt", ".mpg", ".mpeg", ".3gp", ".mkv"],
    "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                  "pptx"],
    "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
                 ".dmg", ".rar", ".xar", ".zip"],
    "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
              ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
    "PLAINTEXT": [".txt", ".in", ".out"],
    "PDF": [".pdf"],
    "CODE": [".py", ".php", ".yml", ".yaml", ".js"],
    "XML": [".xml"],
    "EXECUTABLES": [".exe", ".msi"],
    "SHELL": [".sh", ".ps1"]
}

FILE_FORMATS = {file_format: directory
                for directory, file_formats in DIRECTORIES.items()
                for file_format in file_formats}

def download_file():
    while True:
        try:
            amount = int(input("How many file do you want to download: "))
            break

        except ValueError:
            print("that's not a number.")

    for i in range(amount):
        url = input("Fill in the URL: ")
        filename = url.split("/")[ -1]
        r = requests.get(url, allow_redirects=True, stream=True)
        with open(filename, "wb") as local_file:
            for data in r:
                local_file.write(data)


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return datetime.fromtimestamp(stat.st_birthtime)
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return datetime.fromtimestamp(stat.st_mtime)

def move_file_to_folder(sourceLocation: str, destinationLocation: str):
    try:
        os.mkdir(destinationLocation)
        shutil.move(sourceLocation, destinationLocation)
    except:
        pass


def sort_by_date():
    for entry in os.scandir():
        if entry.is_dir():
            folder = os.path.join(entry)
            filesInFolder = os.listdir(folder)

            for file in filesInFolder:
                file_path = os.path.join(os.getcwd(), folder, file)
                file_creation_date = creation_date(file_path)

                print(file_path)
                print(file_creation_date)
                full_month_name_of_file = file_creation_date.strftime("%B")
                
                destionation_folder = os.path.join(os.getcwd(), folder, full_month_name_of_file)
                move_file_to_folder(file_path, destionation_folder)

            print (folder, "\nnext")
    scan = os.scandir(folder)
    print(scan)


#This will organise your files
def main():

    for entry in os.scandir():
        print("Current dir", entry.name)
        if entry.is_dir():
            continue
        file_path = Path(entry.name)
        file_format = file_path.suffix.lower()
        if file_format in FILE_FORMATS:
            directory_path = Path(FILE_FORMATS[file_format])
            directory_path.mkdir(exist_ok=True)
            file_path.rename(directory_path.joinpath(file_path))
   #if extension not present in the dictionary than create a folder name "OTHER"
    try:
        os.mkdir("OTHER")
    except:
        pass
    for dir in os.scandir():
        try:
            if dir.is_dir():
                os.rmdir(dir)
            else:
                os.rename(os.getcwd() + '/' + str(Path(dir)), os.getcwd() + '/OTHER/' + str(Path(dir)))
        except:
            pass

if __name__ == "__main__":
    download_file()
    main()
    sort_by_date()
