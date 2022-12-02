# page client du Ciné Creuse
# recommmandation de titres de film suivant les genres choisis

import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
import math
from sklearn.preprocessing import StandardScaler
from random import sample


# --------------------
# PAGE CONFIGURATION
# --------------------
st.set_page_config(
    page_title="Ciné'Creuse  - Da’taMiners CREW & CIE",
    page_icon="📽️",
    layout="wide",
    initial_sidebar_state="expanded"
    )

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




def table_machine_learning():

    # 1 generate DataFrame for subgenres
    title_basics = pd.read_csv('C:/Emilie/Pro/PycharmProjects/Projet2/title_basics_clean.txt', parse_dates=['startYear'])
    title_rating = pd.read_csv('C:/Emilie/Pro/PycharmProjects/Projet2/title_rating_clean.txt')
    table_merged = pd.merge(title_basics, title_rating, how='inner', on='tconst')
    table_merged.loc[table_merged.genres.str.contains(","), 'sub_genres'] = table_merged.genres.str.split(",")
    table_merged.loc[~table_merged.genres.str.contains(","), 'sub_genres'] = table_merged.genres.apply(
        lambda val: [val])
    table_merged['sub_genres'] = table_merged['sub_genres'].apply(lambda x: ' '.join(x))
    tfi = TfidfVectorizer()
    sub_genres_table = tfi.fit_transform(table_merged['sub_genres'])
    matrice = sub_genres_table.todense()
    sub_genres_machine_learning = pd.DataFrame(matrice, columns=tfi.get_feature_names())
    table_machine_learning = pd.merge(table_merged, sub_genres_machine_learning, left_index=True, right_index=True)

    # 2 create rankingIndicator column
    table_machine_learning['logNumVotes'] = table_machine_learning.numVotes.apply(lambda x: math.log10(x))
    table_machine_learning['multipFactor'] = table_machine_learning.averageRating * table_machine_learning.logNumVotes
    table_machine_learning['rankingIndicator'] = table_machine_learning.multipFactor.apply(lambda x: round(x * 100 / 60, 1))

    table_machine_learning.drop(['fi',
                                 'isAdult',
                                 'titleType',
                                 'genres',
                                 'averageRating',
                                 'numVotes',
                                 'logNumVotes',
                                 'multipFactor',
                                 'sub_genres'], axis=1, inplace=True)

    return table_machine_learning



def recommandation_films(tconst_list, number_neighbors_per_film):

    # 1 add features DataFrame
    df_features_machine_learning = table_machine_learning()

    # 2 clean data and initiate machine learning model
    df_features_machine_learning['startYear'] = pd.DatetimeIndex(df_features_machine_learning['startYear']).year.astype(int)

    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    df_features_machine_learning_onlynumeric = df_features_machine_learning.select_dtypes(include=numerics)
    X = df_features_machine_learning_onlynumeric
    scaler = StandardScaler().fit(X)
    X_scaled = scaler.transform(X)
    X_scaled[:,5:-1] = X_scaled[:,5:-1] / 5
    X_scaled[:, -1] = X_scaled[:, -1] / 10
    X_scaled[:, 1] = X_scaled[:, 1] / 20

    model_nearest = NearestNeighbors(n_neighbors=number_neighbors_per_film).fit(X_scaled)

    # 3 make a list of all recommanded films
    recommanded_films_for_one = []
    recommanded_films_all = []
    for each in tconst_list:
        film_features = df_features_machine_learning[df_features_machine_learning['tconst'] == each].select_dtypes(include=numerics)
        model_result = model_nearest.kneighbors(film_features)
        for every in range(number_neighbors_per_film):
            nearest_neighbor_id = model_result[1][0][every]
            film_array = df_features_machine_learning['primaryTitle'].iloc[[nearest_neighbor_id]].values
            film_title = film_array[0]
            recommanded_films_for_one.append(film_title)
        recommanded_films_all.append(recommanded_films_for_one)

    return recommanded_films_all

