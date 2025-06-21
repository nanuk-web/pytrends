from fastapi import FastAPI
from pytrends.request import TrendReq
import pandas as pd

app = FastAPI()

@app.get("/get-trends")
def get_trends():
    try:
        pytrends = TrendReq(hl='en-US', tz=360, geo='CA')

        base_keywords = [
            "marketing", "advertising", "SEO", "social media",
            "Google Ads", "Meta Ads", "ecommerce", "artificial intelligence"
        ]

        all_queries = []

        for kw in base_keywords:
            # Suggestions enrichies
            try:
                suggestions = pytrends.suggestions(kw)
                queries = [s['title'] for s in suggestions]
                all_queries.extend(queries)
            except Exception as e_suggest:
                print(f"Suggestion error for {kw}: {str(e_suggest)}")

            # Related queries
            try:
                pytrends.build_payload([kw], cat=0, timeframe='today 3-m', geo='CA', gprop='')
                related = pytrends.related_queries()
                if related and isinstance(related, dict) and kw in related:
                    rising = related[kw].get('rising')
                    if rising is not None and not rising.empty:
                        queries = rising['query'].tolist()
                        all_queries.extend(queries)
            except Exception as e_related:
                print(f"Related queries error for {kw}: {str(e_related)}")

        if not all_queries:
            return {"trends": []}

        clean_trends = list(set(all_queries))

        return {"trends": clean_trends}

    except Exception as e:
        return {"error": str(e)}
