import os

def scanForFiles (directory) : 
    i=0; FilesInFolder = {}
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".sgy") or filename.endswith(".segy") or filename.endswith(".SEG"): 
            # print(os.path.join(directory, filename))
            FilesInFolder[i] = (filename, os.path.join(directory, filename))
            i = i+1
            continue
        else:
            continue
    print("Scanning done")
    return FilesInFolder

