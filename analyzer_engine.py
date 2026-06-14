"""
Arabic Code Auditor Pro - Core Analyzer Engine
محرك التحليل الأساسي - محمي بترخيص
"""
import asyncio
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import subprocess
import tempfile
import os


# Verify license on import

class Severity(Enum):
    CRITICAL = "حرج"
    HIGH = "عالي"
    MEDIUM = "متوسط"
    LOW = "منخفض"
    INFO = "معلومة"

class Language(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    PHP = "php"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    GO = "go"
    RUST = "rust"
    C = "c"
    CPP = "cpp"

@dataclass
class Issue:
    id: str
    file_path: str
    line: int
    column: int
    severity: Severity
    rule_id: str
    message_ar: str
    message_en: str
    code_snippet: str
    fix_suggestion: Optional[str] = None
    documentation_url: Optional[str] = None

@dataclass
class AnalysisResult:
    file_path: str
    language: Language
    total_issues: int
    issues: List[Issue]
    metrics: Dict[str, Any]
    execution_time: float

class AnalyzerEngine:
    """المحرك الأساسي لتحليل الأكواد"""

    def __init__(self):
        self.analyzers = {}
        self._register_default_analyzers()

    def _register_default_analyzers(self):
        from ..analyzers.python.ruff_analyzer import RuffAnalyzer
        from ..analyzers.python.pylint_analyzer import PylintAnalyzer
        from ..analyzers.python.mypy_analyzer import MypyAnalyzer
        from ..analyzers.python.bandit_analyzer import BanditAnalyzer
        from ..analyzers.python.radon_analyzer import RadonAnalyzer
        from ..analyzers.javascript.eslint_analyzer import ESLintAnalyzer
        from ..analyzers.javascript.prettier_analyzer import PrettierAnalyzer
        from ..analyzers.php.phpstan_analyzer import PHPStanAnalyzer
        from ..analyzers.php.phpcsfixer_analyzer import PHPCSFixerAnalyzer

        self.analyzers[Language.PYTHON] = [
            RuffAnalyzer(),
            PylintAnalyzer(),
            MypyAnalyzer(),
            BanditAnalyzer(),
            RadonAnalyzer(),
        ]
        self.analyzers[Language.JAVASCRIPT] = [
            ESLintAnalyzer(),
            PrettierAnalyzer(),
        ]
        self.analyzers[Language.PHP] = [
            PHPStanAnalyzer(),
            PHPCSFixerAnalyzer(),
        ]

    def detect_language(self, file_path: str, content: str = None) -> Language:
        """اكتشاف لغة البرمجة من امتداد الملف"""
        ext = os.path.splitext(file_path)[1].lower()
        mapping = {
            '.py': Language.PYTHON,
            '.js': Language.JAVASCRIPT,
            '.jsx': Language.JAVASCRIPT,
            '.ts': Language.TYPESCRIPT,
            '.tsx': Language.TYPESCRIPT,
            '.php': Language.PHP,
            '.java': Language.JAVA,
            '.go': Language.GO,
            '.rs': Language.RUST,
            '.c': Language.C,
            '.cpp': Language.CPP,
            '.h': Language.C,
        }
        return mapping.get(ext, Language.PYTHON)

    async def analyze_file(self, file_path: str, content: str = None) -> AnalysisResult:
        """تحليل ملف واحد"""
        import time
        start_time = time.time()

        if content is None:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

        language = self.detect_language(file_path, content)
        all_issues = []
        metrics = {}

        # تشغيل جميع المحللات المناسبة
        analyzers = self.analyzers.get(language, [])
        tasks = [analyzer.analyze(file_path, content) for analyzer in analyzers]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                print(f"خطأ في المحلل: {result}")
                continue
            all_issues.extend(result.issues)
            metrics.update(result.metrics)

        execution_time = time.time() - start_time

        return AnalysisResult(
            file_path=file_path,
            language=language,
            total_issues=len(all_issues),
            issues=all_issues,
            metrics=metrics,
            execution_time=execution_time
        )

    async def analyze_project(self, project_path: str) -> List[AnalysisResult]:
        """تحليل مشروع كامل"""
        results = []

        for root, dirs, files in os.walk(project_path):
            # تجاهل المجلدات المخفية
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.git']]

            for file in files:
                file_path = os.path.join(root, file)
                try:
                    result = await self.analyze_file(file_path)
                    results.append(result)
                except Exception as e:
                    print(f"خطأ في تحليل {file_path}: {e}")

        return results

    def get_summary(self, results: List[AnalysisResult]) -> Dict[str, Any]:
        """الحصول على ملخص النتائج"""
        summary = {
            'total_files': len(results),
            'total_issues': sum(r.total_issues for r in results),
            'issues_by_severity': {},
            'issues_by_language': {},
            'total_execution_time': sum(r.execution_time for r in results),
        }

        for result in results:
            lang = result.language.value
            summary['issues_by_language'][lang] = summary['issues_by_language'].get(lang, 0) + result.total_issues

            for issue in result.issues:
                sev = issue.severity.value
                summary['issues_by_severity'][sev] = summary['issues_by_severity'].get(sev, 0) + 1

        return summary

# Singleton instance
_analyzer_engine = None

def get_analyzer_engine() -> AnalyzerEngine:
    global _analyzer_engine
    if _analyzer_engine is None:
        _analyzer_engine = AnalyzerEngine()
    return _analyzer_engine
