#!/bin/bash

python3 ./client/test_classify.py &
python3 ./client/test_summarise.py &
python3 ./client/test_translate.py &

wait
