#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/

# Compile dump RAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -O2 Injection_RQRC_Dump_RAM.c -c -o patch_ram.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x0013B430 patch_ram.o V9m_RAMDLD_01B5.sym -o patch_ram.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_ram.elf -bin -output patch_ram.bin
# Align patch file with 12 (0x0C) bytes.
python3 -c "data=(b'\xFF' * 12)+open('patch_ram.bin','rb').read();open('patch_ram.bin','wb').write(data)"
# Add patch to RAMDLD.
cat V9m_RAMDLD_01B5.ldr patch_ram.bin > V9m_RAMDLD_01B5_Patched_Dump_RAM.ldr
# Add branch patch.
python3 -c "with open('V9m_RAMDLD_01B5_Patched_Dump_RAM.ldr','r+b') as f: f.seek(0x249A);f.write(b'\x38\xF0\xC9\xFF')"

# Compile dump NAND patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -O2 Injection_RQRC_Dump_NAND.c -c -o patch_nand.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x0013B430 patch_nand.o V9m_RAMDLD_01B5.sym -o patch_nand.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand.elf -bin -output patch_nand.bin
# Align patch file with 12 (0x0C) bytes.
python3 -c "data=(b'\xFF' * 12)+open('patch_nand.bin','rb').read();open('patch_nand.bin','wb').write(data)"
# Add patch to RAMDLD.
cat V9m_RAMDLD_01B5.ldr patch_nand.bin > V9m_RAMDLD_01B5_Patched_Dump_NAND.ldr
# Add branch patch.
python3 -c "with open('V9m_RAMDLD_01B5_Patched_Dump_NAND.ldr','r+b') as f: f.seek(0x249A);f.write(b'\x38\xF0\xC9\xFF')"

# Clean intermedianes.
rm -f *.o *.elf patch_ram.bin patch_nand.bin
