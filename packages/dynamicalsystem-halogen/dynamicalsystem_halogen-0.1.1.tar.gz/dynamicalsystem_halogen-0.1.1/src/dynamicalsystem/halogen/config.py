from dotenv import dotenv_values
from dataclasses import dataclass, field
from functools import lru_cache
from os import getenv
from os.path import join, isfile
from sys import exit

singleton = lru_cache(maxsize=1)


@dataclass(frozen=True)
class _Config:
    environment: str = field(init=False)
    data_folder: str = field(init=False)

    _namespace_file: str = field(init=False, repr=False)
    _package_file: str = field(init=False, repr=False)
    _namespace: str = field(init=False, repr=False)
    _package: str = field(init=False, repr=False)
    _prefix: str = field(init=False, repr=False)  # module name

    def __init__(self, context: str):
        """
        context: str - is assumed to be <namespace>.<package>.<module>
        In normal use just pass __name__ as the context so that you
        can assume that the config file is located at:
                ${<namespace>_FOLDER}/<namespace>/config/${ENVIRONMENT}[.package].env

        config will try to load a names file called ${ENVIRONMENT}.env before progressing
        to [.package].env. Values in the package file will override those in the
        namespace file where the variable is duplicated.

        Then, within the dotenv file, you can prefix each variable with the module name and
        get a Config object which is scoped to the module.

        Assumptions include that the environment variables are uppercase and underscore separated.

        The config object's attributes are lowercased and underscore separated.
        """

        self._parse_context(context)

        root_folder = getenv(f"{self._namespace.upper()}_FOLDER") or exit(
            f"{self._namespace.upper()}_FOLDER not set"
        )

        environment = getenv(f"{self._namespace.upper()}_ENVIRONMENT") or exit(
            f"{self.namespace.upper()}_ENVIRONMENT not set"
        )

        object.__setattr__(
            self,
            "_namespace_file",
            join(
                root_folder,
                self._namespace,
                "config",
                f"{self._namespace}.{environment}.env",
            ),
        )

        object.__setattr__(self, "environment", environment)

        self._package_attributes(root_folder)

        object.__setattr__(
            self,
            "data_folder",
            join(root_folder, self._namespace, "data"),
        )

        for key, value in dotenv_values(self._namespace_file).items():
            object.__setattr__(self, key.casefold(), value)

    def _package_attributes(self, root_folder: str):
        file = join(
            getenv(f"{self._namespace.upper()}_FOLDER"),
            self._namespace,
            "config",
            f"{self._package}.{self.environment}.env",
        )

        print(file)

        if isfile(file):
            object.__setattr__(
                self,
                "_package_file",
                join(
                    root_folder,
                    self._namespace,
                    "config",
                    f"{self._package}.{self.environment}.env",
                ),
            )

            for key, value in dotenv_values(file).items():
                if key.startswith(self._prefix.upper()):
                    attribute = key.removeprefix(self._prefix.upper() + "_")
                    object.__setattr__(self, attribute.casefold(), value)

    def _parse_context(self, context: str):
        _ = context.split(".")
        match len(_):
            case 3:
                object.__setattr__(self, "_namespace", _[0])
                object.__setattr__(self, "_package", _[1])
                object.__setattr__(self, "_prefix", _[2])
                return
            case 2:
                object.__setattr__(self, "_namespace", _[0])
                object.__setattr__(self, "_package", _[1])
                object.__setattr__(self, "_prefix", _[1])
                return
            case 1:
                object.__setattr__(self, "_namespace", _[0])
                object.__setattr__(self, "_package", _[0])
                object.__setattr__(self, "_prefix", _[0])
                return
            case _:
                exit("Invalid context")

    def __str__(self):
        return self._namespace_file


@singleton
def config_instance(context: str):
    if not context:
        exit("No configuration context provided")

    _ = _Config(context)

    print(dir(_))
    print(_._package)

    return _
