# page contenant les visualisations des indicateurs sélectionnés


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import plotly.express as px
import math


# path vers le dossier contenant tous les datasets > à changer pour chacun
path =


# --------------------
# PAGE CONFIGURATION
# --------------------
st.set_page_config(
    page_title="Ciné'Creuse  - Da’taMiners CREW & CIE",
    page_icon="📽️",
    layout="wide",
    initial_sidebar_state="expanded",

    )

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://wallpaperaccess.com/full/3240453.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()


# --------------------
# IMPORTATIONS DATASETS
# --------------------
# import des tables title_basics_clean et title_rating_clean depuis le local
df_title_basics_clean = pd.read_csv(path+"title_basics_clean.txt")
table_basic = df_title_basics_clean.copy()
table_basic2 = df_title_basics_clean.copy()
table_basic_kpi = df_title_basics_clean.copy()
table_basic_kpi2 = df_title_basics_clean.copy()
df_titles = df_title_basics_clean.copy()

df_title_rating_clean = pd.read_csv(path+"title_rating_clean.txt")
table_rating = df_title_rating_clean.copy()
df_ratings = df_title_rating_clean.copy()

# dataframe pour kpi acteurs et réalisateurs
#df_principal_actors_clean = pd.read_csv(path+'title_principal_clean_actors.txt')
#df_principal_directors_clean = pd.read_csv(path+'title_principal_clean_directors.txt', sep='w')

# --------------------
# PREPARATION DE LA TABLE title_basics_clean POUR LE 1ER KPI
# --------------------

# séparation de la colonne startYear en 3 colonnes : Year, Month, Day
df_title_basics_clean[['Year', 'Month', 'Day']] = df_title_basics_clean.startYear.str.split('-', expand=True)

# permet d'ordonner les années chronologiquement
df_title_basics_clean.sort_values(by=['Year'], inplace=True)

# séparation des années en décennies
df_title_basics_ratings_70_79 = ((df_title_basics_clean.Year >= '1970') & (df_title_basics_clean.Year < '1980'))
df_title_basics_ratings_80_89 = ((df_title_basics_clean.Year >= '1980') & (df_title_basics_clean.Year < '1990'))
df_title_basics_ratings_90_99 = ((df_title_basics_clean.Year >= '1990') & (df_title_basics_clean.Year < '2000'))
df_title_basics_ratings_00_09 = ((df_title_basics_clean.Year >= '2000') & (df_title_basics_clean.Year <= '2010'))

conditions = [df_title_basics_ratings_70_79, df_title_basics_ratings_80_89, df_title_basics_ratings_90_99, df_title_basics_ratings_00_09]
values = ['1970 à 1979', '1980 à 1989', '1990 à 1999', '2000 à 2010']

# création d'une colonne 'decades'
df_title_basics_clean['decades'] = np.select(conditions, values)


# -------------------
# PREPARATION DE LA TABLE title_rating_clean POUR LE 2E KPI
# -------------------


# séparation de chaque genre en sous-genre ('sub_genres')
table_basic.loc[table_basic.genres.str.contains(","), 'sub_genres'] = table_basic.genres.str.split(",")
table_basic.loc[~table_basic.genres.str.contains(","), 'sub_genres'] = table_basic.genres.apply(lambda val: [val])
table_basic = table_basic.explode('sub_genres')


# fusion de title_rating and title_basics
df_rating_basic = pd.merge(table_rating, table_basic, how='inner', on='tconst')


# obtention des moyennes
meanPerGenres = df_rating_basic.groupby('sub_genres').agg(mean_rating=('averageRating', 'mean')).sort_values(by='mean_rating', ascending=False)
meanPerGenres['sub_genres'] = meanPerGenres.index


# -----------------
# PREPARATION DE LA TABLE title_basic_clean POUR LE 3EME KPI
# -----------------

# séparation de chaque genre en sous-genre ('sub_genres')
table_basic_kpi.loc[table_basic_kpi.genres.str.contains(","), 'sub_genres'] = table_basic_kpi.genres.str.split(",")
table_basic_kpi.loc[~table_basic_kpi.genres.str.contains(","), 'sub_genres'] = table_basic_kpi.genres.apply(lambda val: [val])
table_basic_kpi = table_basic_kpi.explode('sub_genres')

