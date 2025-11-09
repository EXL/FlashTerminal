# Worksheet Examples

## Flashing Worksheet Parameters

### Flashing 8 MB NOR Memory Dump to Motorola C350L

```python
timeout_read = 600000   # 10 min.
timeout_write = 600000  # 10 min.
#	mfp_cmd(er, ew, 'RQHW')
#	mfp_cmd(er, ew, 'RQVN')
mfp_uls_upload(er, ew, 'loaders/C350L_RAMDLD_0000_Patched_Dump_NOR.ldr', 0x12000000, 0x1000, False)
mfp_cmd(er, ew, 'ERASE')
mfp_upload_binary_to_addr(er, ew, 'С350L_ROM_Dump_8M.bin', 0x10000000, None)
```

### Flashing 16 MB NOR Memory Dump to Motorola C450, E380, C550

```python
timeout_read = 600000   # 10 min.
timeout_write = 600000  # 10 min.

# Flash Neptune LCA/LT.
mfp_upload_binary_to_addr(er, ew, 'loaders/E380_RAMDLD_0910_Hacked_Dump.ldr', 0x01FD0000, 0x01FD0010)

# Blank Neptune LCA/LT.
mfp_uls_upload(er, ew, 'loaders/E380_RAMDLD_Hacked_RQHW.ldr', 0x01FD0000, 0x1000, False)

mfp_cmd(er, ew, 'ERASE')

# Flash Neptune LCA/LT.
mfp_upload_binary_to_addr(er, ew, 'C550_ROM_Dump_16M.bin', 0x00000000, None)

# Blank Neptune LCA/LT.
mfp_upload_binary_to_addr(er, ew, 'C550_ROM_Dump_16M.bin', 0x10000000, None)
```

### Flashing and dumping Siemens CC75 on Spansion flash NOR memory chip

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/Hitagi_LTE1_AMD_16.ldr', 0x03FD0000, 0x03FD0000, True)

# Using WORDs writtings.
mfp_cmd(er, ew, 'ERASE')
# Using CHUNKs writtings.
mfp_cmd(er, ew, 'ERASE')

# BackUp Full 32MB Flash.
mfp_dump_read(er, ew, 'CC75_ROM_Dump.bin', 0x10000000, 0x12000000, 0x200)

# Write chunk only.
mfp_upload_binary_to_addr(er, ew, 'CC75_CG0.bin', 0x10080000, None)

# Write Full 32MB Flash.
mfp_upload_binary_to_addr(er, ew, 'CC75_ROM_Dump.bin', 0x10000000, None)
```

### Flashing 4 MB NOR Memory Dump of BP to Motorola MING A1600 (Engineering Prototype)

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/Hitagi_LTE2_Compact_Intel_16.ldr', 0x03FC8000, 0x03FC8010, True)

# Using WORDs writtings.
mfp_cmd(er, ew, 'ERASE')
# Using CHUNKs writtings.
mfp_cmd(er, ew, 'ERASE')

mfp_upload_binary_to_addr(er, ew, 'A1600_BP_ROM_Dump.bin', 0x10000000, None)
```

## Dumping Worksheet Parameters

### Dumping 32 MB NOR Memory from Motorola TRIPLETS-like phones

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/E398_RAMLD_07B0_Hacked_Dump.ldr', 0x03FD0000, 0x03FD0010)
mfp_dump_dump(er, ew, 'E398_ROM_Dump.bin', 0x10000000, 0x12000000, 0x100)
```

### Dumping 64 MB NOR Memory from Motorola RAZR V3x

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/V3x_RAMDLD_0682_RSA_Read.ldr', 0x08000000, 0x08000010, True)
mfp_dump_read(er, ew, 'V3x_ROM_Dump.bin', 0x10000000, 0x14000000, 0x100)
```

### Dumping BP 16 MB NOR Memory from Motorola A1000 and Motorola FOMA M1000

```python
# ./FlashTerminal.py -l
mfp_upload_binary_to_addr(er, ew, 'loaders/A1000_BP_RAMDLD_0651_RSA_Read.ldr', 0x08000000, 0x08000010, True)
mfp_dump_read(er, ew, 'A1000_ROM_Dump.bin', 0x10000000, 0x11000000, 0x100)

# ./FlashTerminal.py
mfp_upload_binary_to_addr(er, ew, 'loaders/A1000_BP_RAMDLD_0651_RSA_Read.ldr', 0x08000000, 0x08000010, True)
mfp_dump_rqrc(er, ew, 'A1000_PDS_ROM_Dump.bin', 0x10010000, 0x10020000)
```

