# Yamba
A Yo-Kai Watch save editor. Provide it with an encrypted .yw save file and it can change the map you are in, as well as your X, Y and Z coordinates and the time.

Only tested with YKW1 3DS.

**NOTE: The game snaps you back onto the floor when changing the Y position. Keep this in mind!**

## Usage

1. Click on Code -> Download ZIP
2. Extract the zip file
3. Run main_cmd.py or main_gui.py depending on your preference
4. Enter your options (press "Go!" on the GUI version), rename output.yw to gameX.yw (X being the save file number) and put it into the game

### Map codes

These can be found at https://tcrf.net/Notes:Yo-kai_Watch_(Nintendo_3DS)#Map_names if you need them!

### How time works

There is a value for the time that can be between 0 and 65535. For some strange reason, while that could've just been it, that huge range only spans half of the possible times, specifically, all of the times on the top half of the radar.

Immediately after the value, there is another that is always either 1 or 2. If it is 1, then the first value will span all the times on the top half of the radar, whereas if it is 2, it will span all the times on the bottom half. I called this second value "sun time" for some reason. I really don't know why I called it that but it's a name.

## Credits

https://github.com/Darkey28/yw_save
