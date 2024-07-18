#!/usr/bin/env python

import sys


def print_usage():
	print('A simple simflex command generator.')
	print('Version: 1.0, (c) EXL, 06-Aug-2023\n')
	print('Usage:')
	print('\t./simflex_helper.py <command> <argument_1> <argument_2>')
	print('Examples:')
	print('\t./simflex_helper.py delete_file /a/mobile/audio/~AlertFile029.mid')
	print('\t./simflex_helper.py change_attr /a/mobile/audio/~AlertFile029.mid 0x04')
	print()
	print('\t./simflex_helper.py create_dir /a/Elf')
	print('\t./simflex_helper.py delete_dir /a/Elf')
	print()
	print('\t./simflex_helper.py read_seem 0032_0001')
	print('\t./simflex_helper.py write_seem 0004_0001 080a00000011325406')
	print('\t./simflex_helper.py view_seem 080a00000011325406')
	exit(1)


def set_int_16(a_command, a_value, a_offset):
	a_command[0 + a_offset] = int(a_value / 0x100) % 0x100
	a_command[1 + a_offset] = a_value % 0x100
	return a_command


def generate_file_command(a_base_cmd, a_filename):
	cmd_size = len(a_base_cmd) + len(a_filename)
	a_base_cmd += a_filename.encode('utf-8') # Not sure about this. Probably 'utf-16-be'?
	a_base_cmd = set_int_16(a_base_cmd, 0x01, 0x00)
	a_base_cmd = set_int_16(a_base_cmd, cmd_size - 8, 0x04)
	return a_base_cmd


def delete_file(a_filename):
	# Examples:
	#  0001004A00150000000000057E416C65727446696C653032392E6D6964

	cmd = bytearray(b'\xFF\xFF\x00\x4A\xAA\xAA\x00\x00\x00\x00\x00\x05')
	print(generate_file_command(cmd, a_filename).hex().upper())


def change_attr(a_filename, a_attr):
	# Examples:
	#  0001004A0019000000000000000000047E416C65727446696C653032392E6D6964
	#  0002004A0004000000000004

	# Open file.
	cmd = bytearray(b'\xFF\xFF\x00\x4A\xAA\xAA\x00\x00\x00\x00\x00\x00\x00\x00\x00\xAA')
	cmd = generate_file_command(cmd, a_filename)
	cmd[0x0F] = int(a_attr, 16)
	print(cmd.hex().upper())

	# Close file.
	cmd = bytearray(b'\xFF\xFF\x00\x4A\x00\x04\x00\x00\x00\x00\x00\x04')
	cmd = set_int_16(cmd, 0x02, 0x00)
	print(cmd.hex().upper())


def create_dir(a_directory):
	# Examples:
	#  0001004A000E00000000000E000000102F612F456C66

	cmd = bytearray(b'\xFF\xFF\x00\x4A\x02\x00\x00\x00\x00\x00\x00\x0E\x00\x00\x00\x10')
	print(generate_file_command(cmd, a_directory).hex().upper())


def delete_dir(a_directory):
	# Examples:
	#  0001004A000E00000000000F000000102F612F456C66

	cmd = bytearray(b'\xFF\xFF\x00\x4A\x02\x00\x00\x00\x00\x00\x00\x0F\x00\x00\x00\x10')
	print(generate_file_command(cmd, a_directory).hex().upper())


def read_seem(seem):
	# Examples:
	#  00010020000800000032000100000000

	seem_rec = seem.split('_')
	cmd = bytearray(b'\xFF\xFF\x00\x20\x00\x08\x00\x00\xAA\xAA\xBB\xBB\x00\x00\x00\x00')
	cmd = set_int_16(cmd, int(seem_rec[0], 16), 0x08)
	cmd = set_int_16(cmd, int(seem_rec[1], 16), 0x0A)
	cmd = set_int_16(cmd, 0x01, 0x00)
	print(cmd.hex().upper())


def write_seem(seem, seem_data):
	# Examples:
	#  0001002F001100000004000100000009080A00000011325406

	seem_rec = seem.split('_')
	data = bytearray.fromhex(seem_data)
	cmd = bytearray(b'\xFF\xFF\x00\x2F\x00\x08\x00\x00\xAA\xAA\xBB\xBB\x00\x00\x00\x00')
	cmd = set_int_16(cmd, len(data) + 8, 0x04)
	cmd = set_int_16(cmd, int(seem_rec[0], 16), 0x08)
	cmd = set_int_16(cmd, int(seem_rec[1], 16), 0x0A)
	cmd = set_int_16(cmd, len(data), 0x0E)
	cmd = set_int_16(cmd, 0x01, 0x00)
	cmd += data
	print(cmd.hex().upper())


def view_seem(seem_data):
	# Examples:
	#  0001002F001100000004000100000009080A00000011325406

	count = 0
	print('Byte10\tByte16\tValue\t76543210')
	print('--------------------------------')
	for byte in bytearray.fromhex(seem_data):
		print('{:04d}\t{:04x}\t{:02x}\t{:08b}'.format(count, count, byte, byte).upper())
		count += 1


if __name__ == '__main__':
	if len(sys.argv) == 3:
		if sys.argv[1] == 'delete_file':
			delete_file(sys.argv[2])
		elif sys.argv[1] == 'create_dir':
			create_dir(sys.argv[2])
		elif sys.argv[1] == 'delete_dir':
			delete_dir(sys.argv[2])
		elif sys.argv[1] == 'read_seem':
			read_seem(sys.argv[2])
		elif sys.argv[1] == 'view_seem':
			view_seem(sys.argv[2])
		else:
			print_usage()
	elif len(sys.argv) == 4:
		if sys.argv[1] == 'change_attr':
			change_attr(sys.argv[2], sys.argv[3])
		elif sys.argv[1] == 'write_seem':
			write_seem(sys.argv[2], sys.argv[3])
		else:
			print_usage()
	else:
		print_usage()
