import os
import subprocess
import sys
import time

# Import helper functions from compile_project_translations
sys.path.append(os.path.dirname(__file__))
from compile_project_translations import parse_po_stream, compile_po_to_mo

def run_extractor(extractor_script, include_dir, output_pot):
    print("=" * 60)
    print("Step 1/3: Extracting translatable strings from Mod JSON...")
    print("=" * 60)
    
    cmd = [
        "python",
        extractor_script,
        "-i", include_dir,
        "-n", "Medieval Mod 1.0",
        "-o", output_pot
    ]
    
    print(f"Running extractor command: {' '.join(cmd)}")
    start_time = time.time()
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Extraction successful! Generated POT template: {output_pot}")
        print(f"Completed in {time.time() - start_time:.2f} seconds.")
    else:
        print("ERROR occurred during extraction:")
        print(result.stderr)
        sys.exit(1)
    print("-" * 50)

def merge_pot_into_po(pot_file, po_file):
    print("=" * 60)
    print("Step 2/3: Merging newly extracted strings into zh_CN.po...")
    print("=" * 60)
    
    new_translations = parse_po_stream(pot_file, allow_empty=True)
    print(f"Extracted {len(new_translations)} translatable keys from current JSONs.")
    
    existing_translations = {}
    if os.path.exists(po_file):
        existing_translations = parse_po_stream(po_file, allow_empty=True)
        print(f"Found {len(existing_translations)} existing translations in PO.")
    else:
        print("Creating a new zh_CN.po file...")
        
    merged_translations = {}
    new_keys_added = 0
    
    for msgid in new_translations:
        if msgid in existing_translations:
            merged_translations[msgid] = existing_translations[msgid]
        else:
            merged_translations[msgid] = ""
            new_keys_added += 1
            
    for msgid, msgstr in existing_translations.items():
        if msgid not in merged_translations:
            # Keep deleted strings or untracked strings as they are
            merged_translations[msgid] = msgstr
            
    # Ensure Mod directory exists
    os.makedirs(os.path.dirname(po_file), exist_ok=True)
    
    # Write back to PO file in standard GNU format
    with open(po_file, "w", encoding="utf-8") as f:
        f.write('msgid ""\nmsgstr ""\n')
        f.write('"Project-Id-Version: Medieval Mod 1.0\\n"\n')
        f.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
        f.write('"Content-Transfer-Encoding: 8bit\\n"\n')
        f.write('"Language: zh_CN\\n"\n')
        f.write('"Language-Team: Cataclysm-Medieval team\\n"\n')
        f.write('"Plural-Forms: nplurals=1; plural=0;\\n"\n\n')
        
        for msgid, msgstr in sorted(merged_translations.items()):
            msgid_esc = msgid.replace('\\', '\\\\').replace('"', '\\"')
            msgstr_esc = msgstr.replace('\\', '\\\\').replace('"', '\\"')
            
            f.write(f'msgid "{msgid_esc}"\n')
            f.write(f'msgstr "{msgstr_esc}"\n\n')
            
    print(f"Successfully merged. Total keys in PO: {len(merged_translations)} (Added {new_keys_added} new untranslated keys).")
    print("-" * 50)

def main():
    root_dir = r"e:\Cataclysm-Medieval"
    extractor_script = os.path.join(root_dir, "lang", "extract_json_strings.py")
    mod_dir = os.path.join(root_dir, "data", "mods", "Medieval")
    
    pot_file = os.path.join(mod_dir, "lang", "Medieval.pot")
    po_file = os.path.join(mod_dir, "lang", "po", "zh_CN.po")
    mo_file = os.path.join(mod_dir, "lang", "zh_CN", "LC_MESSAGES", "Medieval.mo")
    
    # Step 1: Run extractor to update POT template
    run_extractor(extractor_script, mod_dir, pot_file)
    
    # Step 2: Merge POT into PO (clean merge, no hardcoded translation dictionary)
    merge_pot_into_po(pot_file, po_file)
    
    # Step 3: Compile PO to MO
    print("=" * 60)
    print("Step 3/3: Compiling latest zh_CN.po into Medieval.mo...")
    print("=" * 60)
    if os.path.exists(po_file):
        compile_po_to_mo(po_file, mo_file)
        
    print("Clean Mod i18n compilation workflow completed successfully!")

if __name__ == "__main__":
    main()
