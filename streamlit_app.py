import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Tutor Química Biológica II", layout="centered")

# --- SEGURIDAD: API KEY ---
# En Streamlit Cloud, esto se configura en "Secrets" para que no sea público.
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# --- EL PROMPT MAESTRO (Oculto para el alumno) ---
# Aquí incluyes el estilo Lehninger y la guía de problemas.
SYSTEM_PROMPT = """
Eres un tutor experto en Bioquímica para Química Biológica 2. 
Tu estilo es el 'Estilo simple 1': Lehninger aesthetic, jerarquía visual (Enzimas 25px, Metabolitos 20px).

INSTRUCCIONES PEDAGÓGICAS:
1. No des la respuesta directa a los problemas. 
2. Guía al alumno con preguntas sobre el balance de masa o el Control Metabólico.
3. Si el alumno está muy perdido, explica el concepto usando la lógica de flujos metabólicos.

GUÍA DE PROBLEMAS Y RESPUESTAS (Para tu uso interno, no mostrar):
- Problema 1 (PFK-1): La respuesta correcta involucra el efecto del F-2,6-BP.
- Problema 2 (Control): El coeficiente de control de flujo se distribuye entre varias enzimas.
[Añade aquí el resto de tu material]
"""

st.title("🧪 Tutor de Química Biológica II")
st.markdown("Bienvenido. Consulta tus dudas sobre la materia o los problemas de la guía.")

# --- GESTIÓN DEL HISTORIAL DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA DEL CHAT ---
if prompt := st.chat_input("¿Cuál es tu duda sobre la glucólisis o la guía?"):
    # Guardar y mostrar mensaje del alumno
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta de la IA
    with st.chat_message("assistant"):
        # Configuramos el modelo (Flash es el más económico y rápido)
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_PROMPT
        )
        
        # Enviamos el historial para que tenga contexto
        try:
            response = model.generate_content(prompt)
            full_response = response.text
        except Exception as e:
            full_response = f"⚠️ Error detectado: {e}"
            
        
        st.markdown(full_response)
        
        # Botón para que el alumno pueda enviarte la respuesta si tiene dudas
        st.caption("Si esta respuesta no te convence, copia el texto y envíalo al docente.")

    # Guardar respuesta en el historial
    st.session_state.messages.append({"role": "assistant", "content": full_response})