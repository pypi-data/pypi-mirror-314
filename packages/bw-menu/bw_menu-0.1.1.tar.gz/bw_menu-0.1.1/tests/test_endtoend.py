"""
Test the full run of the program with one user, end to end, with multiple
scenarios
"""

import atexit
import importlib
import os
import shutil
import sys
import tempfile

from pathlib import Path
from typing import List
from datetime import datetime, timezone

import jinja2 as jinja
import pytest  # type:ignore
import testpath  # type:ignore
import bw_menu.__main__ as program
from bw_menu import vault

UNAUTHENTICATED: str = "unauthenticated"
LOCKED: str = "locked"
UNLOCKED: str = "unlocked"


USER1: str = "user1@domain.tld"
USER1_APPDATA_DIR: str = tempfile.mkdtemp(prefix="USER1")
VAULT_URI: str = "https://vault.bitwarden.com"
USER1_CLIENT_ID: str = "user.001111111q111vvv"
PASSWORD: str = "PASSWORD"
BW_STATUS_FILE_PATH: str
_, BW_STATUS_FILE_PATH = tempfile.mkstemp()

with open("tests/data/list_items.json", mode="r", encoding="utf-8") as jsonf:
    BW_OUTPUT_ITEMS: str = jsonf.read()
with open("tests/data/list_folders.json", mode="r", encoding="utf-8") as jsonf:
    BW_OUTPUT_FOLDERS: str = jsonf.read()


def cleanup_temp_files():
    """clean up"""
    shutil.rmtree(USER1_APPDATA_DIR)
    Path.unlink(Path(BW_STATUS_FILE_PATH), missing_ok=True)


atexit.register(cleanup_temp_files)


with open("tests/templates/bw.j2", mode="r", encoding="utf-8") as fh:
    bw_template = jinja.Template(fh.read())
    BW_SCRIPT = bw_template.render(
        bw_status_file_path=BW_STATUS_FILE_PATH,
        bw_output_items=BW_OUTPUT_ITEMS,
        bw_output_folders=BW_OUTPUT_FOLDERS,
    )

KEYCTL_KEY_ID: str = "000000000"
KEYCTL_KEY_CONTENTS: str = PASSWORD
with open("tests/templates/keyctl.j2", mode="r", encoding="utf-8") as fh:
    bw_template = jinja.Template(fh.read())
    KEYCTL_SCRIPT = bw_template.render(
        keyctl_key_id=KEYCTL_KEY_ID,
    )

MENU_SCRIPT: str = """
#!/usr/bin/env python3
import sys
print(sys.stdin.readline())
"""

KEYCTL_CMDS: dict = {
    "search": [
        "search",
        "@s",
        "user",
        vault.keyring_label(account_label=USER1, vault_uri=VAULT_URI),
    ],
    "pipe": ["pipe", KEYCTL_KEY_ID],
    "padd": [
        "padd",
        "user",
        vault.keyring_label(account_label=USER1, vault_uri=VAULT_URI),
        "@s",
    ],
}
BW_CMDS: dict = {
    "folders": ["--nointeraction", "list", "folders"],
    "items": ["--nointeraction", "list", "items"],
    "login": ["login", "--apikey"],
    "status": ["status"],
    "sync": ["sync"],
    "unlock": ["unlock"],
}

