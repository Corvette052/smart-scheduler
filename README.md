# Smart Scheduler

This Django project uses a `Procfile` for deployment. The file tells the platform to run:

```
web gunicorn scheduler.wsgi
```

Make sure the file is named `Procfile` (without extension) in the repository root.
