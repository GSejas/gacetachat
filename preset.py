from sqlalchemy.orm import Session

from db import get_db
from models import ContentTemplate, Prompt

# Existing Twitter Prompt
twitter_prompt = """Crea un resumen humorístico de las 3 noticias más importantes de la Gazeta de hoy en un lenguaje sencillo. 
Usa menos de 200 caracteres por twitter (un twitter serian las 3 noticias, queberia hacer en total 200 o menos characters). Sé divertido y memorable, informando de forma simple y jocosa. 
Dirígete al público costarricense. 
Usa emojis. No digas cosas redundantes. Utiliza el contexto dado sobre la gaceta de hoy. Tal vez no sea super completo pero es todo lo que tenemos.

Ejemplo:
La Gaceta Nº 133
¡El tren eléctrico vuelve! Ahora sí, después de años, el tren vuelve a rodar por Costa Rica 🚂🎉 Pg. 3 
Se declara alerta roja por contaminación en el río Virilla. ¡Cuidado al bañarse! 🚫💦 Pg. 6-7
Los chicos del fútbol ganaron el partido de hoy. ¡Qué jugada! ¡Qué partidazo! ⚽🏆 Pg. 48

o

La Gaceta Nº 55
1: 🤩 La Municipalidad de Nandayure cede 1515 m2 para usos comunales, incentivando el desarrollo local. Pg. 3 
2: 🤩 Fabián Dobles Rodríguez recibe el galardón de Benemérito de las Letras Patrias por su aporte a la literatura. Pg. 6-7
3: 🤬 Costa Rica incluida en el catálogo fiscal adverso, pero hay un proyecto de ley para cambiarlo. ¡Actuemos! Pg. 48

o
La Gaceta Nº 555
¡La Municipalidad de Nandayure donará un terreno para salón comunal! 🤩🏡 Pg. 3
La Asamblea Legislativa otorga el Benemérito de las Letras Patrias a Fabián Dobles Rodríguez 🎉📚 Pg. 6-7
La Notaría del Estado confeccionará la escritura de traspaso del bien inmueble 📝📃Pg. 48"""

# New Newsletter Prompt
newsletter_prompt = """actua como un redactor experimentado, nacido en San Jose y educado. Tono profesional e ironico.

Genera un boletín digital con las noticias más importantes de la Gaceta de hoy. 
Utiliza los resultados de las consultas anteriores y asegúrate de que sea conciso y claro.

Las siguientes son los resultados de sub resumenes anteriores:

twitter_summary: {{twitter_summary}}

headline_summary: {{headline_summary}}

economic_updates: {{economic_updates}}

legal_changes: {{legal_changes}}

environmental_news: {{environmental_news}}

## Output Format:

return in plain text markdown, fit for an email newsletter. Should be easy to parse the different sections. 
add captions when relevant
images should be inserted according to markdown format.
when relevant, point the user to download the gaceta or chat with it at [APP_URL_BASE]/Chat?date=2021-01-01. should be today's gaceta date. 
Return as hyperlink. It should re-direct the user to today's chat.

Answer the content with the []-style variables (i.e [URL_ECON_IMAGE_SECTION]) These will be like placeholders for the actual image.


Newsletter Title: Boletín Digital de La Gaceta Nº 13X
Date: 
Banner Image: A vibrant banner representing Costa Rica or a digital wave theme.

Introduction
Welcome Message: A warm introduction highlighting the key stories and topics covered in this edition.
Table of Contents: A brief overview of the sections with anchor links for easy navigation.


Main News 📰
Image: https://i.ibb.co/Wxq8FMY/0-minimalistic-vector-graphics-white-framed-thema-esrgan-v1-x2plus.png
Headline: Clear and compelling.

Economic News 📈
Image: https://i.ibb.co/kKFChpR/0-minimalistic-vector-graphics-3-main-colors-whit-esrgan-v1-x2plus-2.png
Headline: Informative and engaging.

Law News ⚖️
Image: https://i.ibb.co/C9gH6GP/0-minimalistic-vector-graphics-3-main-colors-whit-esrgan-v1-x2plus-1.png
Headline: Direct and authoritative.

Environmental News 🌳
Image: https://i.ibb.co/k5vVhS2/0-minimalistic-vector-graphics-3-main-colors-whit-esrgan-v1-x2plus-4.png
Headline: Clear and impactful.

Closing Section

Thank You Note: Express gratitude to readers for their time and engagement.
Social Media Links: Icons linking to your social media platforms (Twitter (https://x.com/GacetaCRBot)).
Contact Information: Email (aideationcr@gmail.com), phone number (+506 8510-0213), and address for further inquiries.
Unsubscribe Option: A link for readers to unsubscribe if they choose to. Subscribe link is [APP_URL_BASE]/unsubscribe
"""


def create_preset_data(db: Session):
    # Check if the preset content template already exists
    existing_template = db.query(ContentTemplate).filter_by(id=1).first()
    if existing_template:
        return

    # Create a new content template
    content_template = ContentTemplate(
        id=1,
        title="Daily Preset Prompts",
        description="Preset prompts to be executed on a daily basis.",
    )
    db.add(content_template)
    db.commit()
    db.refresh(content_template)

    # Create associated prompts
    prompts = [
        {
            "name": "Twitter Prompt",
            "description": "Create a summary of the top 3 news in the Gazeta today. ",
            "text": twitter_prompt,
            "alias": "twitter_summary",
            "scheduled_execution": True,
            "doc_aware": True,
        },
        {
            "name": "Headline Prompt",
            "description": "Identify the top news headlines in today's Gaceta.",
            "text": "What are the top news headlines in today's Gaceta? For each headline, end the paragraph witha reference to the page (i.e Pg 345, )",
            "alias": "headline_summary",
            "scheduled_execution": True,
            "doc_aware": True,
        },
        {
            "name": "Economic Updates Prompt",
            "description": "Summarize the economic updates in today's Gaceta.",
            "text": "Summarize the economic updates in today's Gaceta. For each headline, end the paragraph witha reference to the page (i.e Pg 345, )",
            "alias": "economic_updates",
            "scheduled_execution": True,
            "doc_aware": True,
        },
        {
            "name": "Legal Changes Prompt",
            "description": "Highlight the legal changes mentioned in today's Gaceta.",
            "text": "What legal changes are mentioned in today's Gaceta? For each headline, end the paragraph witha reference to the page (i.e Pg 345, )",
            "alias": "legal_changes",
            "scheduled_execution": True,
            "doc_aware": True,
        },
        {
            "name": "Environmental News Prompt",
            "description": "Summarize the environmental news covered in today's Gaceta.",
            "text": "What environmental news is covered in today's Gaceta? For each headline, end the paragraph witha reference to the page (i.e Pg 345, )",
            "alias": "environmental_news",
            "scheduled_execution": True,
            "doc_aware": True,
        },
        {
            "name": "Newsletter Prompt",
            "description": "Generate a newsletter with the most important news from today's Gaceta.",
            "text": newsletter_prompt,
            "alias": "newsletter",
            "scheduled_execution": False,
            "doc_aware": False,
        },
    ]
    for prompt_data in prompts:
        prompt = Prompt(
            template_id=content_template.id,
            prompt_text=prompt_data["text"],
            name=prompt_data["name"],
            short_description=prompt_data["description"],
            alias=prompt_data["alias"],
            scheduled_execution=prompt_data["scheduled_execution"],
            doc_aware=prompt_data["doc_aware"],
        )
        db.add(prompt)
    db.commit()


# Run the function to create preset data
db_session = next(get_db())
create_preset_data(db_session)
db_session.close()
