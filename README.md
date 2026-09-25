# Sioyek text tools

This repository is a uv workspace with tools in `packages/`. Sioyek launches
them through `uv run`; both use Python's standard library and Tkinter.

## Setup

1. Install uv and Python 3 with Tkinter.
2. Run `make install` to install the two `uv` tools and copy the Sioyek config
   files to the platform's Sioyek folder. On macOS, it prompts for an
   administrator password and installs the tool environments in
   `/usr/local/share/uv/tools` and their commands in `/usr/local/bin`, making
   them available to all users. The Sioyek config files are copied to
   `~/Library/Application Support/sioyek`. On Windows the script locates the
   WinGet Sioyek installation folder.
3. Copy `.env.example` to `.env` and fill in `DEEPL_AUTH_KEY` if you use DeepL.
4. Reload Sioyek's configuration.

On macOS the commands in `prefs_user.config` deliberately use their absolute
`/usr/local/bin` paths. Finder-launched applications do not inherit your
terminal's `PATH`, so using only `dictionary-lookup` or
`selected-text-translate` makes the shortcuts appear to do nothing. Tool
startup and uncaught launch errors are recorded in
`~/Library/Logs/sioyek-text-tools.log`.

Both tools point `TCL_LIBRARY`/`TK_LIBRARY` at their uv-managed Python before
opening a window. Tcl searches for its library under the virtual environment's
prefix, while uv keeps Tcl/Tk next to the interpreter, so without this every
`tkinter` window fails with `Can't find a usable init.tcl`.

Select a word or phrase and press **F8**, then **o**. The first lookup opens a
standalone window. Later lookups send the new selection to that process,
refresh the same window, and bring it to the front. Oxford is selected by
default. Choose Oxford or Naver from the dictionary dropdown; the selected
dictionary is used for subsequent lookups in that window.

Select text and press **F8**, then **t** to translate it into Korean. The
translator reuses its existing window when new text is selected. Choose Google
Translate, DeepL, Claude, or Codex from the window. Claude uses `claude -p`;
Codex uses `codex exec`. Install and sign in to the chosen CLI first. DeepL
uses the DeepL API Free endpoint. The translator loads `.env` from the workspace
root; values already set in the process environment take precedence.

The dictionary package can also be launched directly with
`uv run --project packages/dictionary-lookup dictionary-lookup WORD`.
Oxford is the default dictionary; start with `--engine naver` to open with
Naver English Dictionary selected.
Dictionary searches query the selected form plus its WordNet lemmas across
noun, verb, adjective, adverb, and satellite adjective categories. On first
use, the app downloads NLTK's WordNet data if it is not already installed.
Both the dictionary and translator windows have a **Font size** control
(8–32 pt). You can also use `Ctrl`/`Cmd` + `+` or `-` to adjust it while the
window is focused.
The translator can be launched with
`uv run --project packages/selected-text-translate selected-text-translate TEXT`.
Set its initial engine with `--engine google`, `--engine deepl`,
`--engine claude`, or `--engine codex`; for example:
`uv run --project packages/selected-text-translate selected-text-translate --engine claude TEXT`.
