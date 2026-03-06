import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="NEXO System", page_icon="⬡", layout="wide")

# 1. PEGA AQUÍ TUS CREDENCIALES (Cámbialo entre las comillas)
URL_CSV_CONTENIDO = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTeGoHOruoyf69vEMKbnLVN0bo7bVxUKrmNW3HYYYL3-tZEeWBayt6Z9v2S5d9If0UYQKg9woQS8ISW/pub?gid=1267612868&single=true&output=csv"
API_KEY_GEMINI = "AIzaSyBkNlbJVUnYmnN0qEke5JKpcvzlYe3VTuA"

# Configurar Gemini
try:
    genai.configure(api_key=API_KEY_GEMINI)
    model = genai.GenerativeModel('gemini-1.5-flash')
    NAVY_ACTIVO = True
except:
    st.error("⚠️ Error: Falta la API Key de Gemini.")
    NAVY_ACTIVO = False

# --- ESTILOS VISUALES (MODO PRO) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #c9d1d9; }
    .navy-terminal { 
        background-color: #0d1b2a; border-left: 4px solid #00b4d8; 
        padding: 15px; border-radius: 5px; margin-bottom: 20px;
        font-family: 'Courier New', monospace; color: #00b4d8;
    }
    .user-input { background-color: #161b22; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def cargar_contenido():
    try:
        return pd.read_csv(URL_CSV_CONTENIDO)
    except:
        return pd.DataFrame()

df_contenido = cargar_contenido()

# --- MEMORIA DE SESIÓN (Progreso del Usuario) ---
if 'nivel_actual' not in st.session_state:
    st.session_state.nivel_actual = 1  # Empezamos en micro-nivel 1
if 'nodo_activo' not in st.session_state:
    st.session_state.nodo_activo = "NUM_00"

# --- LÓGICA PRINCIPAL ---
def main():
    col1, col2 = st.columns([1, 3])

    with col1:
        st.header("⬡ NEXO MAP")
        st.caption("Rama: NÚMEROS | Capa: 0")
        # Aquí dibujaremos el Hexágono visualmente más adelante
        st.info(f"📍 Nodo: {st.session_state.nodo_activo}")
        st.progress(st.session_state.nivel_actual * 10) # Barra de progreso simple

    with col2:
        st.title("🧬 MÓDULO DE APRENDIZAJE")
        
        # Filtrar el contenido actual
        datos_nivel = df_contenido[
            (df_contenido['ID_Nodo_Global'] == st.session_state.nodo_activo) & 
            (df_contenido['Micro_Nivel'] == st.session_state.nivel_actual)
        ]

        if datos_nivel.empty:
            st.warning("⚠️ Esperando datos en el CSV... (O fin del nodo)")
            st.write("Asegúrate de haber llenado la Fila 2 de tu Excel con el Nivel 1.")
        else:
            fila = datos_nivel.iloc[0]
            
            # CEREBRO: Navy genera el reto en tiempo real
            if NAVY_ACTIVO:
                prompt_sistema = f"""
                Actúa como NAVY. Eres un instructor de supervivencia y lógica.
                El usuario (niño 5-7 años) está en el nivel {fila['Micro_Nivel']} del tema '{fila['Concepto_Fisico']}'.
                Contexto técnico: {fila['Prompt_Simulacion_IA']}
                
                Tu tarea:
                1. Saluda brevemente.
                2. Presenta el problema usando emojis y lenguaje simple (piedras, mochilas, espacio).
                3. NO des la respuesta. Haz una pregunta directa.
                """
                
                with st.spinner("Navy está analizando el entorno..."):
                    try:
                        respuesta_navy = model.generate_content(prompt_sistema).text
                        st.markdown(f'<div class="navy-terminal">🤖 <b>NAVY:</b><br>{respuesta_navy}</div>', unsafe_allow_html=True)
                    except:
                        st.error("Error conectando con Navy.")

            # ZONA DE INTERACCIÓN
            respuesta_usuario = st.text_input("Tu respuesta / Acción:", key="input_user")

            if st.button("EJECUTAR ACCIÓN"):
                if respuesta_usuario:
                    # AQUÍ EVALUAREMOS LA RESPUESTA CON IA EN EL SIGUIENTE PASO
                    st.success(f"Acción registrada: {respuesta_usuario}")
                    st.session_state.nivel_actual += 1 # Avanza al siguiente micro-nivel
                    st.rerun()

if __name__ == "__main__":
    main()
