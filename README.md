# Recursive computation service

web service which calculates and displays results for Fibonacci, Ackermann, and Factorial functions.

## Getting started

The easiest way of starting the web service it's by using docker.

```sh
docker compose up
```

Docker compose will instance a Redis instance and a Http web service.

After running the containers, you will be able to also run the test suite.

```sh
docker exec recursive-computation_web_service_1 pytest
```


## How to use it
The web service provides the following endpoints:
| URL                        | HTTP METHOD | description |
|----------------------------|-------------|-------------|
| `/fibonacci/n`        | GET         | it computes the nth fibonacci number |
| `/ackermann/m/n` | GET         | it computes the ackerman function for two positive numbers m and n |
| `/factorial/n `       | GET         | it computes the factorial for a positive number |

## Technologies
- Python
- FastAPI
- Poetry
- Mypy

## Implementations

### Fibonacci function

Given `n` be a number and `F(n)` the nth fibonacci number, then it uses the following identity to compute F(n):

```
| 1 1 |^n      | F(n+1) F(n)   |
| 1 0 |     =  | F(n)   F(n-1) |
```

The problem is then translated to compute the nth power of a 2x2 matrix. To compute it, it uses [exponentiation by squaring](https://simple.wikipedia.org/wiki/Exponentiation_by_squaring).

In the process of computing the final result, it caches the values of the intermediate Fibonacci numbers that are generated in each iteration of the exponentiation by squaring:

```
Power(A, n)   = Power(A, n/2)^2    -> cache value for F(n) ...
Power(A, n/2) = Power(A, n/4)^2    -> cache value for F(n/2) ...
Power(A, n/4) = Power(A, n/8)^2    -> cache value F(n/4) = result[0][1], F(n/4 +1) = result[0][0], F(n/4 -1) = result[1][1]
...
```

For computing the Fibonacci of a negative number, it uses the identity:
```
F(-n) = (-1)^n * F(n)
```

which allows to compute it from the result of its positive version. This allow to reduce the data in cache since it just computes/caches Fibonacci of positive numbers.


### Ackermann function

It solves it using the following definition

```
Ackermann(m, n) = | n + 1, when m = 0
                  | n + 2, when m = 1
				  | (2 -> n + 3 -> m -2) -3, when m >= 2
```

where `->` represents (Conway chained arrow notation)[https://en.wikipedia.org/wiki/Conway_chained_arrow_notation]

Then for m >=2, the problem is equivalent to expand a 3 length chained arrow number.


### Factorial function

It uses the standard recursive definition of the factorial function.

n! = n*(n-1)!

However, it relies on the cached result of the previous operations to reduce the number of multiplications to perform. It achieves this by keeping a sorted set of previously cached factorials and then finding the max cached factorial that is lower than n (n's floor). Thus:


```
Factorial(n) = | factorial_cache[n], when n <= max_computed_n
               | n*(n-1)(n-2)*...*factorial_cache[n_floor]
```

which will perform `(n - max_copmuted_n)` multiplications in the second case.


## Monitoring

The web service has a middleware that registers in an append log file the response time of all success requests. the file is located in `<project-root>/.data/monitoring.log`


## Future improvements

- The Ackermann function produces huge numbers with small inputs, for instance, m = 4, n = 3. Computing arithmetic operations in huge numbers increases dramatically the memory consumption even to a point where the whole machine's memory is not enough to finish the operation. It might be possible to achieve a constant memory consumption when computing Ackermann by performing the multiplication operation in smaller chunks(see big_number.py module)  and reading/saving the numbers in the disk. 