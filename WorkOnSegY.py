import os
os.chdir("D:\\SegyProject\\")
import pandas as pd
import numpy as np
import struct
from Segy_Management import readSegY, writeSegY



# =============================================================================
#%% Read SegY
# =============================================================================
global Segy_Structure;Segy_Structure = {}
Segy_Structure["endian"] = 'big' 
Segy_Structure["encoding"] = 'cp500' 
Segy_Structure["TextH_byte_len"] = 3200
Segy_Structure["BinH_byte_len"] = 400
Segy_Structure["TraceH_byte_len"] = 240
Segy_Structure["SegYFolder"] = "D:\\SegyProject\\"
Segy_Structure["ReadPath"] = Segy_Structure["SegYFolder"] + "filename_read.sgy"
Segy_Structure["WritePath"] = Segy_Structure["SegYFolder"] + "filename_write.sgy"

Text_Header, Bin_Header, Trace_Header, Data = readSegY(Segy_Structure["ReadPath"], Segy_Structure["endian"], Segy_Structure["encoding"])

# =============================================================================
#%%
# =============================================================================


# =============================================================================
#%% Write SegY
# =============================================================================

writeSegY(Text_Header, Bin_Header, Trace_Header, Data, Segy_Structure["WritePath"])

