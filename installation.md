# دليل التثبيت

## Termux

### المتطلبات
- Android 7.0+
- Termux من F-Droid

### الخطوات

1. تحديث الحزم
```bash
pkg update && pkg upgrade -y
```

2. تثبيت Python
```bash
pkg install -y python python-pip
```

3. تحميل المشروع
```bash
git clone https://github.com/GENERAL/arabic-code-auditor-pro.git
cd arabic-code-auditor-pro
```

4. تثبيت المتطلبات
```bash
pip install -r backend/requirements.txt
```

5. تشغيل
```bash
cd backend
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

## Linux/Mac

```bash
# تثبيت Python 3.11+
# تثبيت Node.js 18+

git clone https://github.com/GENERAL/arabic-code-auditor-pro.git
cd arabic-code-auditor-pro
pip install -r backend/requirements.txt
cd frontend && npm install
```

## Windows

```powershell
# تثبيت Python من python.org
# تثبيت Node.js من nodejs.org

git clone https://github.com/GENERAL/arabic-code-auditor-pro.git
cd arabic-code-auditor-pro
pip install -r backend/requirements.txt
cd frontend
npm install
```
