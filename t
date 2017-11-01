#!/usr/bin/env bash
py.test tests/test_add.py
py.test tests/test_github_api.py
echo "complete"

