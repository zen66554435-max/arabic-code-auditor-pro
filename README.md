# Arabic Code Auditor Pro - Flat Structure

## ⚠️ مهم جداً

هذه النسخة **مسطحة** (بدون مجلدات). بعد التحميل يجب إعادة ترتيب الملفات.

## 🚀 التثبيت السريع

```bash
# 1. تحميل الملفات
# 2. نفذ هذا السكربت لإعادة الترتيب:

curl -sL https://raw.githubusercontent.com/GENERAL/arabic-code-auditor-pro/main/install.sh | bash
```

## 📁 إعادة الترتيب يدوياً

```bash
# إنشاء المجلدات
mkdir -p backend/src/core
mkdir -p backend/src/analyzers/python
mkdir -p backend/src/analyzers/javascript
mkdir -p backend/src/analyzers/php
mkdir -p backend/src/api
mkdir -p backend/src/cli
mkdir -p backend/src/database
mkdir -p frontend/src/app

# نقل الملفات
mv backend_src_core_*.py backend/src/core/
mv backend_src_analyzers_python_*.py backend/src/analyzers/python/
mv backend_src_analyzers_javascript_*.py backend/src/analyzers/javascript/
mv backend_src_analyzers_php_*.py backend/src/analyzers/php/
mv backend_src_api_*.py backend/src/api/
mv backend_src_cli_*.py backend/src/cli/
mv backend_src_database_*.py backend/src/database/
mv frontend_src_app_*.tsx frontend/src/app/
mv frontend_src_app_*.css frontend/src/app/

# إعادة التسمية
rename 's/backend_src_core_//' backend/src/core/*.py
rename 's/backend_src_analyzers_python_//' backend/src/analyzers/python/*.py
rename 's/backend_src_analyzers_javascript_//' backend/src/analyzers/javascript/*.py
rename 's/backend_src_analyzers_php_//' backend/src/analyzers/php/*.py
rename 's/backend_src_api_//' backend/src/api/*.py
rename 's/backend_src_cli_//' backend/src/cli/*.py
rename 's/backend_src_database_//' backend/src/database/*.py
rename 's/frontend_src_app_//' frontend/src/app/*
```

## 📋 قائمة الملفات

| # | الملف | الوصف |
|---|-------|-------|
| 1 | README.md | ملف التعريف |
| 2 | LICENSE | الترخيص |
| 3 | CONTRIBUTING.md | دليل المساهمة |
| 4 | CHANGELOG.md | سجل التغييرات |
| 5 | .env | متغيرات البيئة |
| 6 | .gitignore | استثناءات Git |
| 7 | install.sh | تثبيت سريع |
| 8 | uninstall.sh | إلغاء التثبيت |
| 9 | update.sh | تحديث |
| 10 | setup-termux.sh | تثبيت Termux |
| 11 | docker-compose.yml | Docker |
| 12 | backend_requirements.txt | متطلبات Python |
| 13 | backend_Dockerfile | Docker Backend |
| 14 | backend_setup_cython.py | Cython |
| 15 | backend_aca.spec | PyInstaller |
| 16 | backend_obfuscate.py | تشويش |
| 17 | backend_build.sh | بناء |
| 18-24 | backend_src_core_*.py | المحركات الأساسية |
| 25-36 | backend_src_analyzers_*.py | المحللات |
| 37-38 | backend_src_api_*.py | API |
| 39-40 | backend_src_cli_*.py | CLI |
| 41-42 | backend_src_database_*.py | قاعدة البيانات |
| 43-48 | frontend_*.json/js/css/tsx | Frontend |

## 👤 المطور

**الجنرال**
