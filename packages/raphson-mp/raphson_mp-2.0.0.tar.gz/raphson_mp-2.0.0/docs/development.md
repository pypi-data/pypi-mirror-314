# Development

## Development using Docker

With `docker` and `docker-compose-plugin` installed, run the following command to start a local testing server:
```
docker compose up --build
```

Before doing so, you will need to create a music and data directory. You may need to change `user` in the `compose.yaml` file if your user is not using the default id of 1000.

## Development without Docker

pyproject.toml specifies the project's dependencies, which you [have to install manually](https://github.com/pypa/pip/issues/11440) using pip for now.

Fedora packages, if you prefer (this list may be outdated or incomplete):
```
sudo dnf install python3-aiohttp python3-babel python3-jinja2 yt-dlp babel poedit python3-build twine python3-pytest python3-pytest-asyncio
```

Start the web server in development mode, which supports live reloading:
```
python3 -m raphson_mp start --dev
```

## Code structure

  * (`data/`): default database directory.
  * `docker/`: additional files used to build containers.
  * `docs/`: documentation in markdown format.
  * (`music/`): default music directory.
  * `raphson_mp/`: contains program source code
    * `migrations/`: sql files used to update the database.
    * `routes`: files containing route functions (marked with `@route`)
    * `sql/`: sql files used to initialize the database, also useful as a database layout reference.
    * `static/`: static files that are served as-is by the frontend, under the `/static` URL. The files in `/static/js/player/*.js` are served in concatenated form as `/static/js/player.js`.
    * `templates/`: jinja2 template files for web pages.
    * `translations/`: translation files, see translations section.

## Code style

Use `isort .` to sort imports. Use `black` to format source code. `pyproject.toml` contains some settings which should be picked up automatically.

## Preparing for development while offline

### Docker images

If you wish to use Docker for development, use `docker pull` to download the base image (first line of Dockerfile). If you don't do this, buildx will attempt to pull the image very frequently while rebuilding, which won't work offline.

Then, build and start the container: `docker compose up --build`. Following builds will be cached, unless you change one of the `RUN` instructions in the `Dockerfile`.

### Music

Add some music to `./music`. Adding only a small amount is recommended. While online, start the web interface, enable all playlists and skip through all tracks. This will ensure album art and lyrics are downloaded to the cache for all tracks.

## Translations

### For developers

In templates:
```jinja
{% trans %}Something in English{% endtrans %}
{{ gettext('Something in English') }}
```

In Python:
```py
from i18n import gettext

translated_string = gettext('Something in English')
```

### For translators

1. Run `./update-translations.sh`
2. Edit the `messages.po` file in `src/translations/<language_code>/LC_MESSAGES/` using a text editor or PO editor like Poedit. To create a new language, run: `pybabel init -i messages.pot -d src/translations -l <language_code>`
3. Run `./update-translations.sh` again to ensure the language files are in a consistent format.

## Testing

Run all tests: `pytest`

⚠️ Do not run all tests too often. Web scraping can trigger rate limits, especially in the case of automated tests which make the same requests every time.

Run a specific test: `pytest tests/test_server.py`

Measure code coverage:
```
python3 -m coverage run -m pytest
python3 -m coverage report
```

Test coverage history:

| Date | Total code coverage
| - | -
| 2024-12-05 | 48%
| 2024-12-09 | 54%
| 2024-12-11 | 56%
