#!/usr/bin/env python3
"""
Arabic Code Auditor Pro - Code Obfuscation
"""
import os
import base64
import zlib
import marshal

def obfuscate_file(input_file: str, output_file: str):
    with open(input_file, 'rb') as f:
        code = compile(f.read(), input_file, 'exec')

    marshaled = marshal.dumps(code)
    compressed = zlib.compress(marshaled, level=9)
    encoded = base64.b64encode(compressed).decode()

    loader = "import base64, zlib, marshal\n"
    loader += "_code = compile(\"\"\"\n"
    loader += "import base64, zlib, marshal\n"
    loader += "exec(marshal.loads(zlib.decompress(base64.b64decode('" + encoded + "'))))\n"
    loader += "\"\"\", '<protected>', 'exec')\n"
    loader += "exec(_code)\n"

    with open(output_file, 'w') as f:
        f.write(loader)

    print("Obfuscated: " + input_file + " -> " + output_file)

def obfuscate_core():
    core_dir = 'src/core'
    protected_dir = 'src/core_protected'
    os.makedirs(protected_dir, exist_ok=True)

    files = [
        'license_manager.py',
        'analyzer_engine.py',
        'security_engine.py',
        'ai_engine.py',
        'fixer_engine.py',
        'report_engine.py',
        'plugin_engine.py',
    ]

    for filename in files:
        input_path = os.path.join(core_dir, filename)
        output_path = os.path.join(protected_dir, "_" + filename)
        if os.path.exists(input_path):
            obfuscate_file(input_path, output_path)

if __name__ == '__main__':
    obfuscate_core()
