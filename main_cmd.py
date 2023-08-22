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
	
	timeIn = input("Time from -32767 to 32767: ")
	if timeIn != "skip":
		try:
			time = int(timeIn)
		except ValueError:
			print("Not an integer!")
			main()
		if not -32767 <= time <= 32767 and timeIn != "skip":
			print("Number is too large!")
			main()
	
	sunTimeIn = input("Sun time (0 for midnight-midday and 1 for midday-midnight): ")
	if sunTimeIn != "skip":
		try:
			sunTime = int(sunTimeIn)
		except ValueError:
			print("Not an integer!")
			main()
		if sunTime != 0 and sunTime != 1:
			print("Not 0 or 1!")
			main()
	
	keepDecrypted = input("Keep decrypted save file? (y/n): ")
	if keepDecrypted != "y" and keepDecrypted != "n":
		print("Not 'y' or 'n'!")
		main()
	
	os.system("python yw_save/yw_save.py --game yw --decrypt " + save + " decrypted.yw")
	
	with open("decrypted.yw", "r+b") as f:
		if map != "skip":
			f.seek(72)
			f.write(bytes(map, 'utf-8'))
		if xCoordIn != "skip":
			f.seek(20)
			f.write(xCoord.to_bytes(4, byteorder = "big", signed = True))
		if yCoordIn != "skip":
			f.seek(24)
			f.write(yCoord.to_bytes(4, byteorder = "big", signed = True))
		if zCoordIn != "skip":
			f.seek(28)
			f.write(zCoord.to_bytes(4, byteorder = "big", signed = True))
		if timeIn != "skip":
			f.seek(1488)
			f.write(time.to_bytes(2, byteorder = "big", signed = True))
		if sunTimeIn != "skip":
			f.seek(1490)
			if sunTime == 0:
				f.write(int.to_bytes(1, 1, byteorder = "big"))
			if sunTime == 1:
				f.write(int.to_bytes(2, 1, byteorder = "big"))
			
	os.system("python yw_save/yw_save.py --game yw --encrypt decrypted.yw output.yw")
	
	if keepDecrypted == "n":
		os.remove("decrypted.yw")
	
	input("Complete! File saved as output.yw. Press Enter to continue... ")
	sys.exit()

main()