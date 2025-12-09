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

    # Drop unnecessary columns
    columns_to_drop = ['Certificate', 'No_of_Votes', 'Gross']
    df.drop(columns=columns_to_drop, inplace=True)

    # Columns to exclude from the content_soup (for comparison dataframe)
    columns_to_drop_search = ['Poster_Link', 'Runtime', 'IMDB_Rating', 'Meta_score']
    df_compare = df.drop(columns=columns_to_drop_search, errors='ignore')

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
    
    # --- KEYWORD EXTRACTION LOGIC (KORRIGERAD) ---
    try:
        # FIX 1: Tvinga Summa att extrahera max 5 ord för att få ett koncentrerat sökresultat.
        extracted_keywords = keywords.keywords(user_input, words=5).replace('\n', ' ')

        # FIX 2: Använd teckenlängd (> 2) istället för att splitta, för robusthet.
        if len(extracted_keywords) > 2: 
            search_query = extracted_keywords
            print(f"  > Söker med Nyckelord: '{search_query}'")
        else:
            search_query = user_input
            print(f"  > Söker med Rå Inmatning (fallback): '{search_query}'")
            
    except Exception as e:
        # Fallback om Summa stöter på ett runtime-fel
        search_query = user_input
        print(f"  > Summa felade ({e}). Söker med Rå Inmatning: '{search_query}'")


    # Transformera den valda sökfrågan till en TF-IDF-vektor
    # Denna rad var korrekt i din ursprungliga kod
    user_tfidf = tfidf_vectorizer.transform([search_query]) 

    # Beräkna Cosine Similarity
    cosine_sim = linear_kernel(user_tfidf, tfidf_matrix)

    # Hämta poängen och sortera
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Hämta index för de bästa resultaten
    top_indices = [i[0] for i in sim_scores[:num_results]]

    # Hämta de relevanta raderna från original-DataFrame
    recommendations_df = original_df.iloc[top_indices].copy()
    
    # --- KRITISKT STEG: DATABEARBETNING FÖR JSON-KOMPATIBILITET ---
    
    # FIX 3: Konvertera NaN/None till Python None och standardtyper (obligatoriskt för Flask/JSON)
    recommendations_df = recommendations_df.where(pd.notnull(recommendations_df), None)
    
    # Konvertera numeriska fält till standard Python-typer
    for col in ['Released_Year']:
        if col in recommendations_df.columns:
            recommendations_df[col] = recommendations_df[col].apply(lambda x: int(x) if x is not None else None)
            
    for col in ['IMDB_Rating', 'Meta_score']:
         if col in recommendations_df.columns:
            recommendations_df[col] = recommendations_df[col].apply(lambda x: float(x) if x is not None else None)


    # Returnera den städade DataFrame (denna går direkt till .to_dict('records') i main.py)
    return recommendations_df