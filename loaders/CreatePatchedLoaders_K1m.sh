#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/

# Compile dump NAND patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -DFTR_V3M_MSM6500 -O2 ../Injection_RQRC_Dump_NAND.c -c -o patch_nand.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x0013A470 patch_nand.o ../syms/K1m_RAMDLD_0013.sym -o patch_nand.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand.elf -bin -output patch_nand.bin
# Align patch file with 0 (0x00) bytes.
# python3 -c "data=(b'\xFF' * 0)+open('patch_nand.bin','rb').read();open('patch_nand.bin','wb').write(data)"
# Add patch to RAMDLD.
cat K1m_RAMDLD_0013.ldr patch_nand.bin > K1m_RAMDLD_0013_Patched_Dump_NAND.ldr
# Add branch patch.
python3 -c "with open('K1m_RAMDLD_0013_Patched_Dump_NAND.ldr','r+b') as f: f.seek(0x217A);f.write(b'\x38\xF0\x79\xF9')"

## Clean intermedianes.
rm -f *.o *.elf patch_sram.bin patch_nand.bin

# Compile dump NAND patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -DFTR_V3M_MSM6500 -O2 ../Injection_RQRC_Dump_NAND.c -c -o patch_nand.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x00138220 patch_nand.o ../syms/K1mm_RAMDLD_000D.sym -o patch_nand.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand.elf -bin -output patch_nand.bin
# Align patch file with 4 (0x04) bytes.
python3 -c "data=(b'\xFF' * 4)+open('patch_nand.bin','rb').read();open('patch_nand.bin','wb').write(data)"
# Add patch to RAMDLD.
cat K1mm_RAMDLD_000D.ldr patch_nand.bin > K1mm_RAMDLD_000D_Patched_Dump_NAND.ldr
# Add branch patch.
python3 -c "with open('K1mm_RAMDLD_000D_Patched_Dump_NAND.ldr','r+b') as f: f.seek(0x2316);f.write(b'\x35\xF0\x83\xFF')"

## Clean intermedianes.
rm -f *.o *.elf patch_sram.bin patch_nand.bin
