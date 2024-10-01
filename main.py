import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI


template = """\
Para el siguiente texto, extraiga la siguiente \
información:

sentiment: ¿Está satisfecho el cliente con el producto? 
Responda Positivo si sí, Negativo si
no, Neutral si cualquiera de ellos, o Desconocido si se desconoce.

delivery_days: ¿Cuántos días tardó
en llegar el producto? Si esta información
no se encuentra esta información, indique No hay información al respecto.

price_perception: ¿Qué opina el cliente del precio? 
Respuesta Caro si el cliente considera que el producto es caro, 
Barato si el cliente siente que el producto es barato,
no, Neutro si cualquiera de ellos, o Desconocido si es desconocido.

Formatee la salida como texto con viñetas con las \
siguientes teclas:
- Sentimiento
- ¿Cuánto tardó en entregarse?
- ¿Cómo se percibió el precio?

Ejemplo de entrada:
Este vestido es increíble. Llegó en dos días, justo a tiempo para el regalo de aniversario de mi mujer. Es más barato que otros vestidos que hay por ahí, pero creo que merece la pena por las características adicionales.

Ejemplo de salida:
- Sentimiento: Positivo
- ¿Cuánto tardó en entregarse? 2 días
- ¿Cómo se percibió el precio? Barato

text: {review}
"""

#PromptTemplate definición de variables
prompt = PromptTemplate(
    input_variables=["review"],
    template=template,
)


#LLM y función de carga de llaves
def load_LLM(openai_api_key):
    """La lógica para cargar la cadena que desea utilizar debe ir aquí."""
    # Asegúrese de que su openai_api_key se establece como una variable de entorno
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    return llm


#Page title and header
st.set_page_config(page_title="Extraer información clave de las reseñas de productos")
st.header("Extraer información clave de las reseñas de productos")


#Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("Extract key information from a product review.")
    st.markdown("""
        - Sentimiento
        - ¿Cuánto tardó en entregarse?
        - ¿Cómo se percibió el precio?
        """)

with col2:
    st.write("Contacte con [Matias Toro Labra](https://www.linkedin.com/in/luis-matias-toro-labra-b4074121b/) para construir sus proyectos de IA")


#Introducir la clave API de OpenAI
st.markdown("## Introduzca su clave API de OpenAI")

def get_openai_api_key():
    input_text = st.text_input(label="Clave API de OpenAI ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

openai_api_key = get_openai_api_key()


# Entrada
st.markdown("## Introduzca la reseña del producto")

def get_review():
    review_text = st.text_area(label="Revisión del producto", label_visibility='collapsed', placeholder="Su opinión sobre el producto...", key="review_input")
    return review_text

review_input = get_review()

if len(review_input.split(" ")) > 700:
    st.write("Por favor, introduzca una reseña de producto más corta. La extensión máxima es de 700 palabras.")
    st.stop()

    
# Output
st.markdown("###Datos clave extraídos:")

if review_input:
    if not openai_api_key:
        st.warning('Introduzca la clave de la API de OpenAI. \
            Instrucciones [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_review = prompt.format(
        review=review_input
    )

    key_data_extraction = llm(prompt_with_review)

    st.write(key_data_extraction)