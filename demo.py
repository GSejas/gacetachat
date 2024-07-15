
import streamlit as st
from models import *
from process_pdf import process_latest_pdf, search_in_pdf
# from langchain_openai import OpenAIEmbeddings
# app.py
import streamlit as st
import os
from models import Prompt
from pdf_processor import PDFProcessor
from faiss_helper import FAISSHelper
from logging_setup import setup_logging
from config import config
from qa import get_llm, query_folder

setup_logging()

def main():
    # st.title("Daily Gaceta of Costa Rica Chatbot")

    faiss_helper = FAISSHelper()
    pdf_processor = PDFProcessor(faiss_helper)

    # Check if FAISS index exists, load if it does, else process latest PDF
    latest_gaceta_dir = os.path.join(config.GACETA_PDFS_DIR, datetime.now().strftime("%Y-%m-%d"))
    if os.path.exists(os.path.join(latest_gaceta_dir, "index.faiss")):
        db = faiss_helper.load_faiss_index(latest_gaceta_dir)
        index = db.index
    else:
        db, documents = pdf_processor.process_latest_pdf()
        index = db.index

    if db:
        st.subheader("Ask Questions about Today's Gaceta")
        query = """Crea un resumen humorístico de las 3 noticias más importantes de la Gazeta de hoy en un lenguaje sencillo. 
Usa menos de 280 caracteres por noticia. Sé divertido y memorable, informando de forma simple y jocosa. 
Dirígete al público costarricense. 
Usa emojis. No digas cosas redundantes. Utiliza el contexto dado sobre la gaceta de hoy. Tal vez no sea super completo pero es todo lo que tenemos.

Ejemplo:
¡El tren eléctrico vuelve! Ahora sí, después de años, el tren vuelve a rodar por Costa Rica 🚂🎉
Se declara alerta roja por contaminación en el río Virilla. ¡Cuidado al bañarse! 🚫💦
Los chicos del fútbol ganaron el partido de hoy. ¡Qué jugada! ¡Qué partidazo! ⚽🏆

o

1: 🤩 La Municipalidad de Nandayure cede 1515 m2 para usos comunales! 🐠 Incentivando a la comunidad a involucrarse y contribuir al desarrollo y bienestar local. 
2: 🤩 Fabián Dobles Rodríguez recibe el mayor galardón de Benemérito de las Letras Patrias📝 por su aporte a la literatura nacional y la obra de sus predecesores. 
3: 🤬 Costa Rica incluida en el Catálogo de países sin el mejor régimen fiscal. 🤩 Pero hay un proyecto de ley para lograr la exclusión e incluye rentas provenientes del extranjero. 💪 ¡Es nuestro momento de actuar!

o
¡La Municipalidad de Nandayure donará un terreno para salón comunal! 🤩🏡
La Asamblea Legislativa otorga el Benemérito de las Letras Patrias a Fabián Dobles Rodríguez, un escritor de singulares méritos en el campo de la novela y el cuento 🎉📚
La Notaría del Estado confeccionará la escritura de traspaso del bien inmueble, para que su obra literaria siga viva 📝📃"""
        # if st.button("Submit"):
        # answer = pdf_processor.search_in_pdf(query, index, documents)
        
        
        llm = get_llm(model=config.OPENAI_MODEL_NAME, openai_api_key=config.OPENAI_API_KEY, temperature=config.OPENAI_TEMPERATURE)
        result = query_folder(
            folder_index=db,
            query=query,
            # return_all=return_all_chunks,
            llm=llm,
        )
        
        # st.write(answer)
        # st.write(str(answer))
        print(result)
    # st.subheader("Daily Prompts")
    # session = Session()
    # prompts = session.query(Prompt).all()
    # for prompt in prompts:
    #     st.write(prompt.prompt_text)
    #     if st.button(f"Submit Answer for Prompt {prompt.id}"):
    #         answer = st.text_input(f"Your answer for Prompt {prompt.id}")
    #         # Logic to log the answer can be added here

    # session.close()

if __name__ == "__main__":
    main()
