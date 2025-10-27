#define MAX_RESPONSE_DATA_SIZE        (95)
#define BYTES_STEP                  (0x10)

typedef unsigned char               UINT8;
typedef unsigned short             UINT16;
typedef unsigned int               UINT32;

#if !defined(START_ADDR)
#error "Address 'START_ADDR' must be defined like '-DSTART_ADDR=0x00000000' in the build script!"
#endif

#if !defined(NULLED_4BYTES_ADDR)
#error "Address 'NULLED_4BYTES_ADDR' must be defined like '-DNULLED_4BYTES_ADDR=0x03FD5034' in the build script!"
#endif

#define nulled_4bytes_addr_in_ram_rw ((UINT32 *) NULLED_4BYTES_ADDR)

extern void parser_send_packet(UINT8 *command_ptr, UINT8 *data_ptr);

static void util_ui8_to_hexasc(UINT8 val, UINT8 *str_ptr);

extern void handle_command_RQHW(UINT8 *data_ptr) {
	UINT8 response[MAX_RESPONSE_DATA_SIZE];
	UINT8 *response_ptr = &response[0];
	UINT8 *data_start_ptr, *data_end_ptr;

	UINT32 start_addr = (START_ADDR);

	data_start_ptr = (UINT8 *) (start_addr + (*nulled_4bytes_addr_in_ram_rw));
	data_end_ptr   = (UINT8 *) (data_start_ptr + BYTES_STEP);

	while (data_start_ptr < data_end_ptr) {
		util_ui8_to_hexasc(*data_start_ptr, response_ptr);

		data_start_ptr++;
		response_ptr += 2;
	}

	*nulled_4bytes_addr_in_ram_rw += BYTES_STEP;

	parser_send_packet((UINT8 *) "RSHW", response);
}

static void util_ui8_to_hexasc(UINT8 val,UINT8 *str_ptr) {
	UINT8 i, digit;

	for (i = 0; i < 2; ++i) {
		digit = (val >> 4) & 0x0F;
		val <<= 4;
		*str_ptr++ = (digit > 9) ? (digit + '7') : (digit + '0');
	}

	*str_ptr = '\0';
}
