ALTER TABLE news_articles
ADD COLUMN source TEXT,
ADD COLUMN published_at TEXT;

TRUNCATE TABLE news_articles RESTART IDENTITY;

SELECT * FROM public.news_articles
ORDER BY id ASC 