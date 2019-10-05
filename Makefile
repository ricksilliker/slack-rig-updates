.DEFAULT_GOAL := help

# Setup
SHELL := /bin/bash
MMAKE := $(shell which make)
WORKSPACE ?= ${PWD}
PROJECT_NAME := slack_rig_updater

# Maya
DEFAULT_MAYA_VERSION := 2019
MAYA_VERSION := 2019
MAYA_MODULE_PATH := ${WORKSPACE}/dist
MAYA_OSX := ./scripts/run-maya.sh

# Push the variables to the env.
export DEFAULT_MAYA_VERSION MAYA_VERSION WORKSPACE MAYA_MODULE_PATH

# Remove all files related to build Python packages.
.PHONY : clean
clean:
	rm -Rf build dist src/*.egg-info .eggs *.egg
	find . -name "*.pyc" -exec rm -f {} \;

# Build into a useable Maya module in the dist directory at the project root.
.PHONY : build
build:
	${MMAKE} clean
	mkdir -p ${WORKSPACE}/dist/slack_rig_updater/scripts/slack_rig_updater
	cp -r ${WORKSPACE}/slack-rig-updater/src/slack_rig_updater ${WORKSPACE}/dist/slack_rig_updater/scripts
	cp ${WORKSPACE}/slack-rig-updater/src/slack_rig_updater.mod ${WORKSPACE}/dist/slack_rig_updater.mod
	cp ${WORKSPACE}/slack-rig-updater/src/userSetup.py ${WORKSPACE}/dist/slack_rig_updater/scripts/userSetup.py

# Install with symlinks to this folder for faster development.
.PHONY : develop
develop:
	${MMAKE} clean
	mkdir -p ${WORKSPACE}/dist/slack_rig_updater/scripts
	ln -sf ${WORKSPACE}/slack-rig-updater/src/slack_rig_updater ${WORKSPACE}/dist/slack_rig_updater/scripts
	ln -sf ${WORKSPACE}/slack-rig-updater/src/slack_rig_updater.mod ${WORKSPACE}/dist/slack_rig_updater.mod
	ln -sf ${WORKSPACE}/slack-rig-updater/src/userSetup.py ${WORKSPACE}/dist/slack_rig_updater/scripts/userSetup.py

# Open Maya with butterfly.
.PHONY : start-maya
start-maya:
	@echo -e "\n\033[92mDeploying...\033[0m"
	${MAYA_OSX} ${MAYA_VERSION}

# Just some help.
.PHONY : help
help: ${MMAKE}
	${MMAKE} help