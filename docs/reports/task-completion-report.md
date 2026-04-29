# Fyyur Task Completion Report

## Summary

The Fyyur project has been completed against the Udacity SQL and Data Modeling for the Web rubric. The application now uses a real PostgreSQL backend, normalized SQLAlchemy models, Flask-Migrate migrations, database-backed CRUD/search/detail flows, and verified browser-accessible routes.

This project uses a PostgreSQL instance running on an existing local-network data node. Credentials and host settings are loaded from the untracked `.env` file. The application database is named `udacity`.

## Evidence

Local app screenshot:

![Fyyur running locally](../img/Screenshot%202026-04-29%20at%2021.59.57.png)

Verified app URLs:

- `http://127.0.0.1:5000/`
- `http://localhost:5000/`

HTTP curl checks completed successfully:

```text
home:200
venues:200
artists:200
shows:200
venue_search:200
artist_search:200
```

Migration state verified:

```text
20260429_0001 (head)
```

## Work Completed

- Replaced mock venue, artist, show, search, and detail data with SQLAlchemy queries.
- Added separated database models in `models.py`.
- Added normalized `Artist`, `Venue`, `Show`, and `Genre` models.
- Added many-to-many genre relationships for artists and venues.
- Added foreign-key relationships between shows, artists, and venues.
- Added Flask-Migrate setup and initial migration files.
- Added `.env` loading through `python-dotenv`.
- Configured the app to build its PostgreSQL URL from local-network `.env` settings.
- Created the `udacity` database on the configured PostgreSQL server.
- Ran `flask db upgrade` successfully.
- Verified route discovery with `flask routes`.
- Verified app pages with curl against `127.0.0.1:5000`.
- Added browser verification checklist in `docs/tests/browser-check-scenario.md`.
- Updated `README.md` with setup, migration, run, and rubric verification notes.

## Rubric Check

| Rubric Area | Status | Evidence |
| --- | --- | --- |
| Relational normalized data models | Met | `Artist`, `Venue`, `Show`, `Genre`, and association tables are defined in `models.py`. |
| Correct relationships | Met | `Show` has foreign keys to `Artist` and `Venue`; genres use many-to-many tables. |
| PostgreSQL database connection | Met | App loads `.env` and connects to the local-network PostgreSQL `udacity` database. |
| SQLAlchemy model definitions | Met | Models use SQLAlchemy columns, constraints, indexes, relationships, and foreign keys. |
| SQLAlchemy queries for endpoints | Met | List, search, show, create, edit, and detail routes use ORM queries. |
| Joined data for shows/detail pages | Met | Show, venue detail, and artist detail pages pull related artist/venue data through relationships. |
| Create records with constraints | Met | Venue, artist, and show form submissions insert database records; duplicate constraints and rollbacks are handled. |
| Search records | Met | Venue and artist search are partial and case-insensitive. |
| Venue grouping | Met | `/venues` groups venues by city and state. |
| Past/upcoming shows | Met | Artist and venue detail pages split shows by current time. |
| Migration support | Met | `flask db upgrade` creates the schema; database is at `20260429_0001 (head)`. |
| App runs without import/route errors | Met | `import app`, `flask routes`, and curl page checks passed. |
| Browser verification scenario | Met | Manual scenario documented in `docs/tests/browser-check-scenario.md`; screenshot attached as evidence. |

## Verification Notes

The real network database contains smoke-test records created during verification:

- 1 venue
- 1 artist
- 2 shows
- related genre association rows

These records demonstrate the rubric flows and can be used as seed/demo data for review.

## Out Of Scope

The following optional stand-out features were intentionally not implemented:

- artist availability and booking restrictions
- recent venues/artists on the homepage
- city/state search
- albums and songs on artist pages

## Submission Readiness

The project meets the required Udacity rubric criteria. Before final submission, ensure `.env` and `.venv/` remain untracked and submit the source files, migrations, documentation, and screenshot evidence without real credentials.
