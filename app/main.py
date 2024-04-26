import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware 
from sqlalchemy.orm import Session
import secrets

from openAI.openAI import summarize_text
from utils.api_types import CreateRequest, CreateResponse, Summary
from database.postgresql import init_db, get_db
from utils.settings import Settings

settings = Settings()

app = FastAPI(
    title="Text Summarizer API",
    version="1.0",
    docs_url="/docs",
    redoc_url=None, 
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

init_db()  

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.DOCS_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, settings.DOCS_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(user: str = Depends(get_current_user)):
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Text Summarizer API docs")

@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi(user: str = Depends(get_current_user)):
    from fastapi.openapi.utils import get_openapi
    return get_openapi(title="Text Summarizer API", version="1.0", routes=app.routes)

@app.post("/summarize", response_model=CreateResponse, tags=["Text Summarization"])
async def summarize(request: CreateRequest, db: Session = Depends(get_db)):
    try:
        summary_text = summarize_text(request.text)
        summary_record = Summary(text=request.text, summary=summary_text)
        db.add(summary_record)
        db.commit()
        db.refresh(summary_record)
        return CreateResponse(text=summary_record.text, summary=summary_record.summary, createdAt=summary_record.created_at.isoformat())
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=settings.APP_PORT)