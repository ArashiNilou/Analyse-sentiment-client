import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import streamlit as st
import base64


# Charger les données nettoyées
url = "/Users/mac/myenv/df_finale.csv"
df_finale = pd.read_csv(url, sep=",", on_bad_lines="skip")
df_finale.dropna(inplace=True)

# Définir le titre de l'application
st.title("Analyse des avis clients pour améliorer la relation client")


# mettre une image en fond d'écran
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = (
        """
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: contain; /* Utilise contain au lieu de cover */
    background-repeat: no-repeat;
    background-position: center;
    }
    </style>
    """
        % bin_str
    )
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background(
    "vue-dessus-du-jeune-homme-affaires-muscle-serieux-mode-portant-chemise-sans-manches-blanche-baskets-pantalon-rouge-tapant-mains-bandages-avant-formation-boxe-apres-journee-travail-au-bureau.jpg"
)


# Interface utilisateur pour la sélection du produit
produit_recherche = st.text_input("Entrer le nom du produit que vous cherchez : ")

if produit_recherche:
    df_select = df_finale[
        df_finale["famille"].str.contains(produit_recherche, na=False, case=False)
    ]
    unique_familles = df_select["famille"].unique()

    st.write(
        f"Nous avons trouvé {len(unique_familles)} produits qui contiennent le terme que vous avez indiqué:"
    )

    choix_famille = st.selectbox(
        "Merci de choisir le numéro du produit qui vous intéresse :",
        [""] + list(unique_familles),
        key="choix_famille",
    )

    if choix_famille:
        if choix_famille != "":
            df_famille = df_finale[df_finale["famille"] == choix_famille]
            df_note = df_famille[df_famille["note"] <= 2]

            notes = df_note["code_modele"].unique()
            choix_produit = st.selectbox(
                "Merci de choisir le numéro du produit qui vous intéresse :",
                [""] + list(notes),
                key="choix_produit",
            )

            if choix_produit:
                if choix_produit != "":
                    df_tito = df_finale[df_finale["code_modele"] == choix_produit]
                    df_tito = df_tito[df_tito["note"] <= 2]
                    note_1 = df_tito[df_tito["note"] == 1]
                    note_2 = df_tito[df_tito["note"] == 2]

                    st.write(
                        f"Le produit que vous avez sélectionné est le code {choix_produit} qui correspond à la famille {choix_famille}"
                    )
                    st.write(f"Nous avons {len(note_1)} avis avec la note 1")
                    st.write(f"Nous avons {len(note_2)} avis avec la note 2")

                    # Générer le wordcloud pour les reviews des avis notés 1 et 2
                    reviews_negatives = " ".join(df_tito["review"])

                    # Exclure le terme recherché par l'utilisateur et les mots spécifiques du WordCloud
                    stopwords = set(STOPWORDS)
                    custom_stopwords = """
                    a à â abord afin ah ai aie ainsi allaient allo allô allons après assez attendu au aucun aucune
                    aujourd aujourd'hui auquel aura auront aussi autre autres aux auxquelles auxquels avaient avais avait avant
                    avec avoir ayant b bah beaucoup bien bigre boum bravo brrr c ça car ce ceci cela celle celle-ci celle-là
                    celles celles-ci celles-là celui celui-ci celui-là cent cependant certain certaine certaines certains certes
                    ces cet cette ceux ceux-ci ceux-là chacun chaque cher chère chères chers chez chiche chut ci cinq cinquantaine
                    cinquante cinquantième cinquième clac clic combien comme comment compris concernant contre couic crac d da dans
                    de debout dedans dehors delà depuis derrière des dès désormais desquelles desquels dessous dessus deux deuxième
                    deuxièmement devant tre devers devra différent différente différentes différents dire divers diverse diverses dix
                    dix-huit dixième dix-neuf dix-sept doit doivent donc dont douze douzième dring du duquel durant e effet eh elle
                    elle-même elles elles-mêmes en encore entre envers environ es ès est et etant étaient étais était étant etc été
                    etre être eu euh eux eux-mêmes excepté f façon fais faisaient faisant fait feront fi flac floc font g gens h ha
                    hé hein hélas hem hep hi ho holà hop hormis hors hou houp hue hui huit huitième hum hurrah i il ils importe j je
                    jusqu jusque k l la là laquelle las le lequel les lès lesquelles lesquels leur leurs longtemps lorsque lui lui-même
                    m ma maint mais malgré me même mêmes merci mes mien mienne miennes miens mille mince moi moi-même moins mon moyennant
                    n na ne néanmoins neuf neuvième ni nombreuses nombreux non nos notre nôtre nôtres nous nous-mêmes nul o o| ô oh ohé
                    olé ollé on ont onze onzième ore ou où ouf ouias oust ouste outre p paf pan par parmi partant particulier particulière
                    particulièrement pas passé pendant er personne peu peut peuvent peux pff pfft pfut pif plein plouf plus plusieurs plutôt
                    pouah pour pourquoi premier première premièrement près proche psitt puisque q qu quand quant quanta quant-à-soi quarante
                    quatorze quatre quatre-vingt quatrième quatrièmement que quel quelconque quelle quelles quelque quelques quelqu'un quels
                    qui quiconque quinze quoi quoique r revoici revoilà rien s sa sacrebleu sans sapristi sauf se seize selon sept septième
                    sera seront ses si sien sienne siennes siens sinon six sixième soi soi-même soit soixante son sont sous stop suis suivant
                    sur surtout t ta tac tant te té tel telle tellement telles tels tenant tes tic tien tienne tiennes tiens toc toi toi-même
                    ton touchant toujours tous tout toute toutes treize trente très trois troisième troisièmement trop tsoin tsouin tu u un une
                    unes uns v va vais vas vé vers via vif vifs vingt vivat vive vives vlan voici voilà vont vos votre vôtre vôtres vous vous-mêmes
                    vu w x y z zut alors aucuns bon devrait dos droite début essai faites fois force haut ici juste maintenant mine mot nommés
                    nouveaux parce parole personnes pièce plupart seulement soyez sujet tandis valeur voie voient état étions
                    """
                    custom_stopwords = (
                        custom_stopwords.split()
                    )  # Convertir la chaîne en une liste de mots
                    stopwords.update(custom_stopwords)
                    stopwords.update([produit_recherche.lower()])

                    wordcloud = WordCloud(
                        width=800,
                        height=400,
                        background_color="white",  # Fond noir
                        stopwords=stopwords,
                    ).generate(reviews_negatives)

                    # Afficher le wordcloud
                    plt.figure(figsize=(10, 5))
                    plt.imshow(wordcloud, interpolation="bilinear")
                    plt.axis("off")
                    plt.title("Wordcloud des avis négatifs")
                    st.pyplot(plt)

                    # Afficher les id_auteur et les commentaires (full_review)
                    df_comments = df_tito[["id_auteur", "full_review"]].copy()
                    df_comments["id_auteur"] = df_comments["id_auteur"].apply(
                        lambda x: int(x) if pd.notnull(x) else x
                    )
                    st.write("ID Auteurs et leurs Commentaires :")
                    st.table(df_comments)
