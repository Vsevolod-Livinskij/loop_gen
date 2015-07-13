#/bin/bash
python main.py > a.cpp
icc a.cpp -S -vec-report=7
cat a.optrpt
