from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, cgm, alerts, chat, sos, location, ai, preferences, reports, users

app = FastAPI(title="GlyWatch API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(cgm.router)
app.include_router(alerts.router)
app.include_router(chat.router)
app.include_router(sos.router)
app.include_router(location.router)
app.include_router(ai.router)
app.include_router(preferences.router)
app.include_router(reports.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "GlyWatch API is live"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 