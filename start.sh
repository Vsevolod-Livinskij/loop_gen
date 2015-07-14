#/bin/bash
rm func.cpp func.s test.cpp no-opt.log opt.log a.out func.optrpt
python main.py
icc func.cpp -S -O0
icc func.s test.cpp -O0
./a.out > no-opt.log
icc func.cpp -S -vec-report=7 
icc func.s test.cpp
./a.out > opt.log
cat func.optrpt
diff opt.log no-opt.log