# colonne 'YEAR' avec l'année uniquement
table_basic_kpi['YEAR'] = pd.DatetimeIndex(table_basic_kpi['startYear']).year

# regroupement des films par genre et par année
table_basic_kpi = table_basic_kpi.groupby(['YEAR', 'sub_genres']).agg({'runtimeMinutes': sum, 'sub_genres':"count"})

# renommage des colonnes de la table 'table_basic_kpi'
table_basic_kpi.columns=['runtimeMinutes', 'count']

# suppression du multi-index pour en faire 2 colonnes
table_basic_kpi = table_basic_kpi.reset_index()



# -----------------
# PREPARATION DE LA TABLE title_basic_clean POUR LE 4EME KPI
# -----------------

# jointure des 2 dataframes
df = pd.merge(left=df_titles,
              right=df_ratings,
              how='left',
              on='tconst')

# séparation de chaque genre en sous-genre ('sub_genres')
df.loc[df.genres.str.contains(","), 'sub_genres'] = df.genres.str.split(",")
df.loc[~df.genres.str.contains(","), 'sub_genres'] = df.genres.apply(lambda val: [val])
df = df.explode('sub_genres')

# suppression des lignes avec des nan (certains films ne sont pas notés)
df.dropna(inplace=True)

# création d'un facteur d'évaluation tenant compte de la note moyenne du film et du nombre de votes pour ce film
df['logNumVotes'] = df.numVotes.apply(lambda x: math.log10(x))
df['multipFactor'] = df.averageRating * df.logNumVotes
df['rankingIndicator'] = df.multipFactor.apply(lambda x: round(x * 100 / 60, 1))

# dataframe trié par indicateur descendant
df_sorted = df.sort_values(by='rankingIndicator', ascending=False)

# KPI GENRES : dataframe moyenne d'indicateur par genre trié par genre
df_genres = df[['sub_genres', 'rankingIndicator']]
df_groupGenres = df_genres.groupby('sub_genres').agg(mean_rating=('rankingIndicator', 'mean')).sort_values(
    by='mean_rating', ascending=False)
#df_groupGenres['count_rating'] = df_genres.groupby('sub_genres') <- plus utilisé, remplacé par le nuage de mots
#                                           .agg(count_rating=('rankingIndicator', 'count'))
#                                           .sort_values(by='count_rating', ascending=False)

# cloud words
# Counter:
from collections import Counter

# package Nuage de mots :
from wordcloud import WordCloud

# sélection des données :

table_basic2.loc[table_basic2.genres.str.contains(","), 'sub_genres'] = table_basic2.genres.str.split(",")

table_basic2.loc[~table_basic2.genres.str.contains(","), 'sub_genres'] = table_basic2.genres.apply(lambda val: [val])

table_basic2 = table_basic2.explode('sub_genres')
table_basic2['startYear'] = pd.to_datetime(table_basic2['startYear'])

table_basic2['YEAR']= table_basic2['startYear'].dt.strftime('%Y')

table_basic_ = table_basic2.groupby(['YEAR', 'sub_genres']).agg({'runtimeMinutes': sum, 'sub_genres':"count"})

table_basic_nuage = table_basic2.drop(['tconst',
                                      'titleType',
                                      'primaryTitle',
                                      'originalTitle',
                                      'isAdult',
                                      'startYear',
                                      'runtimeMinutes',
                                      'genres',
                                      'YEAR'],
                                     axis =1)

genres = " ".join(table_basic_nuage['sub_genres'])
genres = genres.split(sep =' ')

# préparation visualisation :

def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    h = int(360.0 * 45.0 / 255.0)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)

word_could_dict=Counter(genres)
wordcloud = WordCloud(width = 1000, height = 500, color_func=random_color_func).generate_from_frequencies(word_could_dict)

# KPI ACTEURS : dataframe moyenne d'indicateur par acteur trié par acteur
#df_actors = df[df.primaryProfession.isin(['actor', 'actress'])][
#    ['primaryName', 'rankingIndicator']]  # filtre pour n'avoir que les actors/actresses
#meanPerActor = df_actors.groupby('primaryName').agg(mean_rating=('rankingIndicator', 'mean')).sort_values(
#    by='primaryName')

