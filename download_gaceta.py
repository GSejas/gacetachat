# download_gaceta.py
import os
import schedule
import time
import requests
from models import ExecutionState, GacetaPDF#, Session
from db import Session
# def fetch_pdf(url):
#     import requests
from bs4 import BeautifulSoup
from config import config
from crud import PromptExecutionEngine, get_execution_session_by_date
import datetime

from pdf_processor import PDFProcessor
from faiss_helper import FAISSHelper
from datetime import datetime, timedelta
import pytz
import logging
from logging_setup import setup_logging
setup_logging()


def download_pdf():
    response = requests.get("https://www.imprentanacional.go.cr/gaceta/")
    soup = BeautifulSoup(response.text, "html.parser")
    
    anchor = soup.select_one("#ctl00_PdfGacetaDescargarHyperLink")
    
    if anchor:
        pdf_url = anchor["href"]
        pdf_response = requests.get("https://www.imprentanacional.go.cr" + pdf_url)

        return pdf_response.content
    else:
        return None


def save_pdf_to_db(file_path, date_str):
    try:
        session = Session()
        gaceta = GacetaPDF(date=datetime.strptime(date_str, "%Y-%m-%d"), file_path=file_path)
        session.add(gaceta)
        session.commit()
        session.close()
        logging.info(f"Saved PDF to database for {date_str}")
        return gaceta
    except Exception as e:
        logging.error(f"Failed to save PDF to database: {e}")

def download_daily_gaceta():

    # Set the timezone to Costa Rica
    costa_rica_tz = pytz.timezone('America/Costa_Rica')
    current_time = datetime.now(costa_rica_tz)

    # Get the date string in the format "YYYY-MM-DD"
    date_str = current_time.strftime("%Y-%m-%d")
    
    directory = f"gaceta_pdfs/{date_str}"
    file_path = os.path.join(directory, "gaceta.pdf")
        
    session = Session()
    existing_gaceta = session.query(GacetaPDF).filter_by(date=datetime.strptime(date_str, "%Y-%m-%d")).first()
    
    if not existing_gaceta:
        if os.path.exists(file_path):
            logging.info(f"PDF file for {date_str} already exists, but not in the database. Creating DB entry.")
            gaceta = save_pdf_to_db(file_path, date_str)
        else:
            pdf_data = download_pdf()
            if pdf_data:
                os.makedirs(directory, exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(pdf_data)
                gaceta = save_pdf_to_db(file_path, date_str)
                print(f"Downloaded and saved PDF for {date_str}")
            else:
                print(f"Failed to download PDF for {date_str}")
    else:
        print(f"PDF for {date_str} already exists")

    session.close()     



def check_and_download_today_pdf():

    # Set the timezone to Costa Rica
    costa_rica_tz = pytz.timezone('America/Costa_Rica')
    current_time = datetime.now(costa_rica_tz)

    # Get the date string in the format "YYYY-MM-DD"
    date_str = current_time.strftime("%Y-%m-%d")
    latest_gaceta_dir = os.path.join(config.GACETA_PDFS_DIR, date_str)

    session = Session()
    existing_gaceta = session.query(GacetaPDF).filter_by(date=datetime.strptime(date_str, "%Y-%m-%d")).first()
    if not existing_gaceta:
        logging.info(f"Downloading PDF for {date_str}")
        download_daily_gaceta()
    else:
        logging.info(f"PDF for {date_str} already exists")

    
    faiss_helper = FAISSHelper()
    pdf_processor = PDFProcessor(faiss_helper)

    # Check if FAISS index exists, load if it does, else process latest PDF
    if os.path.exists(os.path.join(latest_gaceta_dir, "index.faiss")):
        db = faiss_helper.load_faiss_index(latest_gaceta_dir)
        index = db.index
        # documents = db.docstore.get_all_documents()
    else:
        db, documents = pdf_processor.process_latest_pdf()
        index = db.index

    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    session_for_today = get_execution_session_by_date(session, date_obj)
    
    prompt_execution_engine = PromptExecutionEngine(session)
    
    if isinstance(session_for_today, list):
        session_for_today = session_for_today[0] if session_for_today else None
    
    if (session_for_today is None or session_for_today.status != ExecutionState.EXECUTED.value) and existing_gaceta is not None:
        prompt_execution_engine.execute_content_template_prompts(None, 1, gaceta_id=existing_gaceta.id)
    else:
        if session_for_today.document_id is None:
            session_for_today.document_id = existing_gaceta.id
            session.commit()
    session.close()

# Configure logging
logging.basicConfig(filename='download.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def initial_check_and_create_missing_entries():
    session = Session()
    directory = config.GACETA_PDFS_DIR
    
    for date_folder in os.listdir(directory):
        folder_path = os.path.join(directory, date_folder)
        if os.path.isdir(folder_path):
            date_str = date_folder
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                existing_gaceta = session.query(GacetaPDF).filter_by(date=datetime.strptime(date_str, "%Y-%m-%d")).first()
                if not existing_gaceta:
                    file_path = os.path.join(folder_path, "gaceta.pdf")
                    if os.path.exists(file_path):
                        logging.info(f"Folder for {date_str} exists, but no DB entry found. Creating DB entry.")
                        save_pdf_to_db(file_path, date_str)
            except ValueError:
                logging.warning(f"Skipping invalid date folder: {date_folder}")
    session.close()

schedule.every(1).minutes.do(check_and_download_today_pdf)

if __name__ == "__main__":
    initial_check_and_create_missing_entries()
    check_and_download_today_pdf()
    while True:
        schedule.run_pending()
        time.sleep(60)