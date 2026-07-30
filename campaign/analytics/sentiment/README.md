# TEL Sentiment Data Store

Daily structured sentiment data scraped from X/Twitter, Reddit, and crypto news.
Each file covers one calendar day. The heat map artifact reads all files to render historical views.

## File naming
`YYYY-MM-DD.json` — one file per day, UTC date.

## Schema

```json
{
  "date": "YYYY-MM-DD",
  "scraped_at": "ISO-8601 UTC timestamp",
  "platforms": {
    "twitter": {
      "mention_count": 0,
      "sentiment": { "positive": 0, "neutral": 0, "negative": 0 },
      "top_topics": ["mainnet", "governance", "price"],
      "notable_posts": [
        { "text": "...", "sentiment": "positive", "engagement_weight": 1.0 }
      ]
    },
    "reddit": {
      "mention_count": 0,
      "sentiment": { "positive": 0, "neutral": 0, "negative": 0 },
      "subreddits": ["r/Telcoin"],
      "notable_posts": []
    },
    "news": {
      "article_count": 0,
      "sentiment": { "positive": 0, "neutral": 0, "negative": 0 },
      "articles": [
        { "title": "...", "source": "...", "sentiment": "neutral" }
      ]
    }
  },
  "composite": {
    "total_mentions": 0,
    "sentiment_score": 0.0,
    "activity_score": 0.0,
    "top_narrative": "",
    "hour_distribution": { "0":0, "1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0, "10":0, "11":0, "12":0, "13":0, "14":0, "15":0, "16":0, "17":0, "18":0, "19":0, "20":0, "21":0, "22":0, "23":0 },
    "topic_scores": {
      "mainnet": 0.0,
      "governance": 0.0,
      "price": 0.0,
      "staking": 0.0,
      "validators": 0.0,
      "tel_upgrade": 0.0,
      "layerzero": 0.0,
      "telx": 0.0
    }
  }
}
```

## sentiment_score
0.0–1.0. Computed as: `positive_count / total_count` across all platforms.
0.5 = neutral baseline. Above 0.6 = positive signal. Below 0.4 = negative signal.

## activity_score
0.0–10.0. Normalized to historical max mentions. Represents relative conversation volume.

## topic_scores
0.0–10.0 per topic. Weighted by engagement and platform (Twitter > Reddit > News).