# KPI REALISATEURS : dataframe moyenne d'indicateur par réalisateur trié par moyenne descendante
#df_directors = df[df.primaryProfession.isin(['director'])][['primaryName', 'rankingIndicator']]  # filtre pour n'avoir que les directors
#meanPerDirector = df_directors.groupby('primaryName').agg(mean_rating=('rankingIndicator', 'mean')).sort_values(by='primaryName')

# KPI ANNEE : dataframe moyenne d'indicateur par décade trié par moyenne descendante
# transformation des dates en année seulement
df.startYear = pd.DatetimeIndex(df.startYear).year
# classification des années en décades
df_year_70_79 = ((df.startYear >= 1970) & (df.startYear < 1980))
df_year_80_89 = ((df.startYear >= 1980) & (df.startYear < 1990))
df_year_90_99 = ((df.startYear >= 1990) & (df.startYear < 2000))
df_year_00_09 = ((df.startYear >= 2000) & (df.startYear <= 2010))

conditions_dec = [df_year_70_79, df_year_80_89, df_year_90_99, df_year_00_09]
values_dec = ['1970 à 1979', '1980 à 1989', '1990 à 1999', '2000 à 2010']

# création d'une colonne 'decades'
df['decades'] = np.select(conditions_dec, values_dec)
df_decades = df[['decades', 'rankingIndicator']]
df_groupDecades = df_decades.groupby('decades').agg(mean_rating=('rankingIndicator', 'mean')).sort_values(by='decades')
df_groupDecades['count_rating'] = df_decades.groupby('decades').agg(
    count_rating=('rankingIndicator', 'count')).sort_values(by='decades')

# KPI DUREE : dataframe moyenne d'indicateur par plage de durée de 30min trié par moyenne descendante
# classification des durées en plages de durées
df_runtime1 = ((df.runtimeMinutes >= 0) & (df.runtimeMinutes < 60))
df_runtime2 = ((df.runtimeMinutes >= 60) & (df.runtimeMinutes < 90))
df_runtime3 = ((df.runtimeMinutes >= 90) & (df.runtimeMinutes < 120))
df_runtime4 = (df.runtimeMinutes >= 120)

conditions_rt = [df_runtime1, df_runtime2, df_runtime3, df_runtime4]
values_rt = ['moins de 60 min', '60 à 90 min', '90 à 120 min', 'plus de 120 min']

# création d'une colonne 'plageRuntime'
df['plageRuntime'] = np.select(conditions_rt, values_rt)
df_plageRuntime = df[['plageRuntime', 'rankingIndicator']]
df_groupRuntime = df_plageRuntime.groupby('plageRuntime').agg(mean_rating=('rankingIndicator', 'mean'))
df_groupRuntime['count_rating'] = df_plageRuntime.groupby('plageRuntime').agg(count_rating=('rankingIndicator', 'count'))

# ------------------
# VISUALISATION STREAMLIT
# ------------------


# création d'onglets
tab1, tab2, tab3, tab4 = st.tabs(['Moyenne par genre', 'Durée des films', 'Films par année', 'Typologie des meilleurs films'])

with tab2:
    st.markdown(
        "<h1 style='text-align: center; color: #FAFAFA'>Dispersion des films suivant leur durée par décennie</h1>",
        unsafe_allow_html=True)
    st.write(' ')
    st.write('Depuis 1970, la durée des films a augmenté jusqu\'aux années 2000.\n'
             'Elle a ensuite diminué, notamment avec l\'arrivée des Talk-Shows.')
    st.write(' ')



    fig_violin, ax_violin = plt.subplots()

    violin = sns.violinplot(data=df_title_basics_clean,
                            x='decades',
                            y=df_title_basics_clean[df_title_basics_clean['runtimeMinutes'] < 180]['runtimeMinutes'],
                            inner='quartile')

    violin.set_xlabel('Décennies', fontsize=15, color='#FAFAFA')
    violin.set_ylabel('Durée des films (minutes)', fontsize=15, color='#FAFAFA')
    violin.set_facecolor('#000000')
    violin.spines['bottom'].set_color('#FAFAFA')
    violin.spines['left'].set_color('#FAFAFA')
    violin.tick_params(axis='x', colors='#FAFAFA')
    violin.tick_params(axis='y', colors='#FAFAFA')
    fig_violin.patch.set_facecolor('#000000')
    st.pyplot(violin.figure)


