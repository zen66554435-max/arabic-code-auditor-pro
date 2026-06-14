"""
Radon Analyzer - Python Complexity Analyzer
"""
import subprocess
import json
from typing import List
from ...core.analyzer_engine import Issue, Severity

class RadonAnalyzer:
    def analyze(self, file_path: str, content: str):
        issues = []
        try:
            result = subprocess.run(
                ['radon', 'cc', '-j', file_path],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                data = json.loads(result.stdout)
                for func_name, func_data in data.get(file_path, {}).items():
                    complexity = func_data.get('complexity', 0)
                    if complexity > 10:
                        issues.append(Issue(
                            id=f"RADON_COMPLEXITY",
                            file_path=file_path,
                            line=func_data.get('lineno', 0),
                            column=0,
                            severity=Severity.HIGH if complexity > 20 else Severity.MEDIUM,
                            rule_id='complexity',
                            message_ar=f"تعقيد دوري عالي: {complexity} (الحد الأقصى المقبول: 10)",
                            message_en=f"High cyclomatic complexity: {complexity}",
                            code_snippet=f"Function: {func_name}"
                        ))
        except Exception as e:
            pass
        return type('Result', (), {'issues': issues, 'metrics': {}})()
