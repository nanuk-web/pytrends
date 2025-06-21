from fastapi import FastAPI
from pytrends.request import TrendReq
import pandas as pd

app = FastAPI()

@app.get("/get-trends")
def get_trends():
    try:
        pytrends = TrendReq(hl='fr-CA', tz=360, geo='CA')
        trending_searches = pytrends.trending_searches(pn='canada')
        trends = trending_searches[0:20].values.tolist()
        return {"trends": trends}
    except Exception as e:
        return {"error": str(e)}
