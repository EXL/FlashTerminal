#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -O2 ../Injection_RQRC_Dump_SRAM.c -c -o patch_nor.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x140182D0 patch_nor.o ../syms/W315_RAMDLD_0106.sym -o patch_nor.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor.elf -bin -output patch_nor.bin

cp W315_RAMDLD_0106.ldr W315_RAMDLD_0106_Patched_Dump_NOR.ldr

# Align patch file with 12 (0x0C) bytes.
python3 -c "data=(b'\xFF' * 12)+open('patch_nor.bin','rb').read();open('patch_nor.bin','wb').write(data)"

# Insert patch to 0x82D0 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('W315_RAMDLD_0106_Patched_Dump_NOR.ldr','r+b') as o: o.seek(0x82C4);o.write(i.read())"

# Add branch patch.
python3 -c "with open('W315_RAMDLD_0106_Patched_Dump_NOR.ldr','r+b') as f: f.seek(0x3CA2);f.write(b'\x04\xF0\x15\xFB')"

# Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
