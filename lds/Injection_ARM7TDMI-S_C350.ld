ENTRY(handle_command_RQRC)
SECTIONS
{
	. = 0x11071B26;
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
