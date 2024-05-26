#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Information #########################################################################################################

'''
A Flash Terminal utility for various Motorola phones using Motorola Flash Protocol.

Python: 3.10+
License: MIT
Authors: EXL, usernameak, kraze1984, dffn3, Vilko, motoprogger, b1er, MotoFan.Ru developers
Date: 10-May-2024
Version: 1.0
'''

## Imports #############################################################################################################

import sys
import time
import logging
import usb.core
import usb.util

## Settings ############################################################################################################

usb_devices = [
	{'usb_vid': 0x22B8, 'usb_pid': 0x2A63, 'desc': 'Motorola PCS Flash MSM6500'},  # Wrong SoC, ic902 uses MSM6800.
	{'usb_vid': 0x22B8, 'usb_pid': 0x2B23, 'desc': 'Motorola PCS Flash MSM6550'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2C63, 'desc': 'Motorola PCS Flash MSM6575/MSM6800'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x1801, 'desc': 'Motorola PCS Flash Rainbow'},
]
delay_ack = 0.00
timeout_read = 100
timeout_write = 100
buffer_write_size = 0x800
buffer_read_size = 0x800

## Worksheet ###########################################################################################################

def worksheet(er, ew):
	er, ew = usb_check_restart_phone(er, ew, '-r' in sys.argv)

	# Various single commands.
	mfp_cmd(er, ew, 'RQHW')
	mfp_cmd(er, ew, 'RQVN')
#	mfp_cmd(er, ew, 'RQSW')
#	mfp_cmd(er, ew, 'RQSN')
#	mfp_cmd(er, ew, 'POWER_DOWN')
#	mfp_addr(er, ew, 0x00100000)

	if '-l' in sys.argv:
		# Upload RAMDLD to phone and wait for RAMDLD start.
#		mfp_upload_binary_to_addr(er, ew, 'V3m_RAMDLD_010C.ldr', 0x00100000, 0x00100000)
#		mfp_upload_binary_to_addr(er, ew, 'V3m_RAMDLD_010C_Patched_Dump_SRAM.ldr', 0x00100000, 0x00100000)
#		mfp_upload_binary_to_addr(er, ew, 'V3m_RAMDLD_010C_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000)
#		mfp_upload_binary_to_addr(er, ew, 'V9m_RAMDLD_01B5.ldr', 0x00100000, 0x00100000)
#		mfp_upload_binary_to_addr(er, ew, 'V9m_RAMDLD_01B5_Patched_Dump_SRAM.ldr', 0x00100000, 0x00100000)
#		mfp_upload_binary_to_addr(er, ew, 'V9m_RAMDLD_01B5_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000)
#		mfp_upload_binary_to_addr(er, ew, 'QA30_RAMDLD_0206_Patched_Dump_SRAM.ldr', 0x002F0000, 0x002F0000)
#		mfp_upload_binary_to_addr(er, ew, 'QA30_RAMDLD_0206_Patched_Dump_NAND.ldr', 0x002F0000, 0x002F0000)
#		mfp_upload_binary_to_addr(er, ew, 'QA30_RAMDLD_0206_Patched_Dump_NAND_WIDE.ldr', 0x002F0000, 0x002F0000)
#		mfp_upload_binary_to_addr(er, ew, 'A830_RAMDLD_0520_Patched_1byte.ldr', 0x07800000, 0x07800010)
#		mfp_upload_binary_to_addr(er, ew, 'A835_RAMDLD_0612_Hacked_RSA_Read.ldr', 0x08000000, 0x08000010)
		time.sleep(1.0)

	# Commands with arguments.
#	mfp_cmd(er, ew, 'RQRC', '00000000,00000400'.encode())
#	mfp_cmd(er, ew, 'RQRC', '60000000,60000010,00000000'.encode())

	# Dump SRAM and NOR flash (64 MiB and 128 MiB).
