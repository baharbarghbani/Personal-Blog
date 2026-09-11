# Bahar Barghbani — Academic Portfolio

A Django academic portfolio and blog with admin-managed profile, research,
projects, posts, comments, CV downloads, and contact email delivery.

## Local development

1. Create and activate a virtual environment.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and fill in the local PostgreSQL settings.
4. Run `python manage.py migrate`.
5. Run `python manage.py runserver`.

The Django admin panel is available at `/admin/`.

## Production deployment contract

The repository is compatible with hosts that run a build command and a web
start command.

- Build command: `./build.sh`
- Start command: `./start.sh`
- Health/start port: supplied through the host's `PORT` environment variable

Required production environment variables:

- `SECRET_KEY`: a new long random production secret
- `DEBUG=False`
- `ALLOWED_HOSTS`: comma-separated hostnames without `https://`
- `CSRF_TRUSTED_ORIGINS`: comma-separated complete origins with `https://`
- `DATABASE_URL`: the PostgreSQL connection URL supplied by the host

Set `DATABASE_SSL_REQUIRE=True` only when the database provider requires SSL.

For a permanently HTTPS domain, also set:

- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`

Start with `SECURE_HSTS_SECONDS=0`. Enable HSTS only after confirming every
route and subdomain works through HTTPS, because browsers remember that policy.

## Static and uploaded files

`build.sh` collects CSS and images into `STATIC_ROOT`. WhiteNoise serves those
versioned static assets from the Django process.

Uploaded files are different. Post images, project images, and the uploaded CV
live under `MEDIA_ROOT`; WhiteNoise does not make them durable. In production,
either mount persistent storage at `MEDIA_ROOT` or configure an object-storage
backend before relying on admin uploads.

## Deploying from GitHub with Liara

[`liara.json`](liara.json) selects Liara's Django runtime, Python 3.12, Tehran
time, static-file collection, and repository-controlled Django settings. The
application remains in GitHub and can redeploy automatically from `main`.

1. In Liara, create a **Django** application and note its identifier. Its free
   hostname will be `https://<app-id>.liara.run`.
2. Create a PostgreSQL database in the same private network. From its
   **Connection** page, copy the private connection URL.
3. Create an application disk and mount it at `/data/media` so uploaded CVs and
   images survive deployments.
4. Add the production environment variables shown below in the application's
   settings. Generate `SECRET_KEY` locally; never commit its value.
5. In Liara account settings, connect GitHub and grant access only to
   `baharbarghbani/Personal-Blog`.
6. Open the application's **New deployment > GitHub** page, select the
   repository and `main`, choose automatic deployment, and deploy once.
7. In the application console, run the migration and administrator commands
   shown below.

```env
SECRET_KEY=<generated-secret>
DEBUG=False
ALLOWED_HOSTS=<app-id>.liara.run
CSRF_TRUSTED_ORIGINS=https://<app-id>.liara.run
DATABASE_URL=<private-postgresql-url>
DATABASE_SSL_REQUIRE=False
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
MEDIA_ROOT=/data/media
MEDIA_URL=/media/
SERVE_MEDIA=True
```

Generate the secret on your computer:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then initialize the production database from Liara's application console:

```bash
python manage.py migrate
python manage.py createsuperuser
```

The Contact page displays the email and professional links stored in the
Academic Profile. It does not submit a server-side form or require SMTP.