### Dumping 16 MB NOR Memory from Motorola A835, A845, C975, E1000 and Siemens U15 (+ IROM)

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/A835_RAMDLD_0612_Hacked_RSA_Read.ldr', 0x08000000, 0x08018818)
#	mfp_cmd(er, ew, 'RQVN')
mfp_cmd(er, ew, 'RQHW')
mfp_binary_cmd(er, ew, b'\x00\x00\x05\x70', False)
mfp_upload_raw_binary(er, ew, 'loaders/A835_Additional_Payload_1.bin', None, False)
mfp_upload_raw_binary(er, ew, 'loaders/A835_Additional_Payload_2.bin')
mfp_binary_cmd(er, ew, b'\x53\x00\x00\x00\x00\x00\x00\xA0\x00')
mfp_binary_cmd(er, ew, b'\x41')
mfp_dump_r(er, ew, 'A835_ROM_Dump.bin', 0x10000000, 0x11000000, 0x100)
mfp_dump_r(er, ew, 'A835_IROM_Dump.bin', 0x00000000, 0x00006100, 0x100)

mfp_dump_r(er, ew, 'C975_ROM_Dump.bin', 0x10000000, 0x12000000, 0x100)
mfp_dump_r(er, ew, 'E1000_ROM_Dump.bin', 0x10000000, 0x14000000, 0x100)
```

### Dumping 16 MB NOR Memory from Motorola A830 and Siemens U10 (+ IROM)

```python
mfp_upload_binary_to_addr(er, ew, 'A830_RAMDLD_0520_Patched_Dump_NOR.ldr', 0x07800000, 0x07800010)
mfp_dump_sram(er, ew, 'U10_ROM_Dump.bin', 0x10000000, 0x11000000, 0x30)
mfp_dump_sram(er, ew, 'A830_IROM_Dump.bin', 0x00000000, 0x00010000, 0x30)
```

### Dumping 8 MB NOR Memory from Motorola C350L (+ IROM)

```python
#	mfp_cmd(er, ew, 'RQHW')
#	mfp_cmd(er, ew, 'RQVN')
mfp_uls_upload(er, ew, 'loaders/C350L_RAMDLD_0000_Patched_Dump_NOR.ldr', 0x12000000, 0x1000, False)
mfp_dump_sram(er, ew, 'C350L_ROM_Dump.bin', 0x10000000, 0x10800000, 0x30)
mfp_dump_sram(er, ew, 'C350L_IROM_Dump.bin', 0x00000000, 0x00040000, 0x30)
```

### Dumping 8 MB and 16 MB NOR Memory from Motorola C330, C350, C450, C550, E380 (+ IROM)

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/E380_RAMDLD_0910_Hacked_Dump.ldr', 0x01FD0000, 0x01FD0010)
mfp_dump_dump(er, ew, 'C350_ROM_Dump.bin', 0x00000000, 0x00800000, 0x100)
mfp_dump_dump(er, ew, 'C350_IROM_Dump.bin', 0x10000000, 0x10400000, 0x100)
mfp_dump_dump(er, ew, 'C550_ROM_Dump.bin', 0x00000000, 0x01000000, 0x100)
```

### Dumping 4 MB and 8 MB NOR Memory from Motorola V60/V60i, Motorola V66/V66i, Motorola V70, Motorola T280 (+ IROM)

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/V60_RAMDLD_0355_Patched_Dump_NOR.ldr', 0x11010000, 0x11010010)
mfp_upload_binary_to_addr(er, ew, 'loaders/V60i_RAMDLD_1007_Patched_Dump_NOR.ldr', 0x11010000, 0x11010010)
mfp_dump_sram(er, ew, 'V60_IROM_Dump.bin', 0x00000000, 0x00400000, 0x30)
mfp_dump_sram(er, ew, 'V60_ROM_Dump.bin', 0x10000000, 0x10400000, 0x30)
mfp_dump_sram(er, ew, 'V70_ROM_Dump.bin', 0x10000000, 0x10800000, 0x30)
```

### Dumping 8 MB NOR Memory from Motorola T720, T720i, T722i (+ IROM)

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/T720_RAMDLD_0370_Patched_Dump_NOR.ldr', 0x11010000, 0x11010010)
mfp_dump_sram(er, ew, 'T720_IROM_Dump.bin', 0x00000000, 0x00400000, 0x30)
mfp_dump_sram(er, ew, 'T720_ROM_Dump.bin', 0x10000000, 0x10800000, 0x30)
```

