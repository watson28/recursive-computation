from fastapi import FastAPI, Path
from .computation import FibonacciSolver, AckermannSolver, FactorialSolver
from .cache import RedisCache

app = FastAPI()
fibonacci_solver: FibonacciSolver
factorial_solver: FactorialSolver
ackermann_solver: AckermannSolver


@app.on_event('startup')
async def app_init():
    global fibonacci_solver
    global factorial_solver
    global ackermann_solver
    fibonacci_solver = FibonacciSolver(RedisCache(db_index=0))
    factorial_solver = FactorialSolver(RedisCache(db_index=1))
    ackermann_solver = AckermannSolver(RedisCache(db_index=2))


@app.get('/fibonacci/{n}')
def get_fibonacci(n: int):
    global fibonacci_solver
    return {'result': fibonacci_solver.solve(n)}


@app.get('/ackermann/{m}/{n}')
def get_ackermann(m: int, n: int):
    global ackermann_solver
    return {'result': ackermann_solver.solve(m, n)}


@app.get('/factorial/{n}')
def get_factorial(n: int = Path(..., ge=0)):
    global factorial_solver
    return {'result': factorial_solver.solve(n)}
