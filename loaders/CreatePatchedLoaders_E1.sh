#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -bigend -apcs /interwork -O2 -DSTART_ADDR=0x00000000 -DNULLED_4BYTES_ADDR=0x03FD5034 ../Injection_RQHW_Dump_SRAM.c -c -o patch_nor.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x03FD4F0C patch_nor.o ../syms/E1_RAMDLD_0A20.sym -o patch_nor.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor.elf -bin -output patch_nor.bin

cp E1_RAMDLD_0A20.ldr E1_RAMDLD_0A20_Patched_Dump_NOR.ldr

# Insert patch to 0x4F0C offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('E1_RAMDLD_0A20_Patched_Dump_NOR.ldr','r+b') as o: o.seek(0x4F0C);o.write(i.read())"

# Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
