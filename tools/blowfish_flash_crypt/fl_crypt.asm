p586
                model flat
locals @@
CODE            segment para public 'CODE' use32

                public start
start           proc near
                push    0
                call    GetModuleHandleA
                mov     Our_Handle, eax

                mov     fname_buf, 0
                mov     fname_t_buf, 0
                mov     OFN_Flags, 80000h
                push    offset OpenFileNameSize
                call    GetOpenFileNameA
                cmp     eax, 0
                jz      @@exit

                push    -1
                push    0
                push    3 ; open existing
                push    0
                push    0
                push    0C0000000h
                push    offset fname_buf
                call    CreateFileA
                mov     FHandle, eax
                cmp     eax, -1
                jz      @@exit

                push    offset fsize_ex
                push    FHandle
                call    GetFileSize
                cmp     eax, 0
                jz      @@exit
                cmp     fsize_ex, 0
                jnz     @@exit
                mov     FSize, eax

                push    eax
                push    40h
                call    GlobalAlloc
                mov     MHandle, eax
                cmp     eax, 0
                jz      @@exit_fclose

                push    0
                push    offset file_readed
                push    FSize
                push    MHandle
                push    FHandle
                call    ReadFile
                cmp     eax, 0
                jz      @@exit_mclose

                push    FHandle
                call    CloseHandle

                mov     esi, MHandle
                mov     ecx, FSize
                shr     ecx, 3
@@loop:
                call    decrypt
                loop    @@loop

                mov     fname_buf, 0
                mov     fname_t_buf, 0
                mov     OFN_Flags, 0
                push    offset OpenFileNameSize
                call    GetSaveFileNameA
                cmp     eax, 0
                jnz     @@savename_ok

@@savename_ok:
                push    -1
                push    0
                push    1 ; Create new
                push    0
                push    0
                push    0C0000000h
                push    offset fname_buf
                call    CreateFileA
                mov     FHandle, eax
                cmp     eax,0
                jz      @@exit

                push    0
                push    offset file_readed
                push    FSize
                push    MHandle
                push    FHandle
                call    WriteFile

@@exit_mclose:
                push    MHandle
                call    GlobalFree
@@exit_fclose:
                push    FHandle
                call    CloseHandle
@@exit:
                push    0
                call    ExitProcess
start           endp

decrypt         proc near
                push    ecx
                push    edx
                push    ebx

                mov     ecx, dword ptr [esi]
                xchg    ch, cl
                rol     ecx, 10h
                xchg    ch, cl

                mov     edx, dword ptr [esi+4]
                xchg    dh, dl
                rol     edx, 10h
                xchg    dh, dl

                xor     edx,  0E229290Eh
                xor     ecx,  3D042139h
                xchg    ecx, edx

                mov     ebx, 0
@@loop:
                xchg    ecx, edx
                push    ecx
                push    edx

                mov     edx, ecx
                shr     edx, 18h
                and     edx, 0FFh
                mov     eax, dword ptr [Tbl1+edx*4]

                mov     edx, ecx
                and     edx,  00FF0000h
                shr     edx, 10h
                add     eax, dword ptr [Tbl2+edx*4]

                mov     edx, ecx
                and     edx,  0000FF00h
                shr     edx, 08h
                xor     eax, dword ptr [Tbl3+edx*4]

                and     ecx, 0FFh
                add     eax, dword ptr [Tbl4+ecx*4]

                pop     edx
                pop     ecx

                xor     edx, eax
                mov     eax, dword ptr [Key+ebx*4]
                xor     ecx, eax

                inc     ebx
                cmp     ebx, 10h
                jnz     @@loop


                xchg    dh, dl
                rol     edx, 10h
                xchg    dh, dl

                xchg    ch, cl
                rol     ecx, 10h
                xchg    ch, cl

                mov     [esi], ecx
                mov     [esi+4], edx
                add     esi, 8

                pop     ebx
                pop     edx
                pop     ecx
                retn
