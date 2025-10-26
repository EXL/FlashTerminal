#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/home/exl/Storage/Projects/Git/MotoFanRu/P2K-ELF-SDK-OLD/ELFKIT_EP1_Linux/bin

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -bigend -apcs /interwork -O2 -DSTART_ADDR=0x00000000 -DNULLED_4BYTES_ADDR=0x8000000C ../Injection_RQHW_Dump_SRAM.c -c -o patch_nor_1.o
${ADS_TOOLCHAIN_BIN_DIR}/tcc -bigend -apcs /interwork -O2 -DSTART_ADDR=0x00404000 -DNULLED_4BYTES_ADDR=0x8000000C ../Injection_RQHW_Dump_SRAM.c -c -o patch_nor_2.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x80001FFC patch_nor_1.o ../syms/M704i_RAMDLD_04C1.sym -o patch_nor_1.elf
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x80001FFC patch_nor_2.o ../syms/M704i_RAMDLD_04C1.sym -o patch_nor_2.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor_1.elf -bin -output patch_nor_1.bin
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor_2.elf -bin -output patch_nor_2.bin

cp M704i_RAMDLD_04C1.ldr M704i_RAMDLD_04C1_Patched_Dump_NOR_IROM1.ldr
cp M704i_RAMDLD_04C1.ldr M704i_RAMDLD_04C1_Patched_Dump_NOR_IROM2.ldr

# Insert patch to 0x1FFC offset.
python3 -c "with open('patch_nor_1.bin','rb') as i,open('M704i_RAMDLD_04C1_Patched_Dump_NOR_IROM1.ldr','r+b') as o: o.seek(0x1FFC);o.write(i.read())"
python3 -c "with open('patch_nor_2.bin','rb') as i,open('M704i_RAMDLD_04C1_Patched_Dump_NOR_IROM2.ldr','r+b') as o: o.seek(0x1FFC);o.write(i.read())"

# Clean intermedianes.
rm -f *.o *.elf patch_nor*.bin
