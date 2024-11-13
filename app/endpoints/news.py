from fastapi import APIRouter, HTTPException
from tavily import TavilyClient
from config import TAVILY_API_KEY  # Add this to your config file

router = APIRouter()

@router.get("/news/{ticker}")
async def get_company_news(ticker: str, limit: int = 5):
    try:
        # Initialize Tavily client
        client = TavilyClient(api_key=TAVILY_API_KEY)
        
        # Search for news about the company
        response = client.search(
            query=f"{ticker} stock company news",
            search_depth="advanced",
            topic="news",
            max_results=limit
        )
        
        # Extract and format relevant news articles
        news_articles = []
        for result in response.get('results', []):
            article = {
                'title': result.get('title'),
                'url': result.get('url'),
                'content': result.get('content'),
                'score': result.get('score')
            }
            news_articles.append(article)
            
        return {
            'ticker': ticker,
            'articles': news_articles
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")