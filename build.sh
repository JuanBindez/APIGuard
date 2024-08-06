#!/bin/bash

git add .
git commit -m 'update'
git push -u origin dev
git tag v1.0-rc5
git push --tag
