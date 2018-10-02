#!/bin/bash
## script to run jupyter notebook in repo

## Source (botcorn)
source /home/marcel/Documents/botcorn/virtenv/botcorn/bin/activate

## Change dir to repo
cd /home/marcel/Documents/botcorn/repo_online

## Update repo
git pull

## Run jupyter notebook
jupyter notebook &
