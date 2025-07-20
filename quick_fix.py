#!/usr/bin/env python3
import re

# Read the file
with open('security_wifi_game.py', 'r') as f:
    content = f.read()

# Fix common syntax issues
fixes = [
    (r'^(\s*)f self\.packet_capture_thread and self\.packet_capture_thread\.is.*$', r'\1if self.packet_capture_thread and self.packet_capture_thread.is_alive():'),
    (r'check=True, capture_output=True\)\)', 'check=True, capture_output=True)'),
    (r'subprocess\.run\(\[([^\]]+)\]\s*\)', r'subprocess.run([\1], check=True, capture_output=True)')
]

for pattern, replacement in fixes:
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

# Write back
with open('security_wifi_game.py', 'w') as f:
    f.write(content)

print("Fixed syntax errors!")
