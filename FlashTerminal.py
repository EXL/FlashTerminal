#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Information #########################################################################################################

'''
A Flash Terminal utility for various Motorola phones using Motorola Flash Protocol.

Python: 3.10+
License: MIT
Authors: EXL, usernameak, kraze1984, dffn3, Vilko, Evy, motoprogger, b1er, dion, whoever, MotoFan.Ru, ROMphonix
Thanks: PUNK-398, asdf, wavvy01, diokhann, metalman87, ahsim2009, greyowls, Ivan_Fox, kostett
Date: 10-May-2024
Version: 1.0
'''

## Imports #############################################################################################################

import os
import sys
import time
import serial
import logging
import usb.core
import usb.util

## Settings ############################################################################################################

usb_devices = [
	{'usb_vid': 0x22B8, 'usb_pid': 0x2823, 'mode': 'flash', 'desc': 'Motorola PCS Flash MSM5100'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2A23, 'mode': 'flash', 'desc': 'Motorola PCS Flash MSM6100'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2B43, 'mode': 'flash', 'desc': 'Motorola PCS Flash MSM6125'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2A63, 'mode': 'flash', 'desc': 'Motorola PCS Flash MSM6500/MSM6800'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2B23, 'mode': 'flash', 'desc': 'Motorola PCS Flash MSM6550'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2C63, 'mode': 'flash', 'desc': 'Motorola PCS Flash MSM6575/MSM6800'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x1801, 'mode': 'flash', 'desc': 'Motorola PCS Flash Rainbow'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x4903, 'mode': 'flash', 'desc': 'Motorola PCS Flash LTE'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x3803, 'mode': 'flash', 'desc': 'Motorola PCS Flash LT'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x5803, 'mode': 'flash', 'desc': 'Motorola PCS Flash ULS'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x1001, 'mode': 'flash', 'desc': 'Motorola PCS Flash Patriot'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x3002, 'mode': 'at', 'desc': 'Motorola PCS A835/E1000 GSM Phone (AT)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x3001, 'mode': 'p2k', 'desc': 'Motorola PCS A835/E1000 GSM Phone (P2K)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x1C02, 'mode': 'at', 'desc': 'Motorola PCS Siemens Phone U10 (AT)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x1C01, 'mode': 'p2k', 'desc': 'Motorola PCS Siemens Phone U10 (P2K)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x4902, 'mode': 'at', 'desc': 'Motorola PCS Triplet GSM Phone (AT)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x4901, 'mode': 'p2k', 'desc': 'Motorola PCS Triplet GSM Phone (P2K)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x5802, 'mode': 'at', 'desc': 'Motorola PCS C350L Phone (AT)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x5801, 'mode': 'p2k', 'desc': 'Motorola PCS C350L Phone (P2K)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x1005, 'mode': 'at', 'desc': 'Motorola PCS V60 Phone (AT)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x1001, 'mode': 'p2k', 'desc': 'Motorola PCS V60 Phone (P2K)'},
]
modem_speed = 115200
modem_device = '/dev/ttyACM0'
at_command = 'AT'
p2k_mode_command = 'AT+MODE=8'
delay_ack = 0.00
delay_switch = 8.00
delay_jump = 1.00
timeout_read = 5000
timeout_write = 5000
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
		logging.debug('Uploading RAMDLD to phone and wait for RAMDLD start.')
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V3m_RAMDLD_010C.ldr', 0x00100000, 0x00100000, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V3m_RAMDLD_010C_Patched_Dump_SRAM.ldr', 0x00100000, 0x00100000, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V3m_RAMDLD_010C_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/K1m_RAMDLD_0013_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/K1mm_RAMDLD_000D_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V325i_RAMDLD_010A_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V9m_RAMDLD_01B5.ldr', 0x00100000, 0x00100000)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V9m_RAMDLD_01B5_Patched_Dump_SRAM.ldr', 0x00100000, 0x00100000)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V9m_RAMDLD_01B5_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/QA30_RAMDLD_0206_Patched_Dump_SRAM.ldr', 0x002F0000, 0x002F0000)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/QA30_RAMDLD_0206_Patched_Dump_NAND.ldr', 0x002F0000, 0x002F0000)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/QA30_RAMDLD_0206_Patched_Dump_NAND_WIDE.ldr', 0x002F0000, 0x002F0000)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/A830_RAMDLD_0520_Patched_Dump_NOR.ldr', 0x07800000, 0x07800010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/E398_RAMDLD_07B0_Hacked_Dump.ldr', 0x03FD0000, 0x03FD0010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V3x_RAMDLD_0682_RSA_Read.ldr', 0x08000000, 0x08000010, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/A835_RAMDLD_0612_Hacked_RSA_Read.ldr', 0x08000000, 0x08018818)
#		mfp_uls_upload(er, ew, 'loaders/C350L_RAMDLD_0000_Patched_Dump_NOR.ldr', 0x12000000, 0x1000, False)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/E380_RAMDLD_0910_Hacked_Dump.ldr', 0x01FD0000, 0x01FD0010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V60_RAMDLD_0355_Patched_Dump_NOR.ldr', 0x11010000, 0x11010010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V60i_RAMDLD_1007_Patched_Dump_NOR.ldr', 0x11010000, 0x11010010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V120e_RAMDLD_0713_Patched_Dump_NOR.ldr', 0x01010000, 0x01010000)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/T720_RAMDLD_0370_Patched_Dump_NOR.ldr', 0x11010000, 0x11010010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V120c_RAMDLD_0312_Patched_Dump_NOR.ldr', 0x41008000, 0x41008010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/E1000_RAMDLD_0610.ldr', 0x07804000, 0x07804010, True)

	# Commands executed on Bootloader or RAMDLD (if loaded) side.
	mfp_cmd(er, ew, 'RQVN')
