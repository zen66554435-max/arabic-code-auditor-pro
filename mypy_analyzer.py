"""
MyPy Analyzer - Python Type Checker
"""
import subprocess
import re
from typing import List
from ...core.analyzer_engine import Issue, Severity

class MypyAnalyzer:
    def analyze(self, file_path: str, content: str):
        issues = []
        try:
            result = subprocess.run(
                ['mypy', file_path, '--show-column-numbers', '--no-error-summary'],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                lines = result.stdout.strip().split('
')
                for line in lines:
                    match = re.match(r'(.+):(\d+):(\d+):\s*(error|warning|note):\s*(.+)', line)
                    if match:
                        issues.append(Issue(
                            id=f"MYPY_TYPE",
                            file_path=match.group(1),
                            line=int(match.group(2)),
                            column=int(match.group(3)),
                            severity=Severity.HIGH if match.group(4) == 'error' else Severity.MEDIUM,
                            rule_id='type-error',
                            message_ar=f"خطأ في الأنواع: {match.group(5)}",
                            message_en=match.group(5),
                            code_snippet=content.split('
')[int(match.group(2))-1] if content else ''
                        ))
        except Exception as e:
            pass
        return type('Result', (), {'issues': issues, 'metrics': {}})()
