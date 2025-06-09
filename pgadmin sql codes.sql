CREATE OR REPLACE VIEW latest_quotes AS
SELECT *
FROM public.stock_quotes
WHERE date = (
    SELECT MAX(date)
    FROM public.stock_quotes
);

SELECT * FROM latest_quotes;
