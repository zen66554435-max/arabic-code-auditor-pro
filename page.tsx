"use client";

import { useState } from 'react';
import axios from 'axios';
import Editor from '@monaco-editor/react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const [code, setCode] = useState(`# اكتب كودك هنا
print("مرحباً بك في Arabic Code Auditor Pro")

# مثال على مشكلة أمان
API_KEY = "sk-1234567890abcdef"

# مثال على SQL Injection
user_id = input("Enter user ID: ")
query = "SELECT * FROM users WHERE id = " + user_id
`);
  const [language, setLanguage] = useState('python');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('scan');

  const handleScan = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/scan/code`, {
        code,
        language,
        file_name: `main.${language}`
      });
      setResults(response.data);
    } catch (error) {
      console.error('Scan error:', error);
      alert('Error scanning code');
    }
    setLoading(false);
  };

  const handleSecurity = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/security/check`, {
        code,
        file_name: `main.${language}`
      });
      setResults(response.data);
    } catch (error) {
      console.error('Security error:', error);
      alert('Error scanning security');
    }
    setLoading(false);
  };

  const handleFix = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/fix/code`, {
        code,
        language
      });
      setResults(response.data);
      if (response.data.fixed_code) {
        setCode(response.data.fixed_code);
      }
    } catch (error) {
      console.error('Fix error:', error);
      alert('Error fixing code');
    }
    setLoading(false);
  };

  const handleExplain = async (issueType) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/ai/explain`, {
        code,
        issue_type: issueType,
        language
      });
      setResults(response.data);
    } catch (error) {
      console.error('Explain error:', error);
    }
    setLoading(false);
  };

  const getSeverityColor = (severity) => {
    const colors = {
      'حرج': 'bg-red-600',
      'عالي': 'bg-orange-500',
      'متوسط': 'bg-yellow-500',
      'منخفض': 'bg-green-500',
      'معلومة': 'bg-blue-500'
    };
    return colors[severity] || 'bg-gray-500';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white">
      {/* Header */}
      <header className="bg-black/30 backdrop-blur-lg border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-red-500 to-pink-600 rounded-xl flex items-center justify-center text-xl font-bold">
              A
            </div>
            <div>
              <h1 className="text-xl font-bold">Arabic Code Auditor Pro</h1>
              <p className="text-xs text-gray-400">منصة فحص الأكواد العربية</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-400">المطور: الجنرال</span>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Code Editor */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex gap-2">
                <select 
                  value={language} 
                  onChange={(e) => setLanguage(e.target.value)}
                  className="bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-sm"
                >
                  <option value="python">Python</option>
                  <option value="javascript">JavaScript</option>
                  <option value="php">PHP</option>
                </select>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setActiveTab('scan')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                    activeTab === 'scan' ? 'bg-red-500 text-white' : 'bg-white/10 hover:bg-white/20'
                  }`}
                >
                  فحص
                </button>
                <button
                  onClick={() => setActiveTab('security')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                    activeTab === 'security' ? 'bg-red-500 text-white' : 'bg-white/10 hover:bg-white/20'
                  }`}
                >
                  أمان
                </button>
                <button
                  onClick={() => setActiveTab('fix')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                    activeTab === 'fix' ? 'bg-green-500 text-white' : 'bg-white/10 hover:bg-white/20'
                  }`}
                >
                  إصلاح
                </button>
              </div>
            </div>

            <div className="rounded-xl overflow-hidden border border-white/10 bg-[#1e1e1e]">
              <Editor
                height="500px"
                language={language}
                value={code}
                onChange={setCode}
                theme="vs-dark"
                options={{
                  fontSize: 14,
                  minimap: { enabled: false },
                  scrollBeyondLastLine: false,
                  rtl: true
                }}
              />
            </div>

            <button
              onClick={activeTab === 'scan' ? handleScan : activeTab === 'security' ? handleSecurity : handleFix}
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-red-500 to-pink-600 rounded-xl font-bold text-lg hover:from-red-600 hover:to-pink-700 transition disabled:opacity-50"
            >
              {loading ? 'جاري الفحص...' : activeTab === 'scan' ? '🔍 فحص الكود' : activeTab === 'security' ? '🔒 فحص الأمان' : '🔧 إصلاح تلقائي'}
            </button>
          </div>

          {/* Results */}
          <div className="space-y-4">
            <h2 className="text-xl font-bold">النتائج</h2>

            {results && (
              <div className="space-y-4">
                {/* Summary */}
                {results.total_issues !== undefined && (
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                      <div className="text-3xl font-bold text-red-400">{results.total_issues}</div>
                      <div className="text-sm text-gray-400">مشاكل إجمالية</div>
                    </div>
                    <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                      <div className="text-3xl font-bold text-green-400">{results.execution_time?.toFixed(2) || '0.00'}s</div>
                      <div className="text-sm text-gray-400">وقت الفحص</div>
                    </div>
                  </div>
                )}

                {results.total_findings !== undefined && (
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                      <div className="text-3xl font-bold text-red-400">{results.total_findings}</div>
                      <div className="text-sm text-gray-400">مشاكل أمان</div>
                    </div>
                    <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                      <div className="text-3xl font-bold text-yellow-400">{results.scan_time?.toFixed(2) || '0.00'}s</div>
                      <div className="text-sm text-gray-400">وقت الفحص</div>
                    </div>
                  </div>
                )}

                {results.fixes_applied !== undefined && (
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                      <div className="text-3xl font-bold text-green-400">{results.fixes_applied}</div>
                      <div className="text-sm text-gray-400">إصلاحات ناجحة</div>
                    </div>
                    <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                      <div className="text-3xl font-bold text-red-400">{results.fixes_failed}</div>
                      <div className="text-sm text-gray-400">إصلاحات فاشلة</div>
                    </div>
                  </div>
                )}

                {/* Issues List */}
                {results.issues && results.issues.length > 0 && (
                  <div className="space-y-2 max-h-96 overflow-y-auto">
                    {results.issues.map((issue, idx) => (
                      <div key={idx} className="bg-white/5 border-r-4 border-red-500 rounded-lg p-3">
                        <div className="flex items-center justify-between mb-1">
                          <span className={`text-xs px-2 py-1 rounded-full ${getSeverityColor(issue.severity)}`}>
                            {issue.severity}
                          </span>
                          <span className="text-xs text-gray-500">{issue.rule_id}</span>
                        </div>
                        <p className="text-sm text-gray-300">{issue.message_ar}</p>
                        <p className="text-xs text-gray-500 mt-1">السطر {issue.line}</p>
                        {issue.code_snippet && (
                          <pre className="mt-2 bg-black/30 rounded p-2 text-xs overflow-x-auto text-left" dir="ltr">
                            {issue.code_snippet}
                          </pre>
                        )}
                        {issue.fix_suggestion && (
                          <div className="mt-2 text-xs text-green-400">
                            💡 {issue.fix_suggestion}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}

                {results.findings && results.findings.length > 0 && (
                  <div className="space-y-2 max-h-96 overflow-y-auto">
                    {results.findings.map((finding, idx) => (
                      <div key={idx} className="bg-white/5 border-r-4 border-red-500 rounded-lg p-3">
                        <div className="flex items-center justify-between mb-1">
                          <span className={`text-xs px-2 py-1 rounded-full ${getSeverityColor(finding.severity)}`}>
                            {finding.severity}
                          </span>
                          <span className="text-xs text-gray-500">{finding.vuln_type}</span>
                        </div>
                        <p className="text-sm text-red-300 font-bold">{finding.message_ar}</p>
                        <p className="text-xs text-gray-400">{finding.message_en}</p>
                        <p className="text-xs text-gray-500 mt-1">السطر {finding.line} | CWE: {finding.cwe_id}</p>
                        {finding.code_snippet && (
                          <pre className="mt-2 bg-black/30 rounded p-2 text-xs overflow-x-auto text-left" dir="ltr">
                            {finding.code_snippet}
                          </pre>
                        )}
                        <div className="mt-2 text-xs text-green-400">
                          🔧 {finding.remediation_ar}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {results.explanation_ar && (
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <h3 className="font-bold text-lg mb-2">شرح المشكلة</h3>
                    <p className="text-gray-300">{results.explanation_ar}</p>
                    {results.code_example && (
                      <pre className="mt-3 bg-black/30 rounded p-3 text-sm overflow-x-auto text-left" dir="ltr">
                        {results.code_example}
                      </pre>
                    )}
                  </div>
                )}

                {results.fixed_code && (
                  <div className="bg-white/5 border border-green-500/30 rounded-xl p-4">
                    <h3 className="font-bold text-lg mb-2 text-green-400">الكود المُصلح</h3>
                    <pre className="bg-black/30 rounded p-3 text-sm overflow-x-auto text-left" dir="ltr">
                      {results.fixed_code}
                    </pre>
                  </div>
                )}

                {results.tests && (
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <h3 className="font-bold text-lg mb-2">اختبارات الوحدة</h3>
                    <pre className="bg-black/30 rounded p-3 text-sm overflow-x-auto text-left" dir="ltr">
                      {results.tests}
                    </pre>
                  </div>
                )}
              </div>
            )}

            {!results && !loading && (
              <div className="flex items-center justify-center h-96 text-gray-500">
                <div className="text-center">
                  <div className="text-6xl mb-4">🔍</div>
                  <p>اكتب كودك واضغط فحص</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