decrypt         endp



CODE            ends

DATA            segment para public 'DATA' use32
Our_Handle      dd 0
FHandle         dd 0
MHandle         dd 0
FSize           dd 0

align 16
Tbl1            dd  6A6B61B3h,0E9242B48h, 0236D969h, 83D0157Ch
                dd 0FBB94332h, 1E9F0B99h, 66AD0521h, 1BE66F69h
                dd  8761091Bh, 4CA93094h,0D4284076h, 80CACB69h
                dd  39BC2D1Fh,0DFCBFCADh, 13E27A57h,0ECD8DD48h
                dd  97A41322h, 40D2576Dh, 92A7A978h,0E535DBB9h
                dd  182E1368h,0BC0DD981h, 12028109h,0A835D8E6h
                dd  10DD5B84h,0C8BDD2F0h,0BA884D4Ah, 12966F22h
                dd  20267AC2h,0C0908F3Dh, 6B692B57h, 3E3DF0D9h
                dd  5BCF2BBCh, 2CEED386h,0FAD48BC7h, 44D66572h
                dd 0D0685EA1h,0BA519AA2h,0C6411A32h, 1775599Eh
                dd  1FE9B6A5h, 4B847064h,0F3347D2Dh,0C8A5438Eh
                dd 0FD1180BFh, 3594555Eh, 4CE7CF3Ch, 0F4B0CF1h
                dd  6B153B7Fh,0FFCE2BD7h, 4A38FEEFh, 37784B67h
                dd  3E7452ACh, 25F4032Fh, 6A74CED9h, 6A52FE03h
                dd 0C74911EDh, 505EE503h, 4E071DF6h, 2F3E3970h
                dd 0CC05CF6Bh,0D5C55411h, 60332FAAh, 2A6BF38Bh
                dd  244B220Dh,0E2912611h, 29EBC2FDh,0EFAF5EBCh
                dd 0B6CA2701h, 3F68D8C9h, 86174E48h, 2C64C049h
                dd 0BEE5B182h,0D6E9EE60h, 42E0D03Eh, 81DD8A7Dh
                dd  5C3DE099h,0A223B13Ah, 5E5161C1h, 16FBFA0Ah
                dd 0BCE5775Dh, 79ACB657h, 5718CCECh, 7BBC4807h
                dd  4A66B01Ah,0DDC6CC6Bh,0A379B3CDh, 81E3D9B7h
                dd  8E46F65Ah,0A3D5229Ah, 2A37BAC0h, 20D69327h
                dd 0C27576ECh, 794728A6h,0FC93F0FDh,0D364F421h
                dd  8CFCCD13h, 09C3DC5Fh, 9A0D9054h, 1B833D7Dh
                dd 0F4590BB9h, 9062F256h, 18E7D0ACh,0C56C4AC6h
                dd 0C141E5F9h,0A3438645h, 2C7E7F06h, 0C4595ABh
                dd  5A39E89Fh,0DEAE78D8h, 591F1DD9h,0A6189933h
                dd  16C8274Bh,0FB1971E9h,0FF1F5CFDh, 6C3EFDD9h
                dd  7BC158EDh, 4B18082Ah, 665BB226h, 4724116Ah
                dd 0E933B479h, 8A98A94Ch, 675A4CF7h,0DC827443h
                dd  4C8C1B5Eh,0DE976D82h,0C6F29CC5h, 34440E61h
                dd 0F5AAA404h, 738D632Dh,0A7BDB2D3h,0B50AF451h
                dd  231BEBD0h,0D3262F8Dh,0DC606C03h, 84D3A570h
                dd  16272644h,0FEBE000Bh, 5852D6CCh, 2B547211h
                dd 0D3355CFFh,0E20523CAh, 77570AE2h, 981A6A8Ch
                dd  51B148F3h,0C3902493h, 6E17E887h, 5ACFDDD1h
                dd  7A1C4CCCh, 1D20C100h,0F70BDB99h, 5C457119h
                dd 0CF350BBAh,0F604F2A7h,0C5A123A3h,0CA2A0D6Dh
                dd  29F04A01h,0A51666C9h,0DB32FD7Ch, 01C48A7Fh
                dd 0B3AB7728h, 472D0398h, 07E29F40h, 3403D0D0h
                dd  985287DAh, 95463C99h,0D88454B6h,0C30CC3D5h
                dd  74BCF91Fh, 22210C84h, 34D63146h,0F5854290h
                dd  9D5B952Fh,0B7502839h,0B8810430h,0EAFE0BBCh
                dd 0B77B5D86h, 894DD089h, 5A497611h, 38AC3702h
                dd  3CD67D54h,0A4BF2E65h, 7F4CF6D1h,0FD51843Bh
                dd  322F4BA6h,0DEB06389h, 7146D540h, 3009E25Ah
                dd  21154F38h,0EA9F4662h, 568591B2h, 31FAE017h
                dd 0DCAA66D8h, 062E788Bh, 0D0D6813h,0D8C9D934h
                dd 0DBF660B6h,0A4159ABBh,0BE92C536h, 2E3593A4h
                dd  4A18B6ADh, 0CEFD6D8h, 3E7C0055h, 18CF85C4h
                dd  45F0E42Eh, 10C9CCB8h,0B0AFDA71h, 7B9B851Bh
                dd 0D4903F12h, 47033DC4h, 43713333h,0B1388F16h
                dd  0293EF0Dh,0A627CEF9h,0D08152E5h,0F95C0299h
                dd  273EC4FCh, 8308365Ah, 5E6EE4C1h,0F6B9D091h
                dd  661B5222h, 3C7BEF1Eh,0E14900F5h, 161BA278h
                dd  362DC94Eh,0EF5519E8h,0F24EA02Dh,0A16CFE55h
                dd  4196C6BBh, 3ECCDAE1h, 5DB2951Dh,0ACEA541Bh
                dd  85090777h,0C6EF35EAh,0DF493CAAh, 9ED1B4D5h
                dd  3B3593EBh,0A19C06BAh,0A10A669Fh, 430E04F9h
                dd 0FFADAFC6h, 52069A66h,0FE7C47C6h, 92EF1AA5h
                dd 0A996C2CEh, 5201ACDBh,0E6FA02ADh, 4DF92BFFh
                dd  1555BC3Bh, 0E1CD985h, 05F3A45Dh, 308BD347h
                dd 0EBAFA77Dh, 33EF4126h,0E417F34Ch, 66683D35h
