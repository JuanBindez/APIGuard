#!/bin/bash

git add .
git commit -m 'APIGuard 1.0.0'
git push -u origin main
git tag v1.0.0
git push --tag
