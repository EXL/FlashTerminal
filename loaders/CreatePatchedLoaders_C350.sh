#!/usr/bin/bash

# Compile dump SRAM patch.
arm-none-eabi-gcc -march=armv4t -mcpu=arm7tdmi -mbig-endian -mthumb -mthumb-interwork -nostdlib -fshort-wchar -fshort-enums -fpack-struct=4 -fno-builtin -fvisibility=hidden \
	-DARM7TDMI_MOTOROLA_C350 -O2 ../Injection_RQRC_Dump_SRAM.c -c -o patch_nor.o
arm-none-eabi-ld -pie -EB -nostdlib -Bstatic patch_nor.o \
	-T../lds/Injection_ARM7TDMI-S_C350.ld -o patch_nor.elf

cp C350_RAMDLD_0372.bin C350_RAMDLD_0372_Patched_Dump_NOR.bin

# Insert patch to 0x13A80 offset.
#python3 -c "with open('patch_nor.bin','rb') as i,open('C350_RAMDLD_0372_Patched_Dump_NOR.bin','r+b') as o: o.seek(0x13A80);o.write(i.read())"

# Add branch patch.
#python3 -c "with open('C350_RAMDLD_0372_Patched_Dump_NOR.bin','r+b') as f: f.seek(0x10776);f.write(b'\xF0\x03\xF9\x83')"

# Clean intermedianes.
#rm -f *.o *.elf patch_nor.bin
