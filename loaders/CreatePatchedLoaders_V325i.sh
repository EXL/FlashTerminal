#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/

# Compile dump NAND patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -DFTR_V3M_MSM6500 -O2 ../Injection_RQRC_Dump_NAND.c -c -o patch_nand.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x0012EAE0 patch_nand.o ../syms/V325i_RAMDLD_010A.sym -o patch_nand.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand.elf -bin -output patch_nand.bin
# Align patch file with 8 (0x08) bytes.
python3 -c "data=(b'\xFF' * 8)+open('patch_nand.bin','rb').read();open('patch_nand.bin','wb').write(data)"
# Add patch to RAMDLD.
cat V325i_RAMDLD_010A.ldr patch_nand.bin > V325i_RAMDLD_010A_Patched_Dump_NAND.ldr
# Add branch patch.
python3 -c "with open('V325i_RAMDLD_010A_Patched_Dump_NAND.ldr','r+b') as f: f.seek(0x1514C);f.write(b'\x19\xF0\xC8\xFC')"

## Clean intermedianes.
rm -f *.o *.elf patch_sram.bin patch_nand.bin
