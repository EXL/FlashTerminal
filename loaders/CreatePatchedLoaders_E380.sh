#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin
ADS_TOOLCHAIN_BIN_DIR=/home/exl/Storage/Projects/Git/MotoFanRu/P2K-ELF-SDK-OLD/ELFKIT_EP1_Linux/bin

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -bigend -apcs /interwork -O2 -DSTART_ADDR=0x10000000 -DNULLED_4BYTES_ADDR=0x01FD37C8 ../Injection_RQHW_Dump_SRAM.c -c -o patch_nor.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x01FD36D8 patch_nor.o ../syms/E380_RAMDLD_Blank.sym -o patch_nor.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor.elf -bin -output patch_nor.bin

cp E380_RAMDLD_Blank.ldr E380_RAMDLD_Hacked_RQHW.ldr

# Insert patch to 0x36D8 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('E380_RAMDLD_Hacked_RQHW.ldr','r+b') as o: o.seek(0x36D8);o.write(i.read())"

# Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
