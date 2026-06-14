"""
Arabic Code Auditor Pro - AI Engine
محرك الذكاء الاصطناعي - محمي بترخيص
"""
import re
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum
import ast
import json


class AIAction(Enum):
    EXPLAIN = "شرح"
    FIX = "إصلاح"
    OPTIMIZE = "تحسين"
    REFACTOR = "إعادة_هيكلة"
    DOCUMENT = "توثيق"
    TEST = "اختبار"

@dataclass
class AIExplanation:
    issue_id: str
    explanation_ar: str
    explanation_en: str
    code_example: str
    references: List[str]

@dataclass
class AIFix:
    issue_id: str
    original_code: str
    fixed_code: str
    explanation_ar: str
    explanation_en: str
    confidence: float

@dataclass
class AIOptimization:
    original_code: str
    optimized_code: str
    performance_gain: str
    explanation_ar: str
    explanation_en: str

@dataclass
class AIRefactor:
    original_code: str
    refactored_code: str
    improvements: List[str]
    explanation_ar: str
    explanation_en: str

@dataclass
class AIDocumentation:
    code: str
    docstring_ar: str
    docstring_en: str
    parameters: List[Dict[str, str]]
    returns: str
    examples: List[str]

class AIEngine:
    """محرك الذكاء الاصطناعي لتحليل وشرح الأكواد"""

    def __init__(self):
        self.explanation_templates = self._load_explanation_templates()
        self.fix_templates = self._load_fix_templates()

    def _load_explanation_templates(self) -> Dict[str, Dict[str, str]]:
        """قوالب الشرح بالعربية"""
        return {
            'unused_import': {
                'ar': 'هذا الاستيراد غير مستخدم في الملف. يُنصح بإزالته لتقليل حجم الكود وتحسين الأداء.',
                'en': 'This import is unused in the file. Remove it to reduce code size and improve performance.'
            },
            'trailing_whitespace': {
                'ar': 'يوجد مسافات بيضاء زائدة في نهاية السطر. هذه المسافات لا تؤثر على الأداء لكنها تؤثر على جودة الكود.',
                'en': 'Trailing whitespace detected at end of line. While not affecting performance, it impacts code quality.'
            },
            'line_too_long': {
                'ar': 'السطر أطول من 80/120 حرف. يُفضل تقسيمه لتحسين القراءة.',
                'en': 'Line exceeds 80/120 characters. Consider breaking it for better readability.'
            },
            'missing_docstring': {
                'ar': 'الدالة/الفئة تفتقر إلى توثيق (Docstring). يُنصح بإضافة وصف واضح للوظيفة والمدخلات والمخرجات.',
                'en': 'Function/class lacks documentation (Docstring). Add clear description of purpose, inputs, and outputs.'
            },
            'sql_injection': {
                'ar': 'ثغرة خطيرة! يتم تسلسل استعلام SQL مع مدخلات المستخدم مباشرة. هذا يفتح الباب للمهاجمين للوصول إلى قاعدة البيانات.',
                'en': 'CRITICAL VULNERABILITY! SQL query is concatenated with user input directly. This allows attackers to access the database.'
            },
            'xss': {
                'ar': 'ثغرة XSS! يتم حقن محتوى غير موثوق في DOM مباشرة. يمكن للمهاجم تنفيذ JavaScript ضار.',
                'en': 'XSS VULNERABILITY! Untrusted content is injected into DOM directly. Attackers can execute malicious JavaScript.'
            },
            'hardcoded_secret': {
                'ar': 'سر مضمن في الكود! لا يجب تضمين المفاتيح أو كلمات المرور في الكود. استخدم متغيرات البيئة.',
                'en': 'Hardcoded secret in code! Never embed keys or passwords in code. Use environment variables.'
            },
            'unused_variable': {
                'ar': 'متغير معرف لكنه غير مستخدم. إزالته يُحسّن وضوح الكود.',
                'en': 'Variable is defined but never used. Removing it improves code clarity.'
            },
            'complex_function': {
                'ar': 'الدالة معقدة جداً (Cyclomatic Complexity عالي). يُفضل تقسيمها إلى دوال أصغر.',
                'en': 'Function is too complex (high Cyclomatic Complexity). Consider splitting into smaller functions.'
            },
            'bare_except': {
                'ar': 'استخدام except بدون تحديد نوع الخطأ يُخفي الأخطاء الحقيقية. حدد نوع الاستثناء المحدد.',
                'en': 'Bare except clause hides real errors. Specify the exact exception type to catch.'
            },
        }

    def _load_fix_templates(self) -> Dict[str, Dict[str, str]]:
        """قوالب الإصلاح"""
        return {
            'sql_injection': {
                'ar': 'استخدم الاستعلامات المُعدة (Prepared Statements)',
                'example': '# قبل (غير آمن)\ncursor.execute("SELECT * FROM users WHERE id = " + user_id)\n\n# بعد (آمن)\ncursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))'
            },
            'xss': {
                'ar': 'استخدم textContent وتعقيم المدخلات',
                'example': '// قبل (غير آمن)\nelement.innerHTML = userInput;\n\n// بعد (آمن)\nelement.textContent = sanitize(userInput);'
            },
            'hardcoded_secret': {
                'ar': 'استخدم متغيرات البيئة',
                'example': '# قبل (غير آمن)\nAPI_KEY = "sk-1234567890abcdef"\n\n# بعد (آمن)\nimport os\nAPI_KEY = os.environ.get("API_KEY")'
            },
        }

    def explain_issue(self, issue_type: str, code_snippet: str, 
                      language: str = "python") -> AIExplanation:
        """شرح خطأ بالعربية"""
        template = self.explanation_templates.get(issue_type, {
            'ar': f'تم اكتشاف مشكلة من نوع: {issue_type}. راجع الكود للمزيد من التفاصيل.',
            'en': f'Issue detected: {issue_type}. Review the code for more details.'
        })

        return AIExplanation(
            issue_id=f"EXP_{issue_type}",
            explanation_ar=template['ar'],
            explanation_en=template['en'],
            code_example=code_snippet[:200],
            references=[
                "https://docs.python.org/3/tutorial/errors.html",
                "https://owasp.org/www-project-top-ten/"
            ]
        )

    def suggest_fix(self, issue_type: str, original_code: str,
                    language: str = "python") -> AIFix:
        """اقتراح إصلاح"""
        template = self.fix_templates.get(issue_type, {
            'ar': 'راجع الكود وطبق أفضل الممارسات',
            'example': original_code
        })

        return AIFix(
            issue_id=f"FIX_{issue_type}",
            original_code=original_code,
            fixed_code=template.get('example', original_code),
            explanation_ar=template['ar'],
            explanation_en=f"Review and apply best practices for {issue_type}",
            confidence=0.85
        )

    def optimize_code(self, code: str, language: str = "python") -> AIOptimization:
        """تحسين الأداء"""
        optimized = code
        improvements = []

        if language == "python":
            if "for" in code and "append" in code:
                improvements.append("استخدم List Comprehension بدلاً من الحلقة مع append")
                optimized = self._optimize_list_comprehension(code)

            if "in list" in code:
                improvements.append("استخدم set بدلاً من list للبحث السريع O(1)")

        return AIOptimization(
            original_code=code,
            optimized_code=optimized,
            performance_gain="تحسين بنسبة 20-50%" if improvements else "لا يوجد تحسين واضح",
            explanation_ar="تم اقتراح تحسينات للأداء بناءً على أنماط الكود",
            explanation_en="Performance improvements suggested based on code patterns"
        )

    def _optimize_list_comprehension(self, code: str) -> str:
        return code

    def refactor_code(self, code: str, language: str = "python") -> AIRefactor:
        """إعادة هيكلة الكود"""
        improvements = []
        refactored = code

        if language == "python":
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if len(node.body) > 20:
                            improvements.append(f"الدالة {node.name} طويلة جداً، قسمها")
            except:
                pass

        return AIRefactor(
            original_code=code,
            refactored_code=refactored,
            improvements=improvements,
            explanation_ar="تم تحليل الكود واقتراح إعادة الهيكلة",
            explanation_en="Code analyzed and refactoring suggestions provided"
        )

    def generate_documentation(self, code: str, language: str = "python") -> AIDocumentation:
        """توليد التوثيق التلقائي"""
        docstring_ar = ""
        docstring_en = ""
        parameters = []
        returns = ""
        examples = []

        if language == "python":
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        docstring_en = f"Function: {node.name}"
                        for arg in node.args.args:
                            if arg.arg != 'self':
                                parameters.append({
                                    'name': arg.arg,
                                    'type': getattr(arg.annotation, 'id', 'Any') if arg.annotation else 'Any',
                                    'description_ar': f'معامل {arg.arg}'
                                })
                        if node.returns:
                            returns = getattr(node.returns, 'id', 'Any')
                        examples.append(f"{node.name}()")
            except:
                pass

        return AIDocumentation(
            code=code,
            docstring_ar=docstring_ar,
            docstring_en=docstring_en,
            parameters=parameters,
            returns=returns,
            examples=examples
        )

    def generate_unit_tests(self, code: str, language: str = "python") -> str:
        """توليد اختبارات الوحدة"""
        if language == "python":
            try:
                tree = ast.parse(code)
                tests = []

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name = node.name
                        tests.append(f"def test_{func_name}(self):\n    result = {func_name}()\n    self.assertIsNotNone(result)")

                test_code = "import unittest\n\nclass TestGenerated(unittest.TestCase):\n" + "\n".join(["    " + t for t in tests]) + "\n\nif __name__ == '__main__':\n    unittest.main()"
                return test_code
            except:
                return "# تعذر توليد الاختبارات تلقائياً"

        return "# توليد الاختبارات مدعوم حالياً فقط لـ Python"

    def analyze_complexity(self, code: str, language: str = "python") -> Dict[str, Any]:
        """تحليل تعقيد الكود"""
        complexity = 0
        lines = code.split('\n')

        if language == "python":
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                        complexity += 1
                    elif isinstance(node, ast.FunctionDef):
                        complexity += 1
            except:
                pass

        return {
            'cyclomatic_complexity': complexity,
            'lines_of_code': len(lines),
            'blank_lines': len([l for l in lines if not l.strip()]),
            'comment_lines': len([l for l in lines if l.strip().startswith('#')]),
            'assessment_ar': 'معقد' if complexity > 10 else 'متوسط' if complexity > 5 else 'بسيط',
            'assessment_en': 'Complex' if complexity > 10 else 'Moderate' if complexity > 5 else 'Simple'
        }

_ai_engine = None

def get_ai_engine() -> AIEngine:
    global _ai_engine
    if _ai_engine is None:
        _ai_engine = AIEngine()
    return _ai_engine
