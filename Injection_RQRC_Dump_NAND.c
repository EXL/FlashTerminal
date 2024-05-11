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
typedef long long INT64;

typedef struct {
	UINT32    start_addr;
	UINT32    end_addr;
} BLOADER_SECTION_ADDR_TBL;

extern BLOADER_SECTION_ADDR_TBL blvar_RAM_section_addr_tbl;
extern UINT8 rsrc_str[];
extern UINT32 nand_ctrl;
extern UINT32 util_hexasc_to_ui32(UINT8 *str_ptr, UINT8 size);
extern void util_ui8_to_hexasc(UINT8 val, UINT8 *str_ptr);
extern void parser_send_packet(UINT8 *command_ptr, UINT8 *data_ptr);
extern void HAPI_WATCHDOG_service(void);
extern int sub_107B3E(UINT8 *b, unsigned int a2, int a3, int a4);
extern int sub_107678(int a1, int a2, int a3, int a4);
extern UINT32 sub_10787C(unsigned int a1);
extern int sub_121A78(void);
extern INT64 sub_121ADC(void);

void handle_command_RQRC(UINT8 *data_ptr) {
	UINT8 response[MAX_RESPONSE_DATA_SIZE];
	UINT8 *response_ptr = &response[0];
	UINT8 *data_start_ptr, *data_end_ptr;
	UINT8 i;
	UINT32 addr = 0;
	UINT32 page;
	int res = 0;
	UINT8 *v;

	for (i = 0; i < MAX_RESPONSE_DATA_SIZE; ++i)
		response[i] = '\0';

	blvar_RAM_section_addr_tbl.start_addr = util_hexasc_to_ui32(&data_ptr[0], ADDR_CMD_ADDR_SIZE);
	blvar_RAM_section_addr_tbl.end_addr = util_hexasc_to_ui32(&data_ptr[ADDR_CMD_ADDR_SIZE + 1], ADDR_CMD_ADDR_SIZE);
	page = util_hexasc_to_ui32(&data_ptr[ADDR_CMD_ADDR_SIZE + 1 + ADDR_CMD_ADDR_SIZE + 1], ADDR_CMD_ADDR_SIZE);

	data_start_ptr = (UINT8 *) blvar_RAM_section_addr_tbl.start_addr;
	data_end_ptr = (UINT8 *) blvar_RAM_section_addr_tbl.end_addr;

//	addr = sub_107B3E((UINT8 *) 0x0125F6DC, 0xB, 0x200, 0x100);
//00000000:  02 52 53 52 43 1E 30 30 30 30 30 30 30 30 45 45  |.RSRC.00000000EE|
//00000010:  36 32 37 36 44 31 32 46 33 45 36 35 38 39 33 43  |6276D12F3E65893C|
//00000020:  45 36 32 36 35 31 37 46 39 45 43 35 32 38 39 43  |E626517F9EC5289C|
//00000030:  30 36 44 43 42 30 38 35 39 32 36 36 32 35 33 46  |06DCB0859266253F|
//00000040:  46 45 34 35 34 39 31 43 37 41 34 35 43 44 31 43  |FE45491C7A45CD1C|
//00000050:  03                                               |.               |
//	addr = sub_107678(1000, 512, 6, 4);
//	addr = sub_10787C(0xA);

	*((UINT32 *) 0x84000174) = 0;
	*((UINT32 *) 0x84000178) = 0x7e;
	*((UINT32 *) 0x8400017c) = 0x1fff;
	*((UINT32 *) 0x84000180) = 0;

	*((UINT32 *) 0x28000000) = 101;
	*((UINT32 *) 0x800002B0) = 2;
	*((UINT32 *) 0x60000304) = page << 9;

	sub_121A78();
	sub_121A78();

	*((UINT32 *) 0x60000300) = 1;
	sub_121ADC();
	sub_121A78();

	*((UINT32 *) 0x60000300) = 7;

//	v = (UINT8 *) &addr;
//	util_ui8_to_hexasc(*v, response_ptr); v++; response_ptr += 2;
//	util_ui8_to_hexasc(*v, response_ptr); v++; response_ptr += 2;
//	util_ui8_to_hexasc(*v, response_ptr); v++; response_ptr += 2;
//	util_ui8_to_hexasc(*v, response_ptr); v++; response_ptr += 2;

//	util_ui8_to_hexasc(0xEE, response_ptr); v++; response_ptr += 2;

	while (data_start_ptr < data_end_ptr) {
		util_ui8_to_hexasc(*data_start_ptr, response_ptr);

		data_start_ptr++;
		response_ptr += 2;

		HAPI_WATCHDOG_service();
	}

	// sub_107678
	// sub_10787C
	// sub_107B3E
	// sub_107C22
	// sub_12363C
	// sub_121F4A
	parser_send_packet((UINT8 *)&rsrc_str[0], response);
}