#	mfp_cmd(er, ew, 'RQSN')
#	mfp_cmd(er, ew, 'RQSF')
#	mfp_cmd(er, ew, 'RQRC', '00000000,00000000'.encode())
#	mfp_cmd(er, ew, 'RQRC', '00000000,00000010'.encode())
#	mfp_cmd(er, ew, 'RQRC', '00000000,00000030'.encode())
#	mfp_cmd(er, ew, 'RQRC', '00000000,00000400'.encode())
#	mfp_cmd(er, ew, 'RQRC', '60000000,60000010,00000000'.encode())
#	mfp_cmd(er, ew, 'DUMP', '10000000'.encode())

	# Dump SRAM and NOR flash.
#	mfp_dump_sram(er, ew, 'V9m_SRAM_Dump.bin', 0x00000000, 0x04000000, 0x30)
#	mfp_dump_sram(er, ew, 'V9m_SRAM_Dump.bin', 0x00000000, 0x08000000, 0x30)
#	mfp_dump_sram(er, ew, 'MSM_IRAM_Dump.bin', 0xFFFF0000, 0xFFFFFFFF, 0x10)
#	mfp_dump_sram(er, ew, 'U10_ROM_Dump.bin', 0x10000000, 0x11000000, 0x30)
#	mfp_dump_sram(er, ew, 'A830_IROM_Dump.bin', 0x00000000, 0x00010000, 0x30)
#	mfp_dump_dump(er, ew, 'E398_ROM_Dump.bin', 0x10000000, 0x12000000, 0x100)
#	mfp_dump_read(er, ew, 'V3x_ROM_Dump.bin', 0x10000000, 0x14000000, 0x100)
#	mfp_dump_sram(er, ew, 'C350L_ROM_Dump.bin', 0x10000000, 0x10800000, 0x30)
#	mfp_dump_sram(er, ew, 'C350L_IROM_Dump.bin', 0x00000000, 0x00040000, 0x30)
#	mfp_dump_dump(er, ew, 'C350_ROM_Dump.bin', 0x00000000, 0x00800000, 0x100)
#	mfp_dump_dump(er, ew, 'C350_IROM_Dump.bin', 0x10000000, 0x10400000, 0x100)
#	mfp_dump_dump(er, ew, 'C550_ROM_Dump.bin', 0x00000000, 0x01000000, 0x100)
#	mfp_dump_sram(er, ew, 'V60_IROM_Dump.bin', 0x00000000, 0x00400000, 0x30)
#	mfp_dump_sram(er, ew, 'V60_ROM_Dump.bin', 0x10000000, 0x10400000, 0x30)
#	mfp_dump_sram(er, ew, 'V70_ROM_Dump.bin', 0x10000000, 0x10800000, 0x30)
#	mfp_dump_sram(er, ew, 'V120e_ROM_Dump.bin', 0x00000000, 0x00500000, 0x30) # 4 MiB + 1 MiB
#	mfp_dump_sram(er, ew, 'T720_IROM_Dump.bin', 0x00000000, 0x00400000, 0x30)
#	mfp_dump_sram(er, ew, 'T720_ROM_Dump.bin', 0x10000000, 0x10800000, 0x30)
#	mfp_dump_sram(er, ew, 'V120c_IROM_Dump.bin', 0x00000000, 0x00400000, 0x30)
#	mfp_dump_sram(er, ew, 'V120c_ROM_Dump.bin', 0x40000000, 0x40400000, 0x30)
#	mfp_dump_rqrc(er, ew, 'E1000_ROM_Dump.bin', 0x10000000, 0x10001000)

	# Motorola A835/A845 dumping tricks.
