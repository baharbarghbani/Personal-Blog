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

## Deploying from GitHub with Render

[`render.yaml`](render.yaml) defines the production web service, PostgreSQL
database, generated Django secret, HTTPS settings, and a persistent disk for
CVs and uploaded images. Both services use Render's smallest persistent paid
plans because the free PostgreSQL database expires and a free web service
cannot attach a persistent disk.

1. Push `main` to GitHub.
2. In Render, choose **New > Blueprint** and connect this GitHub repository.
3. Keep the default `render.yaml` path and apply the Blueprint.
4. Enter the requested Gmail address and App Password when Render prompts for
   secret environment variables.
5. After the first deploy, open the service shell and run
   `python manage.py createsuperuser` once to create the production admin.

Every later push to `main` automatically rebuilds and redeploys the website.
Render supplies the first `onrender.com` hostname automatically; add a custom
domain later by extending `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in the
service environment.

## Contact email

Set the SMTP variables documented in `.env.example`. For Gmail, use an App
Password rather than your normal account password.
