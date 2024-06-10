#if 0
$ tcc -apcs /interwork -O2 Injection_RQRC_Dump_NAND.c -c -o patch_nand.o
$ armlink -ro-base 0x0013B430 patch_nand.o V9m_RAMDLD_01B5.sym -o patch_nand.elf
$ fromelf patch_nand.elf -bin -output patch_nand.bin
#endif

#define ADDR_CMD_ADDR_SIZE              8
#define MAX_RESPONSE_DATA_SIZE         95

typedef unsigned char               UINT8;
typedef unsigned short             UINT16;
typedef unsigned int               UINT32;
typedef int                         INT32;
typedef long long                   INT64;

typedef struct {
	UINT32                     start_addr;
	UINT32                       end_addr;
} BLOADER_SECTION_ADDR_TBL;

extern UINT8 rsrc_str[];
extern BLOADER_SECTION_ADDR_TBL blvar_RAM_section_addr_tbl;

extern void HAPI_WATCHDOG_service(void);
extern void parser_send_packet(UINT8 *command_ptr, UINT8 *data_ptr);
extern void util_ui8_to_hexasc(UINT8 val, UINT8 *str_ptr);
extern UINT32 util_hexasc_to_ui32(UINT8 *str_ptr, UINT8 size);

// MSM6550: V9m, Z6m
extern INT32 watchdog_check_121A78(void);
extern INT64 watchdog_delay_121ADC(void);

// MSM6575, MSM6800: QA30, VE40, ic902
INT32 watchdog_check_delay_326EB8(void);

// MSM6125, MSM6500: V3m, E815, W755, W385
INT32 watchdog_check_delay_110344(void);

