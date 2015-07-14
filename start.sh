#/bin/bash
rm func.cpp func.s test.cpp no-opt.log opt.log a.out func.optrpt
python main.py
icc func.cpp -S -O0 -restrict
icc func.s test.cpp -O0 -restrict
./a.out > no-opt.log
icc func.cpp -S -vec-report=7 -restrict
icc func.s test.cpp -restrict
./a.out > opt.log
cat func.optrpt
diff opt.log no-opt.log
