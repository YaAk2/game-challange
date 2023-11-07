.PHONY: 
build-test: ## builds the test image
	docker build -t game-tests .

.PHONY: 
test: ## runs all tests in the image
	docker run game-tests
