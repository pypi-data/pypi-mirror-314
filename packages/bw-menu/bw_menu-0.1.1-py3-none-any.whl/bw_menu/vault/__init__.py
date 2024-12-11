""" Model a Bitwarden vault """

from datetime import datetime, timezone
from typing import List, Optional
import json
import logging
import os
import re
import subprocess

BW_CMD: str = "bw"
CLIENTID_ENVVAR = "BW_CLIENTID"
BW_SESSION_ENVVAR: str = "BW_SESSION"
DATADIR_ENVVAR: str = "BITWARDENCLI_APPDATA_DIR"
UNAUTHENTICATED: str = "unauthenticated"
LOCKED: str = "locked"
UNLOCKED: str = "unlocked"


def keyring_label(*, account_label: str, vault_uri: str) -> str:
    """
    Produce the formatted string that we are using to label our session keys in
    the kernel keyring
    """
    return f"{account_label}@{vault_uri}"


class VaultLockedError(Exception):
    """Custom Exception raised when an action fails because the vault is locked"""

    def __init__(  # pylint: disable=keyword-arg-before-vararg
        self, msg="Vault locked", *args, **kwargs
    ):
        super().__init__(msg, *args, **kwargs)


class VaultStatusNotRecognized(Exception):
    """
    Custom Exception raised when the vault status state is not recognized
    """

    def __init__(  # pylint: disable=keyword-arg-before-vararg
        self, msg="Vault status not recognized", *args, **kwargs
    ):
        super().__init__(msg, *args, **kwargs)


class VaultUnauthenticatedError(Exception):
    """
    Custom Exception raised when an action fails because the vault is unauthenticated
    """

    def __init__(  # pylint: disable=keyword-arg-before-vararg
        self, msg="Vault unauthenticated", *args, **kwargs
    ):
        super().__init__(msg, *args, **kwargs)


