from fastapi import FastAPI
import fastapi
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

# Endpoint de salud
@app.get("/alive")
def alive():
    return {"status": "Server is running!"}
