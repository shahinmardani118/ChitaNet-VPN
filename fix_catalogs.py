from pathlib import Path
for path in Path('.').rglob('package.json'):
    if 'node_modules' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    if 'catalog:' in text:
        path.write_text(text.replace('catalog:', 'latest'), encoding='utf-8')
