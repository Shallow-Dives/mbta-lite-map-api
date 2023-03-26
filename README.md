# MBTA Lite Map API

API supporting the [MBTA Lite Map Project](https://github.com/Shallow-Dives/mbta-lite-map-rpi).

## Develop workflow

The development workflow commands are aliased in the [Makefile](Makefile).


1) Install development dependencies

        make devel-install

2) Create and populate a `.env` file based on .env.template

        cp .env.template .env

   The USER_API_KEY is required to access any restricted endpoints in this application. A user API key can be generated 
   with `uuid-gen` and then provided to the Raspberry Pi frontend node(s).  Keys to access any external APIs should also be added via `.env`.


3) Lint and reformat any new code

         make format          # Reformats all code

         make format-check    # Reports issues but doesn't auto-format

4) Run tests with Pytest

         make test

      The pytest configuration is specified and can be updated in `tests/pytest.ini`.


5) Build and run the API image

         make devel-build

         make devel-run

   This kicks off a multi-stage docker build to create a pared down final image running a Gunicorn server.

## Deploy workflow

**TODO**

`docker compose up`

## Resources

* [MBTA API Docs](https://www.mbta.com/developers/v3-api)
* [MBTA API Developer Portal](https://api-v3.mbta.com/portal)
* [pymbta3 API Wrapper](https://pypi.org/project/pymbta/)
