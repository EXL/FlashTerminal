#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/home/exl/Storage/Projects/Git/MotoFanRu/P2K-ELF-SDK-OLD/ELFKIT_EP1_Linux/bin

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -bigend -apcs /interwork -O2 -DSTART_ADDR=0x80000000 -DNULLED_4BYTES_ADDR=0x80002360 ../Injection_RQHW_Dump_SRAM.c -c -o patch_nor_1.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x80002068 patch_nor_1.o ../syms/Z9_RAMDLD_0500.sym -o patch_nor_1.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor_1.elf -bin -output patch_nor_1.bin

cp Z9_RAMDLD_0500.ldr Z9_RAMDLD_0500_Patched_Dump_NOR_IROM.ldr

# Insert patch to 0x2068 offset.
python3 -c "with open('patch_nor_1.bin','rb') as i,open('Z9_RAMDLD_0500_Patched_Dump_NOR_IROM.ldr','r+b') as o: o.seek(0x2068);o.write(i.read())"

# Clean intermedianes.
rm -f *.o *.elf patch_nor*.bin
