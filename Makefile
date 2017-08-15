TARGET ?= prod
DOCKER_TAG ?= latest
ifeq ($(TARGET),prod)
	IMAGE_NAME ?= divio/base:$(DOCKER_TAG)
else
	IMAGE_NAME ?= divio/base:$(DOCKER_TAG)-$(TARGET)
endif


build:
	docker build -t $(IMAGE_NAME) --build-arg TARGET=$(TARGET) -f Dockerfile .

test:
	docker run --rm -it $(IMAGE_NAME) pip install psycopg2 cryptography numpy scipy pillow lxml pyyaml

all:
	$(MAKE) build TARGET=prod
	$(MAKE) build TARGET=dev

docker_hub_build:
ifneq (,$(findstring -dev,$(IMAGE_NAME)))
	$(MAKE) build TARGET=dev
else
	$(MAKE) build TARGET=prod
endif
