
ALTER TABLE query_answers
ADD COLUMN sources TEXT;

ALTER TABLE prompts ADD COLUMN name VARCHAR(255);
ALTER TABLE prompts ADD COLUMN short_description TEXT;