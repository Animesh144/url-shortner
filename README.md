# URL Shortener

This project is a minimal Flask-based URL shortener. It uses SQLAlchemy and can connect to PostgreSQL via the `DATABASE_URL` environment variable. When `DATABASE_URL` is not set it falls back to a local `sqlite:///urls.db` file.

Quick start (Windows PowerShell):

```powershell
cd "d:\Online URL shortner New\url-shortner"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Start-Process -FilePath .\venv\Scripts\python.exe -ArgumentList "app.py"
Start-Sleep -Seconds 1
Start-Process "http://127.0.0.1:5000/"
```

To use PostgreSQL in production, set `DATABASE_URL` to a valid connection string, e.g.:

```
postgresql://username:password@hostname:5432/dbname
```

Deployment notes:

- On platforms like Render or Railway, create a Postgres addon and set the `DATABASE_URL` environment variable in the service settings.
- Ensure the `requirements.txt` is used during build so `psycopg2-binary` is installed.
