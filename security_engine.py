"""
Arabic Code Auditor Pro - Security Engine
محرك فحص الأمان - محمي بترخيص
"""
import re
import hashlib
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum
import os


class SecuritySeverity(Enum):
    CRITICAL = "حرج"
    HIGH = "عالي"
    MEDIUM = "متوسط"
    LOW = "منخفض"

class VulnerabilityType(Enum):
    API_KEY = "مفتاح_API"
    TOKEN = "توكن"
    PASSWORD = "كلمة_مرور_صريحة"
    AWS_KEY = "مفتاح_AWS"
    GITHUB_TOKEN = "توكن_GitHub"
    SQL_INJECTION = "SQL_Injection"
    XSS = "XSS"
    SSRF = "SSRF"
    COMMAND_INJECTION = "Command_Injection"
    PATH_TRAVERSAL = "Path_Traversal"
    INSECURE_DESERIALIZATION = "تسلسل_غير_آمن"
    HARDCODED_SECRET = "سر_مضمن"

@dataclass
class SecurityFinding:
    id: str
    file_path: str
    line: int
    column: int
    severity: SecuritySeverity
    vuln_type: VulnerabilityType
    message_ar: str
    message_en: str
    code_snippet: str
    remediation_ar: str
    remediation_en: str
    cwe_id: Optional[str] = None
    owasp_category: Optional[str] = None
    confidence: float = 1.0

@dataclass
class SecurityScanResult:
    file_path: str
    total_findings: int
    findings: List[SecurityFinding]
    scan_time: float

