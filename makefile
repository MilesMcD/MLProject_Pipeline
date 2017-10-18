#this makefile is placed above the src makefile for testing purposes.

.PHONY: all test

all: test

test: all
	python -m pytest src

