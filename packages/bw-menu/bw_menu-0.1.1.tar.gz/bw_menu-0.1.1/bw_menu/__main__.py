#!/usr/bin/env python3
"""
Pop-up BitWarden desktop quick-search. Puts the selection into the clipboard.
Persists the vault login for the duration of the login session.
"""

import argparse
import datetime
import logging
import os
import shlex
import subprocess
import sys
import tkinter as tk
import tkinter.simpledialog
from typing import Dict, List, Optional

from . import vault


def prompt_passphrase(text=""):
    """
    Prompt for text with hidden characters
    """
    logging.debug("Prompting for GUI input: `%s`", text)
    tk.Tk().withdraw()
    passphrase = tkinter.simpledialog.askstring(
        "Input Passphrase",
        text,
        show="*",
    )
    try:
        assert passphrase is not None
    except AssertionError as err:
        raise AssertionError("Input cannot be empty") from err
    return passphrase


def parse_args(argv=None) -> argparse.Namespace:
    """Parse args"""

    usage_examples: str = """examples:

        # Description

        %(prog)s <args>

    """
    descr: str = """
        Pop-up BitWarden desktop quick-search. Puts the selection into the
        clipboard. Persists the vault login for the duration of user's session.
        Supports multiple accounts simultaneously.

            %(prog)s --account arbitrary_account_label ~/path/to/appdata \\
                https://vault.domain.tld <api_client_id>

          Note that the account labels can be any unique value, as they are
          used only internally and are not used in interactions with the actual
          vault.

        Configuring the pop-up menu:

            `%(prog)s` tries to default to appropriate menu commands for
            your compositor - `dmenu` on X and `wofi` on Wayland.

            If you wish to override this, it is preferred to do so via
            evironment variables:

                # A custom prompt
                export MENU_CMD='dmenu -i -p "My custom prompt" -l 7'

                # Or even use a different menu program
                export MENU_CMD='rofi -dmenu -p "" -i'

                # Wayland
                export MENU_CMD='wofi -dmenu -p "" -i'

        Configuring the Clipboard:

            `%(prog)s` tries to default to appropriate clipboard commands for
            your compositor - `xclip` on X and `wl-copy` on Wayland.

            If you wish to override this, it is preferred to do so via
            evironment variables:

                # Xclip
                export CLIPBOARD_CMD='xclip -selection clipboard -in -loops 1'

                # Xsel
                export CLIPBOARD_CMD='xsel --selectionTimeout 5000 --input --clipboard'

                # On wayland, wl-copy
                export CLIPBOARD_CMD='wl-copy --paste-once'
        Examples:

            Type output via `xdotool` instead of putting to clipboard

                CLIPBOARD_CMD='xdotool -' %(prog)s --account account_label \\
                    ~/path/to/appdata https://vault.domain.tld <api_client_key> \\
                    --output-format-string 'type {passphrase}'

        Security:

            Note: The default clipboard commands limit persistence. Overriding
            the clipboard commands and failing to limit persistence could
            present a security risk. Be careful.

        """
    parser = argparse.ArgumentParser(
        description=descr,
        epilog=usage_examples,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--menu-format-string",
        "-f",
        help=(
            "String for Python's `str.format()` which determines how items are listed "
            "in dmenu. The fields made available are: `name`, `account_label`, "
            "`itemid`, and `secret`"
        ),
        default="{itemname} [{itemusername}] [{itemid}]",
        type=str,
    )

    parser.add_argument(
        "--sync-interval",
        "-i",
        help=(
            "The BitWarden CLI does not automatically pull new information after "
            "login. This option allows the user to specify a maximum interval (in"
            "minutes) after which this tool will sync the local vault after running. A"
            "negative value prevents this application from syncing the vault."
        ),
        default=60,
        type=int,
    )

    parser.add_argument(
        "--print-by-id",
        help=(
            "If a specific item ID is given here, `%(prog)s` will not prompt for a "
            "selection or output to the clipboard, instead printing the given id "
            "directly to STDOUT."
        ),
        nargs=2,
        type=str,
    )

    parser.add_argument(
        "--prepend-folders",
        "-p",
        action=argparse.BooleanOptionalAction,
        help=(
            "If set, will prepend folder names to the items listed. Note: this will "
            "make the run take longer, as the BitWarden CLI must be called twice."
        ),
        default=False,
        type=bool,
    )

    parser.add_argument(
        "--prepend-account-label",
        "-l",
        action=argparse.BooleanOptionalAction,
        help=(
            "If set, will prepend the account label to the items listed. Useful if "
            "using multiple accounts."
        ),
        default=False,
        type=bool,
    )

    parser.add_argument(
        "--output-format-string",
        "-o",
        help=(
            "String for Python's `str.format()` which allows dressing up of the"
            "output to the clipboard. The only fields available is `passphrase`."
            "This can be used in combination with the `CLIPBOARD_CMD`"
            "environment variable to, for example, have this tool type the"
            "selection out automatically. See `%(prog)s --help` for more."
        ),
        default="{passphrase}",
        type=str,
    )

    parser.add_argument(
        "--include-session-key",
        "-k",
        action=argparse.BooleanOptionalAction,
        help=(
            "If set, this tool will include the active session key in the dmenu output"
        ),
        default=False,
        type=bool,
    )

    # Prepare default menu and clipboard commands for X/Wayland
    default_clipboard_cmd: str
    default_menu_command: str
    if "wayland" in os.environ.get("XDG_SESSION_TYPE", ""):
        default_clipboard_cmd = "wl-copy --paste-once"
        default_menu_command = "wofi -dmenu -p '' -i"
    else:
        default_clipboard_cmd = "xclip -selection clipboard -in -loops 1"
        default_menu_command = "dmenu -i -p BitWarden -l 7"
    parser.add_argument(
        "--clipboard-cmd",
        "-c",
        default=shlex.split(os.environ.get("CLIPBOARD_CMD", default_clipboard_cmd)),
        type=list,
    )
    parser.add_argument(
        "--menu-cmd",
        "-d",
        help=argparse.SUPPRESS,
        default=shlex.split(os.environ.get("MENU_CMD", default_menu_command)),
        type=str,
    )

    parser.add_argument(
        "--account",
        "-a",
        metavar=("ARBITRARY_LABEL", vault.DATADIR_ENVVAR, "VAULT_URI", "API_CLIENT_ID"),
        action="append",
        dest="accounts",
        help=(
            "The details necessary to log in to a vault with API key. "
            "`ARBITRARY_LABEL` is not used in any interaction with the vault"
            "(that is what the API keys are for), but only to differentiate "
            "between multiple accounts internally."
        ),
        nargs=4,
        required=True,
        type=str,
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        dest="verbosity",
        help="Set output verbosity on STDERR (-v=warning, -vv=debug)",
    )

    args = parser.parse_args(argv) if argv else parser.parse_args()

    if args.print_by_id:
        try:
            assert args.print_by_id[0] in [a[0] for a in args.accounts]
        except AssertionError as err:
            raise AssertionError(
                "The account label for `--print-by-id` must also be present in "
                "`--account`"
            ) from err

    if args.verbosity >= 2:
        log_level = logging.DEBUG
    elif args.verbosity >= 1:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    logging.basicConfig(level=log_level)

    return args