# path vers le dossier contenant tous les datasets > à changer pour chacun
path =

# import de la table 'machine_learning_features' en local
machine_learning_features = pd.read_csv(path+'machine_learning_features.txt')

# extraction du nom des colonnes de la table 'machine_learning_features' dans la liste 'df_columns'
df_columns = machine_learning_features.columns

#####
# automatisation de l'import de chacune des tables-genre contenant les noms des films
# (une table par genre)
#####

for i in df_columns[5:-1]:
    # globals()[i] permet de faire du string 'i' une variable
    globals()[i] = pd.read_csv(path+i+'.txt')


#####
# STREAMLIT
#####


# configuration de la sidebar

with st.sidebar:
    options = st.multiselect('Quels sont vos genres favoris ?',
                             df_columns[5:-1])



#####
# AUTOMATISATION de l'affichage de 5 films au hasard suivant le genre sélectionné avec st.multiselect
#####

col1, col2 = st.columns(2)


with col2:
    st.markdown("<h2 style='text-align: center; color: #FAFAFAFA'>Nous vous recommandons :</h2>",
                unsafe_allow_html=True)
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')



with col1:
    st.markdown("<h2 style='text-align: center; color: #FAFAFA'>Choisissez un genre et cliquez sur le film qui vous botte le plus</h2>", unsafe_allow_html=True)
    st.write(' ')
    for n in df_columns[5: -1]:
        if n in options:
            st.subheader(n)
            titre = globals()[n].sample(5, random_state=1).iloc[0][1]
            tconst = globals()[n].sample(5, random_state=1).iloc[0][0]
            if st.button(titre):
                tconst_machine_learning = []
                tconst_machine_learning.append(tconst)
                recommanded_films = recommandation_films(tconst_machine_learning, 40)[0]
                recommanded_films_random = sample(recommanded_films, 5)
                with col2:
                    for each in recommanded_films_random:
                        st.write(each)
            titre1 = globals()[n].sample(5, random_state=37).iloc[1][1]
            tconst1 = globals()[n].sample(5, random_state=37).iloc[1][0]
            if st.button(titre1):
                tconst_machine_learning = []
                tconst_machine_learning.append(tconst1)
                recommanded_films = recommandation_films(tconst_machine_learning, 40)[0]
                recommanded_films_random = sample(recommanded_films, 5)
                with col2:
                    for each in recommanded_films_random:
                        st.write(each)
            titre2 = globals()[n].sample(5, random_state=2).iloc[2][1]
            tconst2 = globals()[n].sample(5, random_state=2).iloc[2][0]
            if st.button(titre2):
                tconst_machine_learning = []
                tconst_machine_learning.append(tconst2)
                recommanded_films = recommandation_films(tconst_machine_learning, 40)[0]
                recommanded_films_random = sample(recommanded_films, 5)
                with col2:
                    for each in recommanded_films_random:
                        st.write(each)
            titre3 = globals()[n].sample(5, random_state=42).iloc[3][1]
            tconst3 = globals()[n].sample(5, random_state=42).iloc[3][0]
            if st.button(titre3):
                tconst_machine_learning = []
                tconst_machine_learning.append(tconst3)
                recommanded_films = recommandation_films(tconst_machine_learning, 40)[0]
                recommanded_films_random = sample(recommanded_films, 5)
                with col2:
                    for each in recommanded_films_random:
                        st.write(each)
            titre4 = globals()[n].sample(5, random_state=25).iloc[4][1]
            tconst4 = globals()[n].sample(5, random_state=25).iloc[4][0]
            if st.button(titre4):
                tconst_machine_learning = []
                tconst_machine_learning.append(tconst4)
                recommanded_films = recommandation_films(tconst_machine_learning, 40)[0]
                recommanded_films_random = sample(recommanded_films, 5)
                with col2:
                    for each in recommanded_films_random:
                        st.write(each)
