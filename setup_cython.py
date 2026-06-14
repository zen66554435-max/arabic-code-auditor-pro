"""
Arabic Code Auditor Pro - Cython Build
"""
from setuptools import setup, Extension
from Cython.Build import cythonize
import os

CORE_FILES = [
    'src/core/license_manager.py',
    'src/core/analyzer_engine.py',
    'src/core/security_engine.py',
    'src/core/ai_engine.py',
    'src/core/fixer_engine.py',
    'src/core/report_engine.py',
    'src/core/plugin_engine.py',
]

def build_cython():
    extensions = []
    for py_file in CORE_FILES:
        if os.path.exists(py_file):
            module_name = py_file.replace('/', '.').replace('.py', '')
            ext = Extension(
                module_name,
                [py_file],
                extra_compile_args=['-O3'],
            )
            extensions.append(ext)

    if extensions:
        setup(
            ext_modules=cythonize(
                extensions,
                compiler_directives={
                    'language_level': 3,
                    'embedsignature': False,
                }
            ),
            zip_safe=False,
        )

if __name__ == '__main__':
    build_cython()