def put_to_clipboard(*, clipboard_cmd: list, passphrase: str) -> None:
    """
    Given a command (like the default `xclip`), output the selection to it
    """
    try:
        logging.info("Outputting to clipboard command")
        logging.debug(clipboard_cmd)
        with subprocess.Popen(
            clipboard_cmd,
            stdin=subprocess.PIPE,
            text=True,
        ) as clipboard_process:
            # Work with xclip more directly, as `xclip` leaves its stream
            # open and Python's `subprocess.run()` will `wait()` on it forever
            clipboard_process.communicate(passphrase)
    except subprocess.CalledProcessError as err:
        raise RuntimeError("Clipboard placement failed.") from err


def prompt_selection(*, items: List[str], menu_cmd: str) -> str:
    """
    Call the menu command with our item list as input
    return the selected key
    """
    try:
        logging.info("Running external menu command")
        logging.debug(menu_cmd)
        res: subprocess.CompletedProcess = subprocess.run(
            menu_cmd,
            capture_output=True,
            check=True,
            text=True,
            input="\n".join(items),
        )
    except subprocess.CalledProcessError as err:
        raise RuntimeError("Menu prompt failed.") from err
    return res.stdout.strip("\n")


def sync_after_interval(*, uservault: vault.Vault, interval: int) -> None:
    """
    Sync the vault if the last sync time exceeds the limit
    """
    now: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    syncdiff_minutes = (now.timestamp() - uservault.last_sync_time().timestamp()) / 60
    logging.debug(
        "Time since last sync `%s` minutes vs max interval `%s` minutes",
        syncdiff_minutes,
        interval,
    )
    if syncdiff_minutes > interval >= 0:
        uservault.sync()


