
ALTER TABLE query_answers
ADD COLUMN sources TEXT;

ALTER TABLE prompts ADD COLUMN name VARCHAR(255);
ALTER TABLE prompts ADD COLUMN short_description TEXT;
ALTER TABLE execution_sessions ADD COLUMN document_id TEXT;
ALTER TABLE execution_logs DROP COLUMN document_id;
DROP TABLE content_templates;
DROP TABLE prompts;