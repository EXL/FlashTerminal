#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/home/exl/Storage/Projects/Git/MotoFanRu/P2K-ELF-SDK-OLD/ELFKIT_EP1_Linux/bin

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -bigend -apcs /interwork -O2 -DSTART_ADDR=0x10000000 -DNULLED_4BYTES_ADDR=0x03FA3898 ../Injection_RQHW_Dump_SRAM.c -c -o patch_nor.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x03FA379C patch_nor.o ../syms/C350LTS_RAMDLD_0920.sym -o patch_nor.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor.elf -bin -output patch_nor.bin

cp C350LTS_RAMDLD_0920.ldr C350LTS_RAMDLD_0920_Patched_Dump_NOR.ldr

# Insert patch to 0x379C offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('C350LTS_RAMDLD_0920_Patched_Dump_NOR.ldr','r+b') as o: o.seek(0x379C);o.write(i.read())"

# Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
