# private joke
# page affichant aléatoirement 5 titres de films pour adulte
# cette page est protégée par un mot de passe stocké dans .streamlit/secrets.toml


import streamlit as st
import pandas as pd

# configuration de la fenêtre streamlit
st.set_page_config(
    page_title="Ciné'Creuse  - Da’taMiners CREW & CIE",
    page_icon="📽️",
    layout="centered",
    initial_sidebar_state="expanded"
    )

# stockage du chemin du dossier contenant le.s csv nécessaire.s dans une variable
path =

# création d'un dataframe via l'import d'un csv
isAdult_movies = pd.read_csv(path+'isAdult_movies.txt')


# affichage d'une image en fond d'écran
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.etsystatic.com/24223002/r/il/4bfed6/2447110972/il_fullxfull.2447110972_o7uc.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()


# mise en place de la demande de mot de passe
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Mot de passe", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Mot de passe", type="password", on_change=password_entered, key="password"
        )
        st.error("👀 T'es sûr.e d'être au bon endroit ???")
        return False
    else:
        # Password correct.
        return True


# affichage des titres de film si le mot de passe est correct
if check_password():
    st.markdown("<h2 style='text-align: center; color: #E50914'>Maintenant que nous sommes entre nous...</h2>",
                unsafe_allow_html=True)
    st.write(' ')
    st.markdown("<h5 style='text-align: center'>... que dirais-tu de regarder un des films suivants ?</h5>",
                unsafe_allow_html=True)
    st.write(" ")
    st.write(' ')
    st.write(' ')
    st.write(' ')

    choix = isAdult_movies.sample(5)

    for i in range(5):
        st.write("*", choix.iloc[i][0])
