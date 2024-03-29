# =============================================================================
# Def func to read segy 
# =============================================================================
import pandas as pd
import numpy as np
import struct 
global Text_Header;  Text_Header ={}; 
global Bin_Header;Bin_Header = {}; 
global Segy_Structure; Segy_Structure = {};
Segy_Structure["TextH_byte_len"] = 3200
Segy_Structure["BinH_byte_len"] = 400
Segy_Structure["TraceH_byte_len"] = 240

def ibm2ieee(bytes_):
    
    #Converts an IBM floating point number into IEEE format
    ibm = int.from_bytes( bytes_, 'big', signed=False)
    
    if ibm == 0:
        return 0.0
    sign = ibm >> 31 & 0x01
    exponent = ibm >> 24 & 0x7f
    mantissa = (ibm & 0x00ffffff) / float(pow(2, 24))
    return (1 - 2 * sign) * mantissa * pow(16, exponent - 64)
 
def readSegY(path, endian, encoding):

    with open(path, mode="rb") as file:
        Segy_bytes = file.read()

# =============================================================================
#  Read Text Header
# =============================================================================

    ByteStart = 0 
    ByteEnd = 80
    Index = 0

    
    while ByteEnd<=3200 :
        Text_Header[Index] = Segy_bytes[ByteStart:ByteEnd].decode(encoding)
        Index = Index + 1 
        ByteStart = ByteEnd 
        ByteEnd = ByteEnd + 80
        
    print('Text Header written')
    
# =============================================================================
#  Read Binary Header
# =============================================================================
    Bin_Header["JobID"]                 = int.from_bytes(Segy_bytes[3200:3204], endian)
    Bin_Header["LineNumber"]            = int.from_bytes(Segy_bytes[3204:3208], endian)
    Bin_Header["ReelNumber"]            = int.from_bytes(Segy_bytes[3208:3212], endian)
    Bin_Header["DataTracesPerRecord"]   = int.from_bytes(Segy_bytes[3212:3214], endian)
    Bin_Header["AuxTracesPerRecord"]    = int.from_bytes(Segy_bytes[3214:3216], endian)
    Bin_Header["ReelSampleInterval"]    = int.from_bytes(Segy_bytes[3216:3218], endian)
    Bin_Header["FieldSampleInterval"]   = int.from_bytes(Segy_bytes[3218:3220], endian)
    Bin_Header["ReelSamplesPerTrace"]   = int.from_bytes(Segy_bytes[3220:3222], endian)
    Bin_Header["FieldSamplesPerTrace"]  = int.from_bytes(Segy_bytes[3222:3224], endian)
    Bin_Header["DataSampleFormat"]      = int.from_bytes(Segy_bytes[3224:3226], endian)
    Bin_Header["CDPFold"]               = int.from_bytes(Segy_bytes[3226:3228], endian)
    Bin_Header["TraceSorting"]          = int.from_bytes(Segy_bytes[3228:3230], endian)
    Bin_Header["VerticalSumming"]       = int.from_bytes(Segy_bytes[3230:3232], endian)
    Bin_Header["StartSweepFrq"]         = int.from_bytes(Segy_bytes[3232:3234], endian)
    Bin_Header["EndSweepFrq"]           = int.from_bytes(Segy_bytes[3234:3236], endian)
    Bin_Header["SweepLength"]           = int.from_bytes(Segy_bytes[3236:3238], endian)
    Bin_Header["SweepType"]             = int.from_bytes(Segy_bytes[3238:3240], endian)
    Bin_Header["SweepChannelIndex"]     = int.from_bytes(Segy_bytes[3240:3242], endian)
    Bin_Header["SweepStartTaper"]       = int.from_bytes(Segy_bytes[3242:3244], endian)
    Bin_Header["SweepEndTaper"]         = int.from_bytes(Segy_bytes[3244:3246], endian)
    Bin_Header["TaperType"]             = int.from_bytes(Segy_bytes[3246:3248], endian)
    Bin_Header["CorrelatedTraces"]      = int.from_bytes(Segy_bytes[3248:3250], endian)
    Bin_Header["BinaryGainRecovered"]   = int.from_bytes(Segy_bytes[3250:3252], endian)
    Bin_Header["AmplitudeRecovery"]     = int.from_bytes(Segy_bytes[3252:3254], endian)
    Bin_Header["MeasurementSystem"]     = int.from_bytes(Segy_bytes[3254:3256], endian)
    Bin_Header["SignalPolarity"]        = int.from_bytes(Segy_bytes[3256:3258], endian)
    Bin_Header["VibratoryPolarity"]     = int.from_bytes(Segy_bytes[3258:3260], endian)
    Bin_Header["Unassigned1"]            = int.from_bytes(Segy_bytes[3260:3500], endian)
    Bin_Header["RevNumber"]             = int.from_bytes(Segy_bytes[3500:3502], endian)
    Bin_Header["FixedLength]"]          = int.from_bytes(Segy_bytes[3502:3504], endian)
    Bin_Header["NumberOfTextualHeader"] = int.from_bytes(Segy_bytes[3504:3506], endian)
    Bin_Header["Unassigned2"]            = int.from_bytes(Segy_bytes[3506:3600], endian)
    
    print('Binary Header written')

