#!/bin/bash

git add .
git commit -m 'initial'
git push -u origin main
git tag v1.0-rc1
git push --tag
