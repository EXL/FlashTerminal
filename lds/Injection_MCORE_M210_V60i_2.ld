OUTPUT_FORMAT(binary)
ENTRY(handle_command_RQRC)
SECTIONS
{
	. = 0x11019A10;
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
