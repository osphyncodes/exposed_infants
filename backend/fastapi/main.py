# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys, os, django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from endpoints import auth, children

app = FastAPI()

# CORS middleware
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(children.router, prefix='/exposed-infants')
app.include_router(auth.router, prefix="/api/auth")        # now React can call /api/auth/token/

