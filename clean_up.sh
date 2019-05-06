#!/bin/bash

set -e

read -p "Enter number of days: " days

nohup sh -c "./manage.sh clean_up ${days}" > /dev/null 2>&1 &