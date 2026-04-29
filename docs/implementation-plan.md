# Fyyur Database Implementation Specification

## Summary
This implementation replaces the Fyyur starter project's mock data with a PostgreSQL-backed SQLAlchemy data layer. It targets the required Udacity rubric only: normalized models, migration support, real create/edit/search/detail/show flows, and controller responses that preserve the existing template data shapes.

## Data Model
- `Venue` stores venue profile fields, contact links, seeking-talent metadata, timestamps, and a duplicate-prevention constraint on `name`, `city`, `state`, and `address`.
- `Artist` stores artist profile fields, contact links, seeking-venue metadata, timestamps, and a duplicate-prevention constraint on `name`, `city`, and `state`.
- `Show` connects one artist to one venue at a `start_time` using foreign keys, with indexes for artist/venue show lookups and past/upcoming splits.
- `Genre` normalizes genre names and connects to artists and venues through many-to-many association tables.
- Models live in `models.py`; `app.py` initializes `db` and `Flask-Migrate`.

## Application Behavior
- `config.py` reads `DATABASE_URL` first and falls back to `postgresql://localhost:5432/fyyur`.
- `/venues` queries venues from the database, groups them by city/state, and includes upcoming-show counts.
- `/artists` lists database artists by id and name.
- `/shows` joins shows with artists and venues and returns the existing show-card shape.
- Venue and artist search use case-insensitive partial name matching.
- Venue and artist detail pages query one record by id, return genres as string lists, expose `website` from `website_link`, and split shows into past/upcoming lists.
- Create/edit routes validate WTForms, persist scalar fields and genre associations, commit on success, rollback and flash on database errors.
- Show creation validates the form and verifies referenced artist and venue ids before inserting.

## Migration And Setup
- `requirements.txt` includes `Flask-Migrate` and `psycopg2-binary`.
- `migrations/` contains a single initial Alembic revision that creates artists, venues, shows, genres, and genre association tables.
- Expected local setup:
  - Create a PostgreSQL database named `fyyur`, or set `DATABASE_URL`.
  - Run `flask db upgrade` to create tables from the included migration.
  - Use `flask db migrate` for future schema changes.

## Validation And Acceptance Checks
- Create an artist, venue, and show; verify they appear in `/artists`, `/venues`, `/shows`, and search results.
- Search with mixed-case partial names and confirm matching rows are returned.
- Open artist and venue detail pages and confirm the same show appears in matching past/upcoming sections.
- Edit artist and venue fields, including genres and seeking flags, and confirm updates persist.
- Submit invalid forms or invalid show ids and confirm errors are flashed without creating rows.

## Assumptions
- Stand-out features such as recent listings, city/state search, albums/songs, and artist availability are out of scope.
- Local PostgreSQL availability is assumed; no seed data is included.
- Existing templates remain the public contract for controller data shapes.
