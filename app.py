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
