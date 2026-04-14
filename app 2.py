import streamlit as st
import pandas as pd
import pickle

st.set_page_config(layout="wide")

st.title("Test de Personalidad Big Five")
st.write("Por favor, responde a las siguientes preguntas según tu nivel de acuerdo o desacuerdo.")

# Define the Likert scale options
likert_options = {
    1: "Totalmente en desacuerdo",
    2: "En desacuerdo",
    3: "Ni de acuerdo ni en desacuerdo",
    4: "De acuerdo",
    5: "Totalmente de acuerdo"
}

# Mapping of trait names for display
trait_display_names = {
    "ext": "Extraversión",
    "neu": "Neuroticismo",
    "agr": "Amabilidad",
    "con": "Responsabilidad",
    "opn": "Apertura a la Experiencia"
}

#Listas de preguntas
#Definimos el texto de las preguntas
ext_questions = {
    'E1': 'Soy el alma de la fiesta.',
    'E2': 'Hablo mucho.',
    'E3': 'Me siento cómodo(a) con la gente.',
    'E4': 'No me mantengo en un segundo plano.',
    'E5': 'Inicio conversaciones.',
    'E6': 'Tengo mucho que decir.',
    'E7': 'Hablo con muchas personas diferentes en las fiestas.',
    'E8': 'Me gusta llamar la atención.',
    'E9': 'No me importa ser el centro de atención.',
    'E10': 'No soy tímido(a) con los extraños.'
}

neu_questions = {
    'N1': 'Me estreso fácilmente.',
    'N2': 'Me estreso la mayor parte del tiempo.',
    'N3': 'Me preocupo por las cosas.',
    'N4': 'A menudo me siento triste.',
    'N5': 'Me altero fácilmente.',
    'N6': 'Me enfado fácilmente.',
    'N7': 'Cambio mucho de humor.',
    'N8': 'Tengo cambios de humor frecuentes.',
    'N9': 'Me irrito fácilmente',
    'N10': 'A menudo me siento triste.'
}

agr_questions = {
    'A1': 'Me preocupo por los demás.',
    'A2': 'Me intereso por la gente.',
    'A3': 'No insulto a la gente.',
    'A4': 'Me solidarizo con los sentimientos de los demás.',
    'A5': 'Me interesan los problemas de los demás.',
    'A6': 'Tengo un corazón blando',
    'A7': 'Me intereso bastante por los demás.',
    'A8': 'Dedico tiempo a los demás.',
    'A9': 'Siento las emociones de los demás.',
    'A10': 'Hago que la gente se sienta a gusto.'
}

con_questions = {
    'C1': 'Siempre estoy preparado(a).',
    'C2': 'No dejo mis pertenencias por ahí.',
    'C3': 'Presto atención a los detalles.',
    'C4': 'No hago un desastre con las cosas.',
    'C5': 'Hago las tareas de inmediato.',
    'C6': 'Raramente olvido guardar las cosas en su lugar.',
    'C7': 'Me gusta el orden.',
    'C8': 'No eludo mis deberes.',
    'C9': 'Sigo un horario.',
    'C10': 'Soy exigente en mi trabajo.'
}

opn_questions = {
    'O1': 'Tengo un vocabulario rico.',
    'O2': 'Entiendo fácilmente las ideas abstractas.',
    'O3': 'Tengo una imaginación vívida.',
    'O4': 'Me interesan las ideas abstractas.',
    'O5': 'Tengo ideas excelentes.',
    'O6': 'Tengo buena imaginación.',
    'O7': 'Soy rápido(a) para entender las cosas.',
    'O8': 'Uso palabras difíciles.',
    'O9': 'Paso tiempo reflexionando sobre las cosas.',
    'O10': 'Estoy lleno(a) de ideas.'
}

lista_preguntas = [ext_questions, neu_questions,agr_questions,con_questions,opn_questions]

# Initialize an empty dictionary to store user responses in session state
if 'user_responses' not in st.session_state:
    st.session_state.user_responses = {}

# Use a form to group all questions and submit them at once
with st.form("big_five_form"):
    st.header("Preguntas")
    # lista_preguntas is a global variable from previous cells
    # It contains [ext_questions, neu_questions, agr_questions, con_questions, opn_questions]
    for i, trait_dict in enumerate(lista_preguntas):
        # Get the first letter of the question code (e.g., 'E' for Extraversion)
        trait_code = list(trait_dict.keys())[0][0].lower()
        st.subheader(f"Dimension: {trait_display_names.get(trait_code, trait_code.upper())}")

        for q_code, question_text in trait_dict.items():
            current_response = st.session_state.user_responses.get(q_code, 3) # Default to 'Neutro'
            response = st.radio(
                f"**{q_code}.** {question_text}",
                options=list(likert_options.keys()),
                format_func=lambda x: likert_options[x],
                key=f"q_{q_code}",
                index=list(likert_options.keys()).index(current_response)
            )
            st.session_state.user_responses[q_code] = response

    submitted = st.form_submit_button("Enviar Respuestas")

if submitted:
    st.write("### Tus respuestas han sido enviadas!")

    # Calculate scores for each trait
    ext_score = sum(st.session_state.user_responses.get(q, 0) for q in ext_questions.keys())
    neu_score = sum(st.session_state.user_responses.get(q, 0) for q in neu_questions.keys())
    agr_score = sum(st.session_state.user_responses.get(q, 0) for q in agr_questions.keys())
    con_score = sum(st.session_state.user_responses.get(q, 0) for q in con_questions.keys())
    opn_score = sum(st.session_state.user_responses.get(q, 0) for q in opn_questions.keys())

    user_scores = pd.DataFrame({
        'ext_score': [ext_score],
        'neu_score': [neu_score],
        'agr_score': [agr_score],
        'con_score': [con_score],
        'opn_score': [opn_score]
    })

    st.write("### Puntuaciones de tus rasgos de personalidad:")
    st.dataframe(user_scores)

    try:
        # Ensure scaler and kmeans_model are loaded
        # These variables are expected to be in the global scope from previous executed cells
        # if 'scaler' not in globals() or 'kmeans_model' not in globals():
        #     st.error("Error: Scaler o modelo K-Means no encontrados en el entorno.")
        #     st.stop()

        # Standardize the user's scores
        user_scores_scaled = scaler.transform(user_scores)
        user_scores_scaled_df = pd.DataFrame(user_scores_scaled, columns=user_scores.columns)

        st.write("### Puntuaciones escaladas (estandarizadas):")
        st.dataframe(user_scores_scaled_df)

        # Predict the cluster
        predicted_cluster = kmeans_model.predict(user_scores_scaled)[0]
        st.write(f"### Perteneces al Cluster: {predicted_cluster}")

        # Display cluster description/mean values
        st.write("#### Valores promedio de los rasgos para tu Cluster:")
        if 'cluster_means' in globals():
            st.dataframe(cluster_means.loc[[predicted_cluster]])
        else:
            st.write("No hay una descripción detallada disponible para este cluster en este momento. La variable 'cluster_means' no fue encontrada.")

    except Exception as e:
        st.error(f"Error al procesar las puntuaciones o el modelo: {e}")
