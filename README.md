# SegyProject
Codes to work with SegY file format while keeping it as simple as possible. Still work in progress (19-03-24).

Current possibilities : open SegY file from bytes (unique or as a batch process) and rewrite (one by one for now), print the seismic line as an image. 
Contains some example of coordinates processing (done manually at the moment).

Reading is stating to get more robust than the early version.

Reading is available with multiple parameters that have to be tweaked manually :
 - little and big endian are supported (auto recognition will be implemented someday)
 - EBCDIC and ASCII textual headers can be read (auto recognition will be implemented as well)
 - IEEE and IBM bytes encoding (Those are recognized automatically, and are the two most used of the six allowed in SegY encoding)

File encodingand writing remains a lot more rigid than reading, only allowing  writing iine IEEE floating point. Endian can be Little or Big and textual header can be written as EBCDIC or ASCII. 
All the modifocations between reading and writting should be done with care and respect to the SegY file format rev constraints.

If needed, you can find infos about SegY format [here](https://wiki.seg.org/wiki/SEG-Y).



