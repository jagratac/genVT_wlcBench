# Intel Copyright © 2021, Intel Corporation.

APP_NAME := moonshot
BUILDER_DOCKER_IMG := ubuntu
APP_RUNNER_DOCKER := $(USER)/$(APP_NAME)-runner
override DOCKER_REGISTRY := $(and $(DOCKER_REGISTRY),$(DOCKER_REGISTRY)/)
DOCKER_BUILD=docker build

CMD=docker run \
	-v ${CURDIR}:${CURDIR} \
	-w ${CURDIR} \
	--rm \
	-u `id -u`:`id -g` \
	-e HOME=${HOME} \
	$(BUILDER_DOCKER_IMG) \
	echo $@

.PHONY: all clean install package test check

all: clean package

install:
	 $(CMD)

test:
	$(CMD)

check:
	$(CMD)

package: install
	docker build --tag $(DOCKER_REGISTRY)$(APP_RUNNER_DOCKER) .
ifdef DOCKER_REGISTRY
	docker push $(DOCKER_REGISTRY)$(APP_RUNNER_DOCKER)
endif

deploy:
	docker run --rm $(APP_RUNNER_DOCKER)
