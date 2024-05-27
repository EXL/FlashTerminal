#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/armcc -apcs /interwork -DFTR_QA30_MSM6575 -O2 ../Injection_RQRC_Dump_SRAM.c -c -o patch_sram.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x0034E160 patch_sram.o ../syms/QA30_RAMDLD_0206.sym -o patch_sram.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_sram.elf -bin -output patch_sram.bin
# Align patch file with 4 (0x04) bytes.
python3 -c "data=(b'\xFF' * 4)+open('patch_sram.bin','rb').read();open('patch_sram.bin','wb').write(data)"
# Add patch to RAMDLD.
cat QA30_RAMDLD_0206.ldr patch_sram.bin > QA30_RAMDLD_0206_Patched_Dump_SRAM.ldr
# Add branch patch.
python3 -c "with open('QA30_RAMDLD_0206_Patched_Dump_SRAM.ldr','r+b') as f: f.seek(0x1A234);f.write(b'\xC9\x0F\x01\xEB')"

# Compile dump NAND patch.
${ADS_TOOLCHAIN_BIN_DIR}/armcc -apcs /interwork -DFTR_QA30_MSM6575 -O2 ../Injection_RQRC_Dump_NAND.c -c -o patch_nand.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x0034E160 patch_nand.o ../syms/QA30_RAMDLD_0206.sym -o patch_nand.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand.elf -bin -output patch_nand.bin
# Align patch file with 4 (0x04) bytes.
python3 -c "data=(b'\xFF' * 4)+open('patch_nand.bin','rb').read();open('patch_nand.bin','wb').write(data)"
# Add patch to RAMDLD.
cat QA30_RAMDLD_0206.ldr patch_nand.bin > QA30_RAMDLD_0206_Patched_Dump_NAND.ldr
# Add branch patch.
python3 -c "with open('QA30_RAMDLD_0206_Patched_Dump_NAND.ldr','r+b') as f: f.seek(0x1A234);f.write(b'\xC9\x0F\x01\xEB')"

# Compile dump NAND WIDE patch.
${ADS_TOOLCHAIN_BIN_DIR}/armcc -apcs /interwork -DFTR_QA30_MSM6575 -DNAND_WIDE_HACK -O2 ../Injection_RQRC_Dump_NAND.c -c -o patch_nand_wide.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x0034E160 patch_nand_wide.o ../syms/QA30_RAMDLD_0206.sym -o patch_nand_wide.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand_wide.elf -bin -output patch_nand_wide.bin
# Align patch file with 4 (0x04) bytes.
python3 -c "data=(b'\xFF' * 4)+open('patch_nand_wide.bin','rb').read();open('patch_nand_wide.bin','wb').write(data)"
# Add patch to RAMDLD.
cat QA30_RAMDLD_0206.ldr patch_nand_wide.bin > QA30_RAMDLD_0206_Patched_Dump_NAND_WIDE.ldr
# Add branch patch.
python3 -c "with open('QA30_RAMDLD_0206_Patched_Dump_NAND_WIDE.ldr','r+b') as f: f.seek(0x1A234);f.write(b'\xC9\x0F\x01\xEB')"

## Clean intermedianes.
rm -f *.o *.elf patch_sram.bin patch_nand.bin patch_nand_wide.bin
