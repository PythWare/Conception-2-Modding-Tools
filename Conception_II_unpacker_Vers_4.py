import os
import gzip

class Conception2:
    INITIAL_DATA = 3
    BASE_OFFSET = 0x2D7A0 # used as part of calculating the final offset to file data for the 00000000.cfsi file
    BASE_BGM_OFFSET = 0x520 # used as part of calculating the final offset to file data
    BASE_VOICE_OFFSET = 0x95690 # used as part of calculating the final offset to file data
    BASE_VALUE = 16  # multiply the file offset by this then add base offset to get the actual file data offset.
    FOLDERS = 0
    def __init__(self):
        self.main_folder = "Unpacked_Files"
        self.backups = "Backups_Folder"
        self.container = "00000000.cfsi"
        self.bgm = "bgm.cfsi"
        self.voice = "voice.cfsi"
        self.mods_enabled_file = "Conception_II.MODS"
        self.loop_count = 302
        self.other_count = 1
        self.compressed_mark = b'\x01'
        self.not_compressed_mark = b'\x00'
        os.makedirs(self.main_folder, exist_ok=True)
        os.makedirs(self.backups, exist_ok=True)

        self.create_mods_file()
        self.copy()
        self.file_reading()
        self.bgm_reading()
        self.voice_reading()

    def create_mods_file(self):
        """This function is used for creating an empty .MODS file, a file storing enabled mods to be used with the Mod Manager"""
        if not os.path.isfile(self.mods_enabled_file): # if the .MODS file doesn't exist
            with open(self.mods_enabled_file, "a") as w1:
                pass
            
    def copy(self):
        """This function is used for saving copies of the unmodded cfsi container files"""
        cfsi_list = [self.container, self.bgm, self.voice]
        for i in cfsi_list:
            backup_path = os.path.join(self.backups, i)
            if os.path.isfile(backup_path):
                continue
            else:
                print(f"A backup file of {i} is being created before the unpacking begins.")
                with open(i, "rb") as f1, open(backup_path, "ab") as w1:
                    while True:
                        data = f1.read(16 * 1024)
                        if not data:
                            break
                        w1.write(data)
            
    def file_reading(self):
        """Main container reading logic"""
        with open(self.container, "rb") as f1:
            f1.read(self.INITIAL_DATA)
            # Define the sections
            sections = [
                (self.loop_count, 0, 0),
                (self.other_count, 2, 311),
                (93, 0, 0),
                (1, 2, 269)
            ]
            for folder_count, read_offset, max_files in sections:
                self.process_section(f1, self.container, folder_count, read_offset, max_files)

    def bgm_reading(self):
        """handles the other container files related to bgm"""
        with open(self.bgm, "rb") as f1:
            f1.read(self.other_count)
            folder_name_len = int.from_bytes(f1.read(1), "little")
            folder_name = f1.read(folder_name_len).decode()
            dir_name = os.path.dirname(folder_name)
            file_count = int.from_bytes(f1.read(1), "little")
            for _ in range(file_count):
                filename_len = int.from_bytes(f1.read(1), "little")
                filename = f1.read(filename_len).decode()
                orig_offset = f1.tell()
                initial_file_offset = int.from_bytes(f1.read(4), "little")
                file_offset = initial_file_offset * self.BASE_VALUE + self.BASE_BGM_OFFSET # calculate direct offset to file data
                file_size = int.from_bytes(f1.read(4), "little")

                return_to_offset = f1.tell()

                # Seek to the file data and read it
                f1.seek(file_offset)
                file_data = f1.read(file_size)

                # Check if Compression is used
                possible_compression = self.compression_check(file_data)

                if possible_compression:
                    # Write the file to disk
                    self.file_writing(self.bgm, self.compressed_mark, folder_name_len, dir_name, filename_len, filename, file_data, orig_offset, initial_file_offset, file_size)
                else:
                    # Write the file to disk
                    self.file_writing(self.bgm, self.not_compressed_mark, folder_name_len, dir_name, filename_len, filename, file_data, orig_offset, initial_file_offset, file_size)

                # Return to the previous offset
                f1.seek(return_to_offset)

    def voice_reading(self):
        """handles the other container files related to voices"""
        with open(self.voice, "rb") as f1:
            f1.read(self.other_count)
            folder_name_len = int.from_bytes(f1.read(1), "little")
            folder_name = f1.read(folder_name_len).decode()
            dir_name = os.path.dirname(folder_name) # directory name
            f1.read(1)
            file_count = int.from_bytes(f1.read(2), "little")
            for _ in range(file_count):
                filename_len = int.from_bytes(f1.read(1), "little")
                filename = f1.read(filename_len).decode()
                orig_offset = f1.tell() # getting the offset to current metadata section
                initial_file_offset = int.from_bytes(f1.read(4), "little") # before calculation offset to file data
                file_offset = initial_file_offset * self.BASE_VALUE + self.BASE_VOICE_OFFSET # calculate direct offset to file data 
                file_size = int.from_bytes(f1.read(4), "little")

                return_to_offset = f1.tell()

                # Seek to the file data and read it
                f1.seek(file_offset)
                file_data = f1.read(file_size)

                # Check if Compression is used
                possible_compression = self.compression_check(file_data)

                if possible_compression:
                    # Write the file to disk
                    self.file_writing(self.voice, self.compressed_mark, folder_name_len, dir_name, filename_len, filename, file_data, orig_offset, initial_file_offset, file_size)
                else:
                    # Write the file to disk
                    self.file_writing(self.voice, self.not_compressed_mark, folder_name_len, dir_name, filename_len, filename, file_data, orig_offset, initial_file_offset, file_size)
                # Return to the previous offset
                f1.seek(return_to_offset)
                
    def process_section(self, f1, container, folder_count, read_offset, max_files):
        """Process each section with dynamic parameters"""
        for _ in range(folder_count):
            current_point = f1.tell()
            folder_name_len = int.from_bytes(f1.read(1), "little")
            folder_name = f1.read(folder_name_len).decode()
            dir_name = os.path.dirname(folder_name)
            file_count = int.from_bytes(f1.read(1), "little")

            # Skip extra data for sections that have it
            if read_offset:
                f1.read(read_offset)

            for _ in range(max_files if max_files else file_count):
                self.process_file(f1, container, folder_name_len, dir_name)

    def process_file(self, f1, container, folder_name_len, dir_name):
        """Process individual files inside the section"""
        filename_len = int.from_bytes(f1.read(1), "little")
        filename = f1.read(filename_len).decode()
        orig_offset = f1.tell() # getting the offset to current metadata section

        initial_file_offset = int.from_bytes(f1.read(4), "little") # before calculation offset to file data
        file_offset = initial_file_offset * self.BASE_VALUE + self.BASE_OFFSET # calculate direct offset to file data
        file_size = int.from_bytes(f1.read(4), "little")

        return_to_offset = f1.tell()

        # Seek to the file data and read it
        f1.seek(file_offset)
        file_data = f1.read(file_size)

        # Check if Compression is used
        possible_compression = self.compression_check(file_data)

        if possible_compression:
            # Write the decompressed file to disk
            self.file_writing(container, self.compressed_mark, folder_name_len, dir_name, filename_len, filename, possible_compression, orig_offset, initial_file_offset, file_size)
        else:
            # Write the file to disk
            self.file_writing(container, self.not_compressed_mark, folder_name_len, dir_name, filename_len, filename, file_data, orig_offset, initial_file_offset, file_size)


        # Return to the previous offset
        f1.seek(return_to_offset)
        
    def compression_check(self, data):
        """This function handles checking if the file data is compressed"""
        check_header = data[4:6] # GZIP compressed files have a header
        if check_header == b'\x1F\x8B':
            return gzip.decompress(data[4:])
        else:
            return None
    
    def file_writing(self, container, comp_marker, path_len, folder, filename_len, file, data, offset, initial_file_offset, size):
        """Write file data into the directory"""
        orig_folder_path = os.path.join(folder, file)
        folder_path = os.path.join(self.main_folder, folder)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, file)

        # Create the file
        with open(file_path, "wb") as w1:
            w1.write(data)

        # File Tail Metadata, it adds some metadata at the end of file for the mod manager and mod creator to use later
        with open(file_path, "ab") as a1:
            current_position = a1.tell() # used for set where the start of File Tail Metadata begins
            a1.write(len(container).to_bytes(1, "little")) # write the length of the container file's name
            a1.write(container.encode()) # write the encoded container filename, mod manager uses this for mod applying
            a1.write(offset.to_bytes(4, "little")) # offset to the file's metadata section within the container file
            a1.write(initial_file_offset.to_bytes(4, "little")) # initial offset before calculating file data offset, used by mod manager to write the original offset for mod disabling
            a1.write(size.to_bytes(4, "little")) # size of the original file, used by mod manager to write the original size for mod disabling
            a1.write(comp_marker) # write marker saying if the file was originally compressed or not
            a1.write(current_position.to_bytes(4, "little"))
        print(file_path)

if __name__ == "__main__":
    Conception2()
    input(f"Task finished, you may exit now.")
