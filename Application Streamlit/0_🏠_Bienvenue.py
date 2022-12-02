# page d'accueil de l'appli streamlit

import streamlit as st

# configuration de la fenêtre streamlit
st.set_page_config(
    page_title="Ciné'Creuse  - Da’taMiners CREW & CIE", # titre de la page
    page_icon="📽️",                                     # icône de la page
    layout="wide",                                      # affichage 'large' sur la page
    initial_sidebar_state="expanded",                   # statut de la barre latérale = "étendue"
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
    )


# affichage d'une image en fond d'écran
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://wallpaper.dog/large/5445110.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()


# affichage du titre de la page (d'accueil)
st.markdown("<h1 style='text-align: center; color: #FAFAFA'>Bienvenue au Ciné'Creuse</h1>",
                unsafe_allow_html=True)

st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')


# création de colonnes pour le menu de la page d'accueil
col1, col2 = st.columns(2)

# colonne de gauche
with col1:
    st.subheader('🏠 Bienvenue')
    st.markdown('**Accueil**')
    st.write(' ')
    st.subheader('🎞️ Profil utilisateur')
    st.markdown('**Recommandations de films**')
    st.subheader('🔞 Creuse & Chill')
    st.markdown('**Détendez-vous, ça va bien se passer...**')
    st.write(' ')


# colonne de droite
with col2:
    st.subheader('📊 Admin')
    st.markdown('**Visualisations statistiques :**')
    st.markdown('**+ Durée des films**')
    st.markdown('**+ Note moyenne par genre**')
    st.markdown('**+ Nombre de films par année**')
    st.markdown('**+ Typologie des meilleurs films**')
    st.write(' ')


