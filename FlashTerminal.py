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
	{'usb_vid': 0x22B8, 'usb_pid': 0x2B23, 'desc': 'S Flash MSM6550'},
]
delay_ack = 0.00
timeout_read = 100
timeout_write = 100
buffer_write_size = 0x800
buffer_read_size = 0x800

## Worksheet ###########################################################################################################

def worksheet(er, ew, restart_flag):
	if restart_flag:
		mfp_cmd(er, ew, 'RESTART')
		time.sleep(2.0)
		er, ew = usb_init(usb_devices)

	# Various single commands.
	mfp_cmd(er, ew, 'RQHW')
	mfp_cmd(er, ew, 'RQVN')
#	mfp_cmd(er, ew, 'RQSW')
#	mfp_cmd(er, ew, 'RQSN')
#	mfp_cmd(er, ew, 'POWER_DOWN')
#	mfp_addr(er, ew, 0x00100000)

	# Upload RAMDLD to phone.
#	mfp_upload_binary_to_addr(er, ew, 'V9m_RAMDLD_01B5.ldr', 0x00100000, 0x00100000)
#	mfp_upload_binary_to_addr(er, ew, 'V9m_RAMDLD_01B5_Patched_Dump_SRAM.ldr', 0x00100000, 0x00100000)
#	mfp_upload_binary_to_addr(er, ew, 'V9m_RAMDLD_01B5_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000)

	# Wait for RAMDLD start.
	time.sleep(1.0)
#	mfp_cmd(er, ew, 'RQRC', '60000000,60000020'.encode())

	# Dump SRAM (64 MiB and 128 MiB).
#	mfp_dump_sram(er, ew, 'V9m_SRAM_Dump.bin', 0x00000000, 0x04000000, 0x30)
#	mfp_dump_sram(er, ew, 'V9m_SRAM_Dump.bin', 0x00000000, 0x08000000, 0x30)

	# Dump NAND data (64 MiB and 128 MiB) and spare area.
	# Chunks are 528 bytes == 512 bytes is NAND page size + 16 bytes is NAND spare area.
#	mfp_dump_nand(er, ew, 'V9m_NAND_Dump.bin', 0, int(0x04000000 / 512), 0x30)
#	mfp_dump_nand(er, ew, 'V9m_NAND_Dump.bin', 0, int(0x08000000 / 512), 0x30)

## Motorola Flash Protocol #############################################################################################

def calculate_checksum(data):
	checksum = 0
	for byte in data:
		checksum = (checksum + byte) % 256
	return checksum

def insert_to_filename(insert, filename):
	name_part, extension = filename.rsplit('.', 1)
	return f'{name_part}{insert}.{extension}'

def log_dump_info(step, time_start, size, index, file_path, addr_s, addr_e, pages = 0, nand = False):
	time_end = time.process_time()
	speed = (step * size) / (time_end - time_start) / 1024
	if nand:
		logging.info(
			f'Dumped {index:08}/{pages:08} page, 512 bytes to "{file_path}", '
			f'16 bytes to "{insert_to_filename("_spare_area",file_path)}", '
			f'addr=0x{addr_s:08X},0x{addr_e:08X}, speed={speed:.2f} Kb/s'
		)
	else:
		logging.info(f'Dumped {index} bytes to "{file_path}", addr=0x{addr_s:08X}, speed={speed:.2f} Kb/s')
	return time.process_time()  # Reset time.

def mfp_dump_nand(er, ew, file_path, start, end, step = 0x30):
	addr_s = 0x60000000
	addr_e = addr_s + step
	addr_h = 0x60000210
	with open(file_path, 'wb') as dump, open(insert_to_filename('_spare_area', file_path), 'wb') as spare:
		index = 0
		time_start = time.process_time()
		for page in range(start, end):
			logging.debug(f'Dumping NAND {page:08} page, 512+16 bytes to "{file_path}" +spare_area...')
			if index > 0 and (index % 100 == 0):
				time_start = log_dump_info(528, time_start, 100, index, file_path, addr_s, addr_h, (end - start), True)
			while addr_e <= addr_h:
				result_data = mfp_cmd(er, ew, 'RQRC', f'{addr_s:08X},{addr_e:08X},{page:08X}'.encode())
				result_data = result_data[6:]   # Drop start marker and command.
				result_data = result_data[:-1]  # Drop end marker.

				# Last chunk page. Will work only with 0x30 step!
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
			addr_h = 0x60000210

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
				time_start = log_dump_info(step, time_start, 0x100, index, file_path, addr_s, addr_e)
			result_data = mfp_cmd(er, ew, 'RQRC', f'{addr_s:08X},{addr_e:08X}'.encode())
			result_data = result_data[6:]   # Drop start marker and command.
			result_data = result_data[:-1]  # Drop end marker.
			file.write(bytearray.fromhex(result_data.decode()))

			addr_s = addr_s + step
			addr_e = addr_s + step
			index += step

def mfp_upload_binary_to_addr(er, ew, file_path, start, jump = None):
	address = start
	with open(file_path, 'rb') as file:
		while True:
			chunk = file.read(buffer_write_size)
			if not chunk:
				break
			logging.info(f'Uploading {len(chunk)},0x{len(chunk):08X} bytes from "{file_path}" to 0x{address:08X}...')
			mfp_addr(er, ew, address)
			mfp_bin(er, ew, chunk)
			address += len(chunk)
	if jump:
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
	logging.info(f'size={len(data)}, chksum={calculate_checksum(packet)}')
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
	return None

## Utils ###############################################################################################################

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
	er, ew = usb_init(usb_devices)
	if er and ew:
		worksheet(er, ew, '-r' in sys.argv)

if __name__ == '__main__':
	main()
