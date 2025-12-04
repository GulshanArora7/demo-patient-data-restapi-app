# Patient Data API (Python/FastAPI)

A Python FastAPI REST API server that exposes patient data from `dummy_patient_data.json` for use with AI agents.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --reload --port 8000
```

The server will start on `http://localhost:8000` by default.

## API Endpoints

### Health Check
- **GET** `/health`
  - Returns server status

### Root
- **GET** `/`
  - Returns API information and available endpoints

### Patients
- **GET** `/api/patients`
  - Get all patients
  - Response: `{ success: true, count: number, patients: [...] }`

- **GET** `/api/patients/{patientId}`
  - Get a specific patient by ID (e.g., `PAT-001`)
  - Response: `{ success: true, patient: {...} }`

- **GET** `/api/patients/search/name?firstName=...&lastName=...`
  - Search patients by name
  - Query parameters: `firstName` (optional), `lastName` (optional)
  - Response: `{ success: true, count: number, patients: [...] }`

### Patient Details
- **GET** `/api/patients/{patientId}/appointments?type=upcoming|recent|past`
  - Get patient appointments
  - Query parameter: `type` (optional) - `upcoming`, `recent`, `past`, or omit for all
  - Response: `{ success: true, appointments: {...} }`

- **GET** `/api/patients/{patientId}/test-results?testType=Laboratory|Radiology`
  - Get patient test results
  - Query parameter: `testType` (optional) - `Laboratory`, `Radiology`, or omit for all
  - Response: `{ success: true, count: number, testResults: [...] }`

- **GET** `/api/patients/{patientId}/medical-history`
  - Get patient medical history
  - Response: `{ success: true, medicalHistory: {...} }`

- **GET** `/api/patients/{patientId}/insurance`
  - Get patient insurance information
  - Response: `{ success: true, insurance: {...} }`

- **GET** `/api/patients/{patientId}/care-providers`
  - Get patient care providers
  - Response: `{ success: true, careProviders: [...] }`

- **GET** `/api/patients/{patientId}/procedures`
  - Get patient procedures
  - Response: `{ success: true, procedures: [...] }`

## Interactive API Documentation

FastAPI automatically provides interactive documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Example Usage

### Get all patients
```bash
curl http://localhost:8000/api/patients
```

### Get specific patient
```bash
curl http://localhost:8000/api/patients/PAT-001
```

### Search patients by name
```bash
curl "http://localhost:8000/api/patients/search/name?firstName=Sarah"
```

### Get patient appointments
```bash
curl "http://localhost:8000/api/patients/PAT-001/appointments?type=upcoming"
```

### Python example
```python
import requests

# Get all patients
response = requests.get("http://localhost:8000/api/patients")
data = response.json()
print(f"Total patients: {data['count']}")

# Get specific patient
patient = requests.get("http://localhost:8000/api/patients/PAT-001").json()
print(patient['patient']['personalInformation']['firstName'])
```

## Deployment Options (No Local Hosting Required)

### Option 1: Railway (Recommended - Free Tier Available)
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create new project → Deploy from GitHub
4. Connect your repository
5. Railway auto-detects Python and deploys
6. Your API will be live at `https://your-app.railway.app`

**Required files for Railway:**
- `requirements.txt` (already created)
- `Procfile` (create with: `web: uvicorn app:app --host 0.0.0.0 --port $PORT`)

### Option 2: Render (Free Tier Available)
1. Go to [render.com](https://render.com)
2. Sign up and create new Web Service
3. Connect GitHub repository
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Deploy

### Option 3: Fly.io (Free Tier Available)
1. Install flyctl: `curl -L https://fly.io/install.sh | sh`
2. Run: `fly launch`
3. Follow prompts
4. Deploy: `fly deploy`

### Option 4: Vercel (Serverless Functions)
1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```
3. Run: `vercel --prod`

### Option 5: Google Cloud Run (Free Tier Available)
1. Install gcloud CLI
2. Build container: `gcloud builds submit --tag gcr.io/PROJECT-ID/patient-api`
3. Deploy: `gcloud run deploy --image gcr.io/PROJECT-ID/patient-api`

### Option 6: AWS Lambda (Serverless)
Use Mangum adapter to wrap FastAPI for Lambda deployment.

## Alternative: Postman Mock Server (No Code Required)

**Yes, you can use Postman Mock Servers without running anything locally!**

### Steps:
1. **Create Postman Collection:**
   - Open Postman
   - Create a new Collection called "Patient API"
   - Add requests for each endpoint (GET /api/patients, etc.)
   - For each request, add example responses using your JSON data

2. **Create Mock Server:**
   - Click "..." on your collection → "Mock this collection"
   - Configure mock server settings
   - Postman generates a public URL like: `https://your-mock-id.mock.pstmn.io`

3. **Limitations:**
   - Static responses only (no dynamic filtering)
   - Limited to example responses you define
   - Free tier has rate limits
   - Less flexible than a real API

4. **Better Alternative - Postman Cloud:**
   - Postman Cloud can host real APIs but requires subscription
   - Not ideal for this use case

## Recommended Approach

**For AI Agents:** Use **Railway** or **Render** (both free tiers available)
- Real API with full functionality
- Dynamic responses
- No local hosting needed
- Easy deployment from GitHub
- Free tier sufficient for development/testing

## Environment Variables

- `PORT` - Server port (default: 8000)
- Railway/Render automatically set `PORT` in production

## Notes

- The API reads patient data from `../dummy_patient_data.json` at startup
- All endpoints return JSON responses
- CORS is enabled for all origins to allow cross-origin requests from AI agents
- FastAPI automatically generates OpenAPI/Swagger documentation

