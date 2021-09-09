build:
	gcc -c *.c
	gcc -o odesolver *.o -lm
	rm *.o
test1:
	./odesolver "d2x/dt2 = -x" "0,5" "0,5"
test2:
	./odesolver "d2x/dt2 + t = -2*x" "0,5" "0,5"
test3:
	./odesolver "d2x/dt2 + dx/dt = -2*x" "0,5" "0,5"
