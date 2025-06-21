from fastapi import FastAPI
from pytrends.request import TrendReq

app = FastAPI()

@app.get("/get-trends")
def get_trends():
    pytrends = TrendReq(hl='fr-CA', tz=360, geo='CA')
    pytrends.build_payload(kw_list=[], cat=0, timeframe='now 7-d', geo='CA', gprop='')
    trending_searches = pytrends.trending_searches(pn='canada')
    return {"trends": trending_searches[0:20].values.tolist()}