### Dumping 4 MB NOR Memory from Motorola V120c (+ IROM)

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/V120c_RAMDLD_0312_Patched_Dump_NOR.ldr', 0x41008000, 0x41008010)
mfp_dump_sram(er, ew, 'V120c_IROM_Dump.bin', 0x00000000, 0x00400000, 0x30)
mfp_dump_sram(er, ew, 'V120c_ROM_Dump.bin', 0x40000000, 0x40400000, 0x30)
```

### Dumping 64 MB NAND Memory from Motorola RAZR V3m, Motorola W755, Motorola E815, Motorola W385

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/V3m_RAMDLD_010C_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000, True)
mfp_dump_nand(er, ew, 'V3m_NAND_Dump.bin', 0, int(0x04000000 / 512), 0x10, 1, 0x64000000)
```

### Dumping 64 MB NAND Memory from Motorola V325i, Motorola V325xi

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/V325i_RAMDLD_010A_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000, True)
mfp_dump_nand(er, ew, 'V325i_NAND_Dump.bin', 0, int(0x04000000 / 512), 0x10, 1, 0x64000000)
```

### Dumping 64 MB NAND Memory from Motorola K1m, Motorola K1mm

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/K1m_RAMDLD_0013_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000, True)
mfp_upload_binary_to_addr(er, ew, 'loaders/K1mm_RAMDLD_000D_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000, True)
mfp_dump_nand(er, ew, 'K1m_NAND_Dump.bin', 0, int(0x04000000 / 512), 0x10, 1, 0x64000000)
```

### Dumping 64 MB SRAM Memory from Motorola RAZR2 V9m and Motorola ROKR Z6m

```python
mfp_upload_binary_to_addr(er, ew, 'V9m_RAMDLD_01B5_Patched_Dump_SRAM.ldr', 0x00100000, 0x00100000)
mfp_dump_sram(er, ew, 'Z6m_SRAM_Dump.bin', 0x00000000, 0x04000000, 0x30)
mfp_dump_sram(er, ew, 'V9m_SRAM_Dump.bin', 0x00000000, 0x04000000, 0x30)
```

