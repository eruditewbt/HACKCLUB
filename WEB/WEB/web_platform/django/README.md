# Django SaaS app
This is a minimal Django scaffold for the “main app” dashboard/admin.

Production features to extend:
- orgs/teams + RBAC
- subscription and entitlements UI
- audit log browsing
- API key management UI

## Setup
```bash
pip install -r WEB/django/saas_app/requirements.txt
python WEB/django/saas_app/manage.py migrate
python WEB/django/saas_app/manage.py runserver
```

