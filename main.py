#!/usr/bin/env python3
"""
Arabic Code Auditor Pro - CLI
"""
import argparse
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.analyzer_engine import get_analyzer_engine
from core.fixer_engine import get_fixer_engine
from core.security_engine import get_security_engine
from core.report_engine import get_report_engine, ReportData, ReportFormat

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     Arabic Code Auditor Pro - منصة فحص الأكواد العربية     ║
    ║                                                              ║
    ║     المطور: الجنرال                                          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def main():
    parser = argparse.ArgumentParser(
        description="Arabic Code Auditor Pro - CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  aca scan file.py
  aca scan project.zip
  aca fix file.py
  aca security file.py
  aca report project.zip --format html
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan code or project')
    scan_parser.add_argument('target', help='File or directory to scan')
    scan_parser.add_argument('--format', choices=['json', 'html', 'console'], default='console')

    # Fix command
    fix_parser = subparsers.add_parser('fix', help='Auto-fix code issues')
    fix_parser.add_argument('target', help='File or directory to fix')
    fix_parser.add_argument('--apply', action='store_true', help='Apply fixes automatically')

    # Security command
    security_parser = subparsers.add_parser('security', help='Security scan')
    security_parser.add_argument('target', help='File or directory to scan')

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate report')
    report_parser.add_argument('target', help='File or directory')
    report_parser.add_argument('--format', choices=['html', 'json', 'pdf', 'excel'], default='html')
    report_parser.add_argument('--output', '-o', help='Output directory')

    args = parser.parse_args()

    if not args.command:
        print_banner()
        parser.print_help()
        return

    asyncio.run(run_command(args))

async def run_command(args):
    if args.command == 'scan':
        await scan_command(args)
    elif args.command == 'fix':
        await fix_command(args)
    elif args.command == 'security':
        await security_command(args)
    elif args.command == 'report':
        await report_command(args)

async def scan_command(args):
    engine = get_analyzer_engine()

    if os.path.isfile(args.target):
        result = await engine.analyze_file(args.target)
        print(f"\n[+] Scanned: {result.file_path}")
        print(f"[+] Issues found: {result.total_issues}")
        print(f"[+] Language: {result.language.value}")
        print(f"[+] Execution time: {result.execution_time:.2f}s")

        if result.issues:
            print("\n[!] Issues:")
            for issue in result.issues:
                print(f"    [{issue.severity.value}] Line {issue.line}: {issue.message_ar}")
                if issue.fix_suggestion:
                    print(f"    -> Fix: {issue.fix_suggestion}")
        else:
            print("\n[✓] No issues found!")
    else:
        print(f"\n[*] Scanning project: {args.target}")
        results = await engine.analyze_project(args.target)
        summary = engine.get_summary(results)

        print(f"\n[+] Project scan complete!")
        print(f"[+] Files scanned: {summary['total_files']}")
        print(f"[+] Total issues: {summary['total_issues']}")
        print(f"[+] By severity: {summary['issues_by_severity']}")
        print(f"[+] By language: {summary['issues_by_language']}")
        print(f"[+] Total time: {summary['total_execution_time']:.2f}s")

async def fix_command(args):
    engine = get_fixer_engine()
    if os.path.isfile(args.target):
        print(f"\n[*] Fixing: {args.target}")
        result = await engine.fix_file(args.target, auto_apply=args.apply)

        print(f"[+] Fixes applied: {len(result.fixes_applied)}")
        print(f"[+] Fixes failed: {len(result.fixes_failed)}")

        if result.fixes_applied:
            print("\n[!] Applied fixes:")
            for fix in result.fixes_applied:
                print(f"    [{fix.fix_type.value}] {fix.description_ar}")

        if result.backup_path:
            print(f"\n[+] Backup saved: {result.backup_path}")
    else:
        print("[!] Directory fix not yet implemented")

async def security_command(args):
    engine = get_security_engine()
    if os.path.isfile(args.target):
        print(f"\n[*] Security scanning: {args.target}")
        result = await engine.scan_file(args.target)

        print(f"[+] Security findings: {result.total_findings}")
        print(f"[+] Scan time: {result.scan_time:.2f}s")

        if result.findings:
            print("\n[!] Security Issues:")
            for finding in result.findings:
                print(f"    [{finding.severity.value}] {finding.vuln_type.value}")
                print(f"    Line {finding.line}: {finding.message_ar}")
                print(f"    CWE: {finding.cwe_id} | OWASP: {finding.owasp_category}")
                print(f"    Fix: {finding.remediation_ar}\n")
        else:
            print("\n[✓] No security issues found!")
    else:
        print(f"\n[*] Security scanning project: {args.target}")
        results = await engine.scan_project(args.target)
        summary = engine.get_summary(results)

        print(f"\n[+] Security scan complete!")
        print(f"[+] Files with issues: {summary['total_files_scanned']}")
        print(f"[+] Total findings: {summary['total_findings']}")
        print(f"[+] By severity: {summary['findings_by_severity']}")
        print(f"[+] By type: {summary['findings_by_type']}")

async def report_command(args):
    print(f"\n[*] Generating {args.format} report for {args.target}...")
    print("[+] Report generation complete (placeholder)")

if __name__ == '__main__':
    main()
