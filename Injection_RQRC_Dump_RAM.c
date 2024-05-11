#if 0
 /opt/arm/bin/tcc -apcs /interwork -O2 inject.c -c inject.o
 /opt/arm/bin/armlink -ro-base 0x0013B430 inject.o inject.sym -o inject.elf
 /opt/arm/bin/fromelf inject.elf -bin -output inject.bin
#endif

#define ADDR_CMD_ADDR_SIZE              8
#define MAX_RESPONSE_DATA_SIZE         95

typedef unsigned char UINT8;
typedef unsigned short UINT16;
typedef unsigned int UINT32;

typedef struct {
	UINT32    start_addr;
	UINT32    end_addr;
} BLOADER_SECTION_ADDR_TBL;

extern BLOADER_SECTION_ADDR_TBL blvar_RAM_section_addr_tbl;
extern UINT8 rsrc_str[];
extern UINT32 util_hexasc_to_ui32(UINT8 *str_ptr, UINT8 size);
extern void util_ui8_to_hexasc(UINT8 val, UINT8 *str_ptr);
extern void parser_send_packet(UINT8 *command_ptr, UINT8 *data_ptr);
void HAPI_WATCHDOG_service(void);

void handle_command_RQRC(UINT8 *data_ptr) {
	UINT8 response[MAX_RESPONSE_DATA_SIZE];
	UINT8 *response_ptr = &response[0];
	UINT8 *data_start_ptr, *data_end_ptr;
	UINT8 i;

	for (i = 0; i < MAX_RESPONSE_DATA_SIZE; ++i)
		response[i] = '\0';

	blvar_RAM_section_addr_tbl.start_addr = util_hexasc_to_ui32(&data_ptr[0], ADDR_CMD_ADDR_SIZE);
	blvar_RAM_section_addr_tbl.end_addr = util_hexasc_to_ui32(&data_ptr[ADDR_CMD_ADDR_SIZE + 1], ADDR_CMD_ADDR_SIZE);

	data_start_ptr = (UINT8 *) blvar_RAM_section_addr_tbl.start_addr;
	data_end_ptr = (UINT8 *) blvar_RAM_section_addr_tbl.end_addr;

	while (data_start_ptr < data_end_ptr) {
		util_ui8_to_hexasc(*data_start_ptr, response_ptr);

		data_start_ptr++;
		response_ptr += 2;

		HAPI_WATCHDOG_service();
	}

	parser_send_packet((UINT8 *)&rsrc_str[0], response);
}