class SecurityEngine:
    """محرك فحص الأمان المتكامل"""

    # أنماط الكشف عن الأسرار
    SECRET_PATTERNS = {
        'api_key': re.compile(
            r'(?i)(api[_\-]?key|apikey)\s*[:=]\s*["']?([a-zA-Z0-9_\-]{16,})["']?',
            re.MULTILINE
        ),
        'aws_access_key': re.compile(
            r'(?i)(AKIA[0-9A-Z]{16})',
            re.MULTILINE
        ),
        'aws_secret_key': re.compile(
            r'(?i)(aws[_\-]?secret[_\-]?access[_\-]?key)\s*[:=]\s*["']?([a-zA-Z0-9/+=]{40})["']?',
            re.MULTILINE
        ),
        'github_token': re.compile(
            r'(?i)(gh[pousr]_[A-Za-z0-9_]{36,})',
            re.MULTILINE
        ),
        'github_classic_token': re.compile(
            r'(?i)(github[_\-]?token)\s*[:=]\s*["']?([a-f0-9]{40})["']?',
            re.MULTILINE
        ),
        'password': re.compile(
            r'(?i)(password|passwd|pwd)\s*[:=]\s*["']([^"']{4,})["']',
            re.MULTILINE
        ),
        'jwt_token': re.compile(
            r'(?i)(eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*)',
            re.MULTILINE
        ),
        'private_key': re.compile(
            r'-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----',
            re.MULTILINE
        ),
        'slack_token': re.compile(
            r'(?i)(xox[baprs]-[0-9a-zA-Z]{10,48})',
            re.MULTILINE
        ),
        'stripe_key': re.compile(
            r'(?i)(sk_live_[0-9a-zA-Z]{24,})',
            re.MULTILINE
        ),
    }

    # أنماط SQL Injection
    SQLI_PATTERNS = [
        re.compile(r'(?i)(SELECT\s+.*\s+FROM\s+.*\s+WHERE\s+.*["']\s*\+)', re.MULTILINE),
        re.compile(r'(?i)(EXEC\s*\(\s*["']\s*\+)', re.MULTILINE),
        re.compile(r'(?i)(execute\s*\(\s*["']\s*\+)', re.MULTILINE),
        re.compile(r'(?i)(\.query\s*\(\s*[`"'].*\$\{)', re.MULTILINE),
        re.compile(r'(?i)(cursor\.execute\s*\(\s*["'].*%s)', re.MULTILINE),
    ]

    # أنماط XSS
    XSS_PATTERNS = [
        re.compile(r'(?i)(innerHTML\s*=\s*.*\+)', re.MULTILINE),
        re.compile(r'(?i)(document\.write\s*\(.*\+)', re.MULTILINE),
        re.compile(r'(?i)(\.html\s*\(\s*.*\+)', re.MULTILINE),
        re.compile(r'(?i)(dangerouslySetInnerHTML)', re.MULTILINE),
        re.compile(r'(?i)(eval\s*\(.*\+)', re.MULTILINE),
    ]

    # أنماط Command Injection
    CMD_INJECTION_PATTERNS = [
        re.compile(r'(?i)(os\.system\s*\(.*\+)', re.MULTILINE),
        re.compile(r'(?i)(subprocess\.call\s*\(\s*["'].*\+)', re.MULTILINE),
        re.compile(r'(?i)(exec\s*\(.*\+)', re.MULTILINE),
        re.compile(r'(?i)(shell_exec\s*\(.*\$)', re.MULTILINE),
        re.compile(r'(?i)(passthru\s*\(.*\$)', re.MULTILINE),
    ]

    # أنماط SSRF
    SSRF_PATTERNS = [
        re.compile(r'(?i)(requests\.get\s*\(\s*.*\+)', re.MULTILINE),
        re.compile(r'(?i)(urllib\.request\.urlopen\s*\(.*\+)', re.MULTILINE),
        re.compile(r'(?i)(curl_exec\s*\(.*\$)', re.MULTILINE),
        re.compile(r'(?i)(file_get_contents\s*\(.*\$)', re.MULTILINE),
    ]

    def __init__(self):
        self.findings = []

    async def scan_file(self, file_path: str, content: str = None) -> SecurityScanResult:
        """فحص ملف واحد"""
        import time
        start_time = time.time()

        if content is None:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

        self.findings = []

        # فحص الأسرار
        self._scan_secrets(file_path, content)

        # فحص SQL Injection
        self._scan_sqli(file_path, content)

        # فحص XSS
        self._scan_xss(file_path, content)

        # فحص Command Injection
        self._scan_cmd_injection(file_path, content)

        # فحص SSRF
        self._scan_ssrf(file_path, content)

        scan_time = time.time() - start_time

        return SecurityScanResult(
            file_path=file_path,
            total_findings=len(self.findings),
            findings=self.findings,
            scan_time=scan_time
        )

    def _scan_secrets(self, file_path: str, content: str):
        """فحص الأسرار المضمنة"""
        for secret_type, pattern in self.SECRET_PATTERNS.items():
            for match in pattern.finditer(content):
                line_num = content[:match.start()].count('
') + 1
                col_num = match.start() - content.rfind('
', 0, match.start())

                severity = SecuritySeverity.CRITICAL
                if secret_type in ['password']:
                    severity = SecuritySeverity.HIGH
                elif secret_type in ['jwt_token']:
                    severity = SecuritySeverity.MEDIUM

                vuln_type_map = {
                    'api_key': VulnerabilityType.API_KEY,
                    'aws_access_key': VulnerabilityType.AWS_KEY,
                    'aws_secret_key': VulnerabilityType.AWS_KEY,
                    'github_token': VulnerabilityType.GITHUB_TOKEN,
                    'github_classic_token': VulnerabilityType.GITHUB_TOKEN,
                    'password': VulnerabilityType.PASSWORD,
                    'jwt_token': VulnerabilityType.TOKEN,
                    'private_key': VulnerabilityType.HARDCODED_SECRET,
                    'slack_token': VulnerabilityType.TOKEN,
                    'stripe_key': VulnerabilityType.API_KEY,
                }

                finding = SecurityFinding(
                    id=f"SEC_{secret_type}_{hashlib.md5(match.group().encode()).hexdigest()[:8]}",
                    file_path=file_path,
                    line=line_num,
                    column=col_num,
                    severity=severity,
                    vuln_type=vuln_type_map.get(secret_type, VulnerabilityType.HARDCODED_SECRET),
                    message_ar=f"تم العثور على {secret_type.replace('_', ' ')} مضمن في الكود",
                    message_en=f"Hardcoded {secret_type.replace('_', ' ')} found in code",
                    code_snippet=match.group()[:100],
                    remediation_ar="استخدم متغيرات البيئة أو مدير الأسرار بدلاً من تضمين الأسرار في الكود",
                    remediation_en="Use environment variables or a secrets manager instead of hardcoding secrets",
                    cwe_id="CWE-798",
                    owasp_category="A07:2021 - Identification and Authentication Failures",
                    confidence=0.95
                )
                self.findings.append(finding)

    def _scan_sqli(self, file_path: str, content: str):
        """فحص SQL Injection"""
        for pattern in self.SQLI_PATTERNS:
            for match in pattern.finditer(content):
                line_num = content[:match.start()].count('
') + 1
                col_num = match.start() - content.rfind('
', 0, match.start())

                finding = SecurityFinding(
                    id=f"SQLI_{hashlib.md5(match.group().encode()).hexdigest()[:8]}",
                    file_path=file_path,
                    line=line_num,
                    column=col_num,
                    severity=SecuritySeverity.CRITICAL,
                    vuln_type=VulnerabilityType.SQL_INJECTION,
                    message_ar="اكتشاف ثغرة SQL Injection - تسلسل استعلامات قاعدة البيانات بطريقة غير آمنة",
                    message_en="SQL Injection vulnerability detected - unsafe query concatenation",
                    code_snippet=match.group()[:150],
                    remediation_ar="استخدم الاستعلامات المُعدة (Prepared Statements) أو ORM بدلاً من تسلسل الاستعلامات",
                    remediation_en="Use prepared statements or ORM instead of query concatenation",
                    cwe_id="CWE-89",
                    owasp_category="A03:2021 - Injection",
                    confidence=0.85
                )
                self.findings.append(finding)

    def _scan_xss(self, file_path: str, content: str):
        """فحص XSS"""
        for pattern in self.XSS_PATTERNS:
            for match in pattern.finditer(content):
                line_num = content[:match.start()].count('
') + 1
                col_num = match.start() - content.rfind('
', 0, match.start())

                finding = SecurityFinding(
                    id=f"XSS_{hashlib.md5(match.group().encode()).hexdigest()[:8]}",
                    file_path=file_path,
                    line=line_num,
                    column=col_num,
                    severity=SecuritySeverity.HIGH,
                    vuln_type=VulnerabilityType.XSS,
                    message_ar="اكتشاف ثغرة XSS - حقن محتوى غير موثوق في DOM",
                    message_en="XSS vulnerability detected - untrusted content injected into DOM",
                    code_snippet=match.group()[:150],
                    remediation_ar="استخدم textContent بدلاً من innerHTML، وقم بتعقيم المدخلات قبل عرضها",
                    remediation_en="Use textContent instead of innerHTML, sanitize inputs before rendering",
                    cwe_id="CWE-79",
                    owasp_category="A03:2021 - Injection",
                    confidence=0.80
                )
                self.findings.append(finding)

    def _scan_cmd_injection(self, file_path: str, content: str):
        """فحص Command Injection"""
        for pattern in self.CMD_INJECTION_PATTERNS:
            for match in pattern.finditer(content):
                line_num = content[:match.start()].count('
') + 1
                col_num = match.start() - content.rfind('
', 0, match.start())

                finding = SecurityFinding(
                    id=f"CMDI_{hashlib.md5(match.group().encode()).hexdigest()[:8]}",
                    file_path=file_path,
                    line=line_num,
                    column=col_num,
                    severity=SecuritySeverity.CRITICAL,
                    vuln_type=VulnerabilityType.COMMAND_INJECTION,
                    message_ar="اكتشاف ثغرة Command Injection - تنفيذ أوامر النظام بطريقة غير آمنة",
                    message_en="Command Injection vulnerability detected - unsafe system command execution",
                    code_snippet=match.group()[:150],
                    remediation_ar="تجنب استخدام أوامر النظام مع مدخلات المستخدم، استخدم واجهات برمجة آمنة",
                    remediation_en="Avoid system commands with user input, use safe APIs instead",
                    cwe_id="CWE-78",
                    owasp_category="A03:2021 - Injection",
                    confidence=0.85
                )
                self.findings.append(finding)

    def _scan_ssrf(self, file_path: str, content: str):
        """فحص SSRF"""
        for pattern in self.SSRF_PATTERNS:
            for match in pattern.finditer(content):
                line_num = content[:match.start()].count('
') + 1
                col_num = match.start() - content.rfind('
', 0, match.start())

                finding = SecurityFinding(
                    id=f"SSRF_{hashlib.md5(match.group().encode()).hexdigest()[:8]}",
                    file_path=file_path,
                    line=line_num,
                    column=col_num,
                    severity=SecuritySeverity.HIGH,
                    vuln_type=VulnerabilityType.SSRF,
                    message_ar="اكتشاف ثغرة SSRF - طلبات شبكة غير موثوقة قد تصل إلى موارد داخلية",
                    message_en="SSRF vulnerability detected - untrusted network requests may reach internal resources",
                    code_snippet=match.group()[:150],
                    remediation_ar="تحقق من عناوين URL، استخدم قائمة بيضاء، تجنب الوصول إلى الموارد الداخلية",
                    remediation_en="Validate URLs, use allowlists, avoid accessing internal resources",
                    cwe_id="CWE-918",
                    owasp_category="A10:2021 - Server-Side Request Forgery",
                    confidence=0.75
                )
                self.findings.append(finding)

    async def scan_project(self, project_path: str) -> List[SecurityScanResult]:
        """فحص مشروع كامل"""
        results = []

        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.git']]

            for file in files:
                file_path = os.path.join(root, file)
                try:
                    result = await self.scan_file(file_path)
                    if result.total_findings > 0:
                        results.append(result)
                except Exception as e:
                    print(f"خطأ في فحص الأمان {file_path}: {e}")

        return results

    def get_summary(self, results: List[SecurityScanResult]) -> Dict[str, Any]:
        """ملخص نتائج الفحص"""
        summary = {
            'total_files_scanned': len(results),
            'total_findings': sum(r.total_findings for r in results),
            'findings_by_severity': {},
            'findings_by_type': {},
            'total_scan_time': sum(r.scan_time for r in results),
        }

        for result in results:
            for finding in result.findings:
                sev = finding.severity.value
                summary['findings_by_severity'][sev] = summary['findings_by_severity'].get(sev, 0) + 1

                vtype = finding.vuln_type.value
                summary['findings_by_type'][vtype] = summary['findings_by_type'].get(vtype, 0) + 1

        return summary

# Singleton
_security_engine = None

def get_security_engine() -> SecurityEngine:
    global _security_engine
    if _security_engine is None:
        _security_engine = SecurityEngine()
    return _security_engine
