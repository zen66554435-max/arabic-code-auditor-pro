"""
Bandit Analyzer - Python Security Scanner
"""
import subprocess
import json
from typing import List
from ...core.analyzer_engine import Issue, Severity

class BanditAnalyzer:
    def analyze(self, file_path: str, content: str):
        issues = []
        try:
            result = subprocess.run(
                ['bandit', '-f', 'json', '-q', file_path],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                data = json.loads(result.stdout)
                for result_item in data.get('results', []):
                    issues.append(Issue(
                        id=f"BANDIT_{result_item.get('test_id', 'UNKNOWN')}",
                        file_path=file_path,
                        line=result_item.get('line_number', 0),
                        column=result_item.get('col_offset', 0),
                        severity=self._map_severity(result_item.get('issue_severity', 'LOW')),
                        rule_id=result_item.get('test_id', 'UNKNOWN'),
                        message_ar=result_item.get('issue_text', ''),
                        message_en=result_item.get('issue_text', ''),
                        code_snippet=result_item.get('code', '')
                    ))
        except Exception as e:
            pass
        return type('Result', (), {'issues': issues, 'metrics': {}})()

    def _map_severity(self, severity: str) -> Severity:
        mapping = {
            'HIGH': Severity.HIGH,
            'MEDIUM': Severity.MEDIUM,
            'LOW': Severity.LOW
        }
        return mapping.get(severity, Severity.LOW)
