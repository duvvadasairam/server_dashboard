from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import alerts, servers, metrics
import uvicorn

app = FastAPI(
    title="Server Monitoring API",
    description="API for server monitoring dashboard",
    version="0.1.0"
)

# Add CORS middleware
origins = [
    "http://localhost",          #Allow localhost for development
    "http://localhost:3000",     #Common React dev port
    "http://localhost:5173",     #Vite default dev port
    #Add other origins if your frontend is served from a different port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  #accepts  all methods
    allow_headers=["*"],  #accepts all headers
)

#include router's
app.include_router(alerts.router)
app.include_router(servers.router)
app.include_router(metrics.router)

#Root endpoint to show backend is active
@app.get("/", tags=["root"])
async def root():
    """Root endpoint to verify backend is active."""
    return {"message": "Backend is active. Welcome to the Server Monitoring API!"}

#Health check endpoint
@app.get("/health", tags=["healthcheck"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

#Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
