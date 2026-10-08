#!/bin/sh
cd "$(dirname "$0")"
exec ./skifree > log.txt 2>&1
