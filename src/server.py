from src.monitoring import Monitoring
from fastapi import FastAPI, Path, Request
from .computation import FibonacciSolver, AckermannSolver, FactorialSolver
from .cache import RedisCache


class AppBusiness:
    monitoring: Monitoring
    fibonacci_solver: FibonacciSolver
    factorial_solver: FactorialSolver
    ackermann_solver: AckermannSolver

    def initialize(self):
        self.monitoring = Monitoring()
        self.fibonacci_solver = FibonacciSolver(RedisCache(db_index=0))
        self.factorial_solver = FactorialSolver(RedisCache(db_index=1))
        self.ackermann_solver = AckermannSolver(RedisCache(db_index=2))

        self.monitoring.initialize()

    def finalize(self):
        self.monitoring.finalize()


app = FastAPI()
app_business = AppBusiness()


@app.on_event('startup')
async def app_init():
    app_business.initialize()


@app.on_event('shutdown')
def app_shutdown():
    app_business.finalize()


@app.middleware('http')
async def monitor_time_execution(request: Request, call_next):
    with app_business.monitoring.monitor_execution(request.url.path):
        return await call_next(request)


@app.get('/fibonacci/{n}')
def get_fibonacci(n: int):
    return {'result': app_business.fibonacci_solver.solve(n)}


@app.get('/ackermann/{m}/{n}')
def get_ackermann(m: int, n: int):
    return {'result': app_business.ackermann_solver.solve(m, n)}


@app.get('/factorial/{n}')
def get_factorial(n: int = Path(..., ge=0)):
    return {'result': app_business.factorial_solver.solve(n)}
