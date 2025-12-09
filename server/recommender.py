import pandas as pd
import kagglehub
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from summa import keywords

def initialize_recommender():
    """
    Hämtar data, bearbetar den, skapar 'content_soup' och tränar TF-IDF-modellen.
    Returnerar de nödvändiga objekten (vektoriserare, matris, dataframe) för rekommendation.
    """
    print("--- Initialiserar Filmrekommendationssystemet (laddar data...) ---")
    
    # Download latest version of the dataset
    try:
        path = kagglehub.dataset_download("harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows")
    except Exception as e:
        print(f"FEL: Kunde inte ladda ner datasetet från KaggleHub. {e}")
        return None, None, None

    # Find and Load the CSV file
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    if not csv_files:
        print("FEL: Ingen CSV-fil hittades i den nedladdade mappen.")
        return None, None, None
    
    # Load the first CSV found
    df = pd.read_csv(os.path.join(path, csv_files[0]))
    print(f"Datasetet laddat: {len(df)} rader.")

    # 2. GLOBAL CLEANING
    # This fixes the NaN errors for BOTH the soup AND the final display
    # inplace=True modifies df directly
    df.fillna('', inplace=True)

    # Drop unnecessary columns
    columns_to_drop = ['Certificate', 'No_of_Votes', 'Gross']
    df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    # Columns to exclude from the content_soup (for comparison dataframe)
    columns_to_drop_search = ['Poster_Link', 'Runtime', 'IMDB_Rating', 'Meta_score']
    df_compare = df.drop(columns=columns_to_drop_search)

    # Create the "Soup" (en kombinerad textsträng för varje film)
    df_compare['content_soup'] = (
            df_compare['Series_Title'].astype(str) + " " +
            df_compare['Released_Year'].astype(str) + " " +
            df_compare['Genre'].astype(str) + " " +
            df_compare['Director'].astype(str) + " " +
            df_compare['Star1'].fillna('').astype(str) + " " +
            df_compare['Star2'].fillna('').astype(str) + " " +
            df_compare['Star3'].fillna('').astype(str) + " " +
            df_compare['Star4'].fillna('').astype(str) + " " +
            df_compare['Overview'].fillna('').astype(str)
    )

    # Initialize the Vectorizer and train the matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_compare['content_soup'])
    
    print(f"TF-IDF-matris tränad: {tfidf_matrix.shape}")
    print("--- Initialisering slutförd ---")

    return tfidf, tfidf_matrix, df

def get_recommendations(user_input: str, tfidf_vectorizer, tfidf_matrix, original_df, num_results: int = 10):
    """
    Genererar filmrekommendationer baserat på användarens textinmatning 
    med hjälp av Cosine Similarity på TF-IDF-matrisen.

    :param user_input: Textinmatning från användaren.
    :param tfidf_vectorizer: Den tränade TfidfVectorizer.
    :param tfidf_matrix: Den tränade TF-IDF-matrisen för alla filmer.
    :param original_df: Den ursprungliga DataFrame med alla filmdata.
    :param num_results: Antal rekommendationer att returnera.
    :return: En Pandas DataFrame med de bästa rekommendationerna.
    """
    
    # --- KEYWORD EXTRACTION LOGIC ---
    # Försök att extrahera nyckelord med Summa (TextRank)
    extracted_keywords = keywords.keywords(user_input).replace('\n', ' ')

    # LOGIK: Om Summa misslyckas (kort sträng), använd hela inmatningen
    if len(extracted_keywords.split()) > 2:
        search_query = extracted_keywords
        print(f"  > Söker med Nyckelord: '{search_query}'")
    else:
        search_query = user_input
        print(f"  > Söker med Rå Inmatning: '{search_query}'")

    # Transformera användarens inmatning till en TF-IDF-vektor
    user_tfidf = tfidf_vectorizer.transform([search_query])

    # Beräkna Cosine Similarity mellan användarvektorn och alla filmer
    cosine_sim = linear_kernel(user_tfidf, tfidf_matrix)

    # Hämta poängen
    sim_scores = list(enumerate(cosine_sim[0]))

    # Sortera filmerna efter poäng (högst först)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Hämta index för de bästa resultaten
    top_indices = [i[0] for i in sim_scores[:num_results]]

    # Returnera de relevanta raderna från original-DataFrame
    return original_df.iloc[top_indices]