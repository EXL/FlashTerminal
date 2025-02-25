#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/
#ADS_TOOLCHAIN_BIN_DIR=/home/exl/Downloads/Shared/ELFs_Factory/P2K-ELF-SDK-OLD/ELFKIT_EP1_Linux/bin

# Compile dump NAND patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -DFTR_QA30_MSM6575 -O2 ../Injection_RQRC_Dump_NAND.c -c -o patch_nand.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x00809350 patch_nand.o ../syms/VE70_RAMDLD_0101.sym -o patch_nand.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand.elf -bin -output patch_nand.bin
cp VE70_RAMDLD_0101.ldr VE70_RAMDLD_0101_Patched_Dump_NAND.ldr
# Insert patch to 0x9350 offset.
python3 -c "with open('patch_nand.bin','rb') as i,open('VE70_RAMDLD_0101_Patched_Dump_NAND.ldr','r+b') as o: o.seek(0x9350);o.write(i.read())"
# Add branch patch.
python3 -c "with open('VE70_RAMDLD_0101_Patched_Dump_NAND.ldr','r+b') as f: f.seek(0x5F56);f.write(b'\xFC\x0C\x00\xEB')"

# Compile dump NAND WIDE patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -DFTR_QA30_MSM6575 -DNAND_WIDE_HACK -O2 ../Injection_RQRC_Dump_NAND.c -c -o patch_nand_wide.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x00809350 patch_nand_wide.o ../syms/VE70_RAMDLD_0101.sym -o patch_nand_wide.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand_wide.elf -bin -output patch_nand_wide.bin
cp VE70_RAMDLD_0101.ldr VE70_RAMDLD_0101_Patched_Dump_NAND_WIDE.ldr
# Insert patch to 0x9350 offset.
python3 -c "with open('patch_nand_wide.bin','rb') as i,open('VE70_RAMDLD_0101_Patched_Dump_NAND_WIDE.ldr','r+b') as o: o.seek(0x9350);o.write(i.read())"
# Add branch patch.
python3 -c "with open('VE70_RAMDLD_0101_Patched_Dump_NAND_WIDE.ldr','r+b') as f: f.seek(0x5F56);f.write(b'\xFC\x0C\x00\xEB')"

## Clean intermedianes.
rm -f *.o *.elf patch_nand.bin patch_nand_wide.bin
