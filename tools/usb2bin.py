#!/usr/bin/env python3

import sys


CONST_COMMAND_SIZE    = 0x19
CONST_COMMAND_PATTERN = b'\x03\x02\x41\x44\x44\x52\x1E'
CONST_CHECKSUM_SIZE   = 0x01


def check_addr_command(file, chksum):
	offset = file.tell()
	command = file.read(CONST_COMMAND_SIZE)
	try:
		print('0x{:08X} '.format(offset) + command.decode("ascii") + ' ' + bytes(chksum).hex())
	except:
		pass
	return get_start_offset(command)

def get_start_offset(data):
	return data.find(CONST_COMMAND_PATTERN)

def clean_binary(sBlockSize, sFileName):
	with open(sFileName, 'rb') as file, open(sFileName + '_sniffed.bin', 'wb') as output:
		data = file.read()

		offset = get_start_offset(data)
		if offset != (-1):
			print('Start ADDR offset: ' + '0x{:08X}'.format(offset) + '.\n')
		else:
			print('Error: Cannot find start ADDR command!\n')
			exit(1)

		file.seek(offset)

		chksum = 0
		while not check_addr_command(file, chksum):
			bytes = file.read(int(sBlockSize, 16))
			output.write(bytes)
			chksum = file.read(CONST_CHECKSUM_SIZE)
			if not bytes or not chksum:
				break

if __name__ == '__main__':
	print('Get binaries (RAMDLD, FIRMWARE) from USB dumps.')
	print('Version: 1.0, (c) EXL, 03-Aug-2023\n')
	if len(sys.argv) != 3:
		print('Usage:')
		print('\t./usb2bin.py <block size> <output file>')
		print('Example:')
		print('\t./usb2bin.py 0x400 usb_dump.bin')
		exit(1)
	clean_binary(sys.argv[1], sys.argv[2])
