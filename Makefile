SRC_DIR		= otpbot
TEST_DIR	= tests
PULUMI_DIR	= pulumi
CHECK_DIRS = $(SRC_DIR) $(TEST_DIR) $(PULUMI_DIR)

install: 
	poetry run pip install --upgrade pip
	poetry install -v

update: ## Update python dependencies
	poetry update

format: ## Format repository code
	poetry run black $(CHECK_DIRS)
	poetry run isort $(CHECK_DIRS)

format-check: ## Check the code format
	poetry run isort --check $(CHECK_DIRS)
	poetry run black --check $(CHECK_DIRS)

lint: ## Launch the linting tool
	poetry run flake8 $(CHECK_DIRS)

type-check: ## Launch the type checking tool
	poetry run mypy --ignore-missing-imports $(CHECK_DIRS)

check: format-check lint type-check ## Launch all check to approve the code
