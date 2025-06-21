from fastapi import FastAPI
from pytrends.request import TrendReq
import pandas as pd

app = FastAPI()

@app.get("/get-trends")
def get_trends():
    try:
        pytrends = TrendReq(hl='fr-CA', tz=360, geo='CA')

        base_keywords = [
            "marketing", "publicité", "SEO", "réseaux sociaux",
            "Google Ads", "Meta Ads", "ecommerce", "intelligence artificielle"
        ]

        all_related_queries = []

        for kw in base_keywords:
            pytrends.build_payload([kw], cat=0, timeframe='now 7-d', geo='CA', gprop='')
            related = pytrends.related_queries()

            if related and kw in related:
                rising = related[kw].get('rising')
                if rising is not None and not rising.empty:
                    queries = rising['query'].tolist()
                    all_related_queries.extend(queries)

        if not all_related_queries:
            return {"trends": []}

        # Nettoyage et déduplication
        clean_trends = list(set(all_related_queries))

        return {"trends": clean_trends}

    except Exception as e:
        return {"error": str(e)}
