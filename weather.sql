SELECT 
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'weather';

TRUNCATE TABLE weather;

ALTER TABLE weather
ADD CONSTRAINT unique_city UNIQUE (city);

ALTER TABLE weather
ADD COLUMN country TEXT;

ALTER TABLE weather
DROP COLUMN country_id;

SELECT * FROM public.weather
ORDER BY id ASC 