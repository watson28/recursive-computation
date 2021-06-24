from fastapi import FastAPI, Path
from .computation import FibonacciSolver, ackermann, FactorialSolver
from .cache import RedisCache

app = FastAPI()
fibonacci_solver: FibonacciSolver
factorial_solver: FactorialSolver

@app.on_event('startup')
async def app_init():
    global fibonacci_solver
    global factorial_solver 
    fibonacci_solver = FibonacciSolver()
    factorial_solver = FactorialSolver(RedisCache())

@app.get('/fibonacci/{n}')
def get_fibonacci(n: int = Path(..., ge=0)):
    return {'result': fibonacci_solver.solve(n)}

@app.get('/ackermann/{m}/{n}')
def get_ackermann(m: int, n: int):
    return {'result': ackermann(m, n)}

@app.get('/factorial/{n}')
def get_factorial(n: int = Path(..., ge=0)):
    return {'result': factorial_solver.solve(n)}
