#!/bin/sh

set -eux

make clean
docker build -t cms-specifications/parser-generator:latest parser_generator