Tbl2            dd  4C7EC8AFh, 51794E22h,0A91FC31Dh, 8DE286B3h
                dd 0BFE45ADFh, 06866A04h, 6B37774Ch, 30C2F635h
                dd  2CD66FF8h, 6691593Ah, 8A47AF9Ch,0B7F8F97Eh
                dd  12D9DEB3h,0DEBA4BF2h, 998D64CFh,0BB54EB34h
                dd  585059ADh,0C1A9892Bh,0C28B5FBCh, 9821AE66h
                dd  0B570DC6h, 21E11978h, 11D46E7Dh, 73338A21h
                dd  09C8DEEDh,0DA335DE3h, 49724722h,0AFE17253h
                dd  43C56A10h,0E904AB2Dh,0CB20E601h,0CFF8FF58h
                dd  8CEB508Bh, 0173CCE4h, 7C4822E6h,0B67EAE89h
                dd  0804E504h,0E148672Ah, 7B32D18Fh, 14509255h
                dd  246E3E2Fh, 1CF6352Bh,0E1051ADEh,0CB3B0007h
                dd  3588ABBAh,0CD6CF0A2h,0C2901308h,0AB33D9E4h
                dd  12C2D8D6h, 765D4CFBh, 4E79223Eh,0F37D09B4h
                dd 0E25B76F7h, 1C8BFF94h, 196AD48Ch, 7060B663h
                dd 0A4AEF5B0h, 7C168FF1h, 4FAAD239h, 088B3103h
                dd  1E17AA1Fh, 39EF7715h, 8CF5BF58h, 06600F01h
                dd 0BAC8AA9Ch, 55DD638Ch,0DF23F813h, 8E7A4A13h
                dd  9E6F4392h, 19D95D41h, 33BABA7Dh,0C319C20Dh
                dd 0F8A13D58h, 3E7E3979h, 5072D120h,0DD5CA65Ch
                dd  6D78BBC8h, 4746FF9Fh, 7926B018h,0EBCDE285h
                dd  96EEBA7Eh,0FC06928Bh,0BEE80C6Bh, 8C832CC7h
                dd  8698D9E2h,0F7B53499h, 399E46D9h, 03CC9A65h
                dd  1CEA337Ch,0C9D9386Ah, 92413414h,0B45308EEh
                dd  48B76EB0h, 03218F24h, 80EC91B7h, 272DE625h
                dd  2A0672C5h, 3F4CA3F2h,0CFED2EFFh,0FC8C5E85h
                dd  1E841570h, 05A5DE26h, 78FB276Ah, 81C1508Bh
                dd  706FCA49h,0ABECBB94h, 696B0388h, 5E5A2661h
                dd  99BD32FFh, 3BDAA3C1h,0CE787A94h,0E2B0E6CEh
                dd  23BB8AF3h,0D57E813Ah, 41929F87h, 38369AA2h
                dd  5B8DC032h,0D9FEC57Ah,0AF02345Ch, 5BE9BA14h
                dd  55CE73A4h,0C920106Eh, 9D24B09Ch,0D6CB7DC0h
                dd  83A81232h, 2FF83CD1h, 2E50A3E9h, 27879D3Bh
                dd  4A751047h, 5AAC8F33h, 9AA868F8h,0BA847F81h
                dd 0E9F151E3h, 31D540E5h,0B4269035h, 4744C9DCh
                dd  53718BB6h, 11C3936Fh,0E4CECAFFh,0E15B3D84h
                dd  5E02CCBAh, 21615B4Ch, 9B405807h, 56517D6Dh
                dd  69E5FD06h,0BF6A5263h, 6A7302DFh, 15358E5Ah
                dd  9E16F199h, 43212704h,0F05C07CBh, 6C756F1Ah
                dd 0D612B97Dh, 8CBEC0D0h,0FF6C2F3Fh, 0A4A4A69h
                dd  81195A32h, 4415E86Dh, 9A02539Bh,0A760B798h
                dd  9F535FAEh, 1C294912h, 9220203Dh,0E9857CD4h
                dd  3F97AC43h, 9C140CD6h, 486BB839h, 93186520h
                dd  9BB4C996h, 7E34DD7Fh, 596D274Ch, 0F3EAA9Ch
                dd 0D72D3CB5h, 185FA4C5h,0D75F862Dh,0E28C0F05h
                dd  127DE36Dh, 5A756D80h,0F733BA7Ah, 30CD40C7h
                dd  749EFFF0h, 6FF65306h, 92961B6Eh, 0CBFF71Dh
                dd 0C69E355Fh,0D79F2358h, 74D40B21h, 235582E3h
                dd  7F3E0D50h,0BD74B89Ah, 59422448h,0B0A917DBh
                dd 0FD5B05FAh, 0B184D7Ch,0DB0EC07Eh,0B00C0935h
                dd  4E63A094h, 51190B9Eh,0F307AB59h,0C7CAF53Ah
                dd  654835A0h, 88049EF8h, 592D71AEh, 117E283Fh
                dd  96093544h,0BF36F7B3h,0C299B62Fh, 3F033094h
                dd  5C5B9980h,0A2A7466Eh, 8E5AABB7h, 9DEA8352h
                dd  624E633Fh, 4CEB8156h,0A3965F48h, 0BC33466h
                dd  2F3FDFBCh, 36892952h,0EC4D662Eh,0B9818A5Eh
                dd  01DD17DFh,0F2DB97FEh,0AF787727h,0F20A1AD9h
                dd 0F38BE8EBh,0D16A0331h, 13276B84h,0BD500319h
                dd  2D9FF8C2h,0A4361082h,0B686D711h, 31BBBEB8h
                dd 0DFE4BEBCh,0CDD539E2h,0B24FC4EAh, 5F9C54E3h
                dd 0A43A0664h,0DAADB4F8h, 32152634h, 736930FBh
                dd  999498FBh, 5E2F100Dh,0D5B12119h, 569DDCD9h
                dd 0D59D67B7h, 0D72864Bh, 259470BAh, 245A3FCBh
                dd  2F5869E9h, 81C73077h, 3676C62Fh, 9E9F6BA7h
                dd  6436BD76h, 649C9F99h, 641176C4h, 01071189h
