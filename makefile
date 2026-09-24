.PHONY: install

ifeq ($(OS),Windows_NT)
INSTALL_CONFIG = pwsh -ExecutionPolicy Bypass -File install-keys.ps1
else
SIOYEK_CONFIG_DIR = $(HOME)/Library/Application Support/sioyek
INSTALL_CONFIG = mkdir -p "$(SIOYEK_CONFIG_DIR)" && cp keys_user.config prefs_user.config "$(SIOYEK_CONFIG_DIR)/"
endif

install: install-config
	uv tool install --editable packages/dictionary-lookup
	uv tool install --editable packages/selected-text-translate

install-config:
	$(INSTALL_CONFIG)
