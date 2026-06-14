"""
Arabic Code Auditor Pro - Auto Fix Engine
محرك الإصلاح التلقائي - محمي بترخيص
"""
import re
import ast
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import shutil
import os


class FixType(Enum):
    SYNTAX_ERROR = "خطأ_نحوي"
    IMPORT_ERROR = "خطأ_استيراد"
    FORMATTING = "تنسيق"
    DEAD_CODE = "كود_ميت"
    UNUSED_VARIABLE = "متغير_غير_مستخدم"
    SECURITY = "أمان"
    PERFORMANCE = "أداء"

@dataclass
class Fix:
    id: str
    file_path: str
    line_start: int
    line_end: int
    original_code: str
    fixed_code: str
    fix_type: FixType
    description_ar: str
    description_en: str
    confidence: float  # 0.0 to 1.0
    applied: bool = False

@dataclass
class FixResult:
    file_path: str
    fixes_applied: List[Fix]
    fixes_failed: List[Fix]
    backup_path: Optional[str]
    summary: Dict[str, Any]

class FixerEngine:
    """محرك الإصلاح التلقائي للأكواد"""

    def __init__(self):
        self.fixers = {}
        self._register_fixers()

    def _register_fixers(self):
        """تسجيل جميع أدوات الإصلاح"""
        self.fixers[FixType.SYNTAX_ERROR] = self._fix_syntax_errors
        self.fixers[FixType.IMPORT_ERROR] = self._fix_imports
        self.fixers[FixType.FORMATTING] = self._fix_formatting
        self.fixers[FixType.DEAD_CODE] = self._remove_dead_code
        self.fixers[FixType.UNUSED_VARIABLE] = self._remove_unused_vars
        self.fixers[FixType.SECURITY] = self._fix_security_issues

    def create_backup(self, file_path: str) -> str:
        """إنشاء نسخة احتياطية"""
        backup_path = f"{file_path}.aca_backup"
        shutil.copy2(file_path, backup_path)
        return backup_path

    def restore_backup(self, file_path: str, backup_path: str):
        """استعادة النسخة الاحتياطية"""
        shutil.copy2(backup_path, file_path)

    async def fix_file(self, file_path: str, issues: List[Any] = None, 
                       auto_apply: bool = False) -> FixResult:
        """إصلاح ملف واحد"""
        backup_path = self.create_backup(file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        fixes_applied = []
        fixes_failed = []

        # تحليل وإصلاح المشاكل
        try:
            # إصلاح المسافات البيضاء الزائدة
            content, fix = self._fix_trailing_whitespace(content, file_path)
            if fix:
                fixes_applied.append(fix)

            # إصلاح الأسطر الفارغة الزائدة
            content, fix = self._fix_extra_blank_lines(content, file_path)
            if fix:
                fixes_applied.append(fix)

            # إصلاح الاستيرادات غير المستخدمة (لـ Python)
            if file_path.endswith('.py'):
                content, fix = self._fix_unused_imports_python(content, file_path)
                if fix:
                    fixes_applied.append(fix)

            # كتابة المحتوى المُصلح
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        except Exception as e:
            # استعادة النسخة الاحتياطية عند الفشل
            self.restore_backup(file_path, backup_path)
            fixes_failed.append(Fix(
                id="fix_error",
                file_path=file_path,
                line_start=0,
                line_end=0,
                original_code="",
                fixed_code="",
                fix_type=FixType.SYNTAX_ERROR,
                description_ar=f"فشل الإصلاح: {str(e)}",
                description_en=f"Fix failed: {str(e)}",
                confidence=0.0
            ))

        summary = {
            'total_fixes': len(fixes_applied) + len(fixes_failed),
            'applied': len(fixes_applied),
            'failed': len(fixes_failed),
            'types': {}
        }

        for fix in fixes_applied:
            t = fix.fix_type.value
            summary['types'][t] = summary['types'].get(t, 0) + 1

        return FixResult(
            file_path=file_path,
            fixes_applied=fixes_applied,
            fixes_failed=fixes_failed,
            backup_path=backup_path,
            summary=summary
        )

    def _fix_trailing_whitespace(self, content: str, file_path: str) -> tuple:
        """إزالة المسافات البيضاء في نهاية الأسطر"""
        lines = content.split('
')
        fixed_lines = []
        changed = False

        for i, line in enumerate(lines):
            stripped = line.rstrip()
            if stripped != line:
                changed = True
            fixed_lines.append(stripped)

        if changed:
            fix = Fix(
                id="trailing_whitespace",
                file_path=file_path,
                line_start=1,
                line_end=len(lines),
                original_code="أسطر تحتوي على مسافات بيضاء زائدة",
                fixed_code="تمت إزالة المسافات البيضاء الزائدة",
                fix_type=FixType.FORMATTING,
                description_ar="إزالة المسافات البيضاء في نهاية الأسطر",
                description_en="Remove trailing whitespace",
                confidence=1.0,
                applied=True
            )
            return '
'.join(fixed_lines), fix

        return content, None

    def _fix_extra_blank_lines(self, content: str, file_path: str) -> tuple:
        """إزالة الأسطر الفارغة الزائدة"""
        # تقليل الأسطر الفارغة المتتالية إلى سطرين كحد أقصى
        content = re.sub(r'
{4,}', '


', content)

        fix = Fix(
            id="extra_blank_lines",
            file_path=file_path,
            line_start=1,
            line_end=1,
            original_code="أسطر فارغة زائدة",
            fixed_code="تم تقليل الأسطر الفارغة",
            fix_type=FixType.FORMATTING,
            description_ar="تقليل الأسطر الفارغة المتتالية",
            description_en="Reduce consecutive blank lines",
            confidence=1.0,
            applied=True
        )
        return content, fix

    def _fix_unused_imports_python(self, content: str, file_path: str) -> tuple:
        """إزالة الاستيرادات غير المستخدمة في Python"""
        try:
            tree = ast.parse(content)
            imports = []
            used_names = set()

            # جمع جميع الاستيرادات
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    for alias in node.names:
                        imports.append((node, alias.name))
                elif isinstance(node, ast.Name):
                    used_names.add(node.id)

            # إزالة الاستيرادات غير المستخدمة
            lines = content.split('
')
            lines_to_remove = []

            for node, name in imports:
                if name not in used_names and name != '*':
                    lines_to_remove.append(node.lineno - 1)

            if lines_to_remove:
                new_lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]
                fix = Fix(
                    id="unused_imports",
                    file_path=file_path,
                    line_start=min(lines_to_remove) + 1,
                    line_end=max(lines_to_remove) + 1,
                    original_code="استيرادات غير مستخدمة",
                    fixed_code="تمت إزالة الاستيرادات غير المستخدمة",
                    fix_type=FixType.UNUSED_VARIABLE,
                    description_ar="إزالة الاستيرادات غير المستخدمة",
                    description_en="Remove unused imports",
                    confidence=0.9,
                    applied=True
                )
                return '
'.join(new_lines), fix
        except:
            pass

        return content, None

    def _fix_syntax_errors(self, content: str, file_path: str) -> tuple:
        """إصلاح الأخطاء النحوية"""
        return content, None

    def _fix_imports(self, content: str, file_path: str) -> tuple:
        """إصلاح مشاكل الاستيراد"""
        return content, None

    def _fix_formatting(self, content: str, file_path: str) -> tuple:
        """إصلاح التنسيق"""
        return content, None

    def _remove_dead_code(self, content: str, file_path: str) -> tuple:
        """إزالة الكود الميت"""
        return content, None

    def _remove_unused_vars(self, content: str, file_path: str) -> tuple:
        """إزالة المتغيرات غير المستخدمة"""
        return content, None

    def _fix_security_issues(self, content: str, file_path: str) -> tuple:
        """إصلاح مشاكل الأمان"""
        return content, None

# Singleton
_fixer_engine = None

def get_fixer_engine() -> FixerEngine:
    global _fixer_engine
    if _fixer_engine is None:
        _fixer_engine = FixerEngine()
    return _fixer_engine
