OUTPUT_FORMAT(binary)
ENTRY(handle_command_RQRC)
SECTIONS
{
	. = 0x11010040;
	.text :
	{
		*(.text)
	}
	.data :
	{
		*(.data)
		*(.rodata)
	}
}
