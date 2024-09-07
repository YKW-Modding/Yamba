import os
import struct
POSITION_START = 20
save = input("Save file: ")
if os.path.exists("decrypted.yw"): os.remove("decrypted.yw")
os.system("python yw_save/yw_save.py --game yw --decrypt " + save + " decrypted.yw")
with open("decrypted.yw","rb") as f:
    pos = []
    for i in range(3):
        f.seek(POSITION_START+i*4)
        pos.append(struct.unpack('>I', f.read(4))[0])
    print("Position: " + str(pos))