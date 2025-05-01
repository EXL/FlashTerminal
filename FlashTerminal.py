#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Information #########################################################################################################

splash = '''
Motorola Flash Terminal Utility v1.0

	A Flash Terminal utility for various Motorola phones using Motorola Flash Protocol.

Python:
	3.6+

License:
	MIT

Flags:
	-v       - Verbose USB packets
	-r       - Reboot device
	-l       - Upload RAMDLD to RAM
	-s       - Switch device to Flash Mode (Bootloader Mode)
	-2       - Use second USB interface for BP Bootloader
	-p       - Do some P2K stuff (MEMACS, P2K_INFO, FILES_DUMP)
	-at_skip - Skip AT => P2K switching
	-at_usb  - Use AT USB writing instead of /dev/ttyACM0 writing
	-h       - Show help

Developers and Thanks:
	- EXL, usernameak, kraze1984, dffn3, Vilko, Evy, motoprogger, b1er, dion, whoever, muromec
	- MotoFan.Ru developers
	- ROMphonix developers
	- PUNK-398, asdf, wavvy01, diokhann, metalman87, ahsim2009, greyowls, Ivan_Fox, kostett
	- SGXVII, NextG50, ronalp, CrayZor, Paschendale, fkcoder, overglube, MC4f, regenfaellt
	- Den K, WN3DL

10-May-2024, Siberia
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
	{'usb_vid': 0x22B8, 'usb_pid': 0x2A03, 'mode': 'flash', 'desc': 'Motorola PCS Flash MSM6050'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2A23, 'mode': 'flash', 'desc': 'Motorola PCS Flash MSM6100'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2B43, 'mode': 'flash', 'desc': 'Motorola PCS Flash MSM6125'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2A63, 'mode': 'flash', 'desc': 'Motorola PCS Flash MSM6500/MSM6800'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2B23, 'mode': 'flash', 'desc': 'Motorola PCS Flash MSM6550'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2C63, 'mode': 'flash', 'desc': 'Motorola PCS Flash MSM6575/MSM6800'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x1801, 'mode': 'flash', 'desc': 'Motorola PCS Flash Rainbow/Rainbow POG'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x4903, 'mode': 'flash', 'desc': 'Motorola PCS Flash LTE/LTE2/LTE2 irom0400'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x3803, 'mode': 'flash', 'desc': 'Motorola PCS Flash LT'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x5803, 'mode': 'flash', 'desc': 'Motorola PCS Flash ULS'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x1001, 'mode': 'flash', 'desc': 'Motorola PCS Flash Patriot'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x0001, 'mode': 'flash', 'desc': 'Motorola PCS Flash Wally'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x6003, 'mode': 'flash', 'desc': 'Motorola PCS Flash Dalhart'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x6008, 'mode': 'flash', 'desc': 'Motorola PCS Flash Dalhart RAMDLD'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x6023, 'mode': 'flash', 'desc': 'Motorola PCS Flash Bulverde'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x6403, 'mode': 'flash', 'desc': 'Motorola PCS Flash ArgonLV/SCM-A11'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x6460, 'mode': 'flash', 'desc': 'Motorola PCS Flash Argon+'}, # M702iG
	{'usb_vid': 0x22B8, 'usb_pid': 0x2D33, 'mode': 'flash', 'desc': 'Motorola PCS Flash Rhodes'},
	{'usb_vid': 0x22B8, 'usb_pid': 0xBEEF, 'mode': 'flash', 'desc': 'Motorola PCS Flash Bulverde (gen-blob)'},
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
	{'usb_vid': 0x22B8, 'usb_pid': 0x3802, 'mode': 'at', 'desc': 'Motorola PCS EZX Phone (AT)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x6009, 'mode': 'p2k', 'desc': 'Motorola PCS EZX Phone (P2K)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x0005, 'mode': 'at', 'desc': 'Motorola PCS V120c Phone (AT)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x0001, 'mode': 'p2k', 'desc': 'Motorola PCS V120c Phone (P2K)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2822, 'mode': 'at', 'desc': 'Motorola PCS V120e Phone (AT)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2821, 'mode': 'p2k', 'desc': 'Motorola PCS V120e Phone (P2K)'},
	{'usb_vid': 0x1907, 'usb_pid': 0x0001, 'mode': 'at', 'desc': 'Elcoteq Mosel GSM Phone (AT)'},
	{'usb_vid': 0x1907, 'usb_pid': 0x0002, 'mode': 'p2k', 'desc': 'Elcoteq Mosel GSM Phone (P2K)'},
	{'usb_vid': 0x11F5, 'usb_pid': 0x0007, 'mode': 'at', 'desc': 'Siemens CC75 GSM Phone (AT)'},
	{'usb_vid': 0x11F5, 'usb_pid': 0x0008, 'mode': 'p2k', 'desc': 'Siemens CC75 GSM Phone (P2K)'},
	{'usb_vid': 0x11F5, 'usb_pid': 0x0008, 'mode': 'flash', 'desc': 'Siemens CC75 GSM Phone (Flash)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2D34, 'mode': 'at', 'desc': 'Motorola PCS Rhodes Phone (AT)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2D31, 'mode': 'p2k', 'desc': 'Motorola PCS Rhodes Phone (P2K)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x6408, 'mode': 'at', 'desc': 'Motorola PCS FOMA M702iG (AT)'},
	{'usb_vid': 0x22B8, 'usb_pid': 0x2D31, 'mode': 'p2k', 'desc': 'Motorola PCS Rhodes Phone (P2K)'},
]
modem_speed = 115200
modem_device = '/dev/ttyACM0'
at_command = 'AT'
p2k_mode_command = 'AT+MODE=8'
p2k_command_list = 'P2kCommandList.txt'
delay_ack = 0.00
delay_switch = 8.00
delay_jump = 1.00
timeout_read = 5000
timeout_write = 5000
buffer_write_size = 0x2000
buffer_read_size = 0x2000

## Worksheets ##########################################################################################################

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
		check_and_load_ezx_ap_bp_ramdlds(er, ew)
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
#		mfp_upload_binary_to_addr(er, ew, 'loaders/L6_RAMDLD_08D5_RSA_Read.ldr', 0x03FD0000, 0x03FD0010, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/E1000_RAMDLD_0610.ldr', 0x07804000, 0x07804010, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V3x_RAMDLD_0682_RSA_Read.ldr', 0x08000000, 0x08000010, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/A1000_BP_RAMDLD_0651_RSA_Read.ldr', 0x08000000, 0x08000010, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/A835_RAMDLD_0612_Hacked_RSA_Read.ldr', 0x08000000, 0x08018818)
#		mfp_uls_upload(er, ew, 'loaders/C350L_RAMDLD_0000_Patched_Dump_NOR.ldr', 0x12000000, 0x1000, False)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/E380_RAMDLD_0910_Hacked_Dump.ldr', 0x01FD0000, 0x01FD0010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V60_RAMDLD_0355_Patched_Dump_NOR.ldr', 0x11010000, 0x11010010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V60i_RAMDLD_1007_Patched_Dump_NOR.ldr', 0x11010000, 0x11010010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/T720_RAMDLD_0370_Patched_Dump_NOR.ldr', 0x11010000, 0x11010010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/T722i_RAMDLD_0380.ldr', 0x11010000, 0x11010010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V120e_RAMDLD_0713_Patched_Dump_NOR.ldr', 0x01010000, 0x01010000)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/V120c_RAMDLD_0312_Patched_Dump_NOR.ldr', 0x41008000, 0x41008010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/W315_RAMDLD_0106_Patched_Dump_NOR.ldr', 0x14010000, 0x14010000)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/K1s_RAMDLD_0DC0.ldr', 0x03FC8000, 0x03FC8010, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/L72_RAMDLD_0C70.ldr', 0x03FC8000, 0x03FC8010, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/U3_RAMDLD_0CF0.ldr', 0x03FC8000, 0x03FC8010, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/K3_RAMDLD_0320.ldr', 0x80000000, 0x80000038, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/LTE-Hitagi.ldr', 0x03FD0000, 0x03FD0000)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/VE70_RAMDLD_0101.ldr', 0x00800000, 0x00800078, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/VE70_RAMDLD_0101_Patched_Dump_NAND.ldr', 0x00800000, 0x00800078, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/VE70_RAMDLD_0101_Patched_Dump_NAND_WIDE.ldr', 0x00800000, 0x00800078, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/VE66_RAMDLD_0905.ldr', 0x90500000, 0x90500038, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/A910_BP_RAMDLD_0912.ldr', 0x03FC8000, 0x03FC8010, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/A910i_BP_RAMDLD_0982.ldr', 0x03FC8000, 0x03FC8010, True)
		mfp_upload_binary_to_addr(er, ew, 'loaders/M702iG_RAMDLD_0303.ldr', 0x80000000, 0x80000038, True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/M702iS_RAMDLD_0303.ldr', 0x80000000, 0x80000038, True)

	# Commands executed on Bootloader or RAMDLD (if loaded) side.
	mfp_cmd(er, ew, 'RQVN')
#	mfp_cmd(er, ew, 'RQSN')
#	mfp_cmd(er, ew, 'RQSF')
#	mfp_cmd(er, ew, 'RQRC', '00000000,00000000'.encode())
#	mfp_cmd(er, ew, 'RQRC', '00000000,00000010'.encode())
#	mfp_cmd(er, ew, 'RQRC', '00000000,00000030'.encode())
#	mfp_cmd(er, ew, 'RQRC', '10000000,10000400'.encode())
#	mfp_cmd(er, ew, 'RQRC', '00000000,00000400'.encode())
#	mfp_cmd(er, ew, 'RQRC', '60000000,60000010,00000000'.encode())
#	mfp_cmd(er, ew, 'DUMP', '10000000'.encode())

	# LTE Hitagi 0.1 by muromec
	# https://github.com/muromec/lte-hitagi
	# https://github.com/MotoFanRu/LTE-Hitagi
#	mfp_cmd(er, ew, 'RAMLDR')
#	mfp_cmd(er, ew, 'HLP')
#	mfp_cmd(er, ew, 'ECHO', '100'.encode())
#	mfp_binary_cmd(er, ew, b'C')
#	mfp_binary_cmd(er, ew, b'R' + 0x10000000.to_bytes(4, byteorder='big') + 0x00000800.to_bytes(4, byteorder='big'))
#	mfp_dump_dump(er, ew, 'E1_ROM_Dump.bin', 0x10000000, 0x12000000, 0x800)

	# Dump SRAM and NOR flash.
#	mfp_dump_sram(er, ew, 'V9m_SRAM_Dump.bin', 0x00000000, 0x04000000, 0x30)
#	mfp_dump_sram(er, ew, 'V9m_SRAM_Dump.bin', 0x00000000, 0x08000000, 0x30)
#	mfp_dump_sram(er, ew, 'MSM_IRAM_Dump.bin', 0xFFFF0000, 0xFFFFFFFF, 0x10)
#	mfp_dump_sram(er, ew, 'U10_ROM_Dump.bin', 0x10000000, 0x11000000, 0x30)
#	mfp_dump_sram(er, ew, 'A830_IROM_Dump.bin', 0x00000000, 0x00010000, 0x30)
#	mfp_dump_dump(er, ew, 'E398_ROM_Dump.bin', 0x10000000, 0x12000000, 0x100)
#	mfp_dump_dump(er, ew, 'E398_IROM_Dump.bin', 0x00000000, 0x00200000, 0x100)
#	mfp_dump_read(er, ew, 'L6_ROM_Dump.bin', 0x10000000, 0x12000000, 0x100)
#	mfp_dump_rqrc(er, ew, 'E1000_ROM_Dump.bin', 0x10000000, 0x10010000)
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
#	mfp_dump_sram(er, ew, 'W315_ROM_Dump.bin', 0x00000000, 0x01000000, 0x30)
#	mfp_dump_sram(er, ew, 'A760_AP_ROM_Dump.bin', 0x00000000, 0x02000000, 0x30)
#	mfp_dump_sram(er, ew, 'A760_BP_ROM_Dump.bin', 0x00000000, 0x00400000, 0x30)
#	mfp_dump_sram(er, ew, 'A760_BP_IROM_Dump.bin', 0x10000000, 0x10400000, 0x30)
#	mfp_dump_read(er, ew, 'A768i_BP_ROM_Dump.bin', 0x00000000, 0x00400000, 0x100)
#	mfp_dump_read(er, ew, 'A768i_BP_IROM_Dump.bin', 0x10000000, 0x10400000, 0x100)
#	mfp_dump_read(er, ew, 'A780_BP_ROM_Dump.bin', 0x10000000, 0x10400000, 0x100)
#	mfp_dump_read(er, ew, 'A1000_ROM_Dump.bin', 0x10000000, 0x11000000, 0x100)
#	mfp_dump_rqrc(er, ew, 'A1000_PDS_ROM_Dump.bin', 0x10010000, 0x10020000)
#	mfp_dump_read(er, ew, 'L9_ROM_Dump.bin', 0x10000000, 0x14000000, 0x100)
#	mfp_dump_read(er, ew, 'U3_ROM_Dump.bin', 0x10000000, 0x12000000, 0x100)
#	mfp_dump_read(er, ew, 'K3_ROM_Dump_1.bin', 0xA0000000, 0xA2000000, 0x300)
#	mfp_dump_read(er, ew, 'K3_ROM_Dump_2.bin', 0xB4000000, 0xB6000000, 0x300)
#	mfp_dump_read(er, ew, 'A910_BP_ROM_Dump.bin', 0x10000000, 0x10400000, 0x100)
#	mfp_dump_rbin(er, ew, 'A910_AP_ROM_Dump.bin', 0x00000000, 0x04000000, 0x1000)
	mfp_dump_read(er, ew, 'M701iG_IROM_Dump.bin', 0x00000000, 0x00008000)
#	mfp_dump_read(er, ew, 'M701iG_ROM_Dump_1.bin', 0xA0000000, 0xA2000000, 0x300)
#	mfp_dump_read(er, ew, 'M701iG_ROM_Dump_2.bin', 0xB4000000, 0xB6000000, 0x300)

	# Motorola A835/A845 dumping tricks.
#	mfp_cmd(er, ew, 'RQHW')
#	mfp_binary_cmd(er, ew, b'\x00\x00\x05\x70', False)
#	mfp_upload_raw_binary(er, ew, 'loaders/A835_Additional_Payload_1.bin', None, False)
#	mfp_upload_raw_binary(er, ew, 'loaders/A835_Additional_Payload_2.bin')
#	mfp_binary_cmd(er, ew, b'\x53\x00\x00\x00\x00\x00\x00\xA0\x00')
#	mfp_binary_cmd(er, ew, b'\x41')
#	mfp_dump_r(er, ew, 'A835_ROM_Dump.bin', 0x10000000, 0x11000000, 0x100)
#	mfp_dump_r(er, ew, 'C975_ROM_Dump.bin', 0x10000000, 0x12000000, 0x100)
#	mfp_dump_r(er, ew, 'E1000_ROM_Dump.bin', 0x10000000, 0x14000000, 0x100)
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

	# Motorola C350L full 8 MiB ROM flashing!
#	mfp_cmd(er, ew, 'ERASE')
#	mfp_upload_binary_to_addr(er, ew, 'С350L_ROM_Dump_8M.bin', 0x10000000, None)

def check_and_load_ezx_ap_bp_ramdlds(er, ew):
	if not '-2' in sys.argv:
		# EZX AP
#		mfp_upload_binary_to_addr(er, ew, 'loaders/A760_AP_RAMDLD_0000_Patched_Dump_NOR.ldr', 0xA0200000, 0xA0200000, ezx_ap=True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/A768i_AP_RAMDLD_0000_Patched_Dump_NOR.ldr', 0xA0200000, 0xA0200000, ezx_ap=True)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/A780g_AP_RAMDLD_0000.ldr', 0xA0200000, 0xA0200000, ezx_ap=True)

		# EZX AP Set Flag (command-line arguments)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/gen-blob/head.bin', 0xA1000000)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/gen-blob/blob-a1200', 0xA0DE0000, 0xA0DE0000, ezx_ap=True)
		pass
	else:
		# EZX BP
#		mfp_upload_binary_to_addr(er, ew, 'loaders/A760_BP_RAMDLD_0372_Patched_Dump_NOR.ldr', 0x11060000, 0x11060010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/A768i_BP_RAMDLD_0731_Patched_Dump_NOR.ldr', 0x12000000, 0x12000010)
#		mfp_upload_binary_to_addr(er, ew, 'loaders/A780g_BP_RAMDLD_08A0.ldr', 0x03FD0000, 0x03FD0010)
		pass

def worksheet_p2k(p2k_usb_device):
#	p2k_do_memacs_dump(p2k_usb_device, 'E398_MEMACS_DUMP.bin', 0x10000000, 0x12000000, 0x800)
#	p2k_do_memacs_dump(p2k_usb_device, 'CC75_MEMACS_DUMP.bin', 0x10000000, 0x10010000, 0x800)
	p2k_do_memacs_dump(p2k_usb_device, 'E398_MEMACS_DUMP.bin', 0x00000000, 0x00010000, 0x800)
#	p2k_do_info_dump(p2k_usb_device, 'E398_P2KINFO_DUMP.txt')
#	p2k_do_dump_files(p2k_usb_device, 'a')
	return True

## Motorola Test Command Interface (P2K) Protocol ######################################################################

def p2k_save_file(p2k_usb_device, index, file_info):
	logging.info(f'Dumping "{file_info[0]}" file of {file_info[1]} bytes size...')

	# Open file with previous flags.
	# 04 FC 00 4A 00 17 00 00 00 00 00 00 00 00 00 04    .ь.J..........$.
	# 2F 61 2F 56 69 62 5F 64 61 73 68 2E 77 61 76      /a/Vib_dash.wav
	packet_name_size = 0x10 + len(file_info[0]) - 8
	ctrl_packet = int.to_bytes(index, 2, 'big') + b'\x00\x4A' + int.to_bytes(packet_name_size, 2, 'big') + \
		b'\x00\x00\x00\x00\x00\x00\x00\x00' + int.to_bytes(file_info[3], 2, 'big') + file_info[0].encode('CP1251')
	p2k_cmd_execute(p2k_usb_device, ctrl_packet)

	# Seek file to start.
	# 04 FE 00 4A 00 09 00 00 00 00 00 03 00 00 00 00 00
	ctrl_packet = int.to_bytes(index + 2, 2, 'big') + b'\x00\x4A\x00\x09\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00'
	p2k_cmd_execute(p2k_usb_device, ctrl_packet)

	# Write file to disk.
	# 05 00 00 4A 00 08 00 00 00 00 00 01 00 00 04 00
	# 05 00 00 4A 00 08 00 00 00 00 00 01 00 00 01 78
	step = 2
	directory = '.' + os.path.dirname(file_info[0])
	os.makedirs(directory, exist_ok=True)
	with open('.' + file_info[0], 'wb') as file:
		u = int(file_info[1] / 0x400)
		d = int(file_info[1] % 0x400)
		for i in range(0, u):
			ctrl_packet = int.to_bytes(index + step, 2, 'big') + b'\x00\x4A\x00\x08\x00\x00\x00\x00\x00\x01' + \
				int.to_bytes(0x400, 4, 'big')
			result_data = p2k_cmd_execute(p2k_usb_device, ctrl_packet, None, True, True)
			file.write(result_data)
			step += 2
		if d > 0:
			ctrl_packet = int.to_bytes(index + step, 2, 'big') + b'\x00\x4A\x00\x08\x00\x00\x00\x00\x00\x01' + \
				int.to_bytes(d, 4, 'big')
			result_data = p2k_cmd_execute(p2k_usb_device, ctrl_packet, None, True, True)
			file.write(result_data)

	# Close file.
	# 05 02 00 4A 00 04 00 00 00 00 00 04
	ctrl_packet = int.to_bytes(index + (step * 2) + 2, 2, 'big') + b'\x00\x4A\x00\x04\x00\x00\x00\x00\x00\x04'
	p2k_cmd_execute(p2k_usb_device, ctrl_packet)

def p2k_get_file_list(p2k_usb_device, index, disk):
	ctrl_packet = int.to_bytes(index, 2, 'big') + b'\x00\x4A\x00\x05\x00\x00\x00\x00\x00\x08\x03'
	path_size = 0x10C # 268 bytes.
	# FIXME: Something nasty here.
	answer_size = 0x330
	files = []
	while answer_size > 0x10:
		result = p2k_cmd_execute(p2k_usb_device, ctrl_packet)
		answer_size = len(result)
		if answer_size > 0x10:
			file_path_count = result[0]
			for i in range(0, file_path_count):
				start = 3
				slice = result[start + i * path_size:(i * path_size) + path_size + start]
				strings = bytes(slice).split(b'\x00')
				files.append((
					strings[0].decode('CP1251', errors='ignore'), # Path
					int.from_bytes(slice[-4:], 'big'),            # Size
					int.from_bytes(slice[-6:-4], 'big'),          # User
					int.from_bytes(slice[-8:-6], 'big'),          # Flags
				))
	return files

def p2k_disk_init(p2k_usb_device, index, disk):
	ctrl_packet = int.to_bytes(index, 2, 'big') + b'\x00\x4A\x02\x00\x00\x00\x00\x00\x00\x0B\xFF\xFE\x00\x2F\x00' \
		+ disk.encode() + (b'\x00' * 0x1E6)  # 486
	p2k_cmd_execute(p2k_usb_device, ctrl_packet)

	ctrl_packet = int.to_bytes(index + 2, 2, 'big') + b'\x00\x4A\x00\x10\x00\x00\x00\x00\x00\x07\x00\x2F\x00' \
		+ disk.encode() + b'\x00\x2F\xFF\xFE\x00\x2A\x00\x00'
	p2k_cmd_execute(p2k_usb_device, ctrl_packet)

def p2k_get_volume_list(p2k_usb_device, index):
	ctrl_packet = int.to_bytes(index, 2, 'big') + b'\x00\x4A\x00\x04\x00\x00\x00\x00\x00\x0A'
	result = p2k_cmd_execute(p2k_usb_device, ctrl_packet)
	volumes = []
	for byte in result:
		if byte >= 97 and byte <= 122:   # Only lowercase ASCII check.
			volumes.append(chr(byte))
	logging.info(f'Phone disks are {volumes}!')
	return volumes

def p2k_get_info(p2k_usb_device, index, feature, fixup=False):
	# 00 0A 00 39 00 02 00 00 FF FF
	# 00 0C 00 39 00 02 00 00 00 01
	ctrl_packet = int.to_bytes(index, 2, 'big') +  b'\x00\x39\x00\x02\x00\x00' + int.to_bytes(feature, 2, 'big')
	return p2k_cmd_execute(p2k_usb_device, ctrl_packet, None, True, fixup)

def p2k_read_seem(p2k_usb_device, index, seem, rec, file_path=None):
	# 00 06 00 20 00 08 00 00 01 17 00 01 00 00 00 00
	# 00 08 00 20 00 08 00 00 01 7F 00 01 00 00 00 00
	ctrl_packet = int.to_bytes(index, 2, 'big') +  b'\x00\x20\x00\x08\x00\x00' + \
		int.to_bytes(seem, 2, 'big') + int.to_bytes(rec, 2, 'big') +  b'\x00\x00\x00\x00'
	result_data = p2k_cmd_execute(p2k_usb_device, ctrl_packet)
	if file_path:
		with open(file_path, 'wb') as file:
			file.write(result_data)
	return bytes(result_data)

def p2k_memacs(p2k_usb_device, index, addr_s, step, file_path=None):
	# MEMACS P2K Command.
	# 00 02 00 16 00 08 00 00 10 00 00 00 08 00 00 00
	# 00 03 00 16 00 08 00 00 10 00 08 00 08 00 00 00
	ctrl_packet = int.to_bytes(index + 2, 2, 'big') +  b'\x00\x16\x00\x08\x00\x00' + \
		int.to_bytes(addr_s, 4, 'big') + int.to_bytes(step, 2, 'big') +  b'\x00\x00'
	return p2k_cmd_execute(p2k_usb_device, ctrl_packet)

def p2k_cmd_execute(p2k_usb_device, ctrl_packet, size=None, trim_usb_packet=True, fixup=False):
	usb_additional_payload_size = 0x06

	# Send control packet.
	p2k_usb_device.ctrl_transfer(0x41, 0x02, 0x00, 0x08, ctrl_packet, timeout_write)
	logging.debug(
		f'>>> Send USB control packet '
		f'(bmRequestType=0x41, bmRequest=0x02, wValue=0x00, wIndex=0x08) '
		f'to device...\n{hexdump(ctrl_packet)}'
	)

	# Stabilization.
	retry = 0
	while not retry:
		result = p2k_usb_device.ctrl_transfer(0xC1, 0x00, 0x00, 0x08, 0x08, timeout_read)
		logging.debug(
			f'>>> Send USB control packet '
			f'(bmRequestType=0xC1, bmRequest=0x00, wValue=0x00, wIndex=0x08, size=0x08) to device...'
			f'\nresult =\n{hexdump(result)}'
		)
		retry = int.from_bytes(result, 'little')

	# Read count of packets and packet size.
	usb_packet_count = int.from_bytes(result[:2], 'big')
	usb_packet_size  = int.from_bytes(result[2:], 'big')
	logging.debug(
		f'usb_packet_count={usb_packet_count}|0x{usb_packet_count:02X}, '
		f'usb_packet_size={usb_packet_size}|0x{usb_packet_size:02X}'
	)
	if not size:
		size = usb_packet_size + usb_additional_payload_size

	# Read data.
	result = p2k_usb_device.ctrl_transfer(0xC1, 0x01, 0x01, 0x08, size, timeout_read)
	logging.debug(
		f'>>> Send USB control packet '
		f'(bmRequestType=0xC1, bmRequest=0x01, wValue=0x01, wIndex=0x08, size=0x{size:08X}) to device...'
		f'\nresult =\n{hexdump(result)}'
	)
	if trim_usb_packet:
		usb_packet_answer_header_size = size - int.from_bytes(result[10:12], 'big')
		if not fixup:
			usb_packet_answer_header_size += 1
		result_data = result[usb_packet_answer_header_size:]     # Drop first bytes from pipe answer.
	else:
		result_data = result
	if (not result_data) or (len(result_data) == 0):
		result_data = 'NO DATA'.encode()

	return result_data

def p2k_do_dump_files(p2k_usb_device, disk, skip_files=[]):
	logging.info(f'Dumping files from disk /{disk}/!')

	volumes = p2k_get_volume_list(p2k_usb_device, 0x0002)
	if disk not in volumes:
		logging.error(f'There is no disk /{disk}/ in volumes {volumes} on the phone!')
		return False

	p2k_disk_init(p2k_usb_device, 0x0004, disk)

	logging.info(f'Getting file list from disk /{disk}/...')
	file_list = p2k_get_file_list(p2k_usb_device, 0x0008, disk)
	file_list.sort()
	str_list_files = ''
	for file, size, user, flags in file_list:
		str_list_files += f'{file} user=0x{user:02X} flags=0x{flags:02X} size={size} bytes.\n'
	logging.info(str_list_files)

	index = 0x1000
	for file_info in file_list:
		save_flag = True
		for skip in skip_files:
			if file_info[0].endswith(skip):
				save_flag = False
		if save_flag:
			p2k_save_file(p2k_usb_device, index, file_info)
		else:
			logging.info(f'Skipped dumping of "{file_info[0]}" file!')
		index += 2

def p2k_do_info_dump(p2k_usb_device, file_path):
	logging.info(f'Dumping P2K Information to the "{file_path}" file!')
	with open(file_path, 'w') as file:
		file.write('\nSEEM 0074_0001:\n' + hexdump(p2k_read_seem(p2k_usb_device, 0x0003, 0x0074, 0x0001)))
		file.write('\nSEEM 0076_0001:\n' + hexdump(p2k_read_seem(p2k_usb_device, 0x0004, 0x0076, 0x0001)))
		file.write('\nSEEM 0117_0001:\n' + hexdump(p2k_read_seem(p2k_usb_device, 0x0006, 0x0117, 0x0001)))
		file.write('\nSEEM 0117_0001:\n' + hexdump(p2k_read_seem(p2k_usb_device, 0x0008, 0x017F, 0x0001)))
		file.write('\nFTR FFFF:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x000A, 0xFFFF, True)))
		file.write('\nFTR 0001:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x000C, 0x0001, True)))
		file.write('\nFTR 0002:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x000E, 0x0002, True)))
		file.write('\nFTR 0003:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0010, 0x0003, True)))
		file.write('\nFTR 1107:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0012, 0x1107, True)))
		file.write('\nFTR 0006:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0014, 0x0006, True)))
		file.write('\nFTR 0007:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0016, 0x0007, True)))
		file.write('\nFTR 0008:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0018, 0x0008, True)))
		file.write('\nFTR 0009:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x001A, 0x0009, True)))
		file.write('\nFTR 1000:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x001C, 0x1000, True)))
		file.write('\nFTR 1001:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x001E, 0x1001, True)))
		file.write('\nFTR 1002:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0020, 0x1002, True)))
		file.write('\nFTR 1003:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0022, 0x1003, True)))
		file.write('\nFTR 1100:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0024, 0x1100, True)))
		file.write('\nFTR 1101:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0026, 0x1101, True)))
		file.write('\nFTR 1102:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0028, 0x1102, True)))
		file.write('\nFTR 1103:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x002A, 0x1103, True)))
		file.write('\nFTR 1104:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x002C, 0x1104, True)))
		file.write('\nFTR 1105:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x002E, 0x1105, True)))
		file.write('\nFTR 1106:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0030, 0x1106, True)))
		file.write('\nFTR 0004:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0032, 0x0004, True)))
		file.write('\nFTR 1108:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0034, 0x1108, True)))
		file.write('\nFTR 1109:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0036, 0x1109, True)))
		file.write('\nFTR 110A:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0038, 0x110A, True)))
		file.write('\nFTR 110B:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x003A, 0x110B, True)))
		file.write('\nFTR 110C:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x003C, 0x110C, True)))
		file.write('\nFTR 110D:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x003E, 0x110D, True)))
		file.write('\nFTR 1200:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0040, 0x1200, True)))
		file.write('\nFTR 1300:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0042, 0x1300, True)))
		file.write('\nFTR 1301:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0044, 0x1301, True)))
		file.write('\nFTR 1302:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0046, 0x1302, True)))
		file.write('\nFTR 1303:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0048, 0x1303, True)))
		file.write('\nFTR 1304:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x004A, 0x1304, True)))
		file.write('\nFTR 1305:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x004C, 0x1305, True)))
		file.write('\nFTR 1306:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x004E, 0x1306, True)))
		file.write('\nFTR 1307:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0050, 0x1307, True)))
		file.write('\nFTR 1308:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0052, 0x1308, True)))
		file.write('\nFTR 1309:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0054, 0x1309, True)))
		file.write('\nFTR 130A:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0056, 0x130A, True)))
		file.write('\nFTR 1400:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x0058, 0x1400, True)))
		file.write('\nFTR 1401:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x005A, 0x1401, True)))
		file.write('\nFTR 2000:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x005C, 0x2000, True)))
		file.write('\nFTR FFFE:\n' + hexdump(p2k_get_info(p2k_usb_device, 0x005E, 0xFFFE, True)))
	return True

def p2k_do_memacs_dump(p2k_usb_device, file_path, start = 0x10000000, end = 0x12000000, step = 0x0800):
	logging.info(f'Dumping 0x{start:08X}-0x{end:08X} memory region to the "{file_path}" file!')
	addr_s = start
	addr_e = start + step
	with open(file_path, 'wb') as file:
		index = 0
		time_start = time.time()
		while addr_e <= end:
			if addr_e > end:
				addr_e = end
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % 0x50 == 0):
				time_start = progress(step, time_start, 0x50, index * step, file_path, addr_s, addr_e, end)

			result_data = p2k_memacs(p2k_usb_device, index, addr_s, step)
			if len(result_data) != step:
				logging.error(f'Result data is smaller than step: {len(result_data)} != {step}, MEMACS disabled?')
				return False
			file.write(result_data)

			addr_s = addr_s + step
			addr_e = addr_s + step
			index += 1
	return True

def do_p2k_work(modem_device, modem_speed, usb_devices):
	if switch_atmode_to_p2kmode(modem_device, modem_speed, usb_devices):
		p2k_usb_device = find_usb_device(usb_devices, 'p2k')
		if p2k_usb_device:
#			p2k_usb_device.set_configuration()
			config = p2k_usb_device.get_active_configuration()
			logging.debug(config)
			worksheet_p2k(p2k_usb_device)
		else:
			logging.error('Cannot find P2K device!')
	sys.exit(0)

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
		time_start = time.time()
		while addr_e <= end + 0x400:
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % (step * 0x100) == 0):
				time_start = progress(step, time_start, 0x100, index, file_path, addr_s, addr_e, end)

			result_data1 = mfp_cmd(er, ew, 'RQRC', f'{addr_s:08X},{addr_e:08X}'.encode())
			result_data1 = result_data1[6:]   # Drop start marker and command.
			result_data1 = result_data1[:-1]  # Drop end marker.
			result_data1_int = int.from_bytes(bytes.fromhex(result_data1.decode()), 'big')

			result_data2 = mfp_cmd(er, ew, 'RQRC', f'{addr_s + 0x01:08X},{addr_e:08X}'.encode())
			result_data2 = result_data2[6:]   # Drop start marker and command.
			result_data2 = result_data2[:-1]  # Drop end marker.
			result_data2_int = int.from_bytes(bytes.fromhex(result_data2.decode()), 'big')

			result_byte = (result_data1_int - result_data2_int) % 256
			result = int.to_bytes(result_byte,1, 'big')

			file.write(result)

			addr_s = addr_s + step
			addr_e = addr_s + step + 0x400
			index += step

def mfp_dump_r(er, ew, file_path, start, end, step = 0x100):
	addr_s = start
	addr_e = start + step
	with open(file_path, 'wb') as file:
		index = 0
		time_start = time.time()
		while addr_e <= end:
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % (step * 0x100) == 0):
				time_start = progress(step, time_start, 0x100, index, file_path, addr_s, addr_e, end)
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
		time_start = time.time()
		while addr_e <= end:
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % (step * 0x100) == 0):
				time_start = progress(step, time_start, 0x100, index, file_path, addr_s, addr_e, end)
			result_data = mfp_cmd(er, ew, 'READ', f'{addr_s:08X},{step:04X}'.encode())
			result_data = result_data[6:]   # Drop start marker and command.
			result_data = result_data[2:]   # Drop size step.
			result_data = result_data[:-1]  # Drop checksum.
			result_data = result_data[:-1]  # Drop end marker.
			file.write(result_data)

			addr_s = addr_s + step
			addr_e = addr_s + step
			index += step

def mfp_dump_rbin(er, ew, file_path, start, end, step = 0x1000):
	addr_s = start
	addr_e = start + step
	with open(file_path, 'wb') as file:
		index = 0
		time_start = time.time()
		while addr_e <= end:
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % (step * 0x100) == 0):
				time_start = progress(step, time_start, 0x100, index, file_path, addr_s, addr_e, end)
			command_arg = f'{addr_s:08X}{step:04X}'.encode()
			command_arg_chk = f'{addr_s:08X}{step:04X}{calculate_checksum(command_arg):02X}'.encode()
			result_data = mfp_cmd(er, ew, 'RBIN', command_arg_chk)
			result_data = result_data[6:]   # Drop start marker and command.
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
		time_start = time.time()
		while addr_e <= end:
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % (step * 0x100) == 0):
				time_start = progress(step, time_start, 0x100, index, file_path, addr_s, addr_e, end)

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
		time_start = time.time()
		for page in range(start, end):
			for wide in range(wide_nand):
				logging.debug(f'Dumping NAND {page:08} page ({wide:02}), 512+16 bytes to "{file_path}" +spare_area...')
				if index > 0 and (index % 100 == 0):
					time_start = progress(
						528, time_start, 100, index, file_path,
						addr_s, addr_h, end, (end - start) * wide_nand, True
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
		time_start = time.time()
		while addr_e <= end + step:
			if addr_e > end:
				addr_e = end
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % (step * 0x100) == 0):
				time_start = progress(step, time_start, 0x100, index, file_path, addr_s, addr_e, end)
			result_data = mfp_cmd(er, ew, 'RQRC', f'{addr_s:08X},{addr_e:08X}'.encode())
			result_data = result_data[6:]   # Drop start marker and command.
			result_data = result_data[:-1]  # Drop end marker.
			file.write(bytearray.fromhex(result_data.decode()))

			addr_s = addr_s + step
			addr_e = addr_s + step
			index += step

def mfp_dump_byte(er, ew, file_path, start, end):
	addr_s = start
	addr_e = start
	with open(file_path, 'wb') as file:
		index = 0
		time_start = time.time()
		while addr_e < end:
			logging.debug(f'Dumping 0x{addr_s:08X}-0x{addr_e:08X} bytes to "{file_path}"...')
			if index > 0 and (index % (0x01 * 0x100) == 0):
				time_start = progress(0x01, time_start, 0x100, index, file_path, addr_s, addr_e, end)
			result_data = mfp_cmd(er, ew, 'RQRC', f'{addr_s:08X},{addr_e:08X}'.encode())
			result_data = result_data[6:]   # Drop start marker and command.
			result_data = result_data[:-1]  # Drop end marker.
			result_data = result_data[2:]   # Drop leading zero byte.
			file.write(bytearray.fromhex(result_data.decode()))

			addr_s += 1
			addr_e += 1
			index += 1

def mfp_upload_binary_to_addr(er, ew, file_path, start, jump = None, rsrc = None, ezx_ap = None, read_response = True):
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
		mfp_cmd(er, ew, 'JUMP', mfp_get_addr_with_chksum(jump), read_response)
		logging.info(f'Waiting {delay_jump} seconds for RAMDLD init on device...')
		time.sleep(delay_jump)
	if ezx_ap:
		logging.info(f'EZX AP RAMDLD was loaded. Please remove the "-l" flag or add the "-2" flag and rerun script.')
		sys.exit(0)

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

def mfp_cmd(er, ew, cmd, data = None, read_response = True):
	packet = bytearray(b'\x02')  # Start marker.
	packet.extend(cmd.encode())
	if data:
		packet.extend(b'\x1E')  # Data separator.
		packet.extend(data)
	packet.extend(b'\x03')  # End marker.
	logging.debug(f'>>> Send to device...\n{hexdump(packet)}')

	result = mfp_send_recv(er, ew, packet, read_response)
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
				sys.exit(1)
			time.sleep(delay_ack)
	else:
		response = 'NO DATA'.encode()
	return response

## USB Routines ########################################################################################################

def usb_check_restart_phone(er, ew, restart_flag):
	if restart_flag:
		mfp_cmd(er, ew, 'RESTART')
		time.sleep(2.0)
		er, ew = usb_init(usb_devices, 'flash')
		if not er or not ew:
			logging.error('Cannot find USB device!')
			sys.exit(1)
	return er, ew

def get_usb_device_information(usb_device):
	return f'{usb_device["desc"]}: usb_vid={usb_device["usb_vid"]:04X}, usb_pid={usb_device["usb_pid"]:04X}'

def get_endpoints(device, interface_index):
#	device.set_configuration()

	config = device.get_active_configuration()
	logging.debug(config)

	interface = config[(interface_index, 0)]
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
				logging.info(f'Not found: "{get_usb_device_information(usb_device)}"!')
	return None

def usb_init(usb_devices, mode):
	connected_device = find_usb_device(usb_devices, mode)
	if connected_device:
		return get_endpoints(connected_device, 1 if '-2' in sys.argv else 0)
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

def switch_atmode_to_p2kmode(modem_device, modem_speed, usb_devices):
	if '-at_skip' in sys.argv:
		return True
	if '-at_usb' in sys.argv:
		at_usb_device = find_usb_device(usb_devices, 'at')
		if at_usb_device:
			er, ew = get_endpoints(at_usb_device, 1)
			send_at_command = (at_command + '\r\n').encode()
			mfp_binary_cmd(er, ew, send_at_command)
			send_at_command = (p2k_mode_command + '\r\n').encode()
			mfp_binary_cmd(er, ew, send_at_command, False)
			logging.info(f'Wait {delay_switch} sec for AT => P2K switching...')
			time.sleep(delay_switch)
			return True
		else:
			logging.error('Cannot find AT device!')
			return False
		return True
	if os.path.exists(modem_device):
		logging.info(f'USB modem device "{modem_device}" found, switch it to P2K mode!')
		serial_handle = serial.Serial(modem_device, modem_speed, timeout = 1)
		if serial_handle:
			write_read_at_command(serial_handle, at_command, True)
			time.sleep(1.0)
			write_read_at_command(serial_handle, p2k_mode_command, False)
			serial_handle.close()
			logging.info(f'Wait {delay_switch} sec for AT => P2K switching...')
			time.sleep(delay_switch)
			return True
		else:
			logging.error(f'Cannot open "{modem_device}" device on "{modem_speed}" speed!')
	else:
		logging.error(f'Cannot find "{modem_device}" device!')
	return False

def switch_p2kmode_to_flashmode(p2k_usb_device):
	logging.info('P2K device found, switching it to the Flash mode!')
	try:
		with open(p2k_command_list, 'r', newline='') as file:
			for line in file:
				line = line.strip()
				if line and not line.startswith('#'):
#					ctrl_packet = b'\x00\x01\x00\x0D\x00\x00\x00\x00'
					ctrl_packet = bytes.fromhex(line)
					p2k_cmd_execute(p2k_usb_device, ctrl_packet)
	except (FileNotFoundError, IOError) as error:
		logging.error(f'File Error: {error}')
		sys.exit(1)
	except usb.USBError as error:
		logging.error(f'USB Error: {error}')
		sys.exit(1)
	logging.info(f'Wait {delay_switch} sec for P2K => Flash switching...')
	time.sleep(delay_switch)

def reconnect_device_in_flash_mode(modem_device, modem_speed, usb_devices):
	if switch_atmode_to_p2kmode(modem_device, modem_speed, usb_devices):
		p2k_usb_device = find_usb_device(usb_devices, 'p2k')
		if p2k_usb_device:
#			p2k_usb_device.set_configuration()
			config = p2k_usb_device.get_active_configuration()
			logging.debug(config)
			switch_p2kmode_to_flashmode(p2k_usb_device)
			return True
		else:
			logging.error('Cannot find P2K device!')
			return False

## Utils ###############################################################################################################

def insert_to_filename(insert, filename):
	name_part, extension = filename.rsplit('.', 1)
	return f'{name_part}{insert}.{extension}'

def progress(step, time_start, size, index, file_path, addr_s, addr_e, end, pages = 0, nand = False):
	time_end = time.time()
	speed = (step * size) / (time_end - time_start) / 1024
	if nand:
		logging.info(
			f'Dumped: {index:08}/{pages:08} pages | {index*512/1024:>8} KiB | 0x{index*512:08X}={index*512:010d} bytes | '
			f'0x{addr_s:08X}-0x{addr_e:08X}-0x{end:08X} | '
			f'{speed:.2f} KiB/s\n512, 16 bytes => "{file_path}", "{insert_to_filename("_spare_area",file_path)}"'
		)
	else:
		logging.info(
			f'Dumped: {index/1024:>8} KiB | 0x{index:08X}={index:010d} bytes | '
			f'0x{addr_s:08X}-0x{addr_e:08X}-0x{end:08X} | {speed:.2f} KiB/s => "{file_path}"'
		)
	return time.time()  # Reset time.

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
		logging.info(splash)
		sys.exit(1)
	if '-s' in sys.argv:
		reconnect_device_in_flash_mode(modem_device, modem_speed, usb_devices)
	if '-p' in sys.argv:
		do_p2k_work(modem_device, modem_speed, usb_devices)
	er, ew = usb_init(usb_devices, 'flash')
	if er and ew:
		worksheet(er, ew)

if __name__ == '__main__':
	main()
