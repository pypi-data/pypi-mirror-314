bw-dmenu
===========

Pop-up Bitwarden desktop quick-search for Linux. Puts the selection into the clipboard. Persists the vault login for the duration of the user's session. Supports multiple accounts simultaneously.

# Installation

Requires:

* Python 3.9+
* [BitWarden CLI] in your path
* [dmenu] (for X) or [wofi] (for Wayland)
* `xclip` (for X) or `wl-copy` (for Wayland)
* A Bitwarden [Personal API Key]

You can install with [pip]:

```sh
python3 -m pip install bw-menu
```

You can also install from source:

```sh
git clone <url>
pip install bw-menu
```

# Usage

The most minimal usage example:

```sh
# This tool will create the application data directory if it does not exist
bw-menu --account arbitrary_account_label ~/.path/to/bw/data https://vault.bitwarden.com YOUR_API_CLIENT_ID
```

The tool will prompt for an API key on the first run.

It will also re-prompt for the Vault password at the beginning of each new desktop session, and persist until the session ends.

Full usage:

```
usage: bw-menu [-h] [--menu-format-string MENU_FORMAT_STRING]
               [--sync-interval SYNC_INTERVAL]
               [--print-by-id PRINT_BY_ID PRINT_BY_ID]
               [--prepend-folders | --no-prepend-folders | -p]
               [--prepend-account-label | --no-prepend-account-label | -l]
               [--output-format-string OUTPUT_FORMAT_STRING]
               [--include-session-key | --no-include-session-key | -k]
               [--clipboard-cmd CLIPBOARD_CMD] --account ARBITRARY_LABEL
               BITWARDENCLI_APPDATA_DIR VAULT_URI API_CLIENT_ID [--verbose]

        Pop-up BitWarden desktop quick-search. Puts the selection into the
        clipboard. Persists the vault login for the duration of user's session.
        Supports multiple accounts simultaneously.

            bw-menu --account arbitrary_account_label ~/path/to/appdata \
                https://vault.domain.tld <api_client_id>

          Note that the account labels can be any unique value, as they are
          used only internally and are not used in interactions with the actual
          vault.

        Configuring the pop-up menu:

            `bw-menu` tries to default to appropriate menu commands for
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

            `bw-menu` tries to default to appropriate clipboard commands for
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

                CLIPBOARD_CMD='xdotool -' bw-menu --account account_label \
                    ~/path/to/appdata https://vault.domain.tld <api_client_key> \
                    --output-format-string 'type {passphrase}'

        Security:

            Note: The default clipboard commands limit persistence. Overriding
            the clipboard commands and failing to limit persistence could
            present a security risk. Be careful.



options:
  -h, --help            show this help message and exit
  --menu-format-string MENU_FORMAT_STRING, -f MENU_FORMAT_STRING
                        String for Python's `str.format()` which determines
                        how items are listed in dmenu. The fields made
                        available are: `name`, `account_label`, `itemid`, and
                        `secret`
  --sync-interval SYNC_INTERVAL, -i SYNC_INTERVAL
                        The BitWarden CLI does not automatically pull new
                        information after login. This option allows the user
                        to specify a maximum interval (inminutes) after which
                        this tool will sync the local vault after running.
                        Anegative value prevents this application from syncing
                        the vault.
  --print-by-id PRINT_BY_ID PRINT_BY_ID
                        If a specific item ID is given here, `bw-menu` will
                        not prompt for a selection or output to the clipboard,
                        instead printing the given id directly to STDOUT.
  --prepend-folders, --no-prepend-folders, -p
                        If set, will prepend folder names to the items listed.
                        Note: this will make the run take longer, as the
                        BitWarden CLI must be called twice. (default: False)
  --prepend-account-label, --no-prepend-account-label, -l
                        If set, will prepend the account label to the items
                        listed. Useful if using multiple accounts. (default:
                        False)
  --output-format-string OUTPUT_FORMAT_STRING, -o OUTPUT_FORMAT_STRING
                        String for Python's `str.format()` which allows
                        dressing up of theoutput to the clipboard. The only
                        fields available is `passphrase`.This can be used in
                        combination with the `CLIPBOARD_CMD`environment
                        variable to, for example, have this tool type
                        theselection out automatically. See `bw-menu --help`
                        for more.
  --include-session-key, --no-include-session-key, -k
                        If set, this tool will include the active session key
                        in the dmenu output (default: False)
  --clipboard-cmd CLIPBOARD_CMD, -c CLIPBOARD_CMD
  --account ARBITRARY_LABEL BITWARDENCLI_APPDATA_DIR VAULT_URI API_CLIENT_ID, -a ARBITRARY_LABEL BITWARDENCLI_APPDATA_DIR VAULT_URI API_CLIENT_ID
                        The details necessary to log in to a vault with API
                        key. `ARBITRARY_LABEL` is not used in any interaction
                        with the vault(that is what the API keys are for), but
                        only to differentiate between multiple accounts
                        internally.
  --verbose, -v         Set output verbosity on STDERR (-v=warning, -vv=debug)
```

# Overriding menu and clipboard commands

The default menu commands are `dmenu` on X and `wofi` on Wayland.

This program tries to select reasonable defaults depending on the detected compositor by inspecting the `XDG_SESSION_TYPE` environment variable.

The menu command can be overridden with any tool that takes input on STDIN and outputs a selection.

The clipboard commands can be overridden with any tool that takes input on STDIN.

For guidance on overriding the menu and clipboard commands further, see the help output.

# Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you want to change.

To run the test suite:

```bash
# Dependent targets create venv and install dependencies
make
```

Please make sure to update tests along with any changes.

# License

`License :: OSI Approved :: MIT License`


[BitWarden CLI]: https://bitwarden.com/help/cli/#download-and-install
[Personal API Key]: https://bitwarden.com/help/personal-api-key/
[dmenu]: https://tools.suckless.org/dmenu/
[pip]: https://pypi.org/project/pip/
[wofi]: https://sr.ht/~scoopta/wofi/
