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

#if defined(M_CORE_MOTOROLA_A830_SIEMENS_U10)
#define rsrc_str ((UINT8 *) 0x078064CB)
#define blvar_RAM_section_addr_tbl (*(BLOADER_SECTION_ADDR_TBL *) 0x0782AD7C)

#define HAPI_WATCHDOG_service ((void (*)(void)) (0x07803136))
#define parser_send_packet ((void (*)(UINT8 *, UINT8 *)) (0x07800A7A))
#define util_ui8_to_hexasc ((void (*)(UINT8, UINT8 *)) (0x078006C8))
#define util_hexasc_to_ui32 ((UINT32 (*)(UINT8 *, UINT8)) (0x078006A0))
#elif defined(M_CORE_MOTOROLA_V60_0355)
#define rsrc_str ((UINT8 *) 0x1101DA1F)
#define blvar_RAM_section_addr_tbl (*(BLOADER_SECTION_ADDR_TBL *) 0x11025AA0)

#define HAPI_WATCHDOG_service ((void (*)(void)) (0x1101CB02))
#define parser_send_packet ((void (*)(UINT8 *, UINT8 *)) (0x11010B06))
#define util_ui8_to_hexasc ((void (*)(UINT8, UINT8 *)) (0x11012244))
#define util_hexasc_to_ui32 ((UINT32 (*)(UINT8 *, UINT8)) (0x1101221C))
#elif defined(M_CORE_MOTOROLA_V60_0371)
#define rsrc_str ((UINT8 *) 0x00104A8D)
#define blvar_RAM_section_addr_tbl (*(BLOADER_SECTION_ADDR_TBL *) 0x11040068)

#define HAPI_WATCHDOG_service ((void (*)(void)) (0x0010000A))
#define parser_send_packet ((void (*)(UINT8 *, UINT8 *)) (0x001014BA))
#define util_ui8_to_hexasc ((void (*)(UINT8, UINT8 *)) (0x00103FA8))
#define util_hexasc_to_ui32 ((UINT32 (*)(UINT8 *, UINT8)) (0x00103F80))
#elif defined(M_CORE_MOTOROLA_V66I_1001)
#define rsrc_str ((UINT8 *) 0x00104BE9)
#define blvar_RAM_section_addr_tbl (*(BLOADER_SECTION_ADDR_TBL *) 0x11040068)

#define HAPI_WATCHDOG_service ((void (*)(void)) (0x0010000A))
#define parser_send_packet ((void (*)(UINT8 *, UINT8 *)) (0x001014C8))
#define util_ui8_to_hexasc ((void (*)(UINT8, UINT8 *)) (0x0010401C))
#define util_hexasc_to_ui32 ((UINT32 (*)(UINT8 *, UINT8)) (0x00103FF4))
#elif defined(M_CORE_MOTOROLA_V66I_1001_2)
#define rsrc_str ((UINT8 *) 0x110217F5)
#define blvar_RAM_section_addr_tbl (*(BLOADER_SECTION_ADDR_TBL *) 0x11040068)

#define HAPI_WATCHDOG_service ((void (*)(void)) (0x1101CC16))
#define parser_send_packet ((void (*)(UINT8 *, UINT8 *)) (0x1101E0D4))
#define util_ui8_to_hexasc ((void (*)(UINT8, UINT8 *)) (0x11020C28))
#define util_hexasc_to_ui32 ((UINT32 (*)(UINT8 *, UINT8)) (0x11020C00))
#elif defined(ARM7TDMI_MOTOROLA_C350)
#define rsrc_str ((UINT8 *) 0x01FD2E25)
#define blvar_RAM_section_addr_tbl (*(BLOADER_SECTION_ADDR_TBL *) 0x01FD691C)

#define HAPI_WATCHDOG_service ((void (*)(void)) (0x11071418))
#define parser_send_packet ((void (*)(UINT8 *, UINT8 *)) (0x11070568))
#define util_ui8_to_hexasc ((void (*)(UINT8, UINT8 *)) (0x11072038))
#define util_hexasc_to_ui32 ((UINT32 (*)(UINT8 *, UINT8)) (0x11072008))
#else
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

	blvar_RAM_section_addr_tbl.start_addr = util_hexasc_to_ui32(&data_ptr[0], ADDR_CMD_ADDR_SIZE);
	blvar_RAM_section_addr_tbl.end_addr   = util_hexasc_to_ui32(&data_ptr[ADDR_CMD_ADDR_SIZE + 1], ADDR_CMD_ADDR_SIZE);

	data_start_ptr = (UINT8 *) blvar_RAM_section_addr_tbl.start_addr;
	data_end_ptr   = (UINT8 *) blvar_RAM_section_addr_tbl.end_addr;

	while (data_start_ptr < data_end_ptr) {
		util_ui8_to_hexasc(*data_start_ptr, response_ptr);

		data_start_ptr++;
		response_ptr += 2;

		HAPI_WATCHDOG_service();
	}

	parser_send_packet((UINT8 *) rsrc_str, response);
}
