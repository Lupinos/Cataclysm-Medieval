import os

def find_empty_keys():
    po_file = r"e:\Cataclysm-Medieval\data\mods\Medieval\lang\po\zh_CN.po"
    if not os.path.exists(po_file):
        print("PO file does not exist")
        return
        
    with open(po_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Simple parse
    entries = content.split("\n\n")
    empty_entries = []
    
    for entry in entries:
        lines = entry.strip().split("\n")
        msgid = None
        msgstr = None
        
        for line in lines:
            if line.startswith("msgid "):
                msgid = line[6:].strip().strip('"')
            elif line.startswith("msgstr "):
                msgstr = line[7:].strip().strip('"')
                
        if msgid and msgstr == "" and msgid != "":
            empty_entries.append(msgid)
            
    import json
    print(f"Found {len(empty_entries)} empty keys. Writing to empty_keys.json...")
    with open("empty_keys.json", "w", encoding="utf-8") as out:
        json.dump(empty_entries, out, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    find_empty_keys()