Tbl3            dd 0EC6A014Fh,0F22D3F31h, 18110051h, 2164658Dh
                dd  54925A16h, 52E9A649h, 1B93004Eh, 120C1BDCh
                dd 0EAD6842Eh, 581F0031h,0B19DA2F3h, 38D74A9Eh
                dd  029AF580h,0AC782A65h, 7B2083BDh,0CDB9A2E7h
                dd  628FB07Dh,0CD28875Ch, 32A1D885h,0D9054BBAh
                dd  92B539BEh, 6CF165A9h, 46750F54h, 5B88BF33h
                dd  7580B7B8h,0E513564Bh, 9FAC35C2h,0C63E4071h
                dd 0DA4E1853h, 33714FE1h, 9B6DB000h, 74873521h
                dd  1A1369E8h,0C7AE12BDh, 77F18B90h, 3539EF45h
                dd  2794086Dh,0C48B1FE7h,0A38F5322h, 6E0BCDD5h
                dd  47576D20h, 831B9063h, 54B9B689h, 2A8D99B8h
                dd  542A407Dh, 7EC902ECh, 87E4BCDBh,0B27DE029h
                dd  9761ADF5h,0A24A06CFh, 3130D1F4h,0C4333A7Eh
                dd 0E19BB569h,0E39C0B8Eh,0AC2E9B08h,0E36A1062h
                dd  5674457Ah, 0FD86180h, 4C9D9A3Fh,0EB86584Bh
                dd  1A54048Dh, 9004CEAEh, 97E20B5Fh,0F7DCF7D4h
                dd  77E04FC4h, 6D68640Bh, 6DD485D6h, 7B3A37C2h
                dd 0FA8E3E94h, 122008B4h, 25C5416Eh,0F30693D1h
                dd  1436EE70h, 940470CCh,0F19C9954h, 604B1D5Fh
                dd  7581CF35h, 318CDEF5h, 52DD2ED7h,0B5900365h
                dd 0C0D52806h,0CE739EFCh, 02AE69BEh, 78737182h
                dd 0E941B654h, 7F016222h, 6CF942CCh,0E88E2D64h
                dd  74506C2Eh, 6DC74BD9h,0F6401039h, 9D7DDBD7h
                dd  2583F0A1h, 07E73759h,0C0C9209Ah, 8E8143B3h
                dd  6CBDA809h, 6913CF59h, 25015A66h, 33DF646Ch
                dd  397AC42Ah, 7C8689A4h, 6EB3774Bh,0CCE307DEh
                dd 0E11AE5CDh, 3A0E070Dh,0E898FBC8h, 1DE91770h
                dd  4279560Bh,0C8F1CB23h, 4FE416BDh, 0D4E7397h
                dd 0E2EC0E79h, 39F1FFC5h, 9768BA81h,0F2C49F3Dh
                dd  8D1020B0h,0D61D7360h,0F383EC99h, 6DC701DBh
                dd  54020210h, 65E6F362h,0D9CA803Ch, 465D8B8Fh
                dd 0B50D1A48h,0A3050C7Dh, 8018B485h,0C0F577D3h
                dd  9EE44795h, 6DB8AD9Fh, 1B9F124Ch,0FE8F4E7Dh
                dd  62D36DCFh, 10C53402h, 39B836E1h, 9372194Ah
                dd  887DD452h, 0B99D922h, 5D31EB6Dh,0C8696B2Bh
                dd 0FD6C86E2h, 707DA1D3h,0D934CCD3h,0AAE15A5Dh
                dd 0DBCA1104h, 7FA5546Dh, 5845E99Fh, 0A2E1BADh
                dd  59040F5Dh,0E5006696h,0C748D343h,0FA31AB34h
                dd  27E0110Ah,0EBFF8302h, 853F2549h,0A858FF0Fh
                dd  480516F6h, 2492B0B7h,0D339DFE0h, 687DD288h
                dd  7C166ED5h, 2C51A131h, 3427668Ah, 7741968Eh
                dd 0EA214B09h, 8E638CA6h, 3AA3BC16h,0CCFA9495h
                dd  6BCEAE28h, 0DC63DB6h,0BFFBC7F8h, 3F011379h
                dd  862B5658h,0C6E05CA5h,0FD5BBD00h, 3179B2F3h
                dd  4041DD67h, 06999B2Fh,0E1C3AB10h, 5A8D07ECh
                dd 0E2167CE7h,0BD684B79h, 57ACC201h, 7A251351h
                dd  282C26B0h,0C2223CFBh,0C3C7491Dh,0C7ACA675h
                dd 0DB717C86h, 347C2310h, 36FA5761h, 1CC83402h
                dd 0E9069B63h, 95EFC85Fh, 1A2E526Bh,0B294A4E4h
                dd 0D2DE3EF5h, 067E5C40h, 84098D48h,0AF399B0Ah
                dd  419025D3h, 0BC0963Bh,0D3F5A98Eh, 51E37B86h
                dd 0E0405A26h,0B5A19568h, 13A64E0Ch,0C2E3BAFBh
                dd 0C2C2B413h, 8C168F9Bh,0F218FCFDh, 8DD5BEBDh
                dd  01E26B90h,0BAEF4786h, 7C377DECh, 22924045h
                dd 0F3E483BAh,0BAC79695h,0BF3D5591h,0BCF58A47h
                dd  1CF7C58Dh, 7D0F6318h,0CF6BE401h,0A9B9DAF8h
                dd 0E43F3B14h,0F2230ED4h, 40AF20CDh, 26354163h
                dd 0B22E7E53h, 8BA324BFh, 5DA9D911h, 7BBB42C9h
                dd 0B8810475h, 9435AA9Ch, 98963037h, 51248744h
                dd  48987855h, 5BE205F6h, 72638182h, 6D9352D8h
                dd  721D7087h, 0CC8DDEFh, 11CBC95Ch,0F040C67Fh
                dd 0F045E64Ah,0A967F589h,0A59627B4h, 440F28A4h
                dd  5733F6BCh,0E011F52Ah,0DE2E4A66h, 8616B91Ch
                dd 0E80A41DFh, 126D7164h,0B2CA5B7Eh, 700FD146h
