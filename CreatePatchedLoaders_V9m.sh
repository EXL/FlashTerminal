#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -DFTR_V9M_MSM6550 -O2 Injection_RQRC_Dump_SRAM.c -c -o patch_sram.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x0013B430 patch_sram.o V9m_RAMDLD_01B5.sym -o patch_sram.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_sram.elf -bin -output patch_sram.bin
# Align patch file with 12 (0x0C) bytes.
python3 -c "data=(b'\xFF' * 12)+open('patch_sram.bin','rb').read();open('patch_sram.bin','wb').write(data)"
# Add patch to RAMDLD.
cat V9m_RAMDLD_01B5.ldr patch_sram.bin > V9m_RAMDLD_01B5_Patched_Dump_SRAM.ldr
# Add branch patch.
python3 -c "with open('V9m_RAMDLD_01B5_Patched_Dump_SRAM.ldr','r+b') as f: f.seek(0x249A);f.write(b'\x38\xF0\xC9\xFF')"

# Compile dump NAND patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -DFTR_V9M_MSM6550 -O2 Injection_RQRC_Dump_NAND.c -c -o patch_nand.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x0013B430 patch_nand.o V9m_RAMDLD_01B5.sym -o patch_nand.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand.elf -bin -output patch_nand.bin
# Align patch file with 12 (0x0C) bytes.
python3 -c "data=(b'\xFF' * 12)+open('patch_nand.bin','rb').read();open('patch_nand.bin','wb').write(data)"
# Add patch to RAMDLD.
cat V9m_RAMDLD_01B5.ldr patch_nand.bin > V9m_RAMDLD_01B5_Patched_Dump_NAND.ldr
# Add branch patch.
python3 -c "with open('V9m_RAMDLD_01B5_Patched_Dump_NAND.ldr','r+b') as f: f.seek(0x249A);f.write(b'\x38\xF0\xC9\xFF')"

# Clean intermedianes.
rm -f *.o *.elf patch_sram.bin patch_nand.bin
