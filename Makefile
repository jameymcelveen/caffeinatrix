.PHONY: help install start logo pack dist dist-mac dist-win npm-pack npm-publish commit

.DEFAULT_GOAL := help

MSG ?=

help: ## show targets
	@echo "Caffeinatrix — the screen stays awake, the rain keeps falling"
	@echo ""
	@grep -E '^[a-zA-Z0-9_.-]+:.*##' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*## "}; {printf "  make %-12s %s\n", $$1, $$2}'

install: ## npm install
	npm install

start: ## run Electron from source
	npm start

logo: ## regenerate assets/logo.svg
	python3 build_logo.py

pack: ## unpacked app in dist/
	npm run pack

dist-mac: ## macOS .dmg in release/
	npm run dist:mac

dist-win: ## Windows NSIS installer in release/
	npm run dist:win

npm-pack: ## dry-run: list files that would ship to npm
	npm pack --dry-run

npm-publish: ## publish @jameymcelveen/cafx to npm (npm login required)
	npm publish --access=public

commit: ## stage all and commit (MSG="message"; use \n for body lines)
ifndef MSG
	$(error commit requires MSG, e.g. make commit MSG="feat: add keep-awake toggle")
endif
	git add -A
	@git status --short
	@printf '%b' "$(MSG)\n" | git commit -F -
