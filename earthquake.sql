SELECT 
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'earthquakes';

ALTER TABLE earthquakes
ALTER COLUMN id TYPE TEXT;

SELECT *
FROM earthquakes
ORDER BY time DESC;

SELECT * FROM public.earthquakes
ORDER BY id ASC 