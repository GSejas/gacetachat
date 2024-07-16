from sqlalchemy.orm import Session

from db import get_db
from langchain_openai import OpenAIEmbeddings

from models import ContentTemplate, Prompt

db_session = next(get_db())

twitter_prompt = """Crea un resumen humorístico de las 3 noticias más importantes de la Gazeta de hoy en un lenguaje sencillo. 
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




def create_preset_data(db: Session):
    # Check if the preset content template already exists
    existing_template = db.query(ContentTemplate).filter_by(id=1).first()
    if existing_template:
        return

    # Create a new content template
    content_template = ContentTemplate(
        id=1,
        title="Daily Preset Prompts",
        description="Preset prompts to be executed on a daily basis."
    )
    db.add(content_template)
    db.commit()
    db.refresh(content_template)

    # Create associated prompts
    prompts = [
        {
            "name": "Twitter Prompt",
            "description": "Create a humorous summary of the top 3 news in the Gazeta today.",
            "text": twitter_prompt
        },
        {
            "name": "Headline Prompt",
            "description": "Identify the top news headlines in today's Gaceta.",
            "text": "What are the top news headlines in today's Gaceta?"
        },
        {
            "name": "Economic Updates Prompt",
            "description": "Summarize the economic updates in today's Gaceta.",
            "text": "Summarize the economic updates in today's Gaceta."
        },
        {
            "name": "Legal Changes Prompt",
            "description": "Highlight the legal changes mentioned in today's Gaceta.",
            "text": "What legal changes are mentioned in today's Gaceta?"
        },
        {
            "name": "Cultural Events Prompt",
            "description": "Highlight the cultural events listed in today's Gaceta.",
            "text": "Highlight the cultural events listed in today's Gaceta."
        },
        {
            "name": "Environmental News Prompt",
            "description": "Summarize the environmental news covered in today's Gaceta.",
            "text": "What environmental news is covered in today's Gaceta?"
        }
    ]
    for prompt_data in prompts:
        prompt = Prompt(
            template_id=content_template.id,
            prompt_text=prompt_data["text"],
            name=prompt_data["name"],
            short_description=prompt_data["description"]
        )
        db.add(prompt)
    db.commit()

# Run the function to create preset data
create_preset_data(db_session)
db_session.close()