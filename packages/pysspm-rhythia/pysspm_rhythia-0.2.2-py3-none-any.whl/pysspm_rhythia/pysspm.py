from io import BytesIO
from hashlib import sha1
from types import NoneType
from typing import BinaryIO
import numpy as np
from warnings import warn

# TODO: (In order of priority)
# Add typing support for library ✔️
# add proper documentation on github
# add proper documentation in code ✔️
# add loading of sspmV2  ✔️
# add support for creating sspmV2 ✔️
# clean up unused variables from @self ✔️
# add support for sspmv1 loading
# support multiple version of sspm
# add custom block support in loading
# fix small bugs...

"""
Stolen from the SSQE version lol
            var data = new List<byte>(); // final converted data
            data.AddRange(header);
            data.AddRange(hash);
            data.AddRange(metadata);
            data.AddRange(pointers);
            data.AddRange(strings);
            data.AddRange(customData);
            data.AddRange(audio);
            data.AddRange(cover);
            data.AddRange(markerDefinitions);
            data.AddRange(markers);
            return data.ToArray();
"""

class SSPMParser:
    """
    # SSPM Reader

    ### reads and converts Sound space plus maps into many other readable forms.

    for anyone interested in the "Amazing" documentation from the creator: <link>https://github.com/basils-garden/types/blob/main/sspm/v2.md</link>...
    <br>
    More to come soon...
    """

    INVALID_CHARS = {'/', '\\', ':', '*', '?', '"', '<', '>', '|'}
    HEADER_SIGNATURE = b'SS+m'
    DEFAULT_VERSION = b'\x02\x00'
    RESERVED_SPACE_V2 = b'\x00\x00\x00\x00'
    
    DIFFICULTIES = { 
        "N/A": 0x00,
        "Easy": 0x01,
        "Medium": 0x02,
        "Hard": 0x03,
        "Logic": 0x04,
        "Tasukete": 0x05,
    }

    def __init__(self):
        self.exportOffset = 0
        self.Header = bytes([ # base header
            0x53, 0x53, 0x2b, 0x6d, # File type signature "SS+M"
            0x02, 0x00, # SSPM format version (0x02 or 0x01) Set to 2 by default
            0x00, 0x00, 0x00, 0x00, # 4 byte reserved space.
        ])
        self.lastMs = None
        self.metadata = {}
        self.songName = None
        self.requiresMod = 0
        self.strict = False
        self.coverBytes = None
        self.Difficulty = 0
        self.audioBytes = None
        self.mapName = None
        self.mappers = None
        self.Notes = None
        self.mapID = None
        self.customDataOffset = 0

    def _GetNextVariableString(self, data: BinaryIO, fourbytes: bool = False, encoding: str = "ASCII", V2: bool = True) -> str: # Why did this have a self variable??
        # Read 2 bytes for length (assuming little-endian format)
        length_bytes = data.read(2 if V2 else 1)
        
        # Convert the length bytes to an integer | Bugfix reading improper data
        lengthF = np.int32(int.from_bytes(length_bytes, byteorder='little')) if fourbytes else np.int16(int.from_bytes(length_bytes, byteorder='little'))
        
        # Read the string of the determined length
        finalString = data.read(lengthF)
        
        return finalString.decode(encoding=encoding)
    
    def _NewLineTerminatedString(self, data: BinaryIO, encoding: str = "ASCII") -> str: # for SSPMv1

        finalString = bytearray()
        while True:
            stringbyte = data.read(1) # keep going by one bit
            if stringbyte == b'\n': # once it reaches a new line, break
                break
            finalString.extend(stringbyte)
        
        return finalString.decode(encoding=encoding)

    
    def WriteSSPM(self, filename: str = None, forcemapid=False, debug: bool = False, **kwargs) -> bytearray | NoneType:
        """
        Creates a SSPM v2 file based on variables passed in, or already set. <br>
        If no filepath is passed in, it will return file as bytes
        <br>
        Variables that need to be covered:
        1. `coverBytes`: Cover image in bytes form, or None
        2. `audioBytes`: Audio in bytes form, or None
        3. `Difficulty`: one of Difficulties dictionary options, or 0x00 - 05 OR "N/A", "Easy", "Medium", "Hard", "Logic", "Tasukete"
        4. `mapName`: The name of the map. Rhythia guidelines suggests `artist name - song name`
        5. `mappers`: a list of strings containing the mapper(s)
        6. `notes`: a list of tuples as shown below
        7. `forcemapid`: if enabled, overwrite mapId to be added instead | otherwise defaults to mappers + map name | make sure its only ASCII characters
        ```python
        # (x, y, ms)
        self.notes = [
         (1, 2, 1685), # X, Y, MS
         (1.22521, 0.156781, 2000)
        ]#...
        ```
        <br>
        `**kwargs`: pass in any of the variables shown above.
        
        Example usage:

        ```python
        from sspmLib import SSPMParser
        
        sspm = SSPMParser()
        sspm.ReadSSPM(file_path) # reads
        sspm.Difficulty = 5 # changes difficulty to Tasukete
        
        with open(output_path+".sspm", "wb") as f:
            f.write(sspm.WriteSSPM())
        ```
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                warn(f"{key} is not a valid attribute", Warning)


        self.Header = bytes([ # base header
            0x53, 0x53, 0x2b, 0x6d, # File type signature "SS+M"
            0x02, 0x00, # SSPM format version (0x02 or 0x01) Set to 2 by default
            0x00, 0x00, 0x00, 0x00, # 4 byte reserved space.
        ])

        # configs
        self.containsCover = b"\x01" if self.coverBytes != None else b"\x00" # 0 or 1
        self.containsAudio = b"\x01" if self.audioBytes != None else b"\x00" # 0 or 1
        self.requiresMod = b"\x01" if self.requiresMod == 1 or self.requiresMod == b"\x01" else b"\x00" # Who actually uses this though?
        
        #print(self.Notes[-1][2])
        self.lastMs = np.uint32(self.Notes[-1][2]).tobytes()  # np.uint32 object thus far | 4 bytes | base before getting proper one
        self.noteCount = np.uint32(len(self.Notes)).tobytes() # bytes should be length of 4
        self.markerCount = self.noteCount # nothing changed from last time

        self.Difficulty = self.Difficulty if self.DIFFICULTIES.get(self.Difficulty) == None else self.DIFFICULTIES.get(self.Difficulty)
        self.Difficulty = self.Difficulty.to_bytes(1, 'little') if isinstance(self.Difficulty, int) else self.Difficulty

        if debug:
            print("Metadata loaded")

        # good until here
        #self.mapID = 
        self.songName = "sspmLib Song - author".encode("ASCII") if not self.songName else self.songName.encode("ASCII")

        if not forcemapid:
            self.mapID = f"{'_'.join(self.mappers)}_{self.mapName.replace(' ', '_')}".encode("ASCII") # combines mappers and map name to get the id.
        else:
            self.mapID = self.mapID.encode("ASCII")
            
        self.mapIDf = len(self.mapID).to_bytes(2, 'little')
        self.mapName = self.mapName.encode("ASCII")
        self.mapNameF = len(self.mapName).to_bytes(2, 'little')
        self.songNameF = len(self.songName).to_bytes(2, 'little')

        self.mapperCountf = len(self.mappers).to_bytes(2, 'little')
        #self.mappersf = '\n'.join(self.mappers).encode('ASCII') # Possible bug | maybe include breakchar like \n
        mappersf = bytearray()

        # Iterate through each mapper in the mappers list
        for mapper in self.mappers:
            # Encode the mapper string to ASCII bytes
            mapperf = mapper.encode('ASCII')
            
            # Get the length of the mapper string as a 2-byte little-endian value
            mapperLength = len(mapperf).to_bytes(2, 'little')
            
            # Concatenate the length and the actual mapper string
            mapperFinal = mapperLength + mapperf
            
            # Append to the mappersf byte array
            mappersf.extend(mapperFinal)

        # Store the result in the instance variable
        self.mappersf = bytes(mappersf)

        self.strings = self.mapIDf+self.mapID+self.mapNameF+self.mapName+self.songNameF+self.songName+self.mapperCountf+self.mappersf # merge values into a string because we are done with this section
        if debug:
            print("Strings loaded")

        self.customData = b"\x00\x00" # 2 bytes, no custom data supported right neoww

        # FEATURE REQUEST: Add support for custom difficulty here.

        # Pointer locations in byte array

        
        if debug:
            print("1/2 pointers loaded. Note creation next")

        self.Markers = b''

        """ # Old slow code. Keep in case
        count = 0
        totalNotes = len(self.Notes)
        for nx, ny, nms in self.Notes:
            count+=1
            if debug and count % 1000 == 0:
                print(f"Notes completed: {count}/{totalNotes}", end="\r", flush=True)
            # Equivalent to: BitConverter.GetBytes((uint)(note.Ms + exportOffset))
            ms = (np.uint32(nms + self.exportOffset)).tobytes()

            # Equivalent to: new byte[1] (initialized to 0x00)
            markerType = b'\x00'

            # Equivalent to: Math.Round(note.X) == Math.Round(note.X, 2)
            xyInt = round(nx) == round(nx, 2) and round(ny) == round(ny, 2)

            # Equivalent to: new byte[] { (byte)(xyInt ? 0x00 : 0x01) }
            identifier = b'\x00' if xyInt else b'\x01'

            # Equivalent to: Convert x and y based on whether they are integers
            if xyInt:
                x = np.uint16(round(nx)).tobytes()[0:1]
                y = np.uint16(round(ny)).tobytes()[0:1]
            else:
                x = np.float32(nx).tobytes()
                y = np.float32(ny).tobytes()

            # Equivalent to: Concatenate ms, markerType, identifier, x, and y
            finalMarker = ms + markerType + identifier + x + y

            # Add to the markers list
            self.Markers += finalMarker"""

        count = 0
        totalNotes = len(self.Notes)
        
        markers = bytearray()
        lastms = 0
        
        for nx, ny, nms in self.Notes:
            count += 1
            
            if debug and count % 1000 == 0:
                print(f"Notes completed: {count}/{totalNotes}", end="\r", flush=True)
            
            rounded_nx = round(nx)
            rounded_ny = round(ny)
            rounded_nx_2 = round(nx, 2)
            rounded_ny_2 = round(ny, 2)
            
            # Calculate the bytes
            ms_bytes = np.uint32(nms + self.exportOffset).tobytes()
            marker_type = b'\x00'
            identifier = b'\x00' if (rounded_nx == rounded_nx_2 and rounded_ny == rounded_ny_2) else b'\x01'
            
            if identifier == b'\x00':
                x_bytes = np.uint16(rounded_nx).tobytes()[0:1]
                y_bytes = np.uint16(rounded_ny).tobytes()[0:1]
            else:
                x_bytes = np.float32(nx).tobytes()
                y_bytes = np.float32(ny).tobytes()
            if lastms < nms:
                lastms = nms
            
            final_marker = ms_bytes + marker_type + identifier + x_bytes + y_bytes
            markers.extend(final_marker)
        
        self.lastMs = np.uint32(lastms).tobytes() # because list is not in order.

        if debug:
            print("All pointers finished")


        # adding everything together
        metadata = self.lastMs + self.noteCount + self.markerCount + self.Difficulty + b"\x00\x00" + self.containsAudio + self.containsCover + self.requiresMod # level rating Not fully implemented yet 
        offset = len(self.Header) + 20 + len(metadata) + 80 + len(self.strings)
        # pointers
        self.customDataOffset = np.uint64(offset).tobytes()
        self.customDataLength = np.uint64(len(self.customData)).tobytes()
        offset+= len(self.customData)

        
        self.audioOffset = np.uint64(offset).tobytes()
        self.audioLength = np.uint64(len(self.audioBytes)).tobytes() if self.containsAudio == b'\x01' else b'\x00\x00\x00\x00\x00\x00\x00\x00' # 8 bytes filler if no audio length found | Possible bug if no audio found, and reading special block fails. | may default to start of file.
        offset+= len(self.audioBytes) if self.containsAudio == b'\x01' else len(b'\x00\x00\x00\x00\x00\x00\x00\x00') # 8
        self.audioBytes = b'' if self.audioBytes == None else self.audioBytes

        self.coverOffset = np.uint64(offset).tobytes()
        self.coverLength = np.uint64(len(self.coverBytes)).tobytes() if self.containsCover == b'\x01' else b'\x00\x00\x00\x00\x00\x00\x00\x00' # 8 bytes filler if no audio length found 
        offset+= len(self.coverBytes) if self.containsCover == b'\x01' else len(b'\x00\x00\x00\x00\x00\x00\x00\x00') # 8
        self.coverBytes = b'' if self.coverBytes == None else self.coverBytes

        self.NoteDefinition = "ssp_note".encode("ASCII")
        self.NoteDefinitionf = len(self.NoteDefinition).to_bytes(2, 'little') + self.NoteDefinition
        self.markerDefStart = b"\x01"
        self.markerDefEnd = b"\x01\x07\x00" # var markerDefEnd = new byte[] { 0x01, /* one value */ 0x07, /* data type 07 - note */ 0x00 /* end of definition */ };

        self.markerDefinitions = self.markerDefStart+self.NoteDefinitionf+self.markerDefEnd
        self.markerDefinitionsOffset = np.uint64(offset).tobytes()
        self.markerDefinitionsLength = np.uint64(len(self.markerDefinitions)).tobytes()
        offset+=len(self.markerDefinitions)

        # notes n stuff
        self.Markers = markers
        self.markerOffset = np.uint64(offset).tobytes()
        self.markerLength = np.uint64(len(self.Markers)).tobytes()

        # hashing
        self.markerSet = self.markerDefinitions+self.Markers
        sHash = sha1(self.markerSet).digest()

        pointers = b''
        pointers+=self.customDataOffset+self.customDataLength+self.audioOffset+self.audioLength+self.coverOffset+self.coverLength+self.markerDefinitionsOffset+self.markerDefinitionsLength+self.markerOffset+self.markerLength

        if debug:
            print(self.lastMs)
            print(metadata)
            print(pointers)
            print(self.strings)
            print(self.customData)
            print(self.audioBytes[0:10])
            print(self.coverBytes[0:10])

        self.SSPMData = self.Header+sHash+metadata+pointers+self.strings+self.customData+self.audioBytes+self.coverBytes+self.markerDefinitions+self.Markers
        
        if filename:
            with open(filename, 'wb') as f:
                f.write(self.SSPMData)
            return None
        
        return self.SSPMData
        

        raise NotImplementedError("Writing SSPM files at this time is being activly worked on. This currently does not function yet") # Old

    def ReadSSPM(self, file: str | BinaryIO, debug: bool = False):
        """
        Reads and processes any SSPM file. <br>
        `File:` Takes in directory of sspm, or BinaryIO object stored in memory.
        `debug:` Useful for getting readable outputs of steps taken.
        ## Warning
        SSPM (Sound space plus map file) version 1 is not supported at this time. loading this file may raise errors
        <br><br>
        

        ### Returns:
        1. `coverBytes` if cover was found
        2. `audioBytes` if audio was found
        3. `Header`: {"Signature": ..., "Version": ...}
        4. `Hash`: a SHA-1 hash of the markers in the map
        5. `mapID`: A unique combination using the mappers and map name*. 
        6. `mappers`: a list containing each mapper.
        7. `mapName`: The name given to the map.
        8. `songName`: The original name of the audio before imported. Usually left as artist name - song name
        9. `customValues`: NOT IMPLEMENTED | will return a dictionary of found custom blocks.
        10. `isQuantum`: Determins if the level contains ANY float value notes.
        11. `Notes`: A list of tuples containing all notes. | 
        Example of what it Notes is: `[(x, y, ms), (x, y, ms), (x, y, ms) . . .]`
        
        <br><br> ***Returns itself***

        """

        self.coverBytes = None
        self.audioBytes = None

        if isinstance(file, str): # If its a directory we convert it.
            with open(file, "rb") as f:
                fileBytes = BytesIO(f.read())
        else:
            fileBytes = file
                
        self.Header = { # all ascii
            "Signature": fileBytes.read(4),
            "Version": 2 if fileBytes.read(2) == b'\x02\x00' else 1, # checking version of SSPM file
        }
        self.Header["Reserve"] = fileBytes.read(4) if self.Header.get("Version") == 2 else fileBytes.read(2), # reserve (0x00 00 00 00) in v2, otherwise (0x00 00)


        # File check to make sure everything in the header is A-OK
        if debug:
            print("SSPM Version: ", self.Header.get("Version"))

        if self.Header.get("Signature") != b"\x53\x53\x2b\x6d":
            raise ValueError("SS+M signature was not found. What was found instead:", self.Header.get("Signature"))
        if self.Header.get("Version") == 2:
            self._ProcessSSPMV2(fileBytes)
        elif self.Header.get("Version") == 1:
            self._ProcessSSPMV1(fileBytes)
        else:
            raise ValueError("SSPM version does not match known versions. Versions (1, 2) FOUND:", self.Header.get("Version"))


        return self
    
    def _ProcessSSPMV2(self, fileBytes: BinaryIO):
        
        # static metadata

        self.Hash = fileBytes.read(20)
        self.lastMs = int.from_bytes(fileBytes.read(4), 'little') # 32bit uint
        self.noteCount = fileBytes.read(4) # 32bit uint
        self.markerCount = fileBytes.read(4) # No clue what this is, ill figure it out | 32bit uint
        
        self.Difficulty = fileBytes.read(1) # 0x00 01 02 03 04 05
        self.mapRating = fileBytes.read(2) # 16bit uint
        self.containsAudio = fileBytes.read(1) # 0x00 01?
        self.containsCover = fileBytes.read(1) # 0x00 01?
        self.requiresMod = fileBytes.read(1) # 0x00 01?

        # pointers | If not present then is left as 8 bytes of 0
        self.customDataOffset = fileBytes.read(8)
        self.customDataLength = fileBytes.read(8)
        self.audioOffset = fileBytes.read(8)
        self.audioLength = fileBytes.read(8)
        self.coverOffset = fileBytes.read(8)
        self.coverLength = fileBytes.read(8)
        self.markerDefinitionsOffset = fileBytes.read(8)
        self.markerDefinitionsLength = fileBytes.read(8)
        self.markerOffset = fileBytes.read(8)
        self.markerLength = fileBytes.read(8)

        # VariableLength Items..
        self.mapID = self._GetNextVariableString(fileBytes).replace(",", "")
        self.mapName = self._GetNextVariableString(fileBytes)
        self.songName = self._GetNextVariableString(fileBytes)

        for i in range(len(self.mapID)): # getting mapID
            if self.mapID[i] in self.INVALID_CHARS: # Create invalidChars thing
                self.mapID = self.mapID[:i] + '_' + self.mapID[i+1:]
        
        mapperCount = fileBytes.read(2)
        self.mapperCountFloat = int.from_bytes(mapperCount, byteorder="little") #np.uint16(mapperCount)
        self.mappers = [] # for now
        
        for i in range(self.mapperCountFloat): # Can have multiple mappers in a file.
            
            if True:
            #try: # temporary solution until I figure out whats happening
                self.mappers.append(self._GetNextVariableString(fileBytes))
            #except:
            #    pass
        try:
            # Oh god Custom data.... | Only supports custom difficulty thus far
            customData = fileBytes.read(2) # ??
            self.customDataTotalLength = np.uint16(customData)
            
            for i in range(self.customDataTotalLength):
                field = self._GetNextVariableString(fileBytes)
                id = fileBytes.read(1)
                if id[0] == "\x00": # no 0x08 and 0x0a according to SSQE...
                    continue
                elif id[0] == "\x01":
                    fileBytes.read(1) # skipping
                elif id[0] == "\x02":
                    fileBytes.read(2) # skipping
                elif id[0] == "\x03":
                    pass
                elif id[0] == "\x04":
                    pass
                elif id[0] == "\x05":
                    fileBytes.read(4) # skipping
                elif id[0] == "\x06":
                    fileBytes.read(8) # skipping
                elif id[0] == "\x07":
                    caseType = fileBytes.read(1)
                    if caseType == "\x00":
                        fileBytes.read(2)
                    elif caseType == "\x01":
                        fileBytes.read(2) # Possible Bug: In SSQE, reads only 2 bytes from 16 sized buffer...
                    break
                elif id[0] == "\x08":
                    self._GetNextVariableString(fileBytes)
                    break
                elif id[0] == "\x09": # Custom difficulty. NOT FULLY IMPLEMENTED
                    if self.strict:
                        warn("Custom difficulty in V2 and V1 Not supported. Was found in sspm. View raw form by using .CustomDifficulty @self", Warning)
                    self.CustomDifficulty = self._GetNextVariableString(fileBytes)
                    
                elif id[0] == "\x0a":
                    self._GetNextVariableString(fileBytes, fourbytes=True) # BUG: Make sure to implement fourbytes method here. Shouldnt cause issues right now...
                    break
                elif id[0] == "\x0b":
                    warn("CustomBlocks in V2 and V1 Not supported. Was found in sspm.", Warning)
                    self._GetNextVariableString(fileBytes, fourbytes=True) # BUG: Make sure to implement fourbytes method here.
                    break
                elif id[0] == "\x0c": # no more PLEASEEE
                    warn("CustomBlocks in V2 and V1 Not supported. Was found in sspm.", Warning)

                    fileBytes.read(1)
                    valueLength = fileBytes.read(4)
                    valueLengthF = np.uint32(valueLength)
                    
                    fileBytes.read(valueLengthF) # I hope???
                    break

        except Exception as e:
            if self.strict:
                warn("Couldnt properly read customData in V2/V1 sspm. Fell back to audio pointer", BytesWarning)
    
        # If all fails, fallback to audio pointer
        self.audioOffsetF = np.int64(int.from_bytes(self.audioOffset, byteorder='little'))
        
        # Get pointer from bytes
        fileBytes.seek(self.audioOffsetF)

        # reading optional data...
        #print(self.containsAudio[0])
        if self.containsAudio[0] == 1: # found audio
            self.totalAudioLengthF = np.int64(int.from_bytes(self.audioLength, 'little'))
            
            self.audioBytes = fileBytes.read(self.totalAudioLengthF)
            #print(fileBytes.tell())

        if self.containsCover[0] == 1: # True
            self.totalCoverLengthF = np.int64(int.from_bytes(self.coverLength, 'little'))
            #print(self.totalCoverLengthF)
            self.coverBytes = fileBytes.read(self.totalCoverLengthF)
            #print(fileBytes.tell())


        # LAST ANNOYING PART!!!!!! MARKERS..
        self.mapData = self.mapID

        # Reading markers
        self.hasNotes = False
        numDefinitions = fileBytes.read(1)
        #print(numDefinitions[0])

        for i in range(numDefinitions[0]): # byte form
            definition = self._GetNextVariableString(fileBytes)#, encoding="UTF-8")
            self.hasNotes |= definition == "ssp_note" and i == 0 # bitwise shcesadnigans (its 1:30am for me)

            numValues = fileBytes.read(1)

            definitionData = int.from_bytes(b"\x01", 'little')
            while definitionData != int.from_bytes(b"\x00", 'little'): # Read until null BUG HERE
                definitionData = int.from_bytes(fileBytes.read(1), 'little')
        
        if not self.hasNotes: # No notes
            return self.mapData
        
        # process notes
        #print("| | |", fileBytes.tell())
        noteCountF = np.uint32(int.from_bytes(self.noteCount, 'little'))
        Notes = []
        isQuantumChecker = False

        for i in range(noteCountF): # Could be millions of notes. Make sure to keep optimized
            ms = fileBytes.read(4)
            markerType = fileBytes.read(1)
            #print(fileBytes.tell())
            
            isQuantum = int.from_bytes(fileBytes.read(1), 'little')
            

            xF = None
            yF = None

            if isQuantum == 0:
                x = int.from_bytes(fileBytes.read(1), 'little')
                y = int.from_bytes(fileBytes.read(1), 'little')
                xF = x
                yF = y

            else:
                isQuantumChecker = True

                x = fileBytes.read(4)
                y = fileBytes.read(4)

                xF = np.frombuffer(x, dtype=np.float32)[0]
                yF = np.frombuffer(y, dtype=np.float32)[0]

                #xF = np.single(x) # numpy in clutch ngl
                #yF = np.single(y)
            
            msF = np.uint32(int.from_bytes(ms, 'little'))

            Notes.append((xF, yF, msF)) # F = converted lol

        self.Notes = sorted(Notes, key=lambda n: n[2]) # Sort by time
        self.isQuantum = isQuantumChecker

        return self

    def NOTES2TEXT(self) -> str:
        """
        Converts Notes to the standard sound space text file form. Commonly used in Roblox sound space
        """
        textString = ''
        for x, y, ms in self.Notes:
            if textString == '':
                textString+=f",{x}|{y}|{ms}"
            else:
                textString+=f",{x}|{y}|{ms}"
            
        return textString

    
    def _ProcessSSPMV1(self, fileBytes: BinaryIO):
        """
        just going to note, i will be using some of the self variables
        for compatibility with SSPMv2 (such as containsAudio, etc), and 
        i will also be formatting theoutput like SSPMv2, such as splitting 
        mappers by comma to make it into an array

                                                                -fog
        """


        # start of metadata

        self.mapID = self._NewLineTerminatedString(fileBytes).replace(",", "")
        self.mapName = self._NewLineTerminatedString(fileBytes)
        self.songName = self.mapName # lol
        self.mappers = self._NewLineTerminatedString(fileBytes).split(", ") # mappers arent in an array, so i will just split

        self.lastMs = fileBytes.read(4)
        self.noteCount = fileBytes.read(4)
        self.Difficulty = fileBytes.read(1)

        # end of metadata
        
        # start of file data

        self.coverType = int.from_bytes(fileBytes.read(1), byteorder='little')

        self.containsCover = None
        self.coverLength = None
        self.coverBytes = None

        match self.coverType:
            case 2: # PNG
                self.containsCover = b"\x01"

                self.coverLength = fileBytes.read(8)
                coverLengthtoInt = np.int64(int.from_bytes(self.coverLength, 'little'))

                self.coverBytes = fileBytes.read(coverLengthtoInt)
            case _: # for no cover, or non supported format
                self.containsCover = b"\x00"

        self.audioType = int.from_bytes(fileBytes.read(1), 'little')

        self.containsAudio = None
        self.audioLength = None
        self.audioBytes = None

        match self.audioType:
            case 0: # no Audio
                self.containsAudio = b"\x00"
            case 1: # Audio! :)
                self.containsAudio = b"\x01"

                self.audioLength = fileBytes.read(8)
                audioLengthtoInt = int.from_bytes(self.audioLength, 'little')

                self.audioBytes = fileBytes.read(audioLengthtoInt) # must be mp3 or OGG

        # end of file data

        # start of note data

        noteCounttoInt = int.from_bytes(self.noteCount, 'little')
        Notes = []
        isQuantumChecker = False

        for i in range(noteCounttoInt):
            ms = fileBytes.read(4)
            
            # i can just copy and paste the rest of this since its the same

            isQuantum = int.from_bytes(fileBytes.read(1), 'little')

            xF = None
            yF = None

            if isQuantum == 0:
                x = int.from_bytes(fileBytes.read(1), 'little')
                y = int.from_bytes(fileBytes.read(1), 'little')
                xF = x
                yF = y

            else:
                isQuantumChecker = True

                x = fileBytes.read(4)
                y = fileBytes.read(4)

                xF = np.frombuffer(x, dtype=np.float32)[0]
                yF = np.frombuffer(y, dtype=np.float32)[0]
            
            msF = np.uint32(int.from_bytes(ms, 'little'))

            Notes.append((xF, yF, msF))

        
        self.Notes = sorted(Notes, key=lambda n: n[2]) # Sort by time
        self.isQuantum = isQuantumChecker

        return self
        






"""    def _GetNextVariableString(self, data: BinaryIO, fourbytes: bool = False) -> str:
        length = data.read(2)
        length = length.rstrip("\x00")
        lengthF = np.uint32(length) if fourbytes else np.int16(length)
        
        finalString = data.read(lengthF)
        return finalString.decode("ASCII")
"""

"""
        bytes_list = []

        current_byte = data.read(1)

        while current_byte != b'\x0a':  # 0x0a is the ASCII code for newline ('\n')
            bytes_list.append(current_byte[0])
            current_byte = data.read(1)

        return bytes(bytes_list).decode('ascii') # ONLY SUPPORTS ASCII
"""


