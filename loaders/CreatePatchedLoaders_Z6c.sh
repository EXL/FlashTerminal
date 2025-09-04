#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/

# Compile dump NAND patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -DFTR_V9M_MSM6550 -O2 ../Injection_RQRC_Dump_NAND.c -c -o patch_nand.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x0012C2D4 patch_nand.o ../syms/Z6c_RAMDLD_000D.sym -o patch_nand.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand.elf -bin -output patch_nand.bin

# Insert patch to 0x0002C2D2 addr, NOP to align.
cp Z6c_RAMDLD_000D.ldr Z6c_RAMDLD_000D_Patched_Dump_NAND.ldr
python3 -c "with open('Z6c_RAMDLD_000D_Patched_Dump_NAND.ldr','r+b') as f: f.seek(0x2C2D2);f.write(b'\x00\xBF')"
python3 -c "with open('Z6c_RAMDLD_000D_Patched_Dump_NAND.ldr','r+b') as f: f.seek(0x2C2D4); f.write(open('patch_nand.bin','rb').read())"

# Clean intermedianes.
rm -f *.o *.elf patch_sram.bin patch_nand.bin
