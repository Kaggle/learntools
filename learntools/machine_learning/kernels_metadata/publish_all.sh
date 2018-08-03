#!/bin/bash 
find . -type d -depth 1 -exec kaggle kernels push -p {} \;
