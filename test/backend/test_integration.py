import os
from unittest.mock import MagicMock

import pytest

from download_gaceta import check_and_download_today_pdf
from models import ExecutionSession, ExecutionState, GacetaPDF


class Config:
    GACETA_PDFS_DIR = "test/backend/gaceta_pdfs"
    OPENAI_MODEL_NAME = "text-davinci-003"
    OPENAI_API_KEY = "test-openai-api-key"
    OPENAI_TEMPERATURE = 0.7


config = Config()


@pytest.fixture
def mock_ai_service(mocker):
    mocker.patch("faiss_helper.FAISSHelper.load_faiss_index", return_value=MagicMock())
    mocker.patch("qa.get_llm", return_value=MagicMock())
    mocker.patch(
        "qa.query_folder",
        return_value={
            "partial": "query_partial",
            "answer": "query_answer",
            "sources": "query_sources",
        },
    )


def test_integration_check_and_download_today_pdf(db_session, mock_ai_service):
    # Set up existing PDF in the folder
    test_date = "2024-07-15"
    test_pdf_dir = os.path.join(config.GACETA_PDFS_DIR, test_date)
    os.makedirs(test_pdf_dir, exist_ok=True)
    # with open(os.path.join(test_pdf_dir, "gaceta.pdf"), "wb") as f:
    #     f.write(b"Test PDF content")

    # Run the download and process function
    check_and_download_today_pdf()

    # Verify that the PDF was processed and prompts executed
    gaceta = db_session.query(GacetaPDF).filter_by(date=test_date).first()
    assert gaceta is not None

    exec_session = (
        db_session.query(ExecutionSession).filter_by(document_id=gaceta.id).first()
    )
    assert exec_session is not None
    assert exec_session.status == ExecutionState.EXECUTED.value

    logs = exec_session.logs
    for log in logs:
        assert log.state == ExecutionState.EXECUTED.value
        assert log.output.response == "query_answer"
