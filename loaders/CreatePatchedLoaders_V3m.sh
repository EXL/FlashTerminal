#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -DFTR_V3M_MSM6500 -O2 ../Injection_RQRC_Dump_SRAM.c -c -o patch_sram.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x00133D90 patch_sram.o ../syms/V3m_RAMDLD_010C.sym -o patch_sram.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_sram.elf -bin -output patch_sram.bin
# Align patch file with 12 (0x0C) bytes.
python3 -c "data=(b'\xFF' * 12)+open('patch_sram.bin','rb').read();open('patch_sram.bin','wb').write(data)"
# Add patch to RAMDLD.
cat V3m_RAMDLD_010C.ldr patch_sram.bin > V3m_RAMDLD_010C_Patched_Dump_SRAM.ldr
# Add branch patch.
python3 -c "with open('V3m_RAMDLD_010C_Patched_Dump_SRAM.ldr','r+b') as f: f.seek(0x1A35A);f.write(b'\x19\xF0\x19\xFD')"

# Compile dump NAND patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -DFTR_V3M_MSM6500 -O2 ../Injection_RQRC_Dump_NAND.c -c -o patch_nand.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x00133D90 patch_nand.o ../syms/V3m_RAMDLD_010C.sym -o patch_nand.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand.elf -bin -output patch_nand.bin
# Align patch file with 12 (0x0C) bytes.
python3 -c "data=(b'\xFF' * 12)+open('patch_nand.bin','rb').read();open('patch_nand.bin','wb').write(data)"
# Add patch to RAMDLD.
cat V3m_RAMDLD_010C.ldr patch_nand.bin > V3m_RAMDLD_010C_Patched_Dump_NAND.ldr
# Add branch patch.
python3 -c "with open('V3m_RAMDLD_010C_Patched_Dump_NAND.ldr','r+b') as f: f.seek(0x1A35A);f.write(b'\x19\xF0\x19\xFD')"

## Clean intermedianes.
rm -f *.o *.elf patch_sram.bin patch_nand.bin
