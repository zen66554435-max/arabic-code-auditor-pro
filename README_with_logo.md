<div align="center">

<img src="logo.png" alt="Arabic Code Auditor Pro" width="250">

# 🔍 Arabic Code Auditor Pro

**منصة عربية متكاملة لتحليل الأكواد وإصلاحها وشرحها وفحصها أمنياً**

[![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge)](https://github.com/zen66554435-max/arabic-code-auditor-pro)
[![Python](https://img.shields.io/badge/Python-3.11+-green?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Termux](https://img.shields.io/badge/Termux-Supported-black?style=for-the-badge&logo=android)](https://termux.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react)](https://react.dev)

### تطوير عربي مفتوح المصدر

</div>

---

## 🚀 التثبيت السريع (أمر واحد)

### Termux / Linux / Mac

```bash
curl -sL https://raw.githubusercontent.com/zen66554435-max/arabic-code-auditor-pro/main/install.sh | bash
```

### أو بـ Git

```bash
git clone https://github.com/zen66554435-max/arabic-code-auditor-pro.git && cd arabic-code-auditor-pro && bash install.sh
```

### بعد التثبيت

```bash
# فحص ملف
aca scan app.py

# فحص أمان
aca security app.py

# إصلاح تلقائي
aca fix app.py --apply

# تشغيل API
aca-api

# تشغيل Frontend
aca-frontend
```

---

## 📋 جدول المحتويات

- [🎯 نظرة عامة](#-نظرة-عامة)
- [✨ المميزات](#-المميزات)
- [🚀 التثبيت على Termux](#-التثبيت-على-termux)
- [🖥️ التشغيل على Linux/Mac/Windows](#️-التشغيل-على-linuxmacwindows)
- [🔧 استخدام CLI](#-استخدام-cli)
- [🌐 استخدام API](#-استخدام-api)
- [🎨 الواجهة الرسومية](#-الواجهة-الرسومية)
- [🏗️ هيكل المشروع](#️-هيكل-المشروع)
- [📊 المحركات الأساسية](#-المحركات-الأساسية)
- [🔌 نظام الإضافات](#-نظام-الإضافات)
- [🐳 Docker](#-docker)
- [📱 Mobile App](#-mobile-app)
- [🖥️ Desktop App](#️-desktop-app)
- [⚠️ حل المشاكل الشائعة](#️-حل-المشاكل-الشائعة)
- [🤝 المساهمة](#-المساهمة)
- [📄 الترخيص](#-الترخيص)
- [📞 التواصل](#-التواصل)

---

## 🎯 نظرة عامة

**Arabic Code Auditor Pro** هي منصة عربية متكاملة لتحليل الأكواد البرمجية وإصلاحها وشرحها وفحصها أمنياً. تدعم المنصة لغات برمجة متعددة (Python, JavaScript, PHP) وتقدم تقارير احترافية باللغة العربية مع دعم كامل للـ RTL.

### الرؤية
> بناء منصة عربية متكاملة لتحليل الأكواد وإصلاحها وشرحها وفحصها أمنياً وتقييم جودتها وإدارة المشاريع البرمجية من واجهة واحدة.

---

## ✨ المميزات

| الميزة | الوصف | الحالة |
|--------|-------|--------|
| 🔍 **تحليل ساكن** | فحص Python, JavaScript, PHP بأدوات احترافية | ✅ |
| 🔒 **فحص أمان** | كشف الأسرار, SQL Injection, XSS, SSRF, Command Injection | ✅ |
| 🤖 **ذكاء اصطناعي** | شرح الأخطاء بالعربية, اقتراح الإصلاحات, تحسين الأداء | ✅ |
| 🔧 **إصلاح تلقائي** | إصلاح Syntax, Imports, Formatting, Dead Code | ✅ |
| 📊 **تقارير متعددة** | PDF, HTML, JSON, Excel, Markdown مع تصميم RTL | ✅ |
| 🎨 **واجهة عربية** | React + Next.js مع دعم RTL كامل وخط Cairo | ✅ |
| ⚡ **CLI** | سطر أوامر للاستخدام السريع | ✅ |
| 🔌 **نظام إضافات** | Plugin System مع Marketplace وSandbox | ✅ |
| 🐳 **Docker** | دعم Docker و Docker Compose | ✅ |
| 📱 **Mobile** | تطبيق Flutter (قيد التطوير) | 🚧 |
| 🖥️ **Desktop** | تطبيق Tauri (قيد التطوير) | 🚧 |
| 🔗 **GitHub/GitLab** | تكامل مع منصات التطوير (قيد التطوير) | 🚧 |

---

## 🚀 التثبيت على Termux

### المتطلبات
- Android 7.0+
- Termux من F-Droid (**ليس من Google Play**)
- 500MB مساحة فارغة

### الطريقة السريعة (ننصح بها)

```bash
# 1. تحديث الحزم
pkg update && pkg upgrade -y

# 2. تثبيت الأساسيات
pkg install -y python python-pip git curl wget unzip

# 3. تحميل المشروع
cd $HOME
git clone https://github.com/zen66554435-max/arabic-code-auditor-pro.git
cd arabic-code-auditor-pro

# 4. تشغيل سكربت التثبيت
chmod +x setup-termux.sh
bash setup-termux.sh
```

### الطريقة اليدوية

```bash
# 1. تحديث الحزم
pkg update && pkg upgrade -y

# 2. تثبيت Python و Node.js
pkg install -y python python-pip nodejs git

# 3. تثبيت PostgreSQL (اختياري)
pkg install -y postgresql

# 4. تثبيت Redis (اختياري)
pkg install -y redis

# 5. الذهاب لمجلد المشروع
cd $HOME/arabic-code-auditor-pro

# 6. تثبيت متطلبات Python
pip install fastapi uvicorn pydantic sqlalchemy python-multipart aiofiles httpx python-dotenv

# 7. تثبيت أدوات التحليل
pip install ruff pylint mypy bandit radon black

# 8. إنشاء قاعدة البيانات
python -c "from backend.src.database.models import init_db; init_db('sqlite:///aca.db')"
```

### تشغيل API على Termux

```bash
# Terminal 1 - تشغيل API
cd $HOME/arabic-code-auditor-pro/backend
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

ستظهر:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### تشغيل CLI على Termux

```bash
# Terminal 2 - استخدام CLI
cd $HOME/arabic-code-auditor-pro/backend

# فحص ملف
python -m src.cli.main scan /path/to/file.py

# فحص أمان
python -m src.cli.main security /path/to/file.py

# إصلاح تلقائي
python -m src.cli.main fix /path/to/file.py --apply
```

### تشغيل Frontend على Termux

```bash
# Terminal 3 - تشغيل الواجهة
cd $HOME/arabic-code-auditor-pro/frontend
npm install
npm run dev
```

افتح المتصفح:
```bash
termux-open-url http://localhost:3000
```

---

## 🖥️ التشغيل على Linux/Mac/Windows

### المتطلبات
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (اختياري)
- Redis 7+ (اختياري)

### التثبيت

```bash
# 1. تحميل المشروع
git clone https://github.com/zen66554435-max/arabic-code-auditor-pro.git
cd arabic-code-auditor-pro

# 2. تثبيت متطلبات Backend
cd backend
pip install -r requirements.txt

# 3. تثبيت أدوات التحليل
pip install ruff pylint mypy bandit radon

# 4. تثبيت متطلبات Frontend
cd ../frontend
npm install
```

### التشغيل

```bash
# Terminal 1 - API
cd backend
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd frontend
npm run dev

# Terminal 3 - CLI
cd backend
python -m src.cli.main scan file.py
```

---

## 🔧 استخدام CLI

### الأوامر المتاحة

```bash
# ─────────────────────────────────────────
# 🔍 فحص ملف أو مشروع
# ─────────────────────────────────────────
aca scan <file.py>                    # فحص ملف
aca scan <project.zip>                # فحص مشروع ZIP
aca scan <directory/>                 # فحص مجلد
aca scan file.py --format json        # إخراج JSON
aca scan file.py --format html        # إخراج HTML

# ─────────────────────────────────────────
# 🔒 فحص أمان
# ─────────────────────────────────────────
aca security <file.py>                # فحص أمان ملف
aca security <project.zip>            # فحص أمان مشروع
aca security <directory/>             # فحص أمان مجلد

# ─────────────────────────────────────────
# 🔧 إصلاح تلقائي
# ─────────────────────────────────────────
aca fix <file.py>                     # معاينة الإصلاحات
aca fix <file.py> --apply             # تطبيق الإصلاحات
aca fix <project.zip> --apply         # إصلاح مشروع كامل

# ─────────────────────────────────────────
# 📄 توليد تقارير
# ─────────────────────────────────────────
aca report <project.zip>              # تقرير HTML (افتراضي)
aca report <project.zip> --format pdf
aca report <project.zip> --format json
aca report <project.zip> --format excel
aca report <project.zip> -o ./reports # مجلد الإخراج

# ─────────────────────────────────────────
# 📊 معلومات
# ─────────────────────────────────────────
aca --help                            # مساعدة
aca --version                         # الإصدار
```

### أمثلة عملية

```bash
# فحص ملف Python
aca scan app.py

# فحص أمان وكشف أسرار
aca security config.py

# إصلاح تلقائي مع نسخ احتياطي
aca fix app.py --apply

# فحص مشروع كامل
aca scan ./my-project/

# توليد تقرير HTML
aca report ./my-project/ --format html -o ./reports

# فحص وإصلاح في خطوة واحدة
aca scan app.py && aca fix app.py --apply
```

---

## 🌐 استخدام API

### تشغيل API

```bash
cd backend
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### الوثائق التفاعلية
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

| Method | Endpoint | الوصف |
|--------|----------|-------|
| `GET` | `/` | معلومات API |
| `GET` | `/health` | فحص الحالة |
| `POST` | `/scan/code` | فحص كود مباشر |
| `POST` | `/scan/project` | فحص مشروع ZIP |
| `POST` | `/fix/code` | إصلاح تلقائي |
| `POST` | `/security/check` | فحص أمان |
| `POST` | `/ai/explain` | شرح AI |
| `POST` | `/ai/optimize` | تحسين AI |
| `POST` | `/ai/generate-tests` | توليد اختبارات |
| `POST` | `/report/generate` | توليد تقرير |

### أمثلة curl

```bash
# فحص كود
 curl -X POST http://localhost:8000/scan/code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "API_KEY = \"sk-1234567890abcdef\"\nprint(\"Hello\")",
    "language": "python",
    "file_name": "test.py"
  }'

# فحص أمان
 curl -X POST http://localhost:8000/security/check \
  -H "Content-Type: application/json" \
  -d '{
    "code": "import os\nos.system(input(\"Enter: \"))",
    "file_name": "test.py"
  }'

# إصلاح تلقائي
 curl -X POST http://localhost:8000/fix/code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "x = 1\n\n\ny = 2\n",
    "language": "python"
  }'

# شرح AI
 curl -X POST http://localhost:8000/ai/explain \
  -H "Content-Type: application/json" \
  -d '{
    "code": "API_KEY = \"secret123\"",
    "issue_type": "hardcoded_secret",
    "language": "python"
  }'

# توليد اختبارات
 curl -X POST http://localhost:8000/ai/generate-tests \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add(a, b):\n    return a + b",
    "language": "python"
  }'
```

---

## 🎨 الواجهة الرسومية

### المميزات
- ✅ دعم RTL كامل
- ✅ خط Cairo العربي
- ✅ Monaco Editor مع تلوين الأكواد
- ✅ تصميم Dark Mode
- ✅ رسوم بيانية تفاعلية
- ✅ شرح فوري بالعربية

### التشغيل

```bash
cd frontend
npm install
npm run dev
```

افتح: http://localhost:3000

---

## 🏗️ هيكل المشروع

```
arabic-code-auditor-pro/
├── 📁 backend/
│   ├── 📁 src/
│   │   ├── 📁 core/                    # المحركات الأساسية
│   │   │   ├── analyzer_engine.py      # محرك التحليل
│   │   │   ├── fixer_engine.py         # محرك الإصلاح
│   │   │   ├── security_engine.py      # محرك الأمان
│   │   │   ├── ai_engine.py            # محرك الذكاء الاصطناعي
│   │   │   ├── report_engine.py        # محرك التقارير
│   │   │   └── plugin_engine.py        # محرك الإضافات
│   │   ├── 📁 analyzers/
│   │   │   ├── 📁 python/              # Ruff, Pylint, MyPy, Bandit, Radon
│   │   │   ├── 📁 javascript/          # ESLint, Prettier
│   │   │   └── 📁 php/                 # PHPStan, PHP-CS-Fixer
│   │   ├── 📁 api/                     # REST API (FastAPI)
│   │   ├── 📁 cli/                     # سطر الأوامر
│   │   ├── 📁 database/                # نماذج قاعدة البيانات
│   │   └── 📁 plugins/                 # الإضافات
│   ├── requirements.txt
│   └── Dockerfile
│
├── 📁 frontend/                        # React + Next.js
│   ├── 📁 src/app/
│   │   ├── page.tsx                    # الصفحة الرئيسية
│   │   ├── layout.tsx                  # التخطيط
│   │   └── globals.css                 # الأنماط
│   ├── package.json
│   └── next.config.js
│
├── 📁 devops/
│   ├── docker-compose.yml
│   └── 📁 scripts/
│
├── 📁 docs/                            # التوثيق
│   ├── 📁 ar/                          # العربية
│   └── 📁 en/                          # الإنجليزية
│
├── .env                                # متغيرات البيئة
├── .gitignore
├── setup-termux.sh                     # سكربت Termux
└── README.md                           # هذا الملف
```

---

## 📊 المحركات الأساسية

### 🔍 Analyzer Engine
- اكتشاف لغة البرمجة تلقائياً
- تشغيل متوازي للمحللات
- دعم Python, JavaScript, PHP
- مقاييس التعقيد والجودة

### 🔒 Security Engine
- **كشف الأسرار**: API Keys, Tokens, Passwords, AWS Keys, GitHub Tokens
- **فحص الثغرات**:
  - SQL Injection
  - XSS (Cross-Site Scripting)
  - SSRF (Server-Side Request Forgery)
  - Command Injection
  - Path Traversal
- تصنيف CWE و OWASP Top 10

### 🤖 AI Engine
- **شرح الأخطاء بالعربية**: شرح مفصل لكل مشكلة
- **اقتراح الإصلاحات**: كود قبل وبعد الإصلاح
- **تحسين الأداء**: List Comprehension, Set lookup, إلخ
- **إعادة الهيكلة**: تقسيم الدوال المعقدة
- **توليد التوثيق**: Docstrings تلقائية
- **توليد Unit Tests**: اختبارات وحدة جاهزة

### 🔧 Fixer Engine
- إصلاح Syntax Errors
- إصلاح Imports غير المستخدمة
- إصلاح Formatting (trailing whitespace, blank lines)
- إزالة Dead Code
- إزالة Unused Variables
- نسخ احتياطي تلقائي

### 📊 Report Engine
- **HTML Reports**: تصميم RTL احترافي مع خط Cairo
- **PDF Reports**: تقارير PDF قابلة للطباعة
- **JSON Reports**: بيانات خام للتكامل
- **Excel Reports**: جداول Excel
- **Markdown Reports**: ملفات Markdown

---

## 🔌 نظام الإضافات

### إنشاء إضافة جديدة

```bash
# إنشاء قالب إضافة
python -c "
from backend.src.core.plugin_engine import get_plugin_engine
engine = get_plugin_engine()
engine.create_plugin_template(
    'my-plugin',
    'My Plugin',
    'إضافتي',
    PluginType.CUSTOM
)
"
```

### هيكل الإضافة

```
plugins/my-plugin/
├── manifest.json          # بيانات الإضافة
├── main.py               # نقطة الدخول
└── README.md             # التوثيق
```

### manifest.json

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "name_ar": "إضافتي",
  "version": "1.0.0",
  "author": "الجنرال",
  "description": "Custom analyzer plugin",
  "description_ar": "إضافة محلل مخصص",
  "type": "analyzer",
  "entry_point": "main.py",
  "config": {},
  "enabled": true,
  "sandboxed": true
}
```

---

## 🐳 Docker

### بناء وتشغيل

```bash
# بناء الصور
 docker-compose up --build

# تشغيل في الخلفية
 docker-compose up -d

# عرض السجلات
 docker-compose logs -f api

# إيقاف
 docker-compose down
```

### الخدمات

| الخدمة | المنفذ | الوصف |
|--------|--------|-------|
| API | 8000 | خادم FastAPI |
| Frontend | 3000 | واجهة Next.js |
| PostgreSQL | 5432 | قاعدة البيانات |
| Redis | 6379 | التخزين المؤقت |

---

## 📱 Mobile App

تطبيق Flutter قيد التطوير...

```bash
cd mobile
flutter pub get
flutter run
```

---

## 🖥️ Desktop App

تطبيق Tauri قيد التطوير...

```bash
cd desktop
npm install
cargo tauri dev
```

---

## ⚠️ حل المشاكل الشائعة

### 🔴 مشاكل Termux

| المشكلة | السبب | الحل |
|---------|-------|------|
| `command not found: python` | Python غير مثبت | `pkg install python` |
| `No module named 'fastapi'` | المتطلبات غير مثبتة | `pip install -r requirements.txt` |
| `Port 8000 in use` | منفذ مشغول | `kill $(lsof -t -i:8000)` أو غير البورت |
| `Permission denied` | صلاحيات | `chmod +x setup-termux.sh` |
| `Out of memory` | ذاكرة غير كافية | أغلق التطبيقات الأخرى |
| `pkg install failed` | مشكلة في المصادر | `termux-change-repo` |
| `pip install failed` | مشكلة في الشبكة | `pip install --upgrade pip` |
| `uvicorn not found` | Uvicorn غير مثبت | `pip install uvicorn[standard]` |
| `node not found` | Node.js غير مثبت | `pkg install nodejs` |
| `npm install failed` | مشكلة في npm | `npm cache clean --force` |

### 🔴 مشاكل Python

| المشكلة | السبب | الحل |
|---------|-------|------|
| `ModuleNotFoundError` | مكتبة ناقصة | `pip install <package>` |
| `ImportError` | تعارض في الإصدارات | `pip install --upgrade <package>` |
| `SyntaxError` | خطأ في الكود | راجع الكود المصدري |
| `TypeError` | نوع بيانات خاطئ | راجع توثيق API |
| `Connection refused` | API لا يعمل | تأكد من تشغيل `uvicorn` |
| `Database locked` | SQLite مشغول | أغلق العمليات الأخرى |

### 🔴 مشاكل الأمان

| المشكلة | السبب | الحل |
|---------|-------|------|
| `bandit not found` | Bandit غير مثبت | `pip install bandit` |
| `ruff not found` | Ruff غير مثبت | `pip install ruff` |
| `pylint not found` | Pylint غير مثبت | `pip install pylint` |
| `mypy not found` | MyPy غير مثبت | `pip install mypy` |
| `radon not found` | Radon غير مثبت | `pip install radon` |

### 🔴 مشاكل الواجهة

| المشكلة | السبب | الحل |
|---------|-------|------|
| `localhost refused` | Frontend لا يعمل | تأكد من `npm run dev` |
| `CORS error` | سياسة CORS | API يعمل على `0.0.0.0` |
| `Blank page` | خطأ في React | افتح Console في المتصفح |
| `RTL not working` | مشكلة في CSS | تأكد من `dir="rtl"` |

### 🔴 مشاكل Docker

| المشكلة | السبب | الحل |
|---------|-------|------|
| `docker not found` | Docker غير مثبت | `pkg install docker` |
| `port already allocated` | منفذ مشغول | غير المنفذ في docker-compose.yml |
| `volume error` | مشكلة في Volumes | `docker-compose down -v` |
| `build failed` | خطأ في Dockerfile | راجع سجلات البناء |

### 🔴 مشاكل GitHub

| المشكلة | السبب | الحل |
|---------|-------|------|
| `git push failed` | صلاحيات | استخدم SSH أو Token |
| `large files` | ملفات كبيرة | استخدم Git LFS |
| `merge conflict` | تعارض | حل التعارض يدوياً |

---

## 🤝 المساهمة



---

### ❤️ كلمة أخيرة

صُنِع هذا المشروع بأيدٍ عربية، بشغف نحو بناء أدوات تقنية احترافية تخدم المطورين العرب وتُثري المحتوى التقني العربي.

⭐ إذا أعجبك المشروع فلا تنسَ دعم المستودع بنجمة.
