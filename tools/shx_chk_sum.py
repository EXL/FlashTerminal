#!/usr/bin/env python3

import sys

def checksum_srec(srecord):
	old_srec = srecord[:-2]
	old_chk = srecord[-2:]

	new_srec = old_srec[2:]
	byte_sum = sum([int(new_srec[i:i + 2], 16) for i in range(0, len(new_srec), 2)])
	new_chk = ~(byte_sum & 0xFF) & 0xFF
	if old_chk.upper() != f'{new_chk:02X}'.upper():
		print(f'Warning: {old_chk} != {new_chk:02X}')

	return old_srec + f'{new_chk:02X}'

def checksum_16(data):
	checksum = 0
	for byte in data:
		checksum = (checksum + byte) % 65536
	return checksum

def bin_checksum(file_path):
	with open(file_path, 'rb') as binary_file:
		return checksum_16(binary_file.read())

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage: ./shx_chk_sum.py <mode> <file or data>')
		print()
		print('Examples:')
		print('\t./shx_chk_sum.py F CG1.bin')
		print('\t./shx_chk_sum.py S S705435302DD85')
		sys.exit(1)

	mode = sys.argv[1]
	data = sys.argv[2]

	if mode == 'F':
		print(f'{data} checksum_16 is: {bin_checksum(data):04X}')
	elif mode == 'S':
		print(f'{checksum_srec(data)}')
	else:
		print('Unknown mode!')
		sys.exit(1)
	sys.exit(0)
