# timezonefinder_gui

The code for the [timezonefinder GUI and API](https://timezonefinder.michelfe.it/gui) a simple Django website using an interactive [leaflet](https://leafletjs.com) map to query the [timezonefinder](https://github.com/jannikmi/timezonefinder) Python package.

See the Makefile for useful commands.

## License

This project is licensed under the [MIT License](LICENSE), same as the underlying `timezonefinder`.

## TODOs

- load secrets and configs from pydantic settings file, add template, but keep actual values secret: <https://docs.pydantic.dev/1.10/usage/settings/>
  - ALLOWED_HOSTS
  - SECRET_KEY
  - take care of the Mapbox default access token <https://docs.mapbox.com/help/troubleshooting/how-to-use-mapbox-securely/#access-tokens>
  - MAPBOX_ACCESS_TOKEN
- remove unsupported certain_timezone_at() function
- proper dependency management using uv
- add documentation: comprehensive README with setup instructions, Configuration documentation
- Remove any TODOs, debug comments, or temporary code
- code review for security and best practices
- CI/CD for deployment, linting, and testing. GitHub Actions
- consider hosting the project on github.io like https://ringsaturn.github.io/tzf-web/
- adding visualisation for the hexagon spatial index used in the background
- add pre-commit hooks for code quality checks (e.g., black, flake8, isort)
- Add automated tests for API endpoints and core logic
- Set up basic error handling and user-friendly error pages
- Improve input validation and sanitization for API requests, use pydantic
  - consider using fastAPI?!
- Add logging for key actions and errors
- Document API endpoints and usage examples
- Provide Dockerfile or deployment instructions for easy setup
- Add a CONTRIBUTING.md for community contributions
- Ensure static files are served securely in production
- serve the statistic as static file. write once instead of generating on each request