class Vault:  # pylint: disable=too-many-instance-attributes
    """
    This models/works with the BitWarden vault

    Basic intended flow:

    ```
    v = vault.Vault()
    try:
        v.get_session_from_keyring()
        v.get_items()
    except vault.VaultLockedError:
        v.unlock()
    except vault.VaultUnauthenticatedError:
        v.login()
        v.unlock()
    ```
    """

    def __init__(
        self,
        vault_uri: str = "https://vault.bitwarden.com",
        *,
        appdata_path: str,
        client_id: str,
        account_label: str,
    ):
        self.appdata_path: str = appdata_path
        self.vault_uri: str = vault_uri
        self.account_label: str = account_label
        self.client_id: str = client_id
        self.synctime_filepath: str = os.path.join(appdata_path, "last_sync")

        # Add to rather than overwrite existing environ
        self.env: dict = {
            **os.environ,
            **{
                DATADIR_ENVVAR: self.appdata_path,
                CLIENTID_ENVVAR: self.client_id,
            },
        }
        logging.debug("Setting environ for Vault interaction: %s", self.env)

        self.keyring_label = keyring_label(
            account_label=self.account_label, vault_uri=self.vault_uri
        )
        self.session_key: str

    def _record_sync_time(self) -> None:
        """
        Save to file the time of the last sync (by this program) for this vault

        Does not actually query the time of the last sync from `bw` itself, as
        the operation is expensive and ultimately unecessary

        we just need to know how long ago *this program* did it
        """
        now: datetime = datetime.now(timezone.utc)
        logging.info(
            "Recording new last sync time to `%s` as: `%s`",
            self.appdata_path,
            now.isoformat(),
        )
        os.makedirs(self.appdata_path, exist_ok=True)
        with open(
            self.synctime_filepath, "w", encoding="utf-8"
        ) as fh:  # pylint: disable=invalid-name
            fh.write(str(now.isoformat()))

    def last_sync_time(self) -> datetime:
        """
        Get the time that this program last synchronized the vault as an
        *aware* datetime object
        """
        try:
            with open(
                self.synctime_filepath, "r", encoding="utf-8"
            ) as fh:  # pylint: disable=invalid-name
                lasttime = fh.readline().strip("\n")
            return datetime.fromisoformat(lasttime)
        except FileNotFoundError:
            return datetime.fromtimestamp(0, timezone.utc)

    def sync(self) -> None:
        """
        Sync the vault and save the time
        """
        cmd: List[str]
        cmd = [BW_CMD, "sync"]
        logging.info("Syncing vault for `%s`", self.account_label)
        logging.debug(cmd)
        try:
            subprocess.run(  # type:ignore
                cmd,
                capture_output=True,
                check=True,
                env={**self.env, **{BW_SESSION_ENVVAR: self.session_key}},
                text=True,
            )
            self._record_sync_time()
        except subprocess.CalledProcessError as err:
            if err.returncode == 1:
                logging.info(
                    (
                        "`bw sync` failed with return code `1`. Presuming that "
                        "login is required. STDERR: %s"
                    ),
                    err.stderr,
                )
                raise VaultUnauthenticatedError from err

    def _list_objects(self, *, objtype: str) -> List[dict]:
        """
        Given an object type, get the list of that object from `bw` and return as JSON
        """
        objtypes: List[str] = ["items", "folders"]
        try:
            assert objtype in objtypes
        except AssertionError as err:
            raise AssertionError(
                f"`objtype` for `bw list` must be one of `{objtypes}`"
            ) from err

        cmd: List[str]
        cmd = [BW_CMD, "--nointeraction", "list", objtype]
        logging.info("Requesting vault objects of type `%s`", objtype)
        logging.debug(cmd)
        try:
            res: subprocess.CompletedProcess = subprocess.run(  # type:ignore
                cmd,
                capture_output=True,
                check=True,
                env={**self.env, **{BW_SESSION_ENVVAR: self.session_key}},
                text=True,
            )
        except subprocess.CalledProcessError as err:
            status: str = self.status()
            if status == LOCKED:
                raise VaultLockedError from err
            if status == UNAUTHENTICATED:
                raise VaultUnauthenticatedError from err
            if status != UNLOCKED:
                raise VaultStatusNotRecognized from err
        return json.loads(res.stdout)

    def get_items(
        self,
        *,
        fmt: str,
        prepend_folders: bool = False,
        prepend_str: Optional[str] = None,
    ) -> dict:
        """
        Return the items from the `bw list` processed into a dict with the
        actual menu listings as keys, and the secrets as the value.

        The secret value might not be from the password field - tries to return
        `login.password`->`secureNote`->`note` fields in that order of
        preference if exists
        and in that order
        """
        folders: dict
        items: list = self._list_objects(objtype="items")
        if prepend_folders:
            # If we're dealing with folders at all, then insert a new key
            # `folder_name` into each item with its folder name
            folders = {
                # Make into a dict of {folderid:foldername}
                obj["id"]: obj["name"]
                for obj in self._list_objects(objtype="folders")
            }
            for item in items:
                item["folder_name"] = folders[item["folderId"]]
        processed_items: dict = {}
        for item in items:
            name_parts: List[str] = []
            if prepend_str:
                name_parts.append(prepend_str)
            if prepend_folders:
                name_parts.append(item["folder_name"])
            name_parts.append(item["name"])
            secret: str
            if item.get("login", {}).get("password"):
                secret = item["login"]["password"]
            else:
                secret = item.get("notes", "")
            itemusername: str = item.get("login", {}).get("username", "")
            itemid: str = item["id"]
            itemname: str = "/".join(name_parts)
            listing_key: str = fmt.format(
                itemname=itemname,
                itemusername=itemusername,
                account_label=self.account_label,
                itemid=itemid,
                secret=secret,
            )
            processed_items[listing_key] = secret
        return processed_items

    def get_session_from_keyring(self) -> None:
        """
        Get session key, logging in and creating it if necessary
        """
        cmd: List[str]
        cmd = ["keyctl", "search", "@s", "user", self.keyring_label]
        logging.info(
            "Checking kernel keyring for existing session key for `%s@%s`",
            self.account_label,
            self.vault_uri,
        )
        logging.debug(cmd)
        res: subprocess.CompletedProcess = subprocess.run(  # type:ignore
            cmd, check=False, capture_output=True, text=True
        )
        keyid: str
        if res.returncode == 0:
            # If session key found
            keyid = res.stdout.strip("\n")
            logging.info(
                "Session keys for `%s@%s` found in keyring with id %s",
                self.account_label,
                self.vault_uri,
                keyid,
            )
            # Get the actual key
            cmd = ["keyctl", "pipe", keyid]
            logging.info(
                "Requesting `bw` session key from kernel keyring by id %s",
                keyid,
            )
            logging.debug(cmd)
            res: subprocess.CompletedProcess = subprocess.run(  # type:ignore
                cmd, check=True, capture_output=True, text=True
            )
            self.session_key = res.stdout
        else:
            # Else not found, unlock the vault and save the session key
            status: str = self.status()
            if status == LOCKED:
                raise VaultLockedError
            if status == UNAUTHENTICATED:
                raise VaultUnauthenticatedError
            if status != UNLOCKED:
                raise VaultStatusNotRecognized

    def status(self) -> str:
        """
        Return the status reported by `bw` for this vault
        """
        cmd: List[str] = [BW_CMD, "status"]
        logging.info(
            "Fetching vault status with additional environ: `%s=%s`",
            DATADIR_ENVVAR,
            self.appdata_path,
        )
        logging.debug(cmd, self.env)
        res: subprocess.CompletedProcess = subprocess.run(
            cmd, check=True, env=self.env, capture_output=True
        )
        return json.loads(res.stdout)["status"]

    def login(self, *, passphrase: str) -> None:  # pylint: disable=unused-argument
        """
        Log into `bw` via API key.

        This step is required before `bw unlock`
        """
        cmd: List[str] = [BW_CMD, "login", "--apikey"]
        logging.info(
            "Logging into vault with`%s=%s` (and password via STDIN)",
            DATADIR_ENVVAR,
            self.appdata_path,
        )
        logging.debug(cmd, self.env)
        try:
            subprocess.run(
                cmd,
                check=True,
                env=self.env,
                capture_output=True,
                text=True,
                input=passphrase,
            )
        except subprocess.CalledProcessError as err:
            stderr = err.stderr
            raise RuntimeError(
                f"`bw login` failed with returncode `{err.returncode}` and the "
                f"following from STDERR: `{stderr}`",
            ) from err

    def _store_session_key(self, *, session_key: str) -> None:
        """Save a session key and put a copy in the kernel keyring"""
        logging.info(
            "Updating stored session key in the Vault object for `%s",
            self.account_label,
        )
        self.session_key = session_key

        cmd: List[str]
        cmd = ["keyctl", "padd", "user", self.keyring_label, "@s"]
        logging.info(
            "Placing `bw` session key into kernel keyring via STDIN",
        )
        logging.debug(cmd)
        subprocess.run(  # type:ignore
            cmd,
            capture_output=True,
            check=True,
            input=session_key,
            text=True,
        )

    def _bw_extract_session_key(self, *, bw_output: str) -> str:
        """Given the output from `bw login` or `bw unlock`, extract the session key"""
        logging.debug(
            "Attempting to extract session key from `bw` output: %s",
            bw_output.encode("unicode_escape"),
        )
        match: Optional[re.Match] = re.search(
            BW_SESSION_ENVVAR + r'="([^"]+)"', bw_output
        )
        try:
            return match[1]  # type:ignore
        except (IndexError, AttributeError) as err:
            raise RuntimeError(
                "Failed to extract session key from `bw` output. Cannot proceed."
            ) from err

    def unlock(self, *, passphrase: str) -> None:
        """
        Unlock vault
        """
        cmd: List[str] = [BW_CMD, "unlock"]
        logging.info(
            "Unlocking vault with password via STDIN",
        )
        logging.debug(cmd, self.env)
        try:
            res: subprocess.CompletedProcess = subprocess.run(
                cmd,
                check=True,
                env=self.env,
                capture_output=True,
                text=True,
                input=passphrase,
            )
        except subprocess.CalledProcessError as err:
            stderr = err.stderr.encode("unicode_escape")
            raise RuntimeError(
                f"Vault unlock failed with returncode `{err.returncode}` and STDERR: "
                f"`{stderr}`"
            ) from err
        self._store_session_key(
            session_key=self._bw_extract_session_key(bw_output=res.stdout)
        )
        self._record_sync_time()
