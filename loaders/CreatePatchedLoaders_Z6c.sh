#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/
ADS_TOOLCHAIN_BIN_DIR=/home/exl/Storage/Projects/Git/MotoFanRu/P2K-ELF-SDK-OLD/ELFKIT_EP1_Linux/bin/

# Compile dump NAND patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -DFTR_V9M_MSM6550 -O2 ../Injection_RQRC_Dump_NAND.c -c -o patch_nand.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x00127600 patch_nand.o ../syms/Z6c_RAMDLD_000D.sym -o patch_nand.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand.elf -bin -output patch_nand.bin

# Insert patch to 0x00027600 addr, BL to it.
cp Z6c_RAMDLD_000D.ldr Z6c_RAMDLD_000D_Patched_Dump_NAND.ldr
python3 -c "with open('Z6c_RAMDLD_000D_Patched_Dump_NAND.ldr','r+b') as f: f.seek(0x39272);f.write(b'\xEE\xF7\xC5\xF9')"
python3 -c "with open('Z6c_RAMDLD_000D_Patched_Dump_NAND.ldr','r+b') as f: f.seek(0x27600); f.write(open('patch_nand.bin','rb').read())"

# Clean intermedianes.
rm -f *.o *.elf patch_sram.bin patch_nand.bin
