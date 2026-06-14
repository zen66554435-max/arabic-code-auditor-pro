"""
ESLint Analyzer - JavaScript/TypeScript Linter
"""
import subprocess
import json
from typing import List
from ...core.analyzer_engine import Issue, Severity

class ESLintAnalyzer:
    def analyze(self, file_path: str, content: str):
        issues = []
        try:
            result = subprocess.run(
                ['eslint', file_path, '--format', 'json', '--no-eslintrc'],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                eslint_issues = json.loads(result.stdout)
                for file_issues in eslint_issues:
                    for msg in file_issues.get('messages', []):
                        issues.append(Issue(
                            id=f"ESLINT_{msg.get('ruleId', 'UNKNOWN')}",
                            file_path=file_path,
                            line=msg.get('line', 0),
                            column=msg.get('column', 0),
                            severity=self._map_severity(msg.get('severity', 1)),
                            rule_id=msg.get('ruleId', 'UNKNOWN'),
                            message_ar=msg.get('message', ''),
                            message_en=msg.get('message', ''),
                            code_snippet=content.split('
')[msg.get('line', 1)-1] if content else ''
                        ))
        except Exception as e:
            pass
        return type('Result', (), {'issues': issues, 'metrics': {}})()

    def _map_severity(self, severity: int) -> Severity:
        mapping = {2: Severity.HIGH, 1: Severity.MEDIUM, 0: Severity.LOW}
        return mapping.get(severity, Severity.LOW)
