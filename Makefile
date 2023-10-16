# Define a variable for Python and notebook files.
PYTHON_FILES=.

#* Lint
.PHONY: lint
lint:
	poetry run black $(PYTHON_FILES) --check
	poetry run isort --settings-path pyproject.toml ./
