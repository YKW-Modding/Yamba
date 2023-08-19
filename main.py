import mmap
import os
import sys


def main():
	save = input("Save file: ")
	print("Set any of the following to 'skip' to not edit it.")
	map = input("Map code: ")
	
	if len(map) != 7 and map != "skip":
		print("Too long for a map ID!")
		main()
	
	xCoordIn = input("X Coordinate: ")
	if xCoordIn != "skip":
		try:
			xCoord = int(xCoordIn)
		except ValueError:
			print("Not an integer!")
			main()
	yCoordIn = input("Y Coordinate: ")
	if yCoordIn != "skip":
		try:
			yCoord = int(yCoordIn)
		except ValueError:
			print("Not an integer!")
			main()
	zCoordIn = input("Z Coordinate: ")
	if zCoordIn != "skip":
		try:
			zCoord = int(zCoordIn)
		except ValueError:
			print("Not an integer!")
			main()
	
	os.system("python yw_save/yw_save.py --game yw --decrypt " + save + " decrypted.yw")#
	
	with open("decrypted.yw", "r+b") as f:
		if map != "skip":
			f.seek(72)
			f.write(bytes(map, 'utf-8'))
		if xCoordIn != "skip":
			f.seek(20)
			f.write(xCoord.to_bytes(4, byteorder = "little", signed = True))
		if yCoordIn != "skip":
			f.seek(24)
			f.write(yCoord.to_bytes(4, byteorder = "little", signed = True))
		if zCoordIn != "skip":
			f.seek(28)
			f.write(zCoord.to_bytes(4, byteorder = "little", signed = True))
	
	os.system("python yw_save/yw_save.py --game yw --encrypt decrypted.yw output.yw")
	os.remove("decrypted.yw")
	
	input("Complete! File saved as output.yw. Press Enter to continue... ")
	sys.exit()

main()