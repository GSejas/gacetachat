from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from crud import PromptExecutionEngine
from models import ContentExecutionLog, ExecutionSession, ExecutionState, Prompt


@pytest.fixture
def db_session():
    """Fixture to create a mock database session"""
    return MagicMock(spec=Session)


@pytest.fixture
def prompt_execution_engine(db_session):
    """Fixture to create an instance of PromptExecutionEngine"""
    return PromptExecutionEngine(db_session)


def test_run_prompt_by_date(prompt_execution_engine):
    with patch("prompt_execution_engine.FAISSHelper") as mock_faiss_helper, patch(
        "prompt_execution_engine.get_llm"
    ) as mock_get_llm, patch(
        "prompt_execution_engine.query_folder"
    ) as mock_query_folder:

        mock_faiss_helper().load_faiss_index.return_value = MagicMock()
        mock_get_llm.return_value = MagicMock()
        mock_query_folder.return_value = {
            "partial": "prompt_partial",
            "answer": "prompt_answer",
            "sources": "prompt_sources",
        }

        result = prompt_execution_engine.run_prompt_by_date("query text")

        assert result["answer"] == "prompt_answer"


def test_execute_prompt(prompt_execution_engine):
    with patch.object(
        prompt_execution_engine, "get_execution_session_prompts_results"
    ) as mock_get_results, patch.object(
        prompt_execution_engine, "run_prompt_by_date"
    ) as mock_run_prompt:

        mock_get_results.return_value = {"alias1": "result1"}
        mock_run_prompt.return_value = {
            "partial": "query with alias1 replaced",
            "answer": "query_answer",
            "sources": "query_sources",
        }

        result = prompt_execution_engine.execute_prompt(
            "query with {{alias1}}", "session_id"
        )

        assert result["answer"] == "query_answer"
        mock_get_results.assert_called_once_with("session_id")
        mock_run_prompt.assert_called_once_with("query with result1 replaced")


def test_execute_content_template_prompts(prompt_execution_engine, db_session):
    with patch.object(
        prompt_execution_engine, "create_execution_session"
    ) as mock_create_session, patch.object(
        prompt_execution_engine, "execute_prompt"
    ) as mock_execute_prompt, patch.object(
        db_session, "query"
    ) as mock_query:

        mock_create_session.return_value = "session_id"
        mock_execute_prompt.return_value = {
            "partial": "query_partial",
            "answer": "query_answer",
            "sources": "query_sources",
        }

        mock_prompt = MagicMock(spec=Prompt)
        mock_prompt.id = 1
        mock_prompt.scheduled_execution = True
        mock_prompt.prompt_text = "query text"
        mock_query().filter_by().all.return_value = [mock_prompt]

        session_id = prompt_execution_engine.execute_content_template_prompts(
            1, 1, gaceta_id=1
        )

        assert session_id == "session_id"
        mock_create_session.assert_called_once_with(1, 1, 1)
        mock_execute_prompt.assert_called_once_with("query text", "session_id")


def test_re_execute_prompt(prompt_execution_engine, db_session):
    with patch.object(
        prompt_execution_engine, "execute_prompt"
    ) as mock_execute_prompt, patch.object(db_session, "query") as mock_query:

        mock_execute_prompt.return_value = {
            "partial": "query_partial",
            "answer": "query_answer",
            "sources": "query_sources",
        }

        mock_prompt = MagicMock(spec=Prompt)
        mock_prompt.id = 1
        mock_prompt.prompt_text = "query text"  # Set prompt_text to a specific string
        mock_query().filter_by().first.return_value = mock_prompt

        prompt_execution_engine.re_execute_prompt("session_id", 1)

        mock_execute_prompt.assert_called_once_with("query text", "session_id")


def test_get_execution_session_prompts_results(prompt_execution_engine, db_session):
    mock_session = MagicMock(spec=ExecutionSession)
    mock_log = MagicMock(spec=ContentExecutionLog)
    mock_log.state = ExecutionState.EXECUTED.value
    mock_log.query_response_id = "query_response_id"
    mock_log.prompt.alias = "alias1"
    mock_log.output.response = "response1"
    mock_session.logs = [mock_log]
    mock_query = db_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = mock_session

    results = prompt_execution_engine.get_execution_session_prompts_results(
        "session_id"
    )

    assert results == {"alias1": "response1"}
    mock_query.filter_by.assert_called_once_with(id="session_id")


def test_create_execution_session(prompt_execution_engine, db_session):
    session_id = prompt_execution_engine.create_execution_session(1, 1, 1)

    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    assert session_id is not None


def test_log_prompt_execution(prompt_execution_engine, db_session):
    log_entry = prompt_execution_engine.log_prompt_execution(
        1, 1, ExecutionState.EXECUTED.value
    )

    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    assert log_entry is not None
