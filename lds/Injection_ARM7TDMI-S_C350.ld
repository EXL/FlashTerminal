SECTIONS {
    .patch 0x11071B26 : {
        KEEP(*(.data*))
        KEEP(*(.text*))
        KEEP(*(.rodata*))
    }
}