#	mfp_cmd(er, ew, 'RQHW')
#	mfp_binary_cmd(er, ew, b'\x00\x00\x05\x70', False)
#	mfp_upload_raw_binary(er, ew, 'loaders/A835_Additional_Payload_1.bin', None, False)
#	mfp_upload_raw_binary(er, ew, 'loaders/A835_Additional_Payload_2.bin')
#	mfp_binary_cmd(er, ew, b'\x53\x00\x00\x00\x00\x00\x00\xA0\x00')
#	mfp_binary_cmd(er, ew, b'\x41')
#	mfp_dump_r(er, ew, 'A835_ROM_Dump.bin', 0x10000000, 0x11000000, 0x100)
#	mfp_dump_r(er, ew, 'A835_IROM_Dump.bin', 0x00000000, 0x00006100, 0x100)

	# Dump NAND data (64 MiB / 128 MiB / 256 MiB) and spare area.
	# Chunks are 528 bytes == 512 bytes is NAND page size + 16 bytes is NAND spare area.
#	mfp_dump_nand(er, ew, 'Z6m_NAND_Dump.bin', 0, int(0x04000000 / 512), 0x30)
#	mfp_dump_nand(er, ew, 'V9m_NAND_Dump.bin', 0, int(0x08000000 / 512), 0x30)
#	mfp_dump_nand(er, ew, 'VE40_NAND_Dump.bin', 0, int(0x08000000 / 512), 0x10)
#	mfp_dump_nand(er, ew, 'ic902_NAND_Dump.bin', 0, int(0x08000000 / 512), 0x10)
#	mfp_dump_nand(er, ew, 'QA30_NAND_Dump.bin', 0, int(0x04000000 / 512), 0x10, 4)
#	mfp_dump_nand(er, ew, 'V3m_NAND_Dump.bin', 0, int(0x04000000 / 512), 0x10, 1, 0x64000000)
#	mfp_dump_nand(er, ew, 'K1m_NAND_Dump.bin', 0, int(0x04000000 / 512), 0x10, 1, 0x64000000)
#	mfp_dump_nand(er, ew, 'V325i_NAND_Dump.bin', 0, int(0x04000000 / 512), 0x10, 1, 0x64000000)

## Motorola Flash Protocol #############################################################################################

def calculate_checksum(data):
	checksum = 0
	for byte in data:
		checksum = (checksum + byte) % 256
	return checksum

def mfp_dump_rqrc(er, ew, file_path, start, end, step = 0x01):
	addr_s = start
	addr_e = start + step + 0x400
	with open(file_path, 'wb') as file:
		index = 0
		time_start = time.process_time()
		while addr_e <= end + 0x400:
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % (step * 0x100) == 0):
				time_start = progess(step, time_start, 0x100, index, file_path, addr_s, addr_e)

			result_data1 = mfp_cmd(er, ew, 'RQRC', f'{addr_s:08X},{addr_e:08X}'.encode())
			result_data1 = result_data1[6:]   # Drop start marker and command.
			result_data1 = result_data1[:-1]  # Drop end marker.

			result_data2 = mfp_cmd(er, ew, 'RQRC', f'{addr_s + 0x01:08X},{addr_e:08X}'.encode())
			result_data2 = result_data2[6:]   # Drop start marker and command.
			result_data2 = result_data2[:-1]  # Drop end marker.

			result = int.to_bytes(
				int.from_bytes(bytes.fromhex(result_data1.decode()), 'big') -
				int.from_bytes(bytes.fromhex(result_data2.decode()), 'big'),
				1, 'big'
			)

			file.write(result)

			addr_s = addr_s + step
			addr_e = addr_s + step + 0x400
			index += step

def mfp_dump_r(er, ew, file_path, start, end, step = 0x100):
	addr_s = start
	addr_e = start + step
	with open(file_path, 'wb') as file:
		index = 0
		time_start = time.process_time()
		while addr_e <= end:
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % (step * 0x100) == 0):
				time_start = progess(step, time_start, 0x100, index, file_path, addr_s, addr_e)
			binary_cmd = bytearray()
			binary_cmd.extend('R'.encode())
			binary_cmd.extend(addr_s.to_bytes(4, byteorder = 'big'))
			binary_cmd.extend(step.to_bytes(4, byteorder = 'big'))
			result_data = mfp_binary_cmd(er, ew, binary_cmd)
			result_data = mfp_binary_cmd(er, ew, binary_cmd)
			result_data = result_data[:-1]  # Drop checksum.
			file.write(result_data)

			addr_s = addr_s + step
			addr_e = addr_s + step
			index += step

