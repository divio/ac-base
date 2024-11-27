IMAGES=$(shell ls -d py*)


lint:
	find . -type f -name Dockerfile -not -path './EOL-*' -print0 | \
	xargs -0 -I% \
	docker run -v $(shell pwd):/app -e LINT_FILE_DOCKER=% divio/lint \
	/bin/lint --run=docker

test:
	echo $(IMAGES) | tr " " "\n" | xargs -I '{}' ./build.py --repo divio/base --target=prod --tag test-{} build
	echo $(IMAGES) | tr " " "\n" | xargs -I '{}' ./build.py --repo divio/base --target=dev --tag test-{} build
	echo $(IMAGES) | tr " " "\n" | xargs --open-tty -I '{}' ./build.py --repo divio/base --target=dev --tag test-{} test
