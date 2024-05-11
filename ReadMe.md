Flash Terminal
==============

A set of utilities and loaders (RAM downloaders) for researching the Motorola Flash Protocol.

## Usage

The workflow can be configured directly in the [FlashTerminal.py](FlashTerminal.py) file's `Settings` and `Worksheet` sections.

### Activate verbose hexdump USB-packets logging

```diff
-verbose_flag = False
+verbose_flag = True
```

### Dumping 64 MB SRAM from Motorola RAZR2 V9m and Motorola ROKR Z6m

```python
mfp_upload_binary_to_addr(er, ew, 'V9m_RAMDLD_01B5_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000)
time.sleep(1.0)
mfp_dump_sram(er, ew, 'V9m_SRAM_Dump.bin', 0x00000000, 0x04000000, 0x30)
```

### Dumping 128 MB NAND from Motorola RAZR2 V9m and Motorola ROKR Z6m

```python
mfp_upload_binary_to_addr(er, ew, 'V9m_RAMDLD_01B5_Patched_Dump_NAND.ldr', 0x00100000, 0x00100000)
time.sleep(1.0)
mfp_dump_nand(er, ew, 'V9m_NAND_Dump.bin', 0, int(0x08000000 / 512), 0x30)
```