def mfp_dump_read(er, ew, file_path, start, end, step = 0x100):
	addr_s = start
	addr_e = start + step
	with open(file_path, 'wb') as file:
		index = 0
		time_start = time.process_time()
		while addr_e <= end:
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % (step * 0x100) == 0):
				time_start = progess(step, time_start, 0x100, index, file_path, addr_s, addr_e)
			result_data = mfp_cmd(er, ew, 'READ', f'{addr_s:08X},{step:04X}'.encode())
			result_data = result_data[6:]   # Drop start marker and command.
			result_data = result_data[2:]   # Drop size step.
			result_data = result_data[:-1]  # Drop checksum.
			result_data = result_data[:-1]  # Drop end marker.
			file.write(result_data)

			addr_s = addr_s + step
			addr_e = addr_s + step
			index += step

def mfp_dump_dump(er, ew, file_path, start, end, step = 0x100):
	addr_s = start
	addr_e = start + step
	with open(file_path, 'wb') as file:
		index = 0
		time_start = time.process_time()
		while addr_e <= end:
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % (step * 0x100) == 0):
				time_start = progess(step, time_start, 0x100, index, file_path, addr_s, addr_e)

			result_data = mfp_cmd(er, ew, 'DUMP', f'{addr_s:08X}'.encode())
			file.write(result_data)

			addr_s = addr_s + step
			addr_e = addr_s + step
			index += step

def mfp_dump_nand(er, ew, file_path, start, end, step = 0x30, wide_nand = 1, nand_buffer = 0x60000000, fixup = None):
	if fixup:
		nand_buffer += fixup
	addr_s = nand_buffer
	addr_e = addr_s + step
	addr_h = nand_buffer + 0x210
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
				addr_s = nand_buffer
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

def mfp_upload_binary_to_addr(er, ew, file_path, start, jump = None, rsrc = None):
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
		if rsrc:
			loader_file_size = os.path.getsize(file_path)
			end = start + loader_file_size - 1
			logging.info(f'Calculate checksum of "{start:08X},{end:08X}" region.')
			mfp_cmd(er, ew, 'RQRC', f'{start:08X},{end:08X}'.encode())
		logging.info(f'Jumping to 0x{jump:08X} address.')
		mfp_cmd(er, ew, 'JUMP', mfp_get_addr_with_chksum(jump))
		logging.info(f'Waiting {delay_jump} seconds for RAMDLD init on device...')
		time.sleep(delay_jump)

def mfp_uls_upload(er, ew, file_path, load_address = 0x12000000, chunk_size = None, read_response = False):
	binary_file_size = os.path.getsize(file_path)
	with open(file_path, 'rb') as file:
		chunk = file.read()
		chunk = bytearray(chunk)
		payload_magic = b'\x55\x55\x55\xAA'
		payload_body = load_address.to_bytes(4, 'big') + int(binary_file_size << 16).to_bytes(4, 'big')
		chunk = payload_body + chunk
		checksum = 0xFF - calculate_checksum(chunk)
		mfp_upload_raw_binary(er, ew, file_path, chunk_size, read_response, checksum, payload_magic + payload_body)

def mfp_upload_raw_binary(er, ew, file_path, chunk_size = None, read_response = True, checksum = None, payload = None):
	binary_file_size = os.path.getsize(file_path)
	if not chunk_size:
		chunk_size = binary_file_size
	logging.info(f'Uploading "{file_path}" of {binary_file_size} bytes size on {chunk_size} chunk_size...')
	with open(file_path, 'rb') as file:
		index = 0
		while True:
			# First frame.
			if index == 0 and payload:
				chunk = bytearray(payload)
				chunk.extend(file.read(chunk_size - len(payload)))
			else:
				chunk = file.read(chunk_size)

			if not chunk:
				break

			# Last frame.
			if len(chunk) < chunk_size:
				if checksum:
					chunk = bytearray(chunk)
					chunk.extend(checksum.to_bytes(1, 'big'))

			logging.debug(f'Uploading {len(chunk)},0x{len(chunk):08X} bytes from "{file_path}"...')
			mfp_binary_cmd(er, ew, chunk, read_response)
			index += 1
	logging.info(f'Uploading "{file_path}" is done.')

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
	packet.extend(len(data).to_bytes(2, 'big'))
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

