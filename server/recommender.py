import pandas as pd
import kagglehub
from google import genai
from google.genai import types
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from summa import keywords
import json
from dotenv import load_dotenv

# load api key from .env
load_dotenv()

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
            df_compare['Star1'].astype(str) + " " +
            df_compare['Star2'].astype(str) + " " +
            df_compare['Star3'].astype(str) + " " +
            df_compare['Star4'].astype(str) + " " +
            df_compare['Overview'].astype(str)
    )

    # Initialize the Vectorizer and train the matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_compare['content_soup'])
    
    print(f"TF-IDF-matris tränad: {tfidf_matrix.shape}")
    print("--- Initialisering slutförd ---")

    return tfidf, tfidf_matrix, df

def get_recommendations_ml(user_input: str, tfidf_vectorizer, tfidf_matrix, original_df, num_results: int = 10):
    """
    Genererar filmrekommendationer baserat på användarens textinmatning 
    med hjälp av Cosine Similarity på TF-IDF-matrisen.

    :param user_input: Textinmatning från användaren.
    :param tfidf_vectorizer: Den tränade TfidfVectorizer.
    :param tfidf_matrix: Den tränade TF-IDF-matrisen för alla filmer.
    :param original_df: Den ursprungliga DataFrame med alla filmdata.
    :param num_results: Antal rekommendationer att returnera.
    :return: En Pandas DataFrame med de bästa rekommendationerna, extraherade keywords
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
    return original_df.iloc[top_indices], extracted_keywords

def get_recommendations_llm(user_input: str, df):
    # Columns to exclude from the content_soup (for comparison dataframe)
    columns_to_drop_search = ['Poster_Link', 'Runtime', 'IMDB_Rating', 'Meta_score']
    df_compare = df.drop(columns=columns_to_drop_search)

    # # 3. Convert df_compare to a CSV string so the AI can read it
    # # index=False hides the row numbers to save space
    csv_data = df_compare.to_csv(index=True)

    # --- INPUT: Define what the user wants ---
    user_request = user_input

    # 4. Create the Prompt
    # We combine your instructions with the actual data
    final_prompt = f"""
    ### ROLE
    You are a strict data retrieval assistant. Your job is to query the dataset below.

    ### DATASET (Movies with ID)
    {csv_data}

    ### USER REQUEST
    "{user_request}"

    ### INSTRUCTIONS
    1. Analyze the dataset to find the top 10 movies that best match the User Request.
    2. **SORTING:** Order the results by **Relevance** (Best match = First). Do NOT sort numerically.
    3. **OUTPUT FORMAT:** Return a raw JSON list of integers only. Do not write explanations. Do not write "json" or markdown tags.

    ### EXAMPLE OUTPUT
    [45, 12, 998, 34, 545, 75, 85, 03, 135, 777]
    """

    # 5. Initialize Client (Ensure you have your API Key set in environment variables)
    # Or pass it directly: client = genai.Client(api_key="YOUR_KEY")
    client = genai.Client()

    # 6. Call the API
    print("Sending data to Gemini...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # I updated this to the current public thinking model
        contents=final_prompt,
        # config=types.GenerateContentConfig(
        #     thinking_config=types.ThinkingConfig(thinking_level="low")
        # ),
    )
    try:
        # Clean the response (sometimes Gemini adds ```json ... ``` blocks)
        clean_text = response.text.strip().replace("```json", "").replace("```", "")

        # Parse the list
        top_indexes = json.loads(clean_text)  # This turns "[1, 2, 3]" into a Python list [1, 2, 3]

        # SAFETY CHECK: Filter out IDs that might not exist in the dataframe
        valid_indexes = [idx for idx in top_indexes if idx in df.index]

        # Use the indexes
        print("Top Recommendations:", valid_indexes)
        final_movies = df.loc[valid_indexes]  # Retrieve full rows
        print(final_movies[['Series_Title']])

    except json.JSONDecodeError:
        print("The AI didn't return a valid list. Raw response:", response.text)
