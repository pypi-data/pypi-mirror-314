#!/bin/bash

echo "Black:" &&
black --check reacTk example &&
echo "" &&
echo "Flake8:" &&
flake8 --max-line-length 127 reacTk example