Tbl4            dd 0F6B2B1B7h,0A9F5486Dh, 9DD607CFh,0D0F6A186h
                dd  658E8D30h,0F21D2154h,0DB810926h, 1A07A2FBh
                dd  7CD6030Eh, 5C6CC3D2h, 40882716h, 7F1486B4h
                dd 0C16D5C16h,0ED815FACh, 3FA79F87h, 866291FDh
                dd 0ADE2BBEDh,0A1301B84h, 6F06B1E7h, 15F0E7E9h
                dd  2B6D2FE3h, 7B9D12B2h,0EE1CF4BFh,0D0E9DD5Fh
                dd 0D3C857D0h, 914DC172h, 55FE7FEAh, 6059B323h
                dd  9A073AA6h,0CE5F4136h, 9AD787C6h,0F520E2EDh
                dd  3025E09Ch, 063121A1h,0C8CCD3C2h,0D73F1800h
                dd  5A1C2684h, 928BCCC3h,0D1E98E6Dh, 61F67B6Fh
                dd 0E392C665h, 2D2683BCh, 8BDAF89Fh,0C0EDEA76h
                dd 0EC991EDCh,0CAE927DFh, 64291538h, 9018CA49h
                dd 0B3416F73h, 732FD8DFh, 33E875CCh,0AD4FE1C9h
                dd 0F94B28F4h, 6B70D3A8h, 057250B1h, 6CE3533Eh
                dd 0E5D22A0Dh,0E7132E00h,0A4B9234Ch, 9B815F61h
                dd  07E2575Dh,0E49BCE68h, 98A87892h, 3BB8EEAEh
                dd  4F21FA58h, 51794135h, 7E527ACCh,0BC972828h
                dd  05A07892h, 2FB0025Ah,0BCF23700h, 08B73A60h
                dd  849E5741h,0F67C412Ch,0AC0D611Dh, 020D7692h
                dd  4817FED2h, 8C7F2E90h, 4B26D900h, 9D753CE3h
                dd 0A9A6ACF1h, 12D68A91h, 062DEDF7h,0E626BE4Fh
                dd  4B1F801Ah,0B5CE5913h, 20BE8E77h, 76E99001h
                dd  7C275211h,0B46BAA76h, 2FED4B94h, 05EC8EF6h
                dd  44653645h, 9519AA5Fh,0F28AAA51h,0D36A3BE8h
                dd  7FD4518Bh, 8FD402E8h,0AE001EE1h,0A2FA4ACDh
                dd  70EDEF1Fh, 1E53DC68h, 042FDFE9h, 3197E29Bh
                dd  78740B62h,0B15D9BCDh, 54C02BB0h,0CA52172Ch
                dd  39DC1E2Bh, 342DC41Eh, 4273B42Dh,0A4BBADB0h
                dd 0E92D3CA5h, 4F9E7E7Eh,0C443FB36h, 11B935E1h
                dd  41FE373Ch, 29BA419Fh, 09FDCC74h,0A48D0D76h
                dd  54BF713Dh, 12B71BABh, 217560A5h,0D28EE18Eh
                dd 0C9D0F2C8h, 766A5F19h, 68BFBE1Dh, 5183F8DFh
                dd 0B0E05D2Dh,0D56CCC7Dh, 2B05A619h, 158A1208h
                dd 0E3292687h,0D0EF3620h, 70098E61h, 8CCB5759h
                dd  56E1E41Bh, 0191C278h, 34205974h, 29472C54h
                dd 0F8E54C59h, 3B74BF62h,0A76D8F89h, 1292C160h
                dd  34B42A6Fh,0E77827A2h,0F689D014h,0F4C6540Ah
                dd 0CCDD1450h, 212C5507h, 5B7631C4h, 71BC598Ch
                dd 0DCAB759Bh, 50DB681Bh, 5A33C24Eh, 065E2475h
                dd 0FAEDA9B7h, 6147DB18h, 3108D36Fh, 67EC027Dh
                dd  4C0014F0h, 47084A9Dh,0E23432D2h, 98F92F5Dh
                dd 0D3FC2168h, 8ADA67B9h, 81949F22h, 08468DA3h
                dd  6C04AB10h,0BFFEBE67h,0C0B4B36Bh, 5FECE3EBh
                dd 0E9F69C1Ah,0C036CD7Ah, 26D7B5F9h,0C77C728Eh
                dd 0C19E4B05h, 8D878B5Eh, 420E7C38h, 326A70ACh
                dd  1D78BB3Ah, 70B7ED6Fh, 25B96DD7h, 98DB4A50h
                dd  2AE954D3h,0E3C43719h,0C0D3F332h,0B9D48AC3h
                dd 0FB5A3441h, 15875287h, 24C58E8Fh, 6C8842ADh
                dd 0FE934F06h, 556CEE19h, 92D7DE4Ch,0FD08CC1Eh
                dd  1BF411A4h, 7C18BB96h,0DF162C51h,0B06B81DEh
                dd  47170D84h, 61DE4E2Ah, 9E517B2Dh,0F4724C80h
                dd 0E950666Ah,0D29EC532h, 9E14BA1Eh, 88413BADh
                dd  9E7159F6h,0F013D8AFh, 16A9AB52h, 55278231h
                dd 0AFB3BC6Ch, 04EC4CBEh, 8123FA68h, 5DE3D38Ah
                dd  96A4EBD9h, 4AC96CF9h, 53422331h,0D1CE5505h
                dd  2BB893CEh, 79E3E6E1h, 34106CFFh,0EA243577h
                dd 0B055AF90h, 02D26401h, 1B32FA60h, 59AE81CEh
                dd  238D877Fh, 982235C9h,0B5AB1263h,0A1FFB9CCh
                dd  7249DDADh,0ADEF209Bh,0A7A2C467h, 6EA5E18Eh
                dd 0A2757EBDh, 62D1192Dh,0F4E2440Ah, 2F6BCD3Ch
                dd  3EB3A6C3h, 4A50D44Dh,0F2C1DEE0h, 0CC3DB70h
                dd  0BDD0D43h,0B1E370FBh, 5D83AAE3h,0A442728Bh
                dd  31DD25E7h,0E098EF46h, 16028EB4h,0C4D6F799h
                dd 0D4232DC3h,0BAD1E3A5h, 6F14503Ah, 6F0525E7h