### Dumping 128 MB NAND Memory from Motorola ROKR Z6c

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/Z6c_RAMDLD_000D_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000, True)
mfp_dump_nand(er, ew, 'Z6c_NAND_Dump.bin', 0, int(0x08000000 / 512), 0x30)
```

### Dumping 64 MB and 128 MB NAND Memory from Motorola RAZR2 V9m and Motorola ROKR Z6m

```python
mfp_upload_binary_to_addr(er, ew, 'V9m_RAMDLD_01B5_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000)
mfp_dump_nand(er, ew, 'Z6m_NAND_Dump.bin', 0, int(0x04000000 / 512), 0x30)
mfp_dump_nand(er, ew, 'V9m_NAND_Dump.bin', 0, int(0x08000000 / 512), 0x30)
```

### Dumping 128 MB and 256 MB NAND Memory from Motorola VE40 and Motorola Hint QA30 (+ IROM)

```python
mfp_upload_binary_to_addr(er, ew, 'QA30_RAMDLD_0206_Patched_Dump_SRAM.ldr', 0x002F0000, 0x002F0000)
mfp_dump_sram(er, ew, 'MSM_IRAM_Dump.bin', 0xFFFF0000, 0xFFFFFFFF, 0x10)

mfp_upload_binary_to_addr(er, ew, 'QA30_RAMDLD_0206_Patched_Dump_NAND.ldr', 0x002F0000, 0x002F0000)
mfp_dump_nand(er, ew, 'VE40_NAND_Dump.bin', 0, int(0x08000000 / 512), 0x10)

mfp_upload_binary_to_addr(er, ew, 'QA30_RAMDLD_0206_Patched_Dump_NAND_WIDE.ldr', 0x002F0000, 0x002F0000)
mfp_dump_nand(er, ew, 'QA30_NAND_Dump.bin', 0, int(0x04000000 / 512), 0x10, 4)
```

### Dumping 4+1 MB NOR Memory from Motorola V120e

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/V120e_RAMDLD_0713_Patched_Dump_NOR.ldr', 0x01010000, 0x01010000)
mfp_dump_sram(er, ew, 'V120e_ROM_Dump.bin', 0x00000000, 0x00500000, 0x30) # 4 MiB + 1 MiB
```

### Dumping 16 MB NOR Memory from Motorola W315

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/W315_RAMDLD_0106_Patched_Dump_NOR.ldr', 0x14010000, 0x14010000)
mfp_dump_sram(er, ew, 'W315_ROM_Dump.bin', 0x00000000, 0x01000000, 0x30)
```

### Dumping AP and BP NOR Memories from Motorola A760, A768, A768i, A728, A780, E680 (+ IROM)

```python
# AP Part (A760/A768), (A728/A768i)
mfp_upload_binary_to_addr(er, ew, 'loaders/A760_AP_RAMDLD_0000_Patched_Dump_NOR.ldr', 0xA0200000, 0xA0200000, ezx_ap=True)
mfp_upload_binary_to_addr(er, ew, 'loaders/A768i_AP_RAMDLD_0000_Patched_Dump_NOR.ldr', 0xA0200000, 0xA0200000, ezx_ap=True)

mfp_dump_sram(er, ew, 'A760_AP_ROM_Dump.bin', 0x00000000, 0x02000000, 0x30)

sudo ./FlashTerminal.py -l
sudo ./FlashTerminal.py

# BP Part (A760/A768), (A728/A768i/A780/E680)
mfp_upload_binary_to_addr(er, ew, 'loaders/A760_BP_RAMDLD_0372_Patched_Dump_NOR.ldr', 0x11060000, 0x11060010)
mfp_upload_binary_to_addr(er, ew, 'loaders/A768i_BP_RAMDLD_0731_Patched_Dump_NOR.ldr', 0x12000000, 0x12000010)
mfp_upload_binary_to_addr(er, ew, 'loaders/A780g_BP_RAMDLD_08A0.ldr', 0x03FD0000, 0x03FD0010)

mfp_dump_sram(er, ew, 'A760_BP_ROM_Dump.bin', 0x00000000, 0x00400000, 0x30)
mfp_dump_sram(er, ew, 'A760_BP_IROM_Dump.bin', 0x10000000, 0x10400000, 0x30)

mfp_dump_read(er, ew, 'A768i_BP_ROM_Dump.bin', 0x00000000, 0x00400000, 0x400)
mfp_dump_read(er, ew, 'A768i_BP_IROM_Dump.bin', 0x10000000, 0x10400000, 0x400)
mfp_dump_read(er, ew, 'A780_BP_ROM_Dump.bin', 0x10000000, 0x10400000, 0x400)

sudo ./FlashTerminal.py -l
sudo ./FlashTerminal.py -l -2
```

### Dumping AP and BP NOR Memories from Motorola A780, E680, E895, A910, A910i, ROKR E2, MING A1200, MING A1600 (+ IROM)

```python
# AP Part
mfp_upload_binary_to_addr(er, ew, 'loaders/gen-blob/head.bin', 0xA1000000)
mfp_upload_binary_to_addr(er, ew, 'loaders/gen-blob/blob-a780', 0xA0DE0000, 0xA0DE0000, ezx_ap=True)
mfp_upload_binary_to_addr(er, ew, 'loaders/gen-blob/blob-a1200', 0xA0DE0000, 0xA0DE0000, ezx_ap=True)

mfp_dump_rbin(er, ew, 'A910_AP_ROM_Dump.bin', 0x00000000, 0x04000000, 0x1000)

sudo ./FlashTerminal.py -l
sudo ./FlashTerminal.py

# BP Part
mfp_upload_binary_to_addr(er, ew, 'loaders/A910_BP_RAMDLD_0912.ldr', 0x03FC8000, 0x03FC8010, True)
mfp_upload_binary_to_addr(er, ew, 'loaders/A910i_BP_RAMDLD_0982.ldr', 0x03FC8000, 0x03FC8010, True)

mfp_dump_read(er, ew, 'A910_BP_ROM_Dump.bin', 0x10000000, 0x10400000, 0x100)
mfp_dump_read(er, ew, 'A910_BP_IROM_Dump.bin', 0x00000000, 0x00040000, 0x100)

sudo ./FlashTerminal.py -l
```

### Dumping 64 MB NOR Memory from Motorola SLVR L72/L9 and KRZR K1s

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/K1s_RAMDLD_0DC0.ldr', 0x03FC8000, 0x03FC8010, True)
mfp_upload_binary_to_addr(er, ew, 'loaders/L72_RAMDLD_0C70.ldr', 0x03FC8000, 0x03FC8010, True)
mfp_dump_read(er, ew, 'L9_ROM_Dump.bin', 0x10000000, 0x14000000, 0x100)
```

### Dumping 32 MB NOR Memory from Siemens CC75 (Mars, Mosel) using MEMACS

```python
timeout_read = 600000   # 10 min.
timeout_write = 600000  # 10 min.
p2k_do_memacs_dump(p2k_usb_device, 'CC75_MEMACS_DUMP.bin', 0x10000000, 0x12000000, 0x800)
```

### Dumping 32 MB NOR Memory from Motorola PEBL U3

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/U3_RAMDLD_0CF0.ldr', 0x03FC8000, 0x03FC8010, True)
mfp_dump_read(er, ew, 'U3_ROM_Dump.bin', 0x10000000, 0x12000000, 0x100)
```

### Dumping 32+32 MB NOR Memory from Motorola KRZR K3

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/K3_RAMDLD_0320.ldr', 0x80000000, 0x80000038, True)
mfp_dump_read(er, ew, 'K3_ROM_Dump_1.bin', 0xA0000000, 0xA1FFFFFF, 0x300)
mfp_dump_read(er, ew, 'K3_ROM_Dump_2.bin', 0xB4000000, 0xB5FFFFFF, 0x300)
```

### Dumping 64 MB NOR Memory from Motorola RAZR2 V9

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/V9_RAMDLD_R263313_05F4.ldr', 0x80000000, 0x80000038, True)
mfp_dump_read(er, ew, 'V9_ROM_Dump.bin', 0xA0000000, 0xA4000000, 0x200)
```

### Dumping 32+32 MB NOR Memory from Motorola FOMA M702iG and Motorola FOMA M702iS (+ IROM)

```python
mfp_upload_binary_to_addr(er, ew, 'loaders/M702iG_RAMDLD_0303.ldr', 0x80000000, 0x80000038, True)
mfp_upload_binary_to_addr(er, ew, 'loaders/M702iS_RAMDLD_0303.ldr', 0x80000000, 0x80000038, True)

# Engineering prototype.
mfp_dump_rqrc(er, ew, 'M701iG_IROM_Dump_1.bin', 0x00000000, 0x00004000)
mfp_dump_rqrc(er, ew, 'M701iG_IROM_Dump_2.bin', 0x00404000, 0x00408000)
mfp_dump_read(er, ew, 'M701iG_ROM_Dump_1.bin', 0xA0000000, 0xA2000000, 0x300)
mfp_dump_read(er, ew, 'M701iG_ROM_Dump_2.bin', 0xB4000000, 0xB6000000, 0x300)

# Production released phone (Skip PDS).
mfp_dump_read(er, ew, 'M702iS_ROM_Dump_1.bin', 0xA0000000, 0xA0040000, 0x200) # Skip PDS.
mfp_dump_read(er, ew, 'M702iS_ROM_Dump_2.bin', 0xA0080000, 0xA2000000, 0x200) # Skip PDS.
mfp_dump_read(er, ew, 'M702iS_ROM_Dump_3.bin', 0xB4000000, 0xB6000000, 0x200)
```

### Dumping 8 MiB NOR Memory from Motorola V60t Color (+ IROM)

```
mfp_upload_binary_to_addr(er, ew, 'loaders/T720_RAMDLD_0370_Patched_Dump_NOR.ldr', 0x11010000, 0x11010010)
#	mfp_cmd(er, ew, 'RQHW')
mfp_dump_sram(er, ew, 'V60tc_ROM_Dump.bin', 0x10000000, 0x10800000, 0x30)
mfp_dump_sram(er, ew, 'V60tc_IROM_Dump.bin', 0x00000000, 0x00400000, 0x30)
```
