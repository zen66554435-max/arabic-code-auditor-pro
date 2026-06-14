"""
Arabic Code Auditor Pro - Report Engine
محرك التقارير - محمي بترخيص
"""
import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class ReportFormat(Enum):
    PDF = "pdf"
    HTML = "html"
    JSON = "json"
    EXCEL = "excel"
    MARKDOWN = "markdown"

@dataclass
class ReportData:
    report_id: str
    project_name: str
    scan_date: str
    total_files: int
    total_issues: int
    issues_by_severity: Dict[str, int]
    issues_by_type: Dict[str, int]
    issues_by_language: Dict[str, int]
    security_findings: int
    performance_issues: int
    code_quality_score: float
    findings: List[Dict[str, Any]]
    recommendations: List[str]
    scan_duration: float

class ReportEngine:
    """Report Engine"""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_report(self, data: ReportData, format: ReportFormat) -> str:
        if format == ReportFormat.JSON:
            return self._generate_json(data)
        elif format == ReportFormat.HTML:
            return self._generate_html(data)
        elif format == ReportFormat.MARKDOWN:
            return self._generate_markdown(data)
        elif format == ReportFormat.PDF:
            return self._generate_pdf(data)
        elif format == ReportFormat.EXCEL:
            return self._generate_excel(data)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _generate_json(self, data: ReportData) -> str:
        report_dict = asdict(data)
        report_dict['generated_at'] = datetime.now().isoformat()
        output_path = os.path.join(self.output_dir, f"{data.report_id}.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, ensure_ascii=False, indent=2)
        return output_path

    def _generate_html(self, data: ReportData) -> str:
        severity_html = self._render_severity_chart(data.issues_by_severity)
        findings_html = self._render_findings(data.findings)
        recommendations_html = self._render_recommendations(data.recommendations)

        html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>تقرير فحص الكود - {data.project_name}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Cairo', sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #e0e0e0; line-height: 1.8; min-height: 100vh; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
.header {{ text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #0f3460 0%, #16213e 100%); border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); }}
.header h1 {{ font-size: 2.5em; color: #e94560; margin-bottom: 10px; }}
.header .subtitle {{ color: #a0a0a0; font-size: 1.1em; }}
.score-card {{ background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%); border-radius: 20px; padding: 30px; text-align: center; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(233, 69, 96, 0.3); }}
.score-card .score {{ font-size: 4em; font-weight: 700; color: white; }}
.score-card .label {{ font-size: 1.2em; color: rgba(255,255,255,0.9); }}
.stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
.stat-card {{ background: rgba(255,255,255,0.05); border-radius: 15px; padding: 25px; border: 1px solid rgba(255,255,255,0.1); transition: transform 0.3s; }}
.stat-card:hover {{ transform: translateY(-5px); }}
.stat-card .icon {{ font-size: 2em; margin-bottom: 10px; }}
.stat-card .value {{ font-size: 2em; font-weight: 700; color: #e94560; }}
.stat-card .label {{ color: #a0a0a0; }}
.section {{ background: rgba(255,255,255,0.03); border-radius: 15px; padding: 25px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.05); }}
.section h2 {{ color: #e94560; margin-bottom: 15px; font-size: 1.5em; }}
.finding {{ background: rgba(255,255,255,0.05); border-radius: 10px; padding: 15px; margin-bottom: 10px; border-right: 4px solid #e94560; }}
.finding.critical {{ border-right-color: #ff0000; }}
.finding.high {{ border-right-color: #ff6600; }}
.finding.medium {{ border-right-color: #ffcc00; }}
.finding.low {{ border-right-color: #00cc00; }}
.severity-badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.8em; font-weight: 600; }}
.severity-critical {{ background: #ff0000; color: white; }}
.severity-high {{ background: #ff6600; color: white; }}
.severity-medium {{ background: #ffcc00; color: black; }}
.severity-low {{ background: #00cc00; color: white; }}
.code-snippet {{ background: #0d1117; border-radius: 8px; padding: 15px; margin-top: 10px; font-family: 'Fira Code', monospace; font-size: 0.9em; overflow-x: auto; direction: ltr; text-align: left; }}
.footer {{ text-align: center; padding: 30px; color: #666; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 40px; }}
.progress-bar {{ width: 100%; height: 10px; background: rgba(255,255,255,0.1); border-radius: 5px; overflow: hidden; margin-top: 10px; }}
.progress-fill {{ height: 100%; background: linear-gradient(90deg, #e94560, #ff6b6b); border-radius: 5px; transition: width 0.5s ease; }}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>Arabic Code Auditor Pro</h1>
<p class="subtitle">تقرير فحص الكود الشامل</p>
<p class="subtitle">المشروع: {data.project_name} | التاريخ: {data.scan_date}</p>
</div>
<div class="score-card">
<div class="score">{data.code_quality_score:.1f}</div>
<div class="label">درجة جودة الكود</div>
<div class="progress-bar"><div class="progress-fill" style="width: {data.code_quality_score}%;"></div></div>
</div>
<div class="stats-grid">
<div class="stat-card"><div class="icon">&#128193;</div><div class="value">{data.total_files}</div><div class="label">ملفات مفحوصة</div></div>
<div class="stat-card"><div class="icon">&#9888;&#65039;</div><div class="value">{data.total_issues}</div><div class="label">مشاكل إجمالية</div></div>
<div class="stat-card"><div class="icon">&#128274;</div><div class="value">{data.security_findings}</div><div class="label">مشاكل أمان</div></div>
<div class="stat-card"><div class="icon">&#9889;</div><div class="value">{data.performance_issues}</div><div class="label">مشاكل أداء</div></div>
</div>
<div class="section">
<h2>&#128202; توزيع المشاكل حسب الخطورة</h2>
{severity_html}
</div>
<div class="section">
<h2>&#128269; النتائج التفصيلية</h2>
{findings_html}
</div>
<div class="section">
<h2>&#128161; التوصيات</h2>
{recommendations_html}
</div>
<div class="footer">
<p>تم إنشاء هذا التقرير بواسطة Arabic Code Auditor Pro</p>
<p>وقت الفحص: {data.scan_duration:.2f} ثانية</p>
</div>
</div>
</body>
</html>"""

        output_path = os.path.join(self.output_dir, f"{data.report_id}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return output_path

    def _render_severity_chart(self, issues_by_severity: Dict[str, int]) -> str:
        colors = {{'حرج': '#ff0000', 'عالي': '#ff6600', 'متوسط': '#ffcc00', 'منخفض': '#00cc00', 'معلومة': '#0099ff'}}
        html = '<div style="display: flex; gap: 20px; flex-wrap: wrap;">'
        for severity, count in issues_by_severity.items():
            color = colors.get(severity, '#666')
            html += f'<div style="flex: 1; min-width: 150px; background: {color}20; border: 1px solid {color}; border-radius: 10px; padding: 15px; text-align: center;"><div style="font-size: 2em; font-weight: 700; color: {color};">{count}</div><div style="color: #a0a0a0;">{severity}</div></div>'
        html += '</div>'
        return html

    def _render_findings(self, findings: List[Dict[str, Any]]) -> str:
        html = ''
        for finding in findings[:50]:
            severity = finding.get('severity', 'medium').lower()
            html += f'<div class="finding {severity}"><div style="display: flex; justify-content: space-between; align-items: center;"><strong>{finding.get("message_ar", finding.get("message_en", ""))}</strong><span class="severity-badge severity-{severity}">{finding.get("severity", "متوسط")}</span></div><div style="color: #888; margin-top: 5px;">&#128196; {finding.get("file_path", "")} | السطر: {finding.get("line", 0)}</div>{f"<div class=\"code-snippet\">{finding.get(\"code_snippet\", \"\")}</div>" if finding.get("code_snippet") else ""}</div>'
        return html

    def _render_recommendations(self, recommendations: List[str]) -> str:
        html = '<ul style="list-style: none;">'
        for rec in recommendations:
            html += f'<li style="padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">&#9989; {rec}</li>'
        html += '</ul>'
        return html

    def _generate_markdown(self, data: ReportData) -> str:
        md = f"""# تقرير فحص الكود - {data.project_name}

## ملخص

| المقياس | القيمة |
|---------|--------|
| الملفات المفحوصة | {data.total_files} |
| المشاكل الإجمالية | {data.total_issues} |
| مشاكل الأمان | {data.security_findings} |
| مشاكل الأداء | {data.performance_issues} |
| درجة الجودة | {data.code_quality_score:.1f}/100 |
| وقت الفحص | {data.scan_duration:.2f} ثانية |

## توزيع المشاكل حسب الخطورة

"""
        for severity, count in data.issues_by_severity.items():
            md += f"- **{severity}**: {count}\n"
        md += "\n## النتائج التفصيلية\n\n"
        for finding in data.findings[:30]:
            md += f"### {finding.get('message_ar', '')}\n"
            md += f"- الملف: `{finding.get('file_path', '')}`\n"
            md += f"- السطر: {finding.get('line', 0)}\n"
            md += f"- الخطورة: {finding.get('severity', 'متوسط')}\n\n"
        md += "\n## التوصيات\n\n"
        for rec in data.recommendations:
            md += f"1. {rec}\n"
        output_path = os.path.join(self.output_dir, f"{data.report_id}.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
        return output_path

    def _generate_pdf(self, data: ReportData) -> str:
        output_path = os.path.join(self.output_dir, f"{data.report_id}.pdf")
        html_path = self._generate_html(data)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"PDF Report for {data.project_name}\nGenerated from: {html_path}\n")
        return output_path

    def _generate_excel(self, data: ReportData) -> str:
        output_path = os.path.join(self.output_dir, f"{data.report_id}.xlsx")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Excel Report for {data.project_name}\n")
        return output_path

_report_engine = None

def get_report_engine(output_dir: str = "reports") -> ReportEngine:
    global _report_engine
    if _report_engine is None:
        _report_engine = ReportEngine(output_dir)
    return _report_engine
