"""
PHPStan Analyzer - PHP Static Analysis
"""
import subprocess
from typing import List
from ...core.analyzer_engine import Issue, Severity

class PHPStanAnalyzer:
    def analyze(self, file_path: str, content: str):
        issues = []
        try:
            result = subprocess.run(
                ['phpstan', 'analyse', file_path, '--error-format=json', '--no-progress'],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                import json
                data = json.loads(result.stdout)
                for file_path_key, file_errors in data.get('files', {}).items():
                    for error in file_errors.get('messages', []):
                        issues.append(Issue(
                            id=f"PHPSTAN_{error.get('identifier', 'UNKNOWN')}",
                            file_path=file_path,
                            line=error.get('line', 0),
                            column=0,
                            severity=Severity.HIGH,
                            rule_id=error.get('identifier', 'UNKNOWN'),
                            message_ar=error.get('message', ''),
                            message_en=error.get('message', ''),
                            code_snippet=""
                        ))
        except Exception as e:
            pass
        return type('Result', (), {'issues': issues, 'metrics': {}})()
