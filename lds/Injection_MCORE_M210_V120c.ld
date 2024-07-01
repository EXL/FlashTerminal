OUTPUT_FORMAT(binary)
ENTRY(handle_command_RQRC)
SECTIONS
{
	. = 0x41008040;
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