# =============================================================================
# Read Trace Header and Data
# =============================================================================
    
    b_loop = Bin_Header["ReelSamplesPerTrace"]*4 + Segy_Structure["TraceH_byte_len"] 
    print("Reading Traces ...")
    
    Trace_Header = pd.DataFrame( columns = ['TraceSequenceLine','TraceSequenceReel','FieldRecordNumber','TraceSequenceRecord',
                                           'ShotPointNumber','CDPNumber','TraceSequenceCDP','TraceIdentificationCode',
                                           'NumberVerticalSummedTr','NumberHorizontalStackedTr','DataUse','DistanceSPtoReceiver', 'ReceiverElevation',
                                           'SourceSurfaceElevation','SourceDepth','DatumElevationAtReceiver','DatumElevationAtSource',
                                           'WaterDepthAtSource','WaterDepthAtReceiver','ScalarForElevationDepth','ScalarForCoordinates',
                                           'XSourceCoordinate','YSourceCoordinate','XReceiverCoordinate','YReceiverCoordinate',
                                           'CoordinateUnits','WeatheringVelocity','SubWeatheringVelocity','UpholeTimeAtSource',
                                           'UpholeTimeAtReceiver','SourceStaticCorrection','ReceiverStaticCorrection','TotalStaticCorrection',
                                           'LagTimeHeaderBreak','LagTimeBreakShot','LagTimeShotRecording','StartMuteTime',
                                           'EndMuteTime','NumberOfSamples','SampleInterval','InstrumentGainCode',
                                           'InstrumentGainConstant','InstrumentGainDB','Correlated','StartSweepFrq',
                                           'EndSweepFrq','SweepLength','SweepType','SweepStartTaper',
                                           'SweepEndTaper','TaperType','AliasFilterFrq','AliasFilterSlope',
                                           'NotchFilterFrq','NotchFilterSlope','LowCutFrq','HighCutFrq','LowCutSlope',
                                           'HighCutSlope','YearDataRecorded','Day','Hour','Minute','Second','TimeBasis',
                                           'TraceWeightingFactor','GeophoneNumberRollSwitch','GeophoneNumberFirstTrace',
                                           'GeophoneNumberLastTrace','GapSize','TaperOvertravel','XcdpCoordinate',
                                           'YcdpCoordinate','InLineNb','CdpNb','ShotPointNb','ScalarToShotPonitNb',
                                           'TraceValueMesUnit','Transduction','TransductionUnit','TraceIdentifier',
                                           'ScalarToTime','SourceType','SourceEnergy','SourceMeasurementMantissa',
                                           'SourceMeasurementExponent','SourceMeasurementUnit','unassigned','unassigned','unassigned'])
    
    global Data;Data = pd.DataFrame(); 
    Traces = []
    
    TraceNb = 0
    TCount = 1
    Bin_Header["DataTracesPerRecord"] = int((len(Segy_bytes) - 3600)/(Bin_Header["ReelSamplesPerTrace"]*4+240))
    
    while TraceNb < Bin_Header["DataTracesPerRecord"]:
        v = 3200 + 400+ TraceNb*b_loop    
        Byte = 0
        Bytes_6 = [204, 218]
        Bytes_4 = [0,4,8,12,16,20,24,36,40,44,48,52,56,60,64,72,76,80,84,180,184,188,192,196,224,234]
        Header_Trame = []
        
        while Byte < Segy_Structure["TraceH_byte_len"] :
            
            if Byte in Bytes_4 : 
                Header_Trame.append(int.from_bytes(Segy_bytes[v+Byte:v+Byte+4], endian)); Byte = Byte+4
            elif Byte in Bytes_6 : 
                Header_Trame.append(int.from_bytes(Segy_bytes[v+Byte:v+Byte+6], endian)); Byte = Byte+6
            else:
                Header_Trame.append(int.from_bytes(Segy_bytes[v+Byte:v+Byte+2], endian)); Byte = Byte+2
        
        Trace_Header.loc[TraceNb] = Header_Trame
    
        x = 0
        z = Segy_Structure["TraceH_byte_len"]+v
        a = Segy_Structure["TraceH_byte_len"]+4+v 
        if Bin_Header['DataSampleFormat'] == 1:
            while z < (Segy_Structure["TraceH_byte_len"]+v+(Bin_Header["ReelSamplesPerTrace"]*4)):   
                Traces.append(ibm2ieee(Segy_bytes[z:a]))
                x = x+1 
                z = a 
                a = a+4 
        elif Bin_Header['DataSampleFormat'] == 2: return f'Format not supported ({Bin_Header["DataSampleFormat"]}), will be implemented'
        elif Bin_Header['DataSampleFormat'] == 3: return f'Format not supported ({Bin_Header["DataSampleFormat"]}), will be implemented'
        elif Bin_Header['DataSampleFormat'] == 4: return f'Format not supported ({Bin_Header["DataSampleFormat"]}), will be implemented'
        elif Bin_Header['DataSampleFormat'] == 5: 
            while z < (Segy_Structure["TraceH_byte_len"]+v+(Bin_Header["ReelSamplesPerTrace"]*4)):   
                Traces.append(struct.unpack('f', Segy_bytes[z:a]))
                x = x+1 
                z = a 
                a = a+4
        # 6 and 7 are currently not used in segy Rev1 stadards
        elif Bin_Header['DataSampleFormat'] == 8: Traces.append(struct.unpack('f', Segy_bytes[z:a]))
        else : return f'Format not recognized ({Bin_Header["DataSampleFormat"]}), consider changing endian ?'
                        
        TraceNb= TraceNb+1
        if TraceNb % 1000 == 0: 
            print(f'{TCount}000 traces read out of {Bin_Header["DataTracesPerRecord"]}'); TCount = TCount+1
            
    Data = np.reshape(Traces, (Bin_Header["DataTracesPerRecord"],Bin_Header["ReelSamplesPerTrace"])).T
    print("Traces written")
        
    SegY = {"Text_Header":Text_Header ,"Bin_Header": Bin_Header, "Trace_Header":Trace_Header, "Data":Data}
    return SegY

