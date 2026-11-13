## HOW TO READ ROM DUMP

```
./carinfo.py
```
**output:

```
====================================================================================
OFFSET      | SECTION NAME                | DECODED VALUE / NOTES
====================================================================================
0x00-0x04   | Code Index / Calibration ID | '00703'
0x05-0x0D   | Header Padding              | Zero-fill reserved
0x0E-0x0F   | Header Checksum             | CE 89
0x10-0x4B   | Gauge Calibration Tables    | Speedo / Tacho / Fuel / Temp stepper curves
0x4C-0x75   | Variant & Chime Flags       | ABS / TC / Gearbox / Buzzer config
0x76-0x87   | Config Checksum & Flags     | 0C 00 C1 11 00 80 00 00 00 11 10 1E 11 11 11 11 11 11
0x88-0xA9   | Unused EEPROM Space         | Erased 0xFF region
0xAA-0xC7   | Odometer Rolling Block      | Decoded ~1,044,944 km (649,298 mi)
0xC8-0xCD   | Sync / Calibration Header   | 00 FF 82 A0 17 A7
0xCE-0xD1   | 4-Digit ASCII Code / PIN    | '6593' (PIN on Corsa C; Serial on Astra G)
0xD2-0xD7   | Lock / Status Bytes         | 80 20 (0x8020 = Unlocked)
0xD8-0xDE   | Redundant Checksum Pair     | ca 97 47 / ca 97 47
0xDF-0xE3   | Country / Market Code       | 'BR  .' (UK / MPH)
0xE4-0xEB   | EEPROM Format Version       | 63 57 3C 00 00 00 00 00
0xEC-0xF1   | Hardware Build Variant      | 'D201'
0xF2-0xF7   | Service (InSP) Interval     | 00 00 BB BB BB CC
0xF8-0xFD   | Programming Counter         | 00 01 00 00 00 00
0xFE-0xFF   | End-of-File Checksum        | 7C A3
================================================================================
```
