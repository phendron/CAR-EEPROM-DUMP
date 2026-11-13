#!/bin/python3

import struct

with open("st93c56.bin", "rb") as f:
    data = f.read()

print(data)
# Generate a 16-bit byte-swapped copy of the dump
raw_bytes = data

def parse_vdo_93c56(data: bytes) -> None:
  if len(data) != 256:
    print(f"[!] Warning: Expected 256 bytes, got {len(data)} bytes.\n")

  def to_ascii(chunk: bytes) -> str:
    return "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)

  # Decode odometer words at 0xAB-0xB0 (inverted 16-bit big-endian * 16 km)
  odo_words = [
      struct.unpack(">H", data[0xAB:0xAD])[0] ^ 0xFFFF,
      struct.unpack(">H", data[0xAD:0xAF])[0] ^ 0xFFFF,
      struct.unpack(">H", data[0xAF:0xB1])[0] ^ 0xFFFF,
  ]
  km_est = max(odo_words) * 16
  miles_est = round(km_est * 0.621371)

  blocks = [
      (0x00, 0x05, "Code Index / Calibration ID", f"'{to_ascii(data[0x00:0x05])}'"),
      (0x05, 0x0E, "Header Padding", "Zero-fill reserved"),
      (0x0E, 0x10, "Header Checksum", data[0x0E:0x10].hex(" ").upper()),
      (0x10, 0x4C, "Gauge Calibration Tables", "Speedo / Tacho / Fuel / Temp stepper curves"),
      (0x4C, 0x76, "Variant & Chime Flags", "ABS / TC / Gearbox / Buzzer config"),
      (0x76, 0x88, "Config Checksum & Flags", data[0x76:0x88].hex(" ").upper()),
      (0x88, 0xAA, "Unused EEPROM Space", "Erased 0xFF region"),
      (0xAA, 0xC8, "Odometer Rolling Block", f"Decoded ~{km_est:,} km ({miles_est:,} mi)"),
      (0xC8, 0xCE, "Sync / Calibration Header", data[0xC8:0xCE].hex(" ").upper()),
      (0xCE, 0xD2, "4-Digit ASCII Code / PIN", f"'{to_ascii(data[0xCE:0xD2])}' (PIN on Corsa C; Serial on Astra G)"),
      (0xD2, 0xD8, "Lock / Status Bytes", f"{data[0xD2:0xD4].hex(' ').upper()} (0x8020 = Unlocked)"),
      (0xD8, 0xDF, "Redundant Checksum Pair", f"{data[0xD8:0xDB].hex(' ')} / {data[0xDC:0xDF].hex(' ')}"),
      (0xDF, 0xE4, "Country / Market Code", f"'{to_ascii(data[0xDF:0xE4]).strip()}' (UK / MPH)"),
      (0xE4, 0xEC, "EEPROM Format Version", data[0xE4:0xEC].hex(" ").upper()),
      (0xEC, 0xF2, "Hardware Build Variant", f"'{to_ascii(data[0xEC:0xF2]).strip()}'"),
      (0xF2, 0xF8, "Service (InSP) Interval", data[0xF2:0xF8].hex(" ").upper()),
      (0xF8, 0xFE, "Programming Counter", data[0xF8:0xFE].hex(" ").upper()),
      (0xFE, 0x100, "End-of-File Checksum", data[0xFE:0x100].hex(" ").upper()),
  ]

  print("=" * 84)
  print(f"{'OFFSET':<11} | {'SECTION NAME':<27} | {'DECODED VALUE / NOTES'}")
  print("=" * 84)
  for start, end, name, desc in blocks:
    print(f"0x{start:02X}-0x{end-1:02X}   | {name:<27} | {desc}")
  print("=" * 84)


if __name__ == "__main__":
  #raw_bytes = bytes.fromhex(HEX_DUMP)
  # To load from a file instead, uncomment the two lines below:
  # with open("dump.bin", "rb") as f:
  #     raw_bytes = f.read()
    parse_vdo_93c56(raw_bytes)