def main(argv: Optional[list] = None) -> None:  # pylint: disable=too-many-locals
    """Main"""
    args: argparse.Namespace
    if argv:
        args = parse_args(argv)
    else:
        args = parse_args(sys.argv[1:])
    logging.debug("Argparse results: %s", args)

    items: Dict[str, str] = {}
    account: List[str]
    vaults: List[vault.Vault] = []
    for account in args.accounts:
        account_label: str
        datadir_path: str
        vault_uri: str
        client_id: str
        account_label, datadir_path, vault_uri, client_id = account

        uservault: vault.Vault = vault.Vault(
            appdata_path=datadir_path,
            vault_uri=vault_uri,
            account_label=account_label,
            client_id=client_id,
        )

        prepend_str: Optional[str] = (
            account_label if args.prepend_account_label else None
        )
        user_items: dict
        menu_format_string: str = (
            "{account_label}|{itemid}" if args.print_by_id else args.menu_format_string
        )
        try:
            uservault.get_session_from_keyring()
            user_items = uservault.get_items(
                prepend_folders=args.prepend_folders,
                fmt=menu_format_string,
                prepend_str=prepend_str,
            )
        except vault.VaultLockedError:
            logging.debug("Vault locked. Prompting for credentials to unlock.")
            passphrase = prompt_passphrase(
                text=f"Enter passphrase for user `{account_label}` @ `{vault_uri}`"
            )
            uservault.unlock(passphrase=passphrase)
            user_items = uservault.get_items(
                prepend_folders=args.prepend_folders,
                fmt=menu_format_string,
                prepend_str=prepend_str,
            )
        except vault.VaultUnauthenticatedError:
            logging.debug("Vault unauthenticated. Prompting for credentials to login.")
            uservault.login(
                passphrase=prompt_passphrase(
                    text=(
                        f"Enter API client secret for user `{account_label}` @ "
                        f"`{vault_uri}`"
                    )
                )
            )
            passphrase = prompt_passphrase(
                text=f"Enter passphrase for user `{account_label}` @ `{vault_uri}`"
            )
            uservault.unlock(passphrase=passphrase)
            user_items = uservault.get_items(
                prepend_folders=args.prepend_folders,
                fmt=menu_format_string,
                prepend_str=prepend_str,
            )
        if args.include_session_key:
            # If the user would like the seesion keys for eahc account included
            # in the selection menu
            user_items[f"BW_SESSION for {account_label}"] = uservault.session_key
        items = items | user_items
        vaults.append(uservault)

    if args.print_by_id:
        try:
            print(items["|".join(args.print_by_id)])
        except KeyError as err:
            raise KeyError(
                "The account label and item id given to `--print-by-id` were not found"
            ) from err
    else:
        selection: str = items[
            prompt_selection(menu_cmd=args.menu_cmd, items=list(items))
        ]
        output: str = args.output_format_string.format(passphrase=selection)
        put_to_clipboard(clipboard_cmd=args.clipboard_cmd, passphrase=output)

        # Finally ensure we are in sync, but after user interaction is complete
        # to avoid making the user wait
        for uservault in vaults:
            sync_after_interval(uservault=uservault, interval=args.sync_interval)


if __name__ == "__main__":
    main()
