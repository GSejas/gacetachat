# download_gaceta.py
import os
import schedule
import time
import requests
from models import GacetaPDF#, Session
from db import Session
# def fetch_pdf(url):
#     import requests
from bs4 import BeautifulSoup
from config import config

import datetime

import logging

# url = 

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

def save_pdf_to_db(pdf_data, date_str):
    from datetime import datetime
    directory = f"gaceta_pdfs/{date_str}"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, "gaceta.pdf")
    with open(file_path, "wb") as f:
        f.write(pdf_data)
    
    session = Session()
    gaceta = GacetaPDF(date=datetime.strptime(date_str, "%Y-%m-%d"), file_path=file_path)
    session.add(gaceta)
    session.commit()
    session.close()

def download_daily_gaceta():

    # Set the timezone to Costa Rica
    costa_rica_tz = pytz.timezone('America/Costa_Rica')
    current_time = datetime.now(costa_rica_tz)

    # Get the date string in the format "YYYY-MM-DD"
    date_str = current_time.strftime("%Y-%m-%d")
    
    session = Session()
    existing_gaceta = session.query(GacetaPDF).filter_by(date=datetime.strptime(date_str, "%Y-%m-%d")).first()
    
    if not existing_gaceta:
        pdf_data = download_pdf()
        if pdf_data:
            save_pdf_to_db(pdf_data, date_str)
            print(f"Downloaded and saved PDF for {date_str}")
        else:
            print(f"Failed to download PDF for {date_str}")
    else:
        print(f"PDF for {date_str} already exists")

    session.close()     

# schedule.every().day.at("00:34").do(download_daily_gaceta)

# Schedule to run every minute for testing
schedule.every(1).minutes.do(download_daily_gaceta)

from pdf_processor import PDFProcessor
from faiss_helper import FAISSHelper
from datetime import datetime, timedelta
import pytz


def check_and_download_today_pdf():

    # Set the timezone to Costa Rica
    costa_rica_tz = pytz.timezone('America/Costa_Rica')
    current_time = datetime.now(costa_rica_tz)

    # Get the date string in the format "YYYY-MM-DD"
    date_str = current_time.strftime("%Y-%m-%d")

    session = Session()
    existing_gaceta = session.query(GacetaPDF).filter_by(date=datetime.strptime(date_str, "%Y-%m-%d")).first()
    if not existing_gaceta:
        logging.info(f"Downloading PDF for {date_str}")
        download_daily_gaceta()
    else:
        logging.info(f"PDF for {date_str} already exists")
    session.close()

    
    faiss_helper = FAISSHelper()
    pdf_processor = PDFProcessor(faiss_helper)

    # Check if FAISS index exists, load if it does, else process latest PDF
    latest_gaceta_dir = os.path.join(config.GACETA_PDFS_DIR, datetime.now().strftime("%Y-%m-%d"))
    if os.path.exists(os.path.join(latest_gaceta_dir, "index.faiss")):
        db = faiss_helper.load_faiss_index(latest_gaceta_dir)
        index = db.index
        # documents = db.docstore.get_all_documents()
    else:
        db, documents = pdf_processor.process_latest_pdf()
        index = db.index


# Configure logging
logging.basicConfig(filename='download.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    check_and_download_today_pdf()
    while True:
        schedule.run_pending()
        time.sleep(60)