#	mfp_dump_sram(er, ew, 'V9m_SRAM_Dump.bin', 0x00000000, 0x04000000, 0x30)
#	mfp_dump_sram(er, ew, 'V9m_SRAM_Dump.bin', 0x00000000, 0x08000000, 0x30)
#	mfp_dump_sram(er, ew, 'MSM_IRAM_Dump.bin', 0xFFFF0000, 0xFFFFFFFF, 0x10)
#	mfp_dump_sram_1byte(er, ew, 'A830_IROM_Dump.bin', 0x00000000, 0x00010000)
#	mfp_dump_sram_1byte(er, ew, 'A830_ROM_Dump.bin', 0x10000000, 0x11000000)

	# Dump NAND data (64 MiB / 128 MiB / 256 MiB) and spare area.
	# Chunks are 528 bytes == 512 bytes is NAND page size + 16 bytes is NAND spare area.
#	mfp_dump_nand(er, ew, 'Z6m_NAND_Dump.bin', 0, int(0x04000000 / 512), 0x30)
#	mfp_dump_nand(er, ew, 'V9m_NAND_Dump.bin', 0, int(0x08000000 / 512), 0x30)
#	mfp_dump_nand(er, ew, 'VE40_NAND_Dump.bin', 0, int(0x08000000 / 512), 0x10)
#	mfp_dump_nand(er, ew, 'ic902_NAND_Dump.bin', 0, int(0x08000000 / 512), 0x10)
#	mfp_dump_nand(er, ew, 'QA30_NAND_Dump.bin', 0, int(0x04000000 / 512), 0x10, 4)

## Motorola Flash Protocol #############################################################################################

def calculate_checksum(data):
	checksum = 0
	for byte in data:
		checksum = (checksum + byte) % 256
	return checksum

def mfp_dump_nand(er, ew, file_path, start, end, step = 0x30, wide_nand = 1):
	addr_s = 0x60000000
	addr_e = addr_s + step
	addr_h = 0x60000210
	with open(file_path, 'wb') as dump, open(insert_to_filename('_spare_area', file_path), 'wb') as spare:
		index = 0
		time_start = time.process_time()
		for page in range(start, end):
			for wide in range(wide_nand):
				logging.debug(f'Dumping NAND {page:08} page ({wide:02}), 512+16 bytes to "{file_path}" +spare_area...')
				if index > 0 and (index % 100 == 0):
					time_start = progess(
						528, time_start, 100, index, file_path,
						addr_s, addr_h, (end - start) * wide_nand, True
					)
				while addr_e <= addr_h:
					if wide_nand > 1:
						result_data = mfp_cmd(er, ew, 'RQRC',
							f'{addr_s:08X},{addr_e:08X},{page:08X},{wide:08X}'.encode())
					else:
						result_data = mfp_cmd(er, ew, 'RQRC', f'{addr_s:08X},{addr_e:08X},{page:08X}'.encode())
					result_data = result_data[6:]   # Drop start marker and command.
					result_data = result_data[:-1]  # Drop end marker.

					# Last chunk page. Be careful! Will work only with 0x10 and 0x30 step values!
					if addr_e == addr_h:
						spare_area  = result_data[-16 * 2:]  # 16 * 2 because in HEX byte length is 2.
						result_data = result_data[:-16 * 2]  # Trim spare area from the last packet.
						spare.write(bytearray.fromhex(spare_area.decode()))

					dump.write(bytearray.fromhex(result_data.decode()))

					addr_s = addr_s + step
					addr_e = addr_s + step

				index += 1
				addr_s = 0x60000000
				addr_e = addr_s + step

def mfp_dump_sram(er, ew, file_path, start, end, step = 0x30):
	addr_s = start
	addr_e = start + step
	with open(file_path, 'wb') as file:
		index = 0
		time_start = time.process_time()
		while addr_e <= end + step:
			if addr_e > end:
				addr_e = end
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % (step * 0x100) == 0):
				time_start = progess(step, time_start, 0x100, index, file_path, addr_s, addr_e)
			result_data = mfp_cmd(er, ew, 'RQRC', f'{addr_s:08X},{addr_e:08X}'.encode())
			result_data = result_data[6:]   # Drop start marker and command.
			result_data = result_data[:-1]  # Drop end marker.
			file.write(bytearray.fromhex(result_data.decode()))

			addr_s = addr_s + step
			addr_e = addr_s + step
			index += step

def mfp_dump_sram_1byte(er, ew, file_path, start, end):
	addr_s = start
	addr_e = start
	with open(file_path, 'wb') as file:
		index = 0
		time_start = time.process_time()
		while addr_e < end:
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % (0x01 * 0x100) == 0):
				time_start = progess(0x01, time_start, 0x100, index, file_path, addr_s, addr_e)
			result_data = mfp_cmd(er, ew, 'RQRC', f'{addr_s:08X},{addr_e:08X}'.encode())
			result_data = result_data[6:]   # Drop start marker and command.
			result_data = result_data[:-1]  # Drop end marker.
			result_data = result_data[2:]   # Drop leading zero byte.
			file.write(bytearray.fromhex(result_data.decode()))

			addr_s += 1
			addr_e += 1
			index += 1

def mfp_upload_binary_to_addr(er, ew, file_path, start, jump = None):
	address = start
	logging.info(f'Uploading "{file_path}" to 0x{address:08X} with {buffer_write_size} bytes chunks...')
	with open(file_path, 'rb') as file:
		while True:
			chunk = file.read(buffer_write_size)
			if not chunk:
				break
			logging.debug(f'Uploading {len(chunk)},0x{len(chunk):08X} bytes from "{file_path}" to 0x{address:08X}...')
			mfp_addr(er, ew, address)
			mfp_bin(er, ew, chunk)
			address += len(chunk)
	logging.info(f'Uploading "{file_path}" to 0x{address:08X} is done.')
	if jump:
		logging.info(f'Jumping to 0x{jump:08X} address.')
		mfp_cmd(er, ew, 'JUMP', mfp_get_addr_with_chksum(jump))

def mfp_get_addr_with_chksum(address):
	addr_data = bytearray()
	addr_data.extend(f'{address:08X}'.encode())
	addr_data.extend(f'{calculate_checksum(addr_data):02X}'.encode())
	return addr_data

def mfp_addr(er, ew, address):
	result = mfp_cmd(er, ew, 'ADDR', mfp_get_addr_with_chksum(address))
	return result

def mfp_bin(er, ew, data):
	packet = bytearray()
	packet.extend(len(data).to_bytes(2, "big"))
	packet.extend(data)
	packet.append(calculate_checksum(packet))
	logging.debug(f'BIN packet: size={len(data)}, chksum={calculate_checksum(packet)}')
	result = mfp_cmd(er, ew, 'BIN', packet)
	return result

def mfp_cmd(er, ew, cmd, data = None):
	packet = bytearray(b'\x02')  # Start marker.
	packet.extend(cmd.encode())
	if data:
		packet.extend(b'\x1E')  # Data separator.
		packet.extend(data)
	packet.extend(b'\x03')  # End marker.
	logging.debug(f'>>> Send to device...\n{hexdump(packet)}')

	result = mfp_send_recv(er, ew, packet)
	logging.debug(f'<<< Read from device...\n{hexdump(result)}')

	return result

def mfp_recv(er):
	return bytearray(er.read(buffer_read_size, timeout_read))

def mfp_send(ew, data):
	return ew.write(data, timeout_write)

def mfp_send_recv(er, ew, data):
	mfp_send(ew, data)
	response = None
	while not response:
		try:
			response = mfp_recv(er)
		except usb.USBError as error:
			# TODO: Proper USB errors handling.
			logging.error(f'USB Error: {error}')
			exit(1)
		time.sleep(delay_ack)
	return response

## USB Routines ########################################################################################################

def usb_check_restart_phone(er, ew, restart_flag):
	if restart_flag:
		mfp_cmd(er, ew, 'RESTART')
		time.sleep(2.0)
		er, ew = usb_init(usb_devices)
		if not er or not ew:
			logging.error(f'Cannot find USB device!')
			exit(1)
	return er, ew

