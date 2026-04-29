# Browser Check Scenario

Use this checklist for the final manual browser pass before submitting the Udacity project.

## Environment

- App URL: http://127.0.0.1:5000/
- Alternate app URL: http://localhost:5000/
- Database: PostgreSQL database named `udacity`
- Database location: local-network PostgreSQL instance configured by the untracked `.env` file
- Required migration state: `20260429_0001 (head)`

Start the app:

```bash
FLASK_APP=app.py .venv/bin/flask run --host 127.0.0.1 --port 5000
```

## Preflight

1. Visit http://127.0.0.1:5000/.
2. Confirm the home page renders without a server error.
3. Visit http://127.0.0.1:5000/venues.
4. Visit http://127.0.0.1:5000/artists.
5. Visit http://127.0.0.1:5000/shows.

Expected result: all pages load with the Fyyur layout and no stack trace.

## Create Venue

1. Open http://127.0.0.1:5000/venues/create.
2. Submit a venue with:
   - Name: `Browser Test Venue`
   - City: `San Francisco`
   - State: `CA`
   - Address: `500 Browser Test Ave`
   - Phone: `415-555-0100`
   - Genre: `Jazz`
   - Website: `https://example.com/browser-venue`
   - Image: `https://example.com/browser-venue.jpg`
   - Seeking talent: checked
   - Seeking description: `Looking for local artists.`
3. Open http://127.0.0.1:5000/venues.

Expected result: the venue appears under `San Francisco, CA`.

## Create Artist

1. Open http://127.0.0.1:5000/artists/create.
2. Submit an artist with:
   - Name: `Browser Test Artist`
   - City: `San Francisco`
   - State: `CA`
   - Phone: `415-555-0101`
   - Genre: `Jazz`
   - Website: `https://example.com/browser-artist`
   - Image: `https://example.com/browser-artist.jpg`
   - Seeking venue: checked
   - Seeking description: `Available for local shows.`
3. Open http://127.0.0.1:5000/artists.

Expected result: the artist appears in the artist list.

## Create Shows

1. Open the created venue detail page and note the venue ID.
2. Open the created artist detail page and note the artist ID.
3. Open http://127.0.0.1:5000/shows/create.
4. Create a future show:
   - Artist ID: the created artist ID
   - Venue ID: the created venue ID
   - Start time: `2035-04-01 20:00`
5. Open http://127.0.0.1:5000/shows/create again.
6. Create a past show:
   - Artist ID: the created artist ID
   - Venue ID: the created venue ID
   - Start time: `2019-05-21 21:30`
7. Open http://127.0.0.1:5000/shows.

Expected result: both shows appear with the artist and venue names.

## Search

1. Open http://127.0.0.1:5000/venues.
2. Search for `browser venue`.
3. Open http://127.0.0.1:5000/artists.
4. Search for `BROWSER ARTIST`.

Expected result: search is partial and case-insensitive; the created venue and artist are returned.

## Detail Pages

1. Open the created venue detail page.
2. Confirm the created artist appears once in upcoming shows and once in past shows.
3. Open the created artist detail page.
4. Confirm the created venue appears once in upcoming shows and once in past shows.
5. From the artist page, click the venue link for the upcoming show.

Expected result: the linked venue page shows the same upcoming show.

## Edit Flows

1. Open the created venue detail page.
2. Click `Edit`.
3. Change the name to `Browser Test Venue Edited` and save.
4. Confirm the venue detail page shows the edited name.
5. Open the created artist detail page.
6. Click `Edit`.
7. Change the name to `Browser Test Artist Edited` and save.
8. Confirm the artist detail page shows the edited name.

Expected result: edited values persist after redirect and page reload.

## Invalid Show Guard

1. Open http://127.0.0.1:5000/shows/create.
2. Submit:
   - Artist ID: `999999999`
   - Venue ID: a real venue ID
   - Start time: `2035-05-01 20:00`

Expected result: the app flashes an error and does not create a show.

## Pass Criteria

- The app remains reachable at http://127.0.0.1:5000/ throughout the test.
- All created records are visible in list, search, and detail views.
- Past and upcoming shows are separated correctly.
- Edit forms persist changes.
- Invalid show submissions do not create database rows.
