#!/bin/bash

git add .
git commit -m 'update'
git push -u origin dev
git tag v1.0-rc2
git push --tag
