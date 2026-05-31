import os
import struct
import sys
import time

# High-performance GNU gettext .mo compiler in pure Python (0 dependencies)
# Formats catalog as a stream of binary structures:
# Magic: 0x950412de (little endian)
# Format: revision, num_strings, orig_table_offset, trans_table_offset, hash_table_size, hash_table_offset

def parse_po_stream(po_path, allow_empty=False):
    translations = {}
    if not os.path.exists(po_path):
        return translations
        
    with open(po_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    msgid = None
    msgstr = None
    in_msgid = False
    in_msgstr = False
    
    current_msgid_lines = []
    current_msgstr_lines = []
    
    def commit_entry():
        nonlocal msgid, msgstr
        if current_msgid_lines:
            mid = "".join(current_msgid_lines).replace('\\\\', '\\').replace('\\"', '"').replace('\\n', '\n')
            mstr = "".join(current_msgstr_lines).replace('\\\\', '\\').replace('\\"', '"').replace('\\n', '\n')
            if mid:
                if mstr or allow_empty:
                    translations[mid] = mstr
            current_msgid_lines.clear()
            current_msgstr_lines.clear()

    for line in lines:
        line = line.strip()
        if line.startswith('#') or not line:
            continue
            
        if line.startswith('msgid '):
            commit_entry()
            val = line[6:].strip().strip('"')
            current_msgid_lines.append(val)
            in_msgid = True
            in_msgstr = False
        elif line.startswith('msgstr '):
            val = line[7:].strip().strip('"')
            current_msgstr_lines.append(val)
            in_msgid = False
            in_msgstr = True
        elif line.startswith('"') and line.endswith('"'):
            val = line.strip().strip('"')
            if in_msgid:
                current_msgid_lines.append(val)
            elif in_msgstr:
                current_msgstr_lines.append(val)
                
    commit_entry()
    return translations

def make_mo(translations):
    # Sort keys for consistent output
    sorted_keys = sorted(translations.keys())
    num_strings = len(sorted_keys)
    
    orig_table = []
    trans_table = []
    
    # Pack metadata entry (empty string mapped to system metadata headers)
    # CDDA C++ gettext expects this to properly read encoding
    orig_table.append(b"")
    metadata = (
        b"Project-Id-Version: Medieval Mod 1.0\n"
        b"Content-Type: text/plain; charset=UTF-8\n"
        b"Content-Transfer-Encoding: 8bit\n"
        b"Language: zh_CN\n"
        b"Plural-Forms: nplurals=1; plural=0;\n"
    )
    trans_table.append(metadata)
    
    for k in sorted_keys:
        if k == "":
            continue
        orig_table.append(k.encode('utf-8'))
        trans_table.append(translations[k].encode('utf-8'))
        
    num_entries = len(orig_table)
    
    # Calculate binary block offsets
    # Header: magic (4), revision (4), num_strings (4), orig_offset (4), trans_offset (4), hash_size (4), hash_offset (4) = 28 bytes
    header_size = 28
    orig_table_offset = header_size
    trans_table_offset = orig_table_offset + (num_entries * 8)
    
    # String data starts after both index tables
    string_data_offset = trans_table_offset + (num_entries * 8)
    
    orig_indices = []
    trans_indices = []
    
    current_offset = string_data_offset
    
    # Build original strings table indices
    for s in orig_table:
        length = len(s)
        orig_indices.append((length, current_offset))
        current_offset += length + 1 # +1 for null terminator
        
    # Build translated strings table indices
    for s in trans_table:
        length = len(s)
        trans_indices.append((length, current_offset))
        current_offset += length + 1
        
    # Pack binary header
    # Magic for GNU .mo file: 0x950412de
    magic = 0x950412de
    revision = 0
    
    binary_data = bytearray()
    binary_data.extend(struct.pack("<IIIIIII", magic, revision, num_entries, orig_table_offset, trans_table_offset, 0, 0))
    
    # Write original index table
    for length, offset in orig_indices:
        binary_data.extend(struct.pack("<II", length, offset))
        
    # Write translated index table
    for length, offset in trans_indices:
        binary_data.extend(struct.pack("<II", length, offset))
        
    # Write original strings data
    for s in orig_table:
        binary_data.extend(s)
        binary_data.extend(b"\x00")
        
    # Write translated strings data
    for s in trans_table:
        binary_data.extend(s)
        binary_data.extend(b"\x00")
        
    return binary_data

def compile_po_to_mo(po_path, mo_path):
    print(f"Reading and parsing PO file: {po_path}...")
    start_time = time.time()
    translations = parse_po_stream(po_path)
    print(f"Parsed {len(translations)} translation entries in {time.time() - start_time:.2f} seconds.")
    
    if not translations:
        print("WARNING: No translations found. Skipping compiler pack.")
        return
        
    print(f"Compiling and packing into binary MO: {mo_path}...")
    binary_mo = make_mo(translations)
    
    # Check locks and write
    os.makedirs(os.path.dirname(mo_path), exist_ok=True)
    try:
        with open(mo_path, 'wb') as f:
            f.write(binary_mo)
        print(f"Success! Written {len(binary_mo)} bytes.")
        print("-" * 50)
    except PermissionError:
        print("\nERROR: Permission denied. Please close the running Cataclysm game first!")
        print("-" * 50)
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print("Usage: python compile_project_translations.py <po_file> <mo_file>")
        sys.exit(1)
    compile_po_to_mo(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
