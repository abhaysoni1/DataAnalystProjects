from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from generate_map import create_heatmap
from preprocess import get_neighbourhood_groups
import uvicorn
app = FastAPI()
app.mount("/data", StaticFiles(directory="data"), name="data")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    neighborhoods = ["All"] + get_neighbourhood_groups()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "map_exists": False,
        "neighborhoods": neighborhoods,
        "selected_neighborhood": "All"
    })

@app.post("/", response_class=HTMLResponse)
async def post_form(
    request: Request,
    property_cost: float = Form(...),
    neighborhood_group: str = Form("All")
):
    top5_listings = create_heatmap(property_cost, neighborhood_group)
    neighborhoods = ["All"] + get_neighbourhood_groups()
    create_heatmap(property_cost, neighborhood_group)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "map_exists": True,
        "neighborhoods": neighborhoods,
        "selected_neighborhood": neighborhood_group,
        "top5_listings": top5_listings
    })


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)