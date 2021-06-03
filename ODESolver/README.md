# ODESolver
Simple ODE solver written in C
# Building
make build
# Tests
make test1
make test2
make test3
# How to use
./odesolver equation intial_condition time_domain
## Example
./odesolver "d2x/dt2 + dx/dt = -x + 5t" "0,5" "0,3"
