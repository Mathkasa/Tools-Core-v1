import os
root = r'C:\Users\mathy\Downloads\Tools Core-main\Tools Core-main'
repls = [
    ('https://github.com/Mathkasa', 'https://github.com/Mathkasa'),
    ('https://github.com/Mathkasa', 'https://github.com/Mathkasa'),
    ('Mathkasa', 'Mathkasa'),
    ('tools-core', 'tools-core'),
    ('Tools Core', 'Tools Core'),
    ('tools-core', 'tools-core'),
    ('TOOLS CORE', 'TOOLS CORE'),
    ('TOOLS CORE', 'TOOLS CORE'),
    ('tools-core v1.0', 'Tools Core v1.0'),
    ('tools-core', 'tools-core'),
    ('TOOLS CORE', 'TOOLS CORE'),
]
path_repls = [
    ('\\ToolsCore\\', '\\ToolsCore\\'),
    ('\"Void\"', '"ToolsCore"'),
    ("'ToolsCore'", "'ToolsCore'"),
    ('os.path.join(path, "ToolsCore",', 'os.path.join(path, "ToolsCore",'),
    ('path, "ToolsCore",', 'path, "ToolsCore",'),
    ('\\ToolsCore\\', '\\ToolsCore\\'),
]
for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames:
        if not fn.lower().endswith(('.py','.bat','.md','.js','.json','.txt')):
            continue
        if fn == 'error_log.txt':
            continue
        fnp = os.path.join(dirpath, fn)
        try:
            with open(fnp, 'r', encoding='utf-8') as f:
                data = f.read()
        except UnicodeDecodeError:
            continue
        orig = data
        for a, b in repls:
            data = data.replace(a, b)
        for a, b in path_repls:
            data = data.replace(a, b)
        if fn == 'start.bat':
            data = data.replace('title TOOLS CORE v1.0', 'title TOOLS CORE v1.0')
            data = data.replace('title tools-core v1.0', 'title TOOLS CORE v1.0')
            data = data.replace('python Void\\main.py', 'python ToolsCore\\main.py')
        if fn == 'setup.bat':
            data = data.replace('title Void Tool Setup', 'title Tools Core Setup')
            data = data.replace('cd Void\\bot', 'cd ToolsCore\\bot')
        if fn == 'python_installer.bat':
            data = data.replace('title Tools Core Setup', 'title Tools Core Setup')
            data = data.replace('TOOLS CORES SETUP', 'TOOLS CORE SETUP')
        if fn == 'package.json':
            data = data.replace('"name": "tools-core"', '"name": "tools-core"')
        if data != orig:
            with open(fnp, 'w', encoding='utf-8') as f:
                f.write(data)
            print('updated', fnp)
print('done')