def mfp_binary_cmd(er, ew, binary_cmd, read_response = True):
	if binary_cmd:
		logging.debug(f'>>> Send to device...\n{hexdump(binary_cmd)}')

	result = mfp_send_recv(er, ew, binary_cmd, read_response)
	if result:
		logging.debug(f'<<< Read from device...\n{hexdump(result)}')

	return result

def mfp_recv(er):
	return bytearray(er.read(buffer_read_size, timeout_read))

def mfp_send(ew, data):
	return ew.write(data, timeout_write)

def mfp_send_recv(er, ew, data, read_response = True):
	if data:
		mfp_send(ew, data)
	response = None
	if read_response:
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
		er, ew = usb_init(usb_devices, 'flash')
		if not er or not ew:
			logging.error('Cannot find USB device!')
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

def find_usb_device(usb_devices, mode):
	for usb_device in usb_devices:
		if usb_device['mode'] == mode:
			connected_device = usb.core.find(idVendor=usb_device['usb_vid'], idProduct=usb_device['usb_pid'])
			if connected_device:
				logging.info(f'Found: "{get_usb_device_information(usb_device)}"!')
				return connected_device
			else:
				logging.error(f'Not found: "{get_usb_device_information(usb_device)}"!')
	return None

def usb_init(usb_devices, mode):
	connected_device = find_usb_device(usb_devices, mode)
	if connected_device:
		return get_endpoints(connected_device)
	return None, None

def write_read_at_command(serial_handle, at_command, read = True):
	at_command = (at_command + '\r\n').encode()
	logging.debug(f'>>> Send to device...\n{hexdump(at_command)}')
	serial_handle.write(at_command)
	serial_handle.flush()

	if read:
		data_read = serial_handle.readall()
		logging.debug(f'<<< Read from device...\n{hexdump(data_read)}')
		return data_read

	return None

def switch_atmode_to_p2kmode(modem_device, modem_speed):
	if os.path.exists(modem_device):
		logging.info(f'USB modem device "{modem_device}" found, switch it to P2K mode!')
		serial_handle = serial.Serial(modem_device, modem_speed, timeout = 1)
		if serial_handle:
			write_read_at_command(serial_handle, at_command, True)
			time.sleep(1.0)
			write_read_at_command(serial_handle, p2k_mode_command, False)
			serial_handle.close()
			return True
		else:
			logging.error(f'Cannot open "{modem_device}" device on "{modem_speed}" speed!')
	else:
		logging.error(f'Cannot find "{modem_device}" device!')
	return False

def switch_p2kmode_to_flashmode(p2k_usb_device):
	logging.info('P2K device found, switching it to the Flash mode!')
	ctrl_packet = b'\x00\x01\x00\x0D\x00\x00\x00\x00'
	p2k_usb_device.ctrl_transfer(0x41, 0x02, 0x00, 0x08, ctrl_packet, timeout_write)
	logging.debug(f'>>> Send USB control packet '
		f'(bmRequestType=0x41, bmRequest=0x02, wValue=0x00, wIndex=0x08) to device...\n{hexdump(ctrl_packet)}')

def reconnect_device_in_flash_mode(modem_device, modem_speed, usb_devices):
	if switch_atmode_to_p2kmode(modem_device, modem_speed):
		logging.info(f'Wait {delay_switch} sec for AT => P2K switching...')
		time.sleep(delay_switch)
		p2k_usb_device = find_usb_device(usb_devices, 'p2k')
		if p2k_usb_device:
			switch_p2kmode_to_flashmode(p2k_usb_device)
			logging.info(f'Wait {delay_switch} sec for P2K => Flash switching...')
			time.sleep(delay_switch)
			return True
		else:
			logging.error('Cannot find P2K device!')
			return False

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

def hexdump(data, wide = 0x10):
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
				-s - Switch device to Flash Mode (Bootloader Mode)
				-h - Show help

			Developers and Thanks:
				- EXL, usernameak, kraze1984, dffn3, Vilko, Evy, motoprogger, b1er, dion, whoever
				- MotoFan.Ru developers
				- ROMphonix developers
				- PUNK-398, asdf, wavvy01, diokhann, metalman87, ahsim2009, greyowls, Ivan_Fox, kostett

			10-May-2024, Siberia
		''')
		exit(1)
	if '-s' in sys.argv:
		reconnect_device_in_flash_mode(modem_device, modem_speed, usb_devices)
	er, ew = usb_init(usb_devices, 'flash')
	if er and ew:
		worksheet(er, ew)

if __name__ == '__main__':
	main()