with tab1:
    st.markdown("<h1 style='text-align: center; color: #FAFAFA'>Note moyenne des films par genre</h1>",
                unsafe_allow_html=True)
    st.write(' ')
    st.write('Les genres Biographie, Documentaire, Historique sont les mieux notés en moyenne.\n'
             'Ils sont certainement plus pertinents car ils sont visionnés par un public plus intéressé par le sujet que par un divertissement quelconque.')
    st.write(' ')

    fig_bar, ax_bar = plt.subplots()

    barchart = sns.barplot(data=meanPerGenres,
                           y='sub_genres',
                           x='mean_rating',
                           color='#e50914')

    barchart.set_ylabel('Genres', fontsize=15, color='#FAFAFA')
    barchart.set_xlabel('Note moyenne (sur 10)', fontsize=15, color='#FAFAFA')
    barchart.set_facecolor('#000000')
    barchart.spines['bottom'].set_color('#FAFAFA')
    barchart.spines['left'].set_color('#FAFAFA')
    barchart.tick_params(axis='x', colors='#FAFAFA')
    barchart.tick_params(axis='y', colors='#FAFAFA')
    fig_bar.patch.set_facecolor('#000000')

    # inversion des 'ticks' sur l'abscisse
    #plt.gca().invert_xaxis()

    # rotation des 'ticks' (étiquettes) sur l'abscisse de 45°
    #plt.xticks(rotation=90)

    st.pyplot(barchart.figure)


with tab3:
    st.markdown("<h1 style='text-align: center; color: #FAFAFA'>Nombre de films par année et par genre</h1>", unsafe_allow_html=True)

    fig_plot, ax_plot = plt.subplots()

    fig_plotly = px.bar(table_basic_kpi,
                        x='sub_genres',
                        y='count',
                        animation_frame='YEAR',
                        color='sub_genres',
                        color_discrete_map={
                            "Drama": "lime",
                            "Action": "yellowgreen",
                            "Adventure": "grey",
                            "Comedy": "red",
                            "Crime": "mediumvioletred",
                            "Horror": "blue",
                            "Western": "black"},
                        labels={'sub_genres': 'Genres', 'count': 'Nombre de films'}
                        )

    fig_plotly.update_layout(yaxis_range=[0, 3000],
                             font=dict(size=10))
    st.plotly_chart(fig_plotly)