def get_usb_device_information(usb_device):
	return f'{usb_device["desc"]}: usb_vid={usb_device["usb_vid"]:04X}, usb_pid={usb_device["usb_pid"]:04X}'

def get_endpoints(device):
	device.set_configuration()

	config = device.get_active_configuration()
	logging.debug(config)

	interface = config[(0, 0)]
	logging.debug(interface)

	ep_read = usb.util.find_descriptor(
		interface,
		custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
	)
	logging.debug(ep_read)

	ep_write = usb.util.find_descriptor(
		interface,
		custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
	)
	logging.debug(ep_write)

	return (ep_read, ep_write)

def find_usb_device(usb_devices):
	for usb_device in usb_devices:
		logging.info(f'Trying to find "{get_usb_device_information(usb_device)}" USB device...')
		connected_device = usb.core.find(idVendor=usb_device['usb_vid'], idProduct=usb_device['usb_pid'])
		if connected_device:
			logging.info(f'Found: "{get_usb_device_information(usb_device)}"!')
			return connected_device
		else:
			logging.error(f'Not found: "{get_usb_device_information(usb_device)}"!')
	return None

def usb_init(usb_devices):
	connected_device = find_usb_device(usb_devices)
	if connected_device:
		return get_endpoints(connected_device)
	return None, None

## Utils ###############################################################################################################

def insert_to_filename(insert, filename):
	name_part, extension = filename.rsplit('.', 1)
	return f'{name_part}{insert}.{extension}'

def progess(step, time_start, size, index, file_path, addr_s, addr_e, pages = 0, nand = False):
	time_end = time.process_time()
	speed = (step * size) / (time_end - time_start) / 1024
	if nand:
		logging.info(
			f'Dumped {index:08}/{pages:08} pages, 512 bytes to "{file_path}", '
			f'16 bytes to "{insert_to_filename("_spare_area",file_path)}", '
			f'addr=0x{addr_s:08X},0x{addr_e:08X}, speed={speed:.2f} Kb/s'
		)
	else:
		logging.info(f'Dumped {index} bytes to "{file_path}", addr=0x{addr_s:08X}, speed={speed:.2f} Kb/s')
	return time.process_time()  # Reset time.

def hexdump(data, wide = 0x0F):
	line = bytearray()
	result = ''
	index = offset = 0
	for byte in data:
		line.append(byte)
		index += 1
		if index == wide:
			result += hexdump_line(offset, line, wide)
			offset += wide
			index = 0
			line = bytearray()
	if line:
		result += hexdump_line(offset, line, wide)
	return result

def hexdump_line(offset, bytes_array, wide):
	line = f'{offset:08X}:  '
	ascii = ' |'
	for byte in bytes_array:
		line += f'{byte:02X} '
		ascii += chr(byte) if byte in range(32, 127) else '.'
	if len(bytes_array) < wide:
		for i in range(wide - len(bytes_array)):
			line += '   '
			ascii += ' '
	ascii += '|'
	line += ascii
	line += '\n'
	return line

def set_logging_configuration(verbose):
	log_fmt = '%(asctime)s %(levelname)s:\n%(message)s\n'
	if verbose:
		log_fmt = '%(asctime)s %(levelname)s [%(funcName)s]:\n%(message)s\n'
	logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, format=log_fmt, datefmt='%d-%b-%Y %H:%M:%S')

## Entry Point #########################################################################################################

def main():
	set_logging_configuration('-v' in sys.argv)
	if '-h' in sys.argv:
		logging.info('''
			Motorola Flash Terminal Utility v1.0

			Flags:
				-v - Verbose USB packets
				-r - Reboot device
				-l - Upload RAMDLD to RAM
				-h - Show help

			Developers and Thanks:
				- EXL, usernameak, kraze1984, dffn3, Vilko, motoprogger, b1er
				- MotoFan.Ru developers
				- ROMphonix developers

			10-May-2024, Siberia
		''')
		exit(1)
	er, ew = usb_init(usb_devices)
	if er and ew:
		worksheet(er, ew)

if __name__ == '__main__':
	main()
