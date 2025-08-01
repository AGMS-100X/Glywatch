from fastapi import APIRouter

router = APIRouter(prefix="/location", tags=["Location"])

@router.post("/update")
async def update_location(patient_id: str, latitude: float, longitude: float):
    # TODO: Implement location update logic
    return {"message": f"Location updated for patient {patient_id}", "latitude": latitude, "longitude": longitude}

@router.get("/current/{patient_id}")
async def get_current_location(patient_id: str):
    # TODO: Implement current location retrieval
    return {"patient_id": patient_id, "latitude": 0.0, "longitude": 0.0} 