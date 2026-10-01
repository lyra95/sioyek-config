# AGENTS.md

uv workspace with two Sioyek companion tools: Tkinter GUIs using only the Python
standard library (`nltk` in the dictionary package). No tests, linters, or CI —
verify by running the tools.

## Layout

- Root `pyproject.toml` only defines the uv workspace; all code is in `packages/`.
- `packages/dictionary-lookup` → entrypoint `dictionary-lookup`
  (`dictionary_lookup.app:main`), engines `oxford` (default) / `naver`.
- `packages/selected-text-translate` → entrypoint `selected-text-translate`
  (`selected_text_translate.app:main`), engines `google` (default) / `deepl` /
  `claude` / `codex`.
- `keys_user.config` / `prefs_user.config` are **copied into the Sioyek install**,
  never read from the repo. `.env` (gitignored, from `.env.example`) holds
  `DEEPL_AUTH_KEY`.

## Commands

- `make install` — `uv tool install --editable` both packages, then copy configs
  to Sioyek (Windows: WinGet install dirs via `install-keys.ps1`; macOS:
  sudo to `/usr/local`, configs to `~/Library/Application Support/sioyek`).
  Re-run after any change to `keys_user.config` / `prefs_user.config`, then
  reload Sioyek's configuration. `make install-config` copies only the configs.
- `uv run --project packages/dictionary-lookup dictionary-lookup [--engine oxford|naver] WORD`
- `uv run --project packages/selected-text-translate selected-text-translate [--engine google|deepl|claude|codex] TEXT`

## Gotchas

- Sioyek shortcuts are `ad` (lookup) and `as` (translate) per
  `keys_user.config`; the README's "F8 then o / t" is stale. The Sioyek
  shortcuts also force `--engine naver` / `--engine deepl`, so installed
  behavior differs from the CLI defaults (Oxford/Google).
- Single-instance IPC over 127.0.0.1 TCP: while a window is open, a new launch
  just sends its text to the running window instead of opening one (port
  derived from user + app name, see `instance.py`). Close stale windows when
  debugging.
- Keep `_configure_tk_libraries()` early in `app.py` `main()`: uv-managed
  Python needs `TCL_LIBRARY`/`TK_LIBRARY` set, otherwise Tk fails with
  "Can't find a usable init.tcl".
- Translator loads `.env` from the workspace root (path computed from
  `config.py`'s location); values already in the process environment win.
- `claude`/`codex` engines shell out to `claude -p` /
  `codex exec --ephemeral --skip-git-repo-check` and need those CLIs installed
  and signed in; DeepL uses the API Free endpoint; Google uses the unofficial
  `translate.googleapis.com` endpoint.
- Dictionary downloads NLTK WordNet on first use (needs internet); offline, run
  `uv run --project packages/dictionary-lookup python -m nltk.downloader wordnet`.
- Launch errors are logged to `~/Library/Logs/sioyek-text-tools.log` on every
  platform (created under the user's home dir).
