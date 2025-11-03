#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin
ADS_TOOLCHAIN_BIN_DIR=/home/exl/Storage/Projects/Git/MotoFanRu/P2K-ELF-SDK-OLD/ELFKIT_EP1_Linux/bin

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -O2 -DSTART_ADDR=0x00000000 -DNULLED_4BYTES_ADDR=0x10030840 ../Injection_RQHW_Dump_SRAM.c -c -o patch_nor.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x10030728 patch_nor.o ../syms/V710_RAMDLD_0807.sym -o patch_nor.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor.elf -bin -output patch_nor.bin

cp V710_RAMDLD_0807.ldr V710_RAMDLD_0807_Patched_Dump_NOR.ldr

# Insert patch to 0x10728 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('V710_RAMDLD_0807_Patched_Dump_NOR.ldr','r+b') as o: o.seek(0x10728);o.write(i.read())"

# Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
