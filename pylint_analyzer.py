"""
Pylint Analyzer - Python Static Analysis
"""
import subprocess
import json
from typing import List
from ...core.analyzer_engine import Issue, Severity

class PylintAnalyzer:
    def analyze(self, file_path: str, content: str):
        issues = []
        try:
            result = subprocess.run(
                ['pylint', file_path, '--output-format=json', '--disable=I,R'],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                pylint_issues = json.loads(result.stdout)
                for issue in pylint_issues:
                    issues.append(Issue(
                        id=f"PYLINT_{issue.get('symbol', 'UNKNOWN')}",
                        file_path=file_path,
                        line=issue.get('line', 0),
                        column=issue.get('column', 0),
                        severity=self._map_severity(issue.get('type', 'convention')),
                        rule_id=issue.get('symbol', 'UNKNOWN'),
                        message_ar=issue.get('message', ''),
                        message_en=issue.get('message', ''),
                        code_snippet=content.split('
')[issue.get('line', 1)-1] if content else ''
                    ))
        except Exception as e:
            pass
        return type('Result', (), {'issues': issues, 'metrics': {}})()

    def _map_severity(self, type_str: str) -> Severity:
        mapping = {
            'error': Severity.HIGH,
            'fatal': Severity.CRITICAL,
            'warning': Severity.MEDIUM,
            'convention': Severity.LOW,
            'refactor': Severity.LOW
        }
        return mapping.get(type_str, Severity.LOW)
