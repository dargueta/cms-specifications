#!/bin/sh

set -eux

rm -f dependencies.mk
make dependencies.mk
make clean
