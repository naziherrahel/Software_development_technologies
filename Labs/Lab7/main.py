from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="SmartBuilding Devices API")

# In-memory "database"
devices = [
    {
        "id": 1,
        "name": "coffee_machine",
        "energy_usage": 120,
        "status": "active",
        "location": "kitchen"
    },
    {
        "id": 2,
        "name": "smart_lamp",
        "energy_usage": 40,
        "status": "inactive",
        "location": "office"
    }
]

class Device(BaseModel):
    id: int
    name: str
    energy_usage: int
    location: str 
    status: str = "inactive"

