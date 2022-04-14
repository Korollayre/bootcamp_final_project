#!/usr/bin/env bash

set -e

gunicorn -b 0.0.0.0:1234 users_backend.composites.api:app --reload