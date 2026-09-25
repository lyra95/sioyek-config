.PHONY: install

ifeq ($(OS),Windows_NT)
INSTALL_CONFIG = pwsh -ExecutionPolicy Bypass -File install-keys.ps1
else
SIOYEK_CONFIG_DIR = $(HOME)/Library/Application Support/sioyek
INSTALL_CONFIG = mkdir -p "$(SIOYEK_CONFIG_DIR)" && cp keys_user.config prefs_user.config "$(SIOYEK_CONFIG_DIR)/"

ifeq ($(shell uname -s),Darwin)
# Keep uv's managed environments and their command shims in shared locations.
# /usr/local/bin is on the default PATH for macOS users.
UV_TOOL_DIR ?= /usr/local/share/uv/tools
UV_TOOL_BIN_DIR ?= /usr/local/bin
UV = $(shell command -v uv)
INSTALL_TOOLS = sudo env UV_TOOL_DIR="$(UV_TOOL_DIR)" UV_TOOL_BIN_DIR="$(UV_TOOL_BIN_DIR)" "$(UV)" tool install --editable
else
INSTALL_TOOLS = uv tool install --editable
endif
endif

install: install-config
	$(INSTALL_TOOLS) packages/dictionary-lookup
	$(INSTALL_TOOLS) packages/selected-text-translate

install-config:
	$(INSTALL_CONFIG)
