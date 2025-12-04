"""
Patient Data API - FastAPI implementation
A REST API server that exposes patient data for use with AI agents.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
from pathlib import Path
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="Patient Data API",
    description="REST API for patient data to be used with AI agents",
    version="1.0.0"
)

# Enable CORS for all origins (for AI agent access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load patient data
DATA_PATH = Path("dummy_patient_data.json")

try:
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        patient_data = json.load(f)
except FileNotFoundError:
    print(f"Error: Could not find {DATA_PATH}")
    patient_data = {"patients": []}
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON in {DATA_PATH}: {e}")
    patient_data = {"patients": []}


def find_patient_by_id(patient_id: str):
    """Helper function to find patient by ID"""
    for patient in patient_data.get("patients", []):
        if patient.get("patientId") == patient_id:
            return patient
    return None


# Routes

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Patient Data API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "all_patients": "/api/patients",
            "patient_by_id": "/api/patients/{patientId}",
            "search_patients": "/api/patients/search/name",
            "appointments": "/api/patients/{patientId}/appointments",
            "test_results": "/api/patients/{patientId}/test-results",
            "medical_history": "/api/patients/{patientId}/medical-history",
            "insurance": "/api/patients/{patientId}/insurance",
            "care_providers": "/api/patients/{patientId}/care-providers",
            "procedures": "/api/patients/{patientId}/procedures"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Patient API is running"}


@app.get("/api/patients")
async def get_all_patients():
    """Get all patients"""
    return {
        "success": True,
        "count": len(patient_data.get("patients", [])),
        "patients": patient_data.get("patients", [])
    }


@app.get("/api/patients/{patient_id}")
async def get_patient_by_id(patient_id: str):
    """Get patient by ID"""
    patient = find_patient_by_id(patient_id)
    
    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    return {
        "success": True,
        "patient": patient
    }


@app.get("/api/patients/search/name")
async def search_patients_by_name(
    firstName: Optional[str] = Query(None, description="Patient's first name"),
    lastName: Optional[str] = Query(None, description="Patient's last name")
):
    """Search patients by name"""
    results = patient_data.get("patients", [])
    
    if firstName:
        results = [
            p for p in results
            if firstName.lower() in p.get("personalInformation", {}).get("firstName", "").lower()
        ]
    
    if lastName:
        results = [
            p for p in results
            if lastName.lower() in p.get("personalInformation", {}).get("lastName", "").lower()
        ]
    
    return {
        "success": True,
        "count": len(results),
        "patients": results
    }


@app.get("/api/patients/{patient_id}/appointments")
async def get_patient_appointments(
    patient_id: str,
    type: Optional[str] = Query(None, description="Filter by type: upcoming, recent, or past")
):
    """Get patient appointments"""
    patient = find_patient_by_id(patient_id)
    
    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    appointments = patient.get("appointments", {})
    
    if type and type in ["upcoming", "recent", "past"]:
        return {
            "success": True,
            "type": type,
            "appointments": appointments.get(type, [])
        }
    
    return {
        "success": True,
        "appointments": appointments
    }


@app.get("/api/patients/{patient_id}/test-results")
async def get_patient_test_results(
    patient_id: str,
    testType: Optional[str] = Query(None, description="Filter by test type: Laboratory or Radiology")
):
    """Get patient test results"""
    patient = find_patient_by_id(patient_id)
    
    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    results = patient.get("testResults", [])
    
    if testType:
        results = [test for test in results if test.get("testType") == testType]
    
    return {
        "success": True,
        "count": len(results),
        "testResults": results
    }


@app.get("/api/patients/{patient_id}/medical-history")
async def get_patient_medical_history(patient_id: str):
    """Get patient medical history"""
    patient = find_patient_by_id(patient_id)
    
    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    return {
        "success": True,
        "medicalHistory": patient.get("medicalHistory", {})
    }


@app.get("/api/patients/{patient_id}/insurance")
async def get_patient_insurance(patient_id: str):
    """Get patient insurance information"""
    patient = find_patient_by_id(patient_id)
    
    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    return {
        "success": True,
        "insurance": patient.get("insurance", {})
    }


@app.get("/api/patients/{patient_id}/care-providers")
async def get_patient_care_providers(patient_id: str):
    """Get patient care providers"""
    patient = find_patient_by_id(patient_id)
    
    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    return {
        "success": True,
        "careProviders": patient.get("careProviders", [])
    }


@app.get("/api/patients/{patient_id}/procedures")
async def get_patient_procedures(patient_id: str):
    """Get patient procedures"""
    patient = find_patient_by_id(patient_id)
    
    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    return {
        "success": True,
        "procedures": patient.get("procedures", [])
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

