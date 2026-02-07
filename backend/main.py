from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
import asyncio
from dotenv import load_dotenv
from rag_service import RAGService
from datetime import datetime
import json

load_dotenv()

app = FastAPI(title="HOA Bylaws Lookup API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_service = RAGService()

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str
    sources: List[str]

class ChangeRequest(BaseModel):
    homeowner_name: str
    email: EmailStr
    address: str
    change_type: str
    description: str
    urgency: Optional[str] = "normal"

class ChangeRequestResponse(BaseModel):
    request_id: str
    status: str
    submitted_at: str

@app.get("/")
def read_root():
    return {"message": "HOA Bylaws Lookup API", "version": "1.0.0"}

@app.post("/api/ask", response_model=Answer)
async def ask_question(question: Question):
    """Ask a question about HOA bylaws"""
    try:
        # Add timeout to prevent hanging (increased to 120 seconds)
        result = await asyncio.wait_for(
            rag_service.query(question.question),
            timeout=120.0  # 120 second timeout (first query may take longer)
        )
        return Answer(
            answer=result["answer"],
            sources=result["sources"]
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Query timed out after 120 seconds. The LLM may be slow or not responding. If using Ollama, ensure it's running and try: 'ollama run mistral' to warm up the model."
        )
    except Exception as e:
        print(f"Error in ask_question endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-bylaws")
async def upload_bylaws(file: UploadFile = File(...)):
    """Upload PDF bylaws documents to the knowledge base"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Ensure documents directory exists
        os.makedirs("documents", exist_ok=True)
        
        # Read file content
        content = await file.read()
        
        # Validate file is not empty
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        # Save file
        file_path = os.path.join("documents", file.filename)
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Index document
        await rag_service.index_document(file_path)
        
        return {
            "message": f"Document {file.filename} uploaded and indexed successfully",
            "filename": file.filename,
            "size": len(content)
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log and return other errors
        print(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.post("/api/submit-request", response_model=ChangeRequestResponse)
async def submit_change_request(request: ChangeRequest):
    """Submit a request for home modifications"""
    try:
        request_id = f"REQ-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Save request to file (in production, use a database)
        requests_dir = "requests"
        os.makedirs(requests_dir, exist_ok=True)
        
        request_data = {
            "request_id": request_id,
            "homeowner_name": request.homeowner_name,
            "email": request.email,
            "address": request.address,
            "change_type": request.change_type,
            "description": request.description,
            "urgency": request.urgency,
            "status": "submitted",
            "submitted_at": datetime.now().isoformat()
        }
        
        with open(f"{requests_dir}/{request_id}.json", "w") as f:
            json.dump(request_data, f, indent=2)
        
        return ChangeRequestResponse(
            request_id=request_id,
            status="submitted",
            submitted_at=request_data["submitted_at"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    """Check service health and configuration"""
    provider = os.getenv("LLM_PROVIDER", "ollama")
    model = os.getenv("OLLAMA_MODEL" if provider == "ollama" else "HUGGINGFACE_MODEL", "mistral")
    
    return {
        "status": "healthy",
        "rag_initialized": rag_service.is_initialized(),
        "llm_provider": provider,
        "model": model,
        "has_documents": rag_service.vectorstore is not None
    }

@app.get("/api/test-llm")
async def test_llm():
    """Test if LLM is responding"""
    try:
        if not rag_service.llm:
            return {"status": "error", "message": "LLM not initialized"}
        
        # Simple test query
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: rag_service.llm.invoke("Say 'Hello'")
            ),
            timeout=10.0
        )
        
        return {
            "status": "success",
            "message": "LLM is responding",
            "test_response": response
        }
    except asyncio.TimeoutError:
        return {
            "status": "error",
            "message": "LLM timed out. If using Ollama, make sure it's running: 'ollama serve'"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"LLM test failed: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
