ECHO=@
DEMO_GALLERATOR=$(PWD)/../demo-gallerator

default:
	@echo No default rule - look in Makefile
	$(ECHO)exit 1


venv:
	@echo Making venv
	$(ECHO) python3 -m venv venv
	$(ECHO) ./venv/bin/pip3 install $(PWD)

lint:
	@echo Running ruff
	$(ECHO) ruff check --select I

lint-fix:
	@echo Running ruff --fix
	$(ECHO) ruff check --select I --fix

test:
	@echo Testing
	$(ECHO) if [ ! -d $(DEMO_GALLERATOR) ] ; then \
		echo '**Error** $(DEMO_GALLERATOR) was not found' ; \
		exit 1 ; \
	fi
	$(ECHO) python3 -m unittest src/gallerator/tests/*.py

# If you want to use nanogallery2, you'll need to download the distribution
# files. Do that with
# make download-nanogallery2
download-nanogallery2:
	$(ECHO) ./src/gallerator/renderers/nanogallery2/download.sh

# If you want to remove these files again
remove-download-nanogallery2:
	$(ECHO) ./src/gallerator/renderers/nanogallery2/removeDownloaded.sh

update-readme-usage:
	@echo Updating README.md
	$(ECHO) ./release-tools/replace-markdown-block.sh README.md usage

update-docs: update-readme-usage
