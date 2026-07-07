from fastapi import FastAPI
from server.api import router

app=FastAPI(title="Pyshki Queue")
app.include_router(router)

@app.get("/")
def root():
    return {"name":"Pyshki Queue","status":"running"}
