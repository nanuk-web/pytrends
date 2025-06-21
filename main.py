from fastapi import FastAPI
from pytrends.request import TrendReq
import pandas as pd

app = FastAPI()

@app.get("/get-trends")
def get_trends():
    try:
        pytrends = TrendReq(hl='fr-CA', tz=360, geo='CA')
        # Exemple avec top charts 2024
        df = pytrends.top_charts(2024, hl='fr-CA', geo='CA')
        trends = df['title'].values.tolist()
        return {"trends": trends}
    except Exception as e:
        return {"error": str(e)}
