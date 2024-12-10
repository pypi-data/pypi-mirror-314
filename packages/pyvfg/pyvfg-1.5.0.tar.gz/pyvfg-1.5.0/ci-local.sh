#!/usr/bin/env zsh
set -e

## Runs gh-workflow locally using [act](https://github.com/nektos/act)

act --container-architecture linux/amd64 -P ubuntu-latest-xl=catthehacker/ubuntu:act-latest -s GITHUB_TOKEN=`gh auth token`