DMENU_CMD = ["-i", "-p", "BitWarden", "-l", "7"]
CLIPBD_CMD = ["-selection", "clipboard", "-in", "-loops", "1"]


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            # A totally new user with an unauthenticated vault
            # Keyring shows old keys, requiring updating
            [
                "--account",
                USER1,
                USER1_APPDATA_DIR,
                VAULT_URI,
                USER1_CLIENT_ID,
            ],
            {
                "returncode": 0,
                "output": "mypassword",
                "vault_start": UNAUTHENTICATED,
                "bw_args": [
                    BW_CMDS["items"],
                    BW_CMDS["status"],
                    BW_CMDS["login"],
                    BW_CMDS["unlock"],
                    BW_CMDS["items"],
                ],
                "keyctl_args": [
                    KEYCTL_CMDS["search"],
                    KEYCTL_CMDS["pipe"],
                    KEYCTL_CMDS["padd"],
                ],
                "dmenu_args": [DMENU_CMD],
                "clipbd_args": [CLIPBD_CMD],
            },
        ),
        (
            # Vault authenticated but not unlocked
            # Keyring shows old keys, requiring updating
            [
                "--account",
                USER1,
                USER1_APPDATA_DIR,
                VAULT_URI,
                USER1_CLIENT_ID,
            ],
            {
                "returncode": 0,
                "output": "mypassword",
                "vault_start": LOCKED,
                "bw_args": [
                    BW_CMDS["items"],
                    BW_CMDS["status"],
                    BW_CMDS["unlock"],
                    BW_CMDS["items"],
                ],
                "keyctl_args": [
                    KEYCTL_CMDS["search"],
                    KEYCTL_CMDS["pipe"],
                    KEYCTL_CMDS["padd"],
                ],
                "dmenu_args": [DMENU_CMD],
                "clipbd_args": [CLIPBD_CMD],
            },
        ),
        (
            # Vault already unlocked with valid keys in keyring
            [
                "--account",
                USER1,
                USER1_APPDATA_DIR,
                VAULT_URI,
                USER1_CLIENT_ID,
            ],
            {
                "returncode": 0,
                "output": "mypassword",
                "vault_start": UNLOCKED,
                "bw_args": [
                    BW_CMDS["items"],
                ],
                "keyctl_args": [
                    KEYCTL_CMDS["search"],
                    KEYCTL_CMDS["pipe"],
                ],
                "dmenu_args": [DMENU_CMD],
                "clipbd_args": [CLIPBD_CMD],
            },
        ),
        (
            # Vault already unlocked with valid keys in keyring. User requests
            # that folder names are prepended to the listing
            [
                "--account",
                USER1,
                USER1_APPDATA_DIR,
                VAULT_URI,
                USER1_CLIENT_ID,
                "--prepend-folders",
            ],
            {
                "returncode": 0,
                "output": "mypassword",
                "vault_start": UNLOCKED,
                "bw_args": [
                    BW_CMDS["items"],
                    BW_CMDS["folders"],
                ],
                "keyctl_args": [
                    KEYCTL_CMDS["search"],
                    KEYCTL_CMDS["pipe"],
                ],
                "dmenu_args": [DMENU_CMD],
                "clipbd_args": [CLIPBD_CMD],
            },
        ),
        (
            # Vault already unlocked with valid keys in keyring, and a last
            # sync time that is over the default time
            [
                "--account",
                USER1,
                USER1_APPDATA_DIR,
                VAULT_URI,
                USER1_CLIENT_ID,
            ],
            {
                "returncode": 0,
                "output": "mypassword",
                "vault_start": UNLOCKED,
                "last_sync_time": datetime.fromtimestamp(0, timezone.utc),
                "bw_args": [
                    BW_CMDS["items"],
                    BW_CMDS["sync"],
                ],
                "keyctl_args": [
                    KEYCTL_CMDS["search"],
                    KEYCTL_CMDS["pipe"],
                ],
                "dmenu_args": [DMENU_CMD],
                "clipbd_args": [CLIPBD_CMD],
            },
        ),
        (
            # Vault already unlocked with valid keys in keyring. Should print a
            # specific ID to stdout.
            [
                "--account",
                USER1,
                USER1_APPDATA_DIR,
                VAULT_URI,
                USER1_CLIENT_ID,
                "--print-by-id",
                USER1,
                "item_id",
            ],
            {
                "returncode": 0,
                "stdout": "PASSWORD",
                "vault_start": UNLOCKED,
                "bw_args": [
                    BW_CMDS["items"],
                ],
                "keyctl_args": [
                    KEYCTL_CMDS["search"],
                    KEYCTL_CMDS["pipe"],
                ],
                "dmenu_args": [],
                "clipbd_args": [],
            },
        ),
    ],
)
# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_end_to_end(test_input, expected, capsys) -> None:
    """Test"""
    args: List[str] = [str(x) for x in test_input]
    with testpath.MockCommand("bw", python=BW_SCRIPT,) as bwcli, testpath.MockCommand(
        "keyctl",
        python=KEYCTL_SCRIPT,
    ) as keyctl, testpath.MockCommand(
        "dmenu",
        python=MENU_SCRIPT,
    ) as dmenu, testpath.MockCommand.fixed_output(
        "xclip", ""
    ) as clipbd:
        # Mock Tkinter to just pass back a string as if the user had filled it
        # out
        sys.modules["tkinter"] = importlib.import_module("tkinter")
        with open(BW_STATUS_FILE_PATH, mode="w", encoding="utf-8") as bw_status_file:
            bw_status_file.write(expected["vault_start"])
        if "last_sync_time" in expected:
            with open(
                os.path.join(USER1_APPDATA_DIR, "last_sync"), mode="w", encoding="utf-8"
            ) as last_sync_file:
                last_sync_file.write(str(expected["last_sync_time"]))
        program.main(argv=args)

    if "stdout" in expected:
        assert capsys.readouterr().out.strip("\n") == expected["stdout"]

    for mock_cmd, all_expected_args in [
        (bwcli, expected["bw_args"]),
        (keyctl, expected["keyctl_args"]),
        (dmenu, expected["dmenu_args"]),
        [clipbd, expected["clipbd_args"]],
    ]:
        # Go through each mocked external command and ensure that they were
        # all called with the right arguments and in the right order
        cmds_run: List[str] = [a["argv"][1:] for a in mock_cmd.get_calls()]
        # print(cmds_run)
        # print(all_expected_args)
        assert len(cmds_run) == len(all_expected_args)
        for called_args, expected_args in zip(cmds_run, all_expected_args):
            assert " ".join(called_args) == " ".join(expected_args), (
                "The commands that we expected to be called must all have run, and "
                "in the same order - ",
            )


# pylint: enable=unused-argument
# pylint: enable=redefined-outer-name
