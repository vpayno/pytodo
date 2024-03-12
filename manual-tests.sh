#!/usr/bin/env bash

set -e

rm -fv todos.db
pdm run main show
pdm run main add running Sports
pdm run main add sleeping Rest
pdm run main update 1 --task reading --category Study
pdm run main complete 1
pdm run main delete 1
pdm run main show
