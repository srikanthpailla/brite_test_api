SHELL := /bin/bash
DOCKER_IMG = srikanthreddypailla/learning

define version
$(shell cat Dockerfile.version)
endef


define version_check
@if docker pull -q $(DOCKER_IMG):$(call version) >/dev/null 2>/dev/null; then \
	echo "ERROR: please increment version in Dockerfile.$(1).version"; \
	exit 1; \
fi
endef

.PHONY: build
build:
	docker build -t $(DOCKER_IMG):$(call version) .

.PHONY: release
release: build
	$(call version_check)
	docker push (DOCKER_IMG):$(call version)
	docker tag (DOCKER_IMG):$(call version) (DOCKER_IMG):latest
	docker push (DOCKER_IMG):latest