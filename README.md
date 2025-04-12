# Conception-II-Modding-Tools
Conception II lightweight Python coded Modding Tools. The scripts are extremely lightwegiht in my opinion with few dependencies, the goal was lightweight GUI based modding tools to make modding easier for modders. The file size of mods made is not a concern, whether your mod becomes smaller or larger than the original game's files doesn't matter anymore since the Mod Manager makes sure the game supports the change in file size. Essentially, mod without worry about file size because the Mod Manager will make sure your mod is applied regardless of the size of the file.

Requirements: The scripts must be in the same directory as Conception 2's game directory, you must have python 3 installed, and must not alter the files the Mod Creator makes unless you know what you're doing since the custom formats I designed are meant to be used by the Mod Manager and Mod Creator.

1. Unpacker(Console based): The Unpacker will first backup the original CFSI container files into a "Backups_Folder", unpack files from the CFSI container files into the Unpacked_Files folder, and decompress any files that use compression. It will also add metadata at the end of every file unpacked for the mod creator and mod manager to use later. It's essential you don't modify the Tail metadata(the metadata written at the end of every file by the unpacker) so that the Mod Creator and Mod Manager work without issue.

2. Mod Creator(GUI Tkinter based): The Mod Creator creates .CON2 files(custom format mod files designed by me to be used with the Mod Manager) which are mod files to apply and disable with the Mod Manager, allows the user to type a description of the mod, and then name the mod file. The idea is that once you finish modding a file, you create the mod file with the Mod Creator script so the Mod Manager can then easily apply and disable the mod. When you mod game files, use the Create Mod button after you enter the name and description of the mod. Use the Convert File button when you want to add files into the CFSI container files that weren't originally part of the game. An example is BGM modding. let's say you want to replace the game's original file bgm003.ogg with a custom or different song file from outside of the game. You enter the mod name and description you want, click Convert File, select the file you want to convert into a valid Conception 2 mod file, and the file you want to replace. The file you're replacing isn't lost after the mod is made, what's done is the CFSI container will read the data from the injected/appended mod(after you apply it with the Mod Manager) instead of the original game file. Essentially, use Convert File button when making mods with files the game didn't come with or use Create Mod button for mods that involved you modding a game file such as a game texture file like h0201_body.dds which in that case you would use the Create Mod button. Each button when hovered over will display a message explaining the purpose of it. ![tools2](https://github.com/user-attachments/assets/e55d221f-8f1a-4a28-8f72-d301a2c07153)


3. Mod Manager(GUI Tkinter based): The Mod Manager supports applying and disabling mods by injecting/appending the mods at the end of the CFSI container files rather than rebuilding the container files or reading and writing to various offsets where the original files were, tracking currently enabled mods through the .MODS file(a custom format binary mod file designed by me that stores currently enabled mods), display of a mod description, and a refresh button labeled as "Disable All Mods and replace CFSI container files" which basically deletes the .MODS file and replaces the CFSI container files with fresh unmodded copies. Each button when hovered over will display a message explaining the purpose of it. It doesn't matter how small or large your mods is since the Mod Manager will make sure the CFSI file is updated to support mods that exceed the original file's size. ![tools1](https://github.com/user-attachments/assets/6cf1a714-ca80-40af-9245-dd26d084df48)


   Info on the Mod Applying and Disabling process: The Mod Manager relies on Injecting/patching rather than rebuilding container files or shifting file data to apply and disable mods. This is both faster and safer since the mods are always applied at the end of every container file and the only original data modded is the metadata offsets to file data at the start of the container files which are changed to point to the current offset of wherever the mod is located at the end of the CFSI files. When a mod is disabled(you disable a mod by selecting the .CON2 file you want disabled or click the "Disable All Mods and replace CFSI container files" button) the mod Manager will revert the CFSI file to use the original game files by updating those metadata offsets.

   Extra Info: The current scripts are the initial release so please keep that in mind when using them. I haven't been able to have anyone else try the scripts so if you encounter any issues, let me know either here or on the Conception2 subreddit. Since the mods are appended at the end of the container files, the file size of the CFSI files will grow but to be honest the CFSI container files are small anyways. If you eventually want to decrease the file size of the CFSI files, click the "Disable All Mods and replace CFSI container files" button which disables all mods and replaces the CFSI files with unmodded/fresh copies. I included some example mods to show. The partial german translation mod only translates 1 item in the Item shop since it's an example mod and I had to use google translate for translating. There's a lot of modding potential for Conception II.

Lust Dungeon Floor 1 Mod: This example Mod adds 5 more sub rooms and some more enemies to the first floor of the Lust Dungeon to fill some of the sub rooms. 
With mod enabled: ![ex1](https://github.com/user-attachments/assets/054e274f-7688-40bb-874a-8d3c51426994)

With mod disabled: ![ex2](https://github.com/user-attachments/assets/27724571-3f57-483a-9bb8-8f9140ced4c5)
