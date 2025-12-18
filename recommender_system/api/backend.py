from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from api.input_handler import process_input 
import traceback
app = FastAPI(title="Assessment Recommendation API")

# 1. Enable CORS so your HTML/JS frontend can communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Define Request Model
class QueryRequest(BaseModel):
    query: str

# 3. Health Check Endpoint (As requested in image_cb8aaf.png)
@app.get("/health", summary="Health Check Endpoint")
async def health_check():
    """
    Provides a simple status check to verify the API is running.
    """
    return {"status": "healthy"}

# 4. Recommendation Endpoint (As requested in image_cb0acf.png)
@app.post("/recommend")
async def recommend_assessments(request: QueryRequest):
    try:
        # Calls the function that processes retrieval, reranking, and domain mapping
        result = process_input(request.query)
        
        # Ensure the response is returned with a 200 OK status
        return JSONResponse(content=result, status_code=200)
    
    except Exception as e:
        traceback.print_exc()
        # Returns a 500 error if something fails in the pipeline
        raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     # Starts the server on port 8000
#     uvicorn.run(app, host="0.0.0.0", port=8000)