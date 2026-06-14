"""
Ruff Analyzer - Python Linter
"""
import subprocess
import json
from typing import List
from ...core.analyzer_engine import Issue, Severity

class RuffAnalyzer:
    def analyze(self, file_path: str, content: str):
        issues = []
        try:
            result = subprocess.run(
                ['ruff', 'check', file_path, '--output-format', 'json'],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                ruff_issues = json.loads(result.stdout)
                for issue in ruff_issues:
                    issues.append(Issue(
                        id=f"RUFF_{issue.get('code', 'UNKNOWN')}",
                        file_path=file_path,
                        line=issue.get('location', {}).get('row', 0),
                        column=issue.get('location', {}).get('column', 0),
                        severity=self._map_severity(issue.get('code', '')),
                        rule_id=issue.get('code', 'UNKNOWN'),
                        message_ar=issue.get('message', ''),
                        message_en=issue.get('message', ''),
                        code_snippet=content.split('
')[issue.get('location', {}).get('row', 1)-1] if content else ''
                    ))
        except Exception as e:
            pass
        return type('Result', (), {'issues': issues, 'metrics': {}})()

    def _map_severity(self, code: str) -> Severity:
        if code.startswith('E'): return Severity.HIGH
        if code.startswith('W'): return Severity.MEDIUM
        return Severity.LOW
