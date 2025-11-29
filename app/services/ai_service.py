from openai import AsyncOpenAI
from app.config import settings
from models.content import SentimentEnum
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def analyze_text(text: str) -> Tuple[str, SentimentEnum]:
    """
    Analyze text using OpenAI API to generate summary and sentiment.
    
    Args:
        text: The text content to analyze
        
    Returns:
        Tuple of (summary, sentiment)
    """
    try:
        # Create the prompt for analysis
        prompt = f"""Analyze the following text and provide:
1. A concise summary (2-3 sentences)
2. The overall sentiment (Positive, Negative, or Neutral)

Text: {text}

Respond in the following format:
SUMMARY: [your summary here]
SENTIMENT: [Positive/Negative/Neutral]"""
        
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes text content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        result = response.choices[0].message.content
        
        # Parse the response
        lines = result.strip().split('\n')
        summary = ""
        sentiment_str = "Neutral"
        
        for line in lines:
            if line.startswith("SUMMARY:"):
                summary = line.replace("SUMMARY:", "").strip()
            elif line.startswith("SENTIMENT:"):
                sentiment_str = line.replace("SENTIMENT:", "").strip()
        
        # Map sentiment to enum
        sentiment_mapping = {
            "positive": SentimentEnum.POSITIVE,
            "negative": SentimentEnum.NEGATIVE,
            "neutral": SentimentEnum.NEUTRAL
        }
        sentiment = sentiment_mapping.get(sentiment_str.lower(), SentimentEnum.NEUTRAL)
        
        return summary, sentiment
        
    except Exception as e:
        logger.error(f"Error analyzing text with OpenAI: {str(e)}")
        # Return default values on error
        return "Analysis unavailable at this time.", SentimentEnum.NEUTRAL
