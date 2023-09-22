from definitions import *
import os

save = input("Save file path: ")
if save[0] in ["'", '"']: save = save[1:-1] #to get rid of automatic quotes
while not os.path.exists(save) or ".yw" not in save:
    print("Invalid path.")
    save = input("Save file path: ")
    if save[0] in ["'", '"']: save = save[1:-1]

print("Leave any of the following blank to skip it.")

print("You can get map codes from definitions.py")
mapID = get_input("Map code (7 characters): ", lambda x: x if x in reverse_locations else None)
print("Coordinates from 0 to 4294967295")
xCoord = get_input("X: ", lambda x: x if x.isdecimal() and int(x) <= 4294967295 else None)
yCoord = get_input("Y: ", lambda x: x if x.isdecimal() and int(x) <= 4294967295 else None)
zCoord = get_input("Z: ", lambda x: x if x.isdecimal() and int(x) <= 4294967295 else None)
time = get_input("Time from 0 to 65535: ", lambda x: x if x.isdecimal() and int(x) <= 65535 else None)
sunTime = get_input("Sun time (1, 2, 3, or 4): ", lambda x: x if x.isdecimal() and 1 <= int(x) <= 4 else None)

if save[-3:] == "ywd":
    inject(open(save, "r+b"), mapID, xCoord, yCoord, zCoord, time, sunTime)
else:
    import yw_save
    import io
    with open(save, "r+b") as f:
        out = inject(io.BytesIO(yw_save.yw_proc(f.read(), False)), mapID, xCoord, yCoord, zCoord, time, sunTime)
        f.seek(0)
        f.write(yw_save.yw_proc(out, True))