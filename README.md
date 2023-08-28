# Yamba
A Yo-Kai Watch save editor. It currently is able to change the map you are in, as well as your position and the time. Only tested with YKW1 3DS.

**NOTE: The game snaps you back onto the floor when changing the Y position. Keep this in mind!**

![image](https://github.com/YKW-Modding/Yamba/assets/115092262/9399076e-7307-4664-99cc-27955e08c71f)

## Features:

- Moving maps
- Position modification
- Changine the time
- Changing the sun time

## Usage

***Make sure you have your Python directory added to PATH before doing this!!!***

1. Click on Code -> Download ZIP
2. Extract the zip file
3. Run either main_cmd.py or *main_gui.py (requires PyQt5)*
4. Enter your options (press "Go!" on the GUI version), rename output.yw to gameX.yw (X being the save file number) and put it into the game

### Map codes

These can be found at https://tcrf.net/Notes:Yo-kai_Watch_(Nintendo_3DS)#Map_names if you need them!

### How time works

There is a value for the time that can be between 0 and 65535. For some strange reason, while that could've just been it, that huge range only spans a quarter of the possible times.

Immediately after the value, there is another value that is always 1, 2, 3 or 4. 1 is morning to midday, 2 is midday to night, 3 is night to midnight and 4 is midnight to morning.

## Credits

https://github.com/Darkey28/yw_save
