from __future__ import annotations

import datetime
import shutil
import sys
from json import JSONDecodeError
from pathlib import Path
from typing import Tuple

from rich.console import Console

from cli.settings import token_file as tf
from cli.settings.token_file import TokenFile

err_console = Console(stderr=True)


CONFIG_DIR_PATH = Path.home() / ".config" / "remotive"
INCORRECT_CONFIG_DIR_PATH = Path.home() / ".config" / ".remotive"
DEPRECATED_CONFIG_DIR_PATH = Path.home() / ".remotive"

ACTIVE_TOKEN_FILE_NAME = "cloud.secret.token"
PERSONAL_TOKEN_FILE_PREFIX = "personal-token-"
SERVICE_ACCOUNT_TOKEN_FILE_PREFIX = "service-account-token-"


TokenFileMetadata = Tuple[TokenFile, Path]


class InvalidSettingsFilePathError(Exception):
    """Raised when trying to access an invalid settings file or file path"""


class TokenNotFoundError(Exception):
    """Raised when a token cannot be found in settings"""


class Settings:
    """
    Settings for the remotive CLI
    """

    config_dir: Path

    def __init__(self, config_dir: Path, deprecated_config_dirs: list[Path] | None = None) -> None:
        self.config_dir = config_dir
        self._active_secret_token_path = self.config_dir / ACTIVE_TOKEN_FILE_NAME

        # no migration of deprecated config dirs if the new config dir already exists
        if self.config_dir.exists():
            return

        # create the config dir and try to migrate legacy config dirs if they exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        if deprecated_config_dirs:
            for deprecated_config_dir in deprecated_config_dirs:
                self._migrate_legacy_config_dir(deprecated_config_dir)

    def get_active_token(self) -> str:
        """
        Get the current active token secret
        """
        token_file = self.get_active_token_file()
        return token_file.token

    def get_active_token_file(self) -> TokenFile:
        """
        Get the current active token file
        """
        if not self._active_secret_token_path.exists():
            raise TokenNotFoundError("no active token file found")

        return self._read_token_file(self._active_secret_token_path)

    def activate_token(self, name: str) -> None:
        """
        Activate a token by name or path

        The token secret will be set as the current active secret.
        """
        token_file = self.get_token_file(name)
        self._write_token_file(self._active_secret_token_path, token_file)

    def clear_active_token(self) -> None:
        """
        Clear the current active token
        """
        self._active_secret_token_path.unlink(missing_ok=True)

    def get_token_file(self, name: str) -> TokenFile:
        """
        Get a token file by name or path
        """
        if Path(name).exists():
            return self._read_token_file(Path(name))

        return self._get_token_by_name(name)[0]

    def remove_token_file(self, name: str) -> None:
        """
        Remove a token file by name or path

        TODO: what about manually downloaded tokens?
        """
        if Path(name).exists():
            if self.config_dir not in Path(name).parents:
                raise InvalidSettingsFilePathError(f"cannot remove a token file not located in settings dir {self.config_dir}")
            return Path(name).unlink()

        # TODO: what about the active token? # pylint: disable=fixme

        path = self._get_token_by_name(name)[1]
        return path.unlink()

    def add_and_activate_short_lived_cli_token(self, token: str) -> TokenFile:
        """
        Activates a short lived token
        """
        token_file = tf.loads(token)
        self._write_token_file(self._active_secret_token_path, token_file)
        return token_file

    def add_personal_token(
        self,
        token: str,
        activate: bool = False,
        overwrite_if_exists: bool = False,
    ) -> TokenFile:
        """
        Add a personal token
        """
        token_file = tf.loads(token)

        file = f"{PERSONAL_TOKEN_FILE_PREFIX}{token_file.name}.json"
        path = self.config_dir / file
        if path.exists() and not overwrite_if_exists:
            raise FileExistsError(f"Token file already exists: {path}")

        self._write_token_file(path, token_file)

        if activate:
            self.activate_token(token_file.name)

        return token_file

    def list_personal_tokens(self) -> list[TokenFile]:
        """
        List all personal tokens
        """
        return [f[0] for f in self._list_personal_tokens()]

    def list_personal_token_files(self) -> list[Path]:
        """
        List paths to all personal token files
        """
        return [f[1] for f in self._list_personal_tokens()]

    def add_service_account_token(self, service_account: str, token: str) -> TokenFile:
        """
        Add a service account token to the config directory
        """
        token_file = tf.loads(token)

        file = f"{SERVICE_ACCOUNT_TOKEN_FILE_PREFIX}{service_account}-{token_file.name}.json"
        path = self.config_dir / file
        if path.exists():
            raise FileExistsError(f"Token file already exists: {path}")

        self._write_token_file(path, token_file)
        return token_file

    def list_service_account_tokens(self) -> list[TokenFile]:
        """
        List all service account tokens
        """
        return [f[0] for f in self._list_service_account_tokens()]

    def list_service_account_token_files(self) -> list[Path]:
        """
        List paths to all service account token files
        """
        return [f[1] for f in self._list_service_account_tokens()]

    def _list_personal_tokens(self) -> list[TokenFileMetadata]:
        return self._list_token_files(prefix=PERSONAL_TOKEN_FILE_PREFIX)

    def _list_service_account_tokens(self) -> list[TokenFileMetadata]:
        return self._list_token_files(prefix=SERVICE_ACCOUNT_TOKEN_FILE_PREFIX)

    def _get_token_by_name(self, name: str) -> TokenFileMetadata:
        token_files = self._list_token_files()
        matches = [token_file for token_file in token_files if token_file[0].name == name]
        if len(matches) != 1:
            raise TokenNotFoundError(f"Ambiguous token file name {name}, found {len(matches)} files")
        return matches[0]

    def _list_token_files(self, prefix: str = "") -> list[TokenFileMetadata]:
        # list all tokens with the correct prefix in the config dir, but omit the special active token file
        def is_path_prefixed_and_not_active_secret(path: Path) -> bool:
            has_correct_prefix = path.is_file() and path.name.startswith(prefix)
            is_active_secret = path == self._active_secret_token_path
            return has_correct_prefix and not is_active_secret

        paths = [path for path in self.config_dir.iterdir() if is_path_prefixed_and_not_active_secret(path)]

        return [(self._read_token_file(token_file), token_file) for token_file in paths]

    def _read_token_file(self, path: Path) -> TokenFile:
        data = self._read_file(path)
        return tf.loads(data)

    def _read_file(self, path: Path) -> str:
        if not path.exists():
            raise TokenNotFoundError(f"File could not be found: {path}")
        return path.read_text(encoding="utf-8")

    def _write_token_file(self, path: Path, token: TokenFile) -> Path:
        data = tf.dumps(token)
        return self._write_file(path, data)

    def _write_file(self, path: Path, data: str) -> Path:
        if self.config_dir not in path.parents:
            raise InvalidSettingsFilePathError(f"file {path} not in settings dir {self.config_dir}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding="utf8")
        return path

    def _migrate_legacy_config_dir(self, path: Path) -> None:
        if not path.exists():
            return

        sys.stderr.write(f"migrating deprecated config directory {path} to {self.config_dir}\n")
        shutil.copytree(str(path), str(self.config_dir), dirs_exist_ok=True)
        secret = path / ACTIVE_TOKEN_FILE_NAME
        if secret.exists():
            value = secret.read_text(encoding="utf-8").strip()
            # The existing token file might either be a token file, or simply a string. We handle both cases...
            try:
                token = tf.loads(value)
            except JSONDecodeError:
                token = tf.TokenFile(
                    name="MigratedActiveToken",
                    token=value,
                    created=str(datetime.datetime.now().isoformat()),
                    expires="unknown",
                )
            self.add_and_activate_short_lived_cli_token(tf.dumps(token))
        shutil.rmtree(str(path))


def create_settings() -> Settings:
    """Create remotive CLI config directory and return its settings instance"""
    return Settings(CONFIG_DIR_PATH, deprecated_config_dirs=[DEPRECATED_CONFIG_DIR_PATH, INCORRECT_CONFIG_DIR_PATH])


settings = create_settings()
"""
Global/module-level settings instance. Module-level variables are only loaded once, at import time.

TODO: Migrate away from singleton instance
"""