with tab4:
    st.markdown("<h1 style='text-align: center; color: #FAFAFA'>Typologie des meilleurs films</h1>", unsafe_allow_html=True)
    'La typologie définit pour chaque catégorie les films qui ont le plus de succès. Le gérant du cinéma peut ainsi choisir les meilleurs films pour attirer plus de spectateurs.'
    'Afin de définir les meilleurs films, il fallait tenir compte à la fois de la note moyenne et du nombre de votes. L\'indicateur SCORE a été créé en ce sens.'
    # radioboxes de sélection de KPI
    st.markdown("<h4 style='text-align: center; color: #FAFAFA'>Catégories</h4>", unsafe_allow_html=True)
    radio_buttons = st.radio('',
                             #['Genres', 'Acteurs', 'Réalisateurs', 'Décennies', 'Durée'],
                             ['Genres', 'Décennies', 'Durée'],
                             horizontal=True)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    if radio_buttons == 'Genres':

        col_barplot, col_wordcloud = st.columns(2)
        #fig, ax = plt.subplots(2, 1) <- problème d'affichage avec une figure à deux subplots, les éléments se superposent. D'où la création de containers

        with col_barplot:

            # lineplot
            fig1, ax1 = plt.subplots(1, 1)
            #ax1 = plt.subplot(111)
            ax1 = sns.barplot(data=df_groupGenres,
                              y= df_groupGenres.index,
                              x='mean_rating',
                              color='#E50914'
                              )
            ax1.set_xlabel('Score moyen /100', fontsize=15, color='#FAFAFA')
            ax1.set_ylabel('Genres', fontsize=15, color='#FAFAFA')
            ax1.set_facecolor('#000000')
            ax1.spines['bottom'].set_color('#FAFAFA')
            ax1.spines['left'].set_color('#FAFAFA')
            ax1.tick_params(axis='x', colors='#FAFAFA')
            ax1.tick_params(axis='y', colors='#FAFAFA')
            fig1.patch.set_facecolor('#000000')
            st.pyplot(fig1)

        with col_wordcloud:

            # wordcloud
            fig2, ax2 = plt.subplots(1, 1)
            #ax2 = plt.subplot(111)
            ax2.imshow(wordcloud)
            ax2.axis("off")
            plt.title('Proportion du nombre de films par genre\n', fontsize=15, color='#E50914', fontweight='bold')
            fig2.patch.set_facecolor('#000000')
            st.pyplot(fig2)

        #st.pyplot(fig)


    elif radio_buttons == 'Acteurs':
        'Feature in progress...'
        #actors_choice = st.multiselect('Choisissez des acteurs.trices',
        #                               labels=meanPerActor.index)
        #st.write(meanPerActor[meanPerActor.isin(actors_choice)])

    elif radio_buttons == 'Réalisateurs':
        'Feature in progress...'
        #directors_choice = st.multiselect('Choisissez un réalisateur.trice',
        #                                  labels=meanPerDirector.index)
        #st.write(meanPerDirector[meanPerDirector.isin(directors_choice)])

    elif radio_buttons == 'Décennies':

        # Figure
        #fig, ax = plt.subplots(2, 1)
        col_lineplot, col_piechart = st.columns(2)

        with col_lineplot:
            # lineplot
            fig3, ax3 = plt.subplots(1, 1)
            ax3.plot(df_groupDecades.index,
                    df_groupDecades.mean_rating,
                    color='#E50914',
                    linewidth=2)
            ax3.set_ylabel('Score moyen /100', fontsize=15, color='#FAFAFA')
            ax3.set_xlabel('Décennie', fontsize=15, color='#FAFAFA')
            ax3.set_facecolor('#000000')
            ax3.spines['bottom'].set_color('#FAFAFA')
            ax3.spines['left'].set_color('#FAFAFA')
            ax3.tick_params(axis='x', colors='#FAFAFA')
            ax3.tick_params(axis='y', colors='#FAFAFA')
            fig3.patch.set_facecolor('#000000')
            st.pyplot(fig3)

        with col_piechart:
            # pie chart
            fig4, ax4 = plt.subplots(1, 1)
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
            explode = (0.05, 0.05, 0.05, 0.05)
            ax4.pie(x=df_groupDecades.count_rating,
                    colors=colors,
                    labels=df_groupDecades.index,
                    autopct=lambda x: f'{x:.0f}%',
                    startangle=90,
                    explode=explode,
                    shadow=True,
                    textprops={'fontsize':10, 'color':'#FAFAFA'})

            ax4.axis('equal')
            plt.title('Proportion du nombre de films par décennie', fontsize=15, color='#E50914', fontweight='bold')
            fig4.patch.set_facecolor('#000000')
            st.pyplot(fig4)

    elif radio_buttons == 'Durée':

        col_barplot2, col_piechart2 = st.columns(2)

        with col_barplot2:
            # barplot
            fig5, ax5 = plt.subplots(1, 1)

            ax5 = sns.barplot(data=df_groupRuntime,
                              x=df_groupRuntime.index,
                              y='mean_rating',
                              order=values_rt,
                              color='#E50914'
                              )
            ax5.set_ylabel('Score moyen /100', fontsize=15, color='#FAFAFA')
            ax5.set_xlabel(None)
            ax5.set_facecolor('#000000')
            ax5.spines['bottom'].set_color('#FAFAFA')
            ax5.spines['left'].set_color('#FAFAFA')
            ax5.tick_params(axis='x', colors='#FAFAFA')
            ax5.tick_params(axis='y', colors='#FAFAFA')
            fig5.patch.set_facecolor('#000000')
            st.pyplot(fig5)

        with col_piechart2:
            # pie chart
            fig6, ax6 = plt.subplots(1, 1)
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
            explode = (0.05, 0.05, 0.05, 0.05)
            ax6.pie(x=df_groupRuntime.count_rating,
                    colors=colors,
                    labels=df_groupRuntime.index,
                    autopct=lambda x: f'{x:.1f}%',
                    startangle=90,
                    explode=explode,
                    shadow=True,
                    textprops={'fontsize':10, 'color':'#FAFAFA'})

            ax6.axis('equal')
            plt.title('Proportion du nombre de films par durée', fontsize=15, color='#E50914', fontweight='bold')
            fig6.patch.set_facecolor('#000000')

            st.pyplot(fig6)
