# Fyyur

Fyyur is a musical venue and artist booking site. The starter project has been completed with real PostgreSQL persistence, normalized SQLAlchemy models, Flask-Migrate migrations, database-backed search, and create/edit/detail flows for venues, artists, and shows.

## Rubric Coverage

- PostgreSQL-backed application configuration is implemented in `config.py`.
- Models are separated into `models.py` and use normalized relationships:
  - `Artist`
  - `Venue`
  - `Show`
  - `Genre`
  - artist/venue genre association tables
- `Show` connects artists and venues with foreign keys.
- Venue and artist genres are normalized through many-to-many relationships.
- Controllers no longer use mock data for venues, artists, shows, search, or detail pages.
- Venue and artist search use partial, case-insensitive matching.
- Venue and artist detail pages split related shows into past and upcoming sections.
- Venue, artist, and show creation persist real database records.
- Venue and artist edit flows update real database records.
- Flask-Migrate migrations create the full schema.

Stand-out features such as artist availability, recent homepage listings, city/state search, and albums/songs are intentionally out of scope for this rubric-only implementation.

## Local Setup

This project uses a PostgreSQL instance that already exists in the local network. Connection details are stored in an untracked `.env` file. Do not commit real credentials.

Create `.env` from `.env.example` and provide values for:

```bash
DATA_NODE_IP=...
POSTGRES_PORT=5432
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=udacity
```

The app loads `.env` automatically. `DATABASE_URL` is supported if present; otherwise `config.py` builds the SQLAlchemy URL from the `POSTGRES_*` variables, with `DB_POSTGRESDB_*` aliases as fallbacks.

Use Python 3.9 for the dependency versions in this project:

```bash
python3.9 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Create the target database if it does not exist:

```bash
createdb udacity
```

When using a remote/local-network database, create it through your Postgres admin tooling or with the configured `.env` user if that user has `CREATEDB` privileges.

Run migrations:

```bash
FLASK_APP=app.py .venv/bin/flask db upgrade
FLASK_APP=app.py .venv/bin/flask db current
```

Expected migration state:

```text
20260429_0001 (head)
```

## Run The App

Start the development server:

```bash
FLASK_APP=app.py .venv/bin/flask run --host 127.0.0.1 --port 5000
```

Open the app at:

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

The equivalent localhost URL is:

[http://localhost:5000/](http://localhost:5000/)

## Manual Verification

A browser checklist is documented in [docs/tests/browser-check-scenario.md](docs/tests/browser-check-scenario.md).

Minimum verification before submission:

- Open `/venues`, `/artists`, and `/shows`.
- Create a venue.
- Create an artist.
- Create one future show and one past show for that venue/artist pair.
- Search for the venue and artist with partial mixed-case terms.
- Open the venue detail page and confirm past/upcoming show sections.
- Open the artist detail page and confirm matching past/upcoming show sections.
- Edit the venue and artist and confirm changes persist.
- Try creating a show with an invalid artist or venue id and confirm it is rejected.

## Project Structure

```text
app.py                  Flask application and controllers
models.py               SQLAlchemy models and relationships
forms.py                Flask-WTF forms
config.py               Environment/database configuration
migrations/             Flask-Migrate/Alembic migrations
templates/              Jinja templates
static/                 Static assets
docs/                   Planning and verification notes
```

## Notes

- `.env`, `.venv/`, `__pycache__/`, and `*.pyc` are ignored by git.
- The included migration creates all required rubric tables.
- No real credentials should be included in submitted files.