# =============================================================================
# %% Def func to write Segy 
# =============================================================================

def writeSegY(SegY, path, endian, encoding ):
    Text_Header = SegY["Text_Header"]
    Bin_Header = SegY["Bin_Header"]
    Trace_Header = SegY["Trace_Header"]
    Data = SegY["Data"]
    
# =============================================================================
# Encode Text Header
# =============================================================================
    
    Index = 0
    while Index<len(Text_Header) :
        if Index ==0 :
            ByteArray_TextHeader = Text_Header[Index].encode(encoding)
        else : ByteArray_TextHeader = ByteArray_TextHeader + Text_Header[Index].encode(encoding)
        Index = Index + 1 
        
    print('Text Header encoded')
    
# =============================================================================
# Encode Bin  Header
# =============================================================================
    
    Bin_Header['DataSampleFormat'] = 5 # To update
    
    bytes_increment=[4,4,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,240,2,2,2,94]
    Byte_Bin_Header =list(Bin_Header.values())
    Index = 0
    while Index<len(Bin_Header) :
        if Index ==0 :
            ByteArray_BinHeader = Byte_Bin_Header[Index].to_bytes(bytes_increment[Index], endian)
        else : ByteArray_BinHeader = ByteArray_BinHeader + Byte_Bin_Header[Index].to_bytes(bytes_increment[Index], endian)
        Index = Index+1 
    
    print('Bin Header encoded')
    
    MainHeader = ByteArray_TextHeader + ByteArray_BinHeader
    
# =============================================================================
# Encode Data Header
# =============================================================================
    TraceNb = 0 
    TCount = 1
    Bytes_6 = [204, 218]
    Bytes_4 = [0,4,8,12,16,20,24,36,40,44,48,52,56,60,64,72,76,80,84,180,184,188,192,196,224,234]
    
    print("Encoding traces ...")
    
    while TraceNb < Bin_Header["DataTracesPerRecord"] :
        ByteNb = 0
        SampleNb = 0
        while ByteNb < Segy_Structure["TraceH_byte_len"]:
            if ByteNb in Bytes_4 : 
                Converted_Byte = Trace_Header.iloc[TraceNb, SampleNb].tolist().to_bytes(4, endian)
                ByteNb = ByteNb + 4
                SampleNb = SampleNb+1
            elif ByteNb in Bytes_6 : 
                Converted_Byte = Trace_Header.iloc[TraceNb, SampleNb].tolist().to_bytes(6, endian)
                ByteNb = ByteNb+6
                SampleNb = SampleNb+1
            else:
                Converted_Byte = Trace_Header.iloc[TraceNb, SampleNb].tolist().to_bytes(2, endian)
                ByteNb = ByteNb+2
                SampleNb = SampleNb+1
            if ByteNb == 4 : Byte_Array = Converted_Byte
            else: Byte_Array = Byte_Array + Converted_Byte
            
        MainHeader = MainHeader + Byte_Array
            
        count = 0
        
        while count < Bin_Header["FieldSamplesPerTrace"]:
            if count == 0 : Byte_Array = struct.pack(">f", Data[count, TraceNb])
            else : Byte_Array = Byte_Array +  struct.pack(">f", Data[count, TraceNb])
            count = count +  1
        
        MainHeader = MainHeader + Byte_Array
        
        TraceNb = TraceNb + 1 
        if TraceNb % 1000 == 0: print(f'{TCount}000 traces read out of {Bin_Header["DataTracesPerRecord"]}'); TCount = TCount+1
    
    print("Traces encoded")
    
    #Write to path
    
    f = open(path, "wb")
    f.write(MainHeader)
    f.close()   

