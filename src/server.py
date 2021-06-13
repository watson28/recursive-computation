from fastapi import FastAPI, Path
from .computation import fibonacci, ackermann, factorial

app = FastAPI()


@app.get('/fibonacci/{n}')
def get_fibonacci(n: int = Path(..., ge=0)):
    return {'result': fibonacci(n)}

@app.get('/ackermann/{m}/{n}')
def get_ackermann(m: int, n: int):
    return {'result': ackermann(m, n)}

@app.get('/factorial/{n}')
def get_factorial(n: int):
    return {'result': factorial(n)}
