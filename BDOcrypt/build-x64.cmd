@mkdir obj\x64 2>nul
x86_64-w64-mingw32-g++.exe -O3 -c BDO_encrypt.cpp -o obj/x64/BDO_encrypt.o -Iheader -lz
x86_64-w64-mingw32-g++.exe -O3 -c BDO_decrypt.cpp -o obj/x64/BDO_decrypt.o -Iheader -lz
@mkdir bin\x64 2>nul
x86_64-w64-mingw32-g++.exe -o bin/x64/BDO_encrypt.exe obj/x64/BDO_encrypt.o -s -static -Iheader -lz
x86_64-w64-mingw32-g++.exe -o bin/x64/BDO_decrypt.exe obj/x64/BDO_decrypt.o -s -static -Iheader -lz
