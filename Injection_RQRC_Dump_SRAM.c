#if 0
$ tcc -apcs /interwork -O2 Injection_RQRC_Dump_RAM.c -c -o patch_ram.o
$ armlink -ro-base 0x0013B430 patch_ram.o V9m_RAMDLD_01B5.sym -o patch_ram.elf
$ fromelf patch_ram.elf -bin -output patch_ram.bin

$ mcore-elf-gcc -nostdinc -nostdlib -fshort-wchar -funsigned-char -fpic -fpie -mbig-endian -m340 \
	-DM_CORE_MOTOROLA_A830_SIEMENS_U10 -O2 -c Injection_RQRC_Dump_SRAM.c -o Injection_RQRC_Dump_SRAM.o
$ mcore-elf-ld -nostdinc -nostdlib -Bstatic Injection_RQRC_Dump_SRAM.o -TInjection_MCORE_M340.ld -o injection.bin
#endif

#define ADDR_CMD_ADDR_SIZE              8
#define MAX_RESPONSE_DATA_SIZE         95

typedef unsigned char               UINT8;
typedef unsigned short             UINT16;
typedef unsigned int               UINT32;

typedef struct {
	UINT32                     start_addr;
	UINT32                       end_addr;
} BLOADER_SECTION_ADDR_TBL;

#if defined(M_CORE_MOTOROLA_A830_SIEMENS_U10)        /* Motorola A820, A830, Siemens U10. */

/* Rainbow */
#define rsrc_str ((UINT8 *) 0x078064CB)
#define blvar_RAM_section_addr_tbl (*(BLOADER_SECTION_ADDR_TBL *) 0x0782AD7C)

#define HAPI_WATCHDOG_service ((void (*)(void)) (0x07803136))
#define parser_send_packet ((void (*)(UINT8 *, UINT8 *)) (0x07800A7A))
#define util_ui8_to_hexasc ((void (*)(UINT8, UINT8 *)) (0x078006C8))
#define util_hexasc_to_ui32 ((UINT32 (*)(UINT8 *, UINT8)) (0x078006A0))

#elif defined(M_CORE_MOTOROLA_V60_0355)              /* Motorola V60, V66, V60i, V66i, V70, T280, T280i, P280, P280i. */

/* Patriot */
#define rsrc_str ((UINT8 *) 0x1101DA1F)
#define blvar_RAM_section_addr_tbl (*(BLOADER_SECTION_ADDR_TBL *) 0x11025AA0)

#define HAPI_WATCHDOG_service ((void (*)(void)) (0x1101CB02))
#define parser_send_packet ((void (*)(UINT8 *, UINT8 *)) (0x11010B06))
#define util_ui8_to_hexasc ((void (*)(UINT8, UINT8 *)) (0x11012244))
#define util_hexasc_to_ui32 ((UINT32 (*)(UINT8 *, UINT8)) (0x1101221C))

#elif defined(M_CORE_MOTOROLA_V60I_1007)             /* Motorola V60i, V66i on 10.xx bootloaders. */

/* Patriot */
#define rsrc_str ((UINT8 *) 0x00104D71)
#define blvar_RAM_section_addr_tbl (*(BLOADER_SECTION_ADDR_TBL *) 0x11019CEC)

#define HAPI_WATCHDOG_service ((void (*)(void)) (0x0010000A))
#define parser_send_packet ((void (*)(UINT8 *, UINT8 *)) (0x0010159C))
#define util_ui8_to_hexasc ((void (*)(UINT8, UINT8 *)) (0x001042B4))
#define util_hexasc_to_ui32 ((UINT32 (*)(UINT8 *, UINT8)) (0x0010428C))

#elif defined(M_CORE_MOTOROLA_V120C_0312)            /* Motorola V120c. */

/* Wally */
#define rsrc_str ((UINT8 *) 0x4100A733)
#define blvar_RAM_section_addr_tbl (*(BLOADER_SECTION_ADDR_TBL *) 0x4100E948)

#define HAPI_WATCHDOG_service ((void (*)(void)) (0x410098A6))
#define parser_send_packet ((void (*)(UINT8 *, UINT8 *)) (0x41008AC8))
#define util_ui8_to_hexasc ((void (*)(UINT8, UINT8 *)) (0x4100A148))
#define util_hexasc_to_ui32 ((UINT32 (*)(UINT8 *, UINT8)) (0x4100A120))

#elif defined(M_CORE_MOTOROLA_T720_0370)             /* Motorola T720, T720i, T721, T722i. */

/* Patriot */
#define rsrc_str ((UINT8 *) 0x00104B69)
#define blvar_RAM_section_addr_tbl (*(BLOADER_SECTION_ADDR_TBL *) 0x11040068)

#define HAPI_WATCHDOG_service ((void (*)(void)) (0x0010000A))
#define parser_send_packet ((void (*)(UINT8 *, UINT8 *)) (0x001014BE))
#define util_ui8_to_hexasc ((void (*)(UINT8, UINT8 *)) (0x00104004))
#define util_hexasc_to_ui32 ((UINT32 (*)(UINT8 *, UINT8)) (0x00103FDC))

#else                                                /* Any other Motorola phones. */

/* Undefined/ADS */
extern UINT8 rsrc_str[];
extern BLOADER_SECTION_ADDR_TBL blvar_RAM_section_addr_tbl;

extern void HAPI_WATCHDOG_service(void);
extern void parser_send_packet(UINT8 *command_ptr, UINT8 *data_ptr);
extern void util_ui8_to_hexasc(UINT8 val, UINT8 *str_ptr);
extern UINT32 util_hexasc_to_ui32(UINT8 *str_ptr, UINT8 size);

#endif

extern void handle_command_RQRC(UINT8 *data_ptr) {
	UINT8 response[MAX_RESPONSE_DATA_SIZE];
	UINT8 *response_ptr = &response[0];
	UINT8 *data_start_ptr, *data_end_ptr;

#if defined(EZX_AP)
	data_start_ptr = (UINT8 *) util_hexasc_to_ui32(&data_ptr[0], ADDR_CMD_ADDR_SIZE);
	data_end_ptr   = (UINT8 *) util_hexasc_to_ui32(&data_ptr[ADDR_CMD_ADDR_SIZE + 1], ADDR_CMD_ADDR_SIZE);
#else
	blvar_RAM_section_addr_tbl.start_addr = util_hexasc_to_ui32(&data_ptr[0], ADDR_CMD_ADDR_SIZE);
	blvar_RAM_section_addr_tbl.end_addr   = util_hexasc_to_ui32(&data_ptr[ADDR_CMD_ADDR_SIZE + 1], ADDR_CMD_ADDR_SIZE);

	data_start_ptr = (UINT8 *) blvar_RAM_section_addr_tbl.start_addr;
	data_end_ptr   = (UINT8 *) blvar_RAM_section_addr_tbl.end_addr;
#endif
	while (data_start_ptr < data_end_ptr) {
		util_ui8_to_hexasc(*data_start_ptr, response_ptr);

		data_start_ptr++;
		response_ptr += 2;
#if !defined(EZX_AP)
		HAPI_WATCHDOG_service();
#endif
	}

	parser_send_packet((UINT8 *) rsrc_str, response);
}
