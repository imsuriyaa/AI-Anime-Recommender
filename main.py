from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from src.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@lru_cache(maxsize=1)
def get_pipeline():
    return AnimeRecommendationPipeline()

@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/submit')
async def handle_form(request: Request):
    form_data = await request.form()
    anime_preferences = form_data.get("anime_preferences")
    if not anime_preferences:
        return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
    
    pipeline = get_pipeline()
    recommendations = pipeline.recommend(anime_preferences)
    return templates.TemplateResponse("index.html", {"request": request, "recommendations": recommendations})


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}

