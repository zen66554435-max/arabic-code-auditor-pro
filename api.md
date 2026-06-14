# دليل API

## التشغيل

```bash
cd backend
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

## Endpoints

### فحص كود

```bash
POST /scan/code
Content-Type: application/json

{
  "code": "print('Hello')",
  "language": "python",
  "file_name": "test.py"
}
```

### فحص أمان

```bash
POST /security/check
Content-Type: application/json

{
  "code": "API_KEY = 'secret'",
  "file_name": "test.py"
}
```

### إصلاح تلقائي

```bash
POST /fix/code
Content-Type: application/json

{
  "code": "x = 1


y = 2",
  "language": "python"
}
```

### شرح AI

```bash
POST /ai/explain
Content-Type: application/json

{
  "code": "API_KEY = 'secret'",
  "issue_type": "hardcoded_secret",
  "language": "python"
}
```
