# Halogen

Halogen contains common objects and functions for dynamicalsystem projects:

## Config

`dynamicalsystem.halogen.config` provides a single instance immutable object which will provide a project's config given a name (typically `__name__`) in the presence of two environment variables:

- `DYNAMICAL_SYSTEM_FOLDER` - a path to the config folders
- `DYNAMICAL_SYSTEM_ENVIRONMENT` - the environment which the config applies to (dev, test, prod, e.g.)

## Utils

`dynamicalsystem.halogen.utils` provides common functions which do fun stuff like:

- `url_join` which jangs some `/`s into the right places given some url fragments as a string and a list of strings.
- `cli_hyperlink` which creates a hyperlink which will display on the cli.
- `possessive` which turns a provided noun into the possessive form in English.
