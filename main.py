from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from decouple import config

import psycopg2
import psycopg2.extras

conn = psycopg2.connect(database=config('DATABASE_NAME'),
                        host=config('DATABASE_HOST'),
                        user=config('DATABASE_USER'),
                        port=config('DATABASE_PORT'))

cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

async def index(request: Request):
  return JSONResponse(content={"msg": "Hello, world!"})

def records(request: Request):
  cursor.execute("SELECT * FROM records")
  res = cursor.fetchall()
  return JSONResponse(content={"data": res})

routes = [
  Route("/", endpoint = index, methods=['GET']),
  Route("/records", endpoint = records, methods=['GET']),
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*']),
]

app=Starlette(
  debug = True,
  routes = routes,
  middleware = middleware
)