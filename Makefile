lint:
	find . -type f -name Dockerfile -not -path './EOL-*' -print0 | \
	xargs -0 -I% \
	docker run -v $(shell pwd):/app -e LINT_FILE_DOCKER=% divio/lint \
	/bin/lint --run=docker