void handle_command_RQRC(UINT8 *data_ptr) {
	UINT8 response[MAX_RESPONSE_DATA_SIZE];
	UINT8 *response_ptr = &response[0];
	UINT8 *data_start_ptr, *data_end_ptr;
	UINT32 page;
	UINT32 wide;

	blvar_RAM_section_addr_tbl.start_addr = util_hexasc_to_ui32(&data_ptr[0], ADDR_CMD_ADDR_SIZE);
	blvar_RAM_section_addr_tbl.end_addr = util_hexasc_to_ui32(&data_ptr[ADDR_CMD_ADDR_SIZE + 1], ADDR_CMD_ADDR_SIZE);
	page = util_hexasc_to_ui32(&data_ptr[ADDR_CMD_ADDR_SIZE + 1 + ADDR_CMD_ADDR_SIZE + 1], ADDR_CMD_ADDR_SIZE);
#if defined(NAND_WIDE_HACK)
	wide = util_hexasc_to_ui32(&data_ptr[ADDR_CMD_ADDR_SIZE * 2 + 3], ADDR_CMD_ADDR_SIZE);
#else
	wide = 3;
#endif

	data_start_ptr = (UINT8 *) blvar_RAM_section_addr_tbl.start_addr;
	data_end_ptr   = (UINT8 *) blvar_RAM_section_addr_tbl.end_addr;

#if 0
	{
		UINT32 addr = blvar_RAM_section_addr_tbl.start_addr;
		UINT8 *ptar = (UINT8 *) &addr;
		util_ui8_to_hexasc(*ptar, response_ptr); ptar++; response_ptr += 2;
		util_ui8_to_hexasc(*ptar, response_ptr); ptar++; response_ptr += 2;
		util_ui8_to_hexasc(*ptar, response_ptr); ptar++; response_ptr += 2;
		util_ui8_to_hexasc(*ptar, response_ptr); ptar++; response_ptr += 2;
		util_ui8_to_hexasc(0xAA,  response_ptr); response_ptr += 2; /* sep. */
	}
#endif

//	Qualcomm MSM6550 NAND Flash Memory Interface!
//	Additional informatrion:
//		1. 80-V7196-2-MSM6150-6550-SoftwareInterface.pdf
//		2. 80-V6968-2_MSM6280_Software_Interface.pdf
//		3. https://github.com/dumpit3315/dumpit
//
//		12-May-2024 02:09:57 DEBUG [mfp_cmd]:
//		>>> Send to device...
//		00000000:  02 52 51 52 43 1E 36 30 30 30 30 30 30 30 2C  |.RQRC.60000000,|
//		0000000F:  36 30 30 30 30 30 33 30 2C 30 30 30 30 30 30  |60000030,000000|
//		0000001E:  30 30 03                                      |00.            |
//
//		12-May-2024 02:09:57 DEBUG [mfp_cmd]:
//		<<< Read from device...
//		00000000:  02 52 53 52 43 1E 30 36 30 30 30 30 45 41 39  |.RSRC.060000EA9|
//		0000000F:  31 30 30 30 30 45 41 39 30 30 30 30 30 45 41  |10000EA900000EA|
//		0000001E:  38 46 30 30 30 30 45 41 38 45 30 30 30 30 45  |8F0000EA8E0000E|
//		0000002D:  41 38 44 30 30 30 30 45 41 38 43 30 30 30 30  |A8D0000EA8C0000|
//		0000003C:  45 41 38 42 30 30 30 30 45 41 33 34 30 32 39  |EA8B0000EA34029|
//		0000004B:  46 45 35 30 30 44 30 41 30 45 31 38 30 30 34  |FE500D0A0E18004|
//		0000005A:  41 30 45 33 30 30 32 30 41 30 45 33 03        |A0E30020A0E3.  |

#if defined(FTR_V9M_MSM6550) /* Motorola PCS Flash MSM6550: V9m, Z6m, etc. */
	//	See sub_107678 in the "V9m_RAMDLD_01B5.ldr" file.
	*((UINT32 *) 0x28000000) = 101;
	*((UINT32 *) 0x800002B0) =   2;

	*((UINT32 *) 0x60000304) = page << 9; // 0x0304 / NAND_FLASH_ADDR, 31:9 bits - NAND_FLASH_PAGE_ADDRESS

	watchdog_check_121A78();
	watchdog_check_121A78();

	*((UINT32 *) 0x60000300) = 1;         // 0x0300 / NAND_FLASH_CMD, 2:0 bits - OP_CMD, 001 - page_read

	watchdog_delay_121ADC();
	watchdog_check_121A78();

	*((UINT32 *) 0x60000300) = 7;         // 0x0300 / NAND_FLASH_CMD, 2:0 bits - OP_CMD, 111 - reset
#elif defined(FTR_QA30_MSM6575) /* Motorola PCS Flash MSM6575/MSM6800: QA30, VE40, etc. */
	//	See sub_327F04 in the "QA30_RAMDLD_0206.ldr" file.
	if (blvar_RAM_section_addr_tbl.start_addr == 0x60000000) {
		// 0x0328 / NAND_FLASH_CFG1, 0 bit - ECC_DISABLE
//		*((UINT32 *) 0x60000328) = *((UINT32 *) 0x60000328) & 0xFFE | 1;

		*((UINT32 *) 0x60000300) = page << 9; // 0x0304 / NAND_FLASH_ADDR, 31:9 bits - NAND_FLASH_PAGE_ADDRESS

		watchdog_check_delay_326EB8();

		*((UINT32 *) 0x60000304) = 1;         // 0x0300 / NAND_FLASH_CMD, 2:0 bits - OP_CMD, 001 - page_read

		watchdog_check_delay_326EB8();

		// 0x0328 / NAND_FLASH_CFG1, 0 bit - ECC_DISABLE
//		*((UINT32 *) 0x60000328) = *((UINT32 *) 0x60000328) & 0xFFE;

		if (blvar_RAM_section_addr_tbl.start_addr == 0x60000200 && wide == 3) {
			*((UINT32 *) 0x60000304) = 7;     // 0x0300 / NAND_FLASH_CMD, 2:0 bits - OP_CMD, 111 - reset
		}
	}
#elif defined(FTR_V3M_MSM6500) /* Motorola PCS Flash MSM6125/MSM6500: V3m, E815, W755, W385, etc. */
		//	See sub_110622 in the "V3m_RAMDLD_010C.ldr" file.
		*((UINT32 *) 0x80000904) = 0x2000;
		// 0x031C / NAND_FLASH_CFG1, 0 bit - ECC_DISABLE
//		*((UINT32 *) 0x6400031C) = *((UINT32 *) 0x6400031C) & 0xFFFFFFFE | 1;

		*((UINT32 *) 0x64000304) = page << 9; // 0x0304 / NAND_FLASH_ADDR, 31:9 bits - NAND_FLASH_PAGE_ADDRESS

		*((UINT32 *) 0x80000904) = 0x2000;
		*((UINT32 *) 0x64000300) = 1;         // 0x0300 / NAND_FLASH_CMD, 2:0 bits - OP_CMD, 001 - page_read

		watchdog_check_delay_110344();

		// 0x031C / NAND_FLASH_CFG1, 0 bit - ECC_DISABLE
//		*((UINT32 *) 0x80000904) = 0x2000;
//		*((UINT32 *) 0x6400031C) = *((UINT32 *) 0x6400031C) & 0xFFFFFFFE;
//		watchdog_check_delay_110344();
#else
	#error "Unknown device or unknown MSM SoC!"
#endif

	while (data_start_ptr < data_end_ptr) {
		util_ui8_to_hexasc(*data_start_ptr, response_ptr);

		data_start_ptr++;
		response_ptr += 2;

		HAPI_WATCHDOG_service();
	}

	parser_send_packet((UINT8 *) &rsrc_str[0], response);
}
