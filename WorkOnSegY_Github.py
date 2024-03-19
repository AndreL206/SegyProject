import pandas as pd
from Segy_Management import readSegY, writeSegY
from Print_Line import printLine
from Merge_Files import MergeTraceHeader 
from ScanForFiles import scanForFiles


#%% Read 1 SegY
OpenSegy_Parameters = {"path" : "Path of the file tou want to read", 
                       "endian" : "little", # little or big (big is SegY standard)
                       "encoding": "ascii"} # ascii or cp500 (EBCDIC)

SegY = readSegY(OpenSegy_Parameters["path"], OpenSegy_Parameters["endian"], OpenSegy_Parameters["encoding"])


#%% Read Multiple SegY
OpenSegy_Parameters = {"endian" : "little", # little or big (big is SegY standard)
                       "encoding": "ascii"} # ascii or cp500 (EBCDIC)
OpenedFileDict = {}
AllDataDict = {}

FilesInFolder = scanForFiles("Folder containing SEG or sgy or segy extension files")

for i in FilesInFolder:
    OpenedFileDict["Text_Header"], OpenedFileDict["Bin_Header"], OpenedFileDict["Trace_Header"], OpenedFileDict["Data"] = readSegY(FilesInFolder[i][1], OpenSegy_Parameters["endian"], OpenSegy_Parameters["encoding"])
    AllDataDict[FilesInFolder[i][0]] = OpenedFileDict


#%% Some example of coordinates conversion (arcsec to meters)

Coordinates = pd.DataFrame(SegY["Trace_Header"]["XSourceCoordinate"])
Coordinates["YSourceCoordinate"] = SegY["Trace_Header"]["YSourceCoordinate"] # Extract coordinates

Coordinates["X_Scalar"] = Coordinates["XSourceCoordinate"]*SegY["Trace_Header"]["ScalarForCoordinates"] #multiply by scalar ?? unused
Coordinates["Y_Scalar"] = Coordinates["YSourceCoordinate"]*SegY["Trace_Header"]["ScalarForCoordinates"]
Coordinates["X_Deg"] = Coordinates["XSourceCoordinate"]/3600 #CoordinateUnits = 2 so convert seconds of arc to meter
Coordinates["Y_Deg"] = Coordinates["YSourceCoordinate"]/3600
Coordinates["X_Deg_100"] = Coordinates["X_Deg"]/1000 ## get the correct range
Coordinates["Y_Deg_100"] = Coordinates["Y_Deg"]/1000
Coordinates["X_Scalar_Deg"] = Coordinates["X_Scalar"]/3600 #CoordinateUnits = 2 so convert seconds of arc to meter using scalar ?? unused
Coordinates["Y_Scalar_Deg"] = Coordinates["Y_Scalar"]/3600

Coordinates.to_csv('Coord_test.csv', sep=',', decimal='.')# Write the nav to csv


#%% Print figure of a line
AllDataDict.keys()
printLine(AllDataDict['The SegY line name']["Data"], 'The SegY line name' ) # %matplotlib qt 


#%% Write SegY
WriteSegy_Parameters = {"path" : "Your writing path name here", 
                        "endian" : "little", # little or big (big is SegY standard)
                        "encoding": "ascii"}

writeSegY(SegY["Text_Header"], SegY["Bin_Header"], SegY["Trace_Header"], SegY["Data"], WriteSegy_Parameters["path"], WriteSegy_Parameters["endian"], WriteSegy_Parameters["encoding"] )