Key             dd  402D8CC9h,0C4CE9D6Dh, 62D546DAh, 3BD92E2Ch
                dd  3EDBB819h, 184DFEF0h, 2D9F66E0h, 7F7FD518h
                dd 0C54E1F0Ch, 0C296024h, 0D2E767ADh, 6CB3265Dh
                dd 0E484C60Ch, 522ACDC3h, 61C16CAAh, 63F1738Fh

OpenFileNameSize  dd 4Ch ;    DWORD         lStructSize;
                  dd 0   ;    HWND          hwndOwner;
                  dd 0   ;    HINSTANCE     hInstance;
ofn_filter        dd offset str_ofn_filter   ;    LPCTSTR       lpstrFilter;
                  dd 0   ;    LPTSTR        lpstrCustomFilter;
                  dd 0   ;    DWORD         nMaxCustFilter;
                  dd 0   ;    DWORD         nFilterIndex;
                  dd offset fname_buf       ;    LPTSTR        lpstrFile;
                  dd 1FFh                   ;    DWORD         nMaxFile;
                  dd offset fname_t_buf     ;    LPTSTR        lpstrFileTitle;
                  dd 1FFh                   ;    DWORD         nMaxFileTitle;
                  dd 0   ;    LPCTSTR       lpstrInitialDir;
                  dd 0   ;    LPCTSTR       lpstrTitle;
OFN_Flags         dd 0   ;    DWORD         Flags;
                  dd 0
                         ;    WORD          nFileOffset;
                         ;    WORD          nFileExtension;
                  dd 0   ;    LPCTSTR       lpstrDefExt;
                  dd 0   ;    DWORD         lCustData;
                  dd 0   ;    LPOFNHOOKPROC lpfnHook;
                  dd 0   ;    LPCTSTR       lpTemplateName;

fsize_ex        dd 0
file_readed     dd 0
str_ofn_filter  db 'All files', 0
                db '*.*', 0, 0
align 4
fname_buf       db 200h dup (?)
fname_t_buf     db 200h dup (?)

DATA            ends

include externs.inc
                end start
