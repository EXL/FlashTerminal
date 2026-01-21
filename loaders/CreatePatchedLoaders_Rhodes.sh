#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin

# Compile dump NAND patch.
${ADS_TOOLCHAIN_BIN_DIR}/armcc -apcs /interwork -DFTR_QA30_MSM6575 -O2 ../Injection_RQRC_Dump_NAND.c -c -o patch_nand.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x0016CF58 patch_nand.o ../syms/RHODES_RAMDLD_0000.sym -o patch_nand.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand.elf -bin -output patch_nand.bin
# Add patch to RAMDLD.
cp RHODES_RAMDLD_0000.ldr RHODES_RAMDLD_0000_Patched_Dump_NAND.ldr
# Insert patch to 0x1CF58 offset.
python3 -c "with open('patch_nand.bin','rb') as i,open('RHODES_RAMDLD_0000_Patched_Dump_NAND.ldr','r+b') as o: o.seek(0x1CF58);o.write(i.read())"

# Compile dump NAND WIDE patch.
${ADS_TOOLCHAIN_BIN_DIR}/armcc -apcs /interwork -DFTR_QA30_MSM6575 -DNAND_WIDE_HACK -O2 ../Injection_RQRC_Dump_NAND.c -c -o patch_nand_wide.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x0016CF58 patch_nand_wide.o ../syms/RHODES_RAMDLD_0000.sym -o patch_nand_wide.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nand_wide.elf -bin -output patch_nand_wide.bin
# Add patch to RAMDLD.
cp RHODES_RAMDLD_0000.ldr RHODES_RAMDLD_0000_Patched_Dump_NAND_WIDE.ldr
# Insert patch to 0x1CF58 offset.
python3 -c "with open('patch_nand_wide.bin','rb') as i,open('RHODES_RAMDLD_0000_Patched_Dump_NAND_WIDE.ldr','r+b') as o: o.seek(0x1CF58);o.write(i.read())"

## Clean intermedianes.
rm -f *.o *.elf patch_nand.bin patch_nand_wide.bin
