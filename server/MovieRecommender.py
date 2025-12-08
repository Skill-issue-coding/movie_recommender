import pandas as pd
import kagglehub
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from summa import keywords

# Download latest version
path = kagglehub.dataset_download("harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows")

# 2. Find and Load the CSV file
# kagglehub returns a folder path, so we find the .csv file inside it
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
if csv_files:
    # Load the first CSV found
    df = pd.read_csv(os.path.join(path, csv_files[0]))

    # Define the list of columns to remove
    columns_to_drop = ['Certificate', 'No_of_Votes', 'Gross']
    # Define the list of columns to remove from search
    columns_to_drop_search = ['Poster_Link', 'Runtime', 'IMDB_Rating', 'Meta_score']

    # Drop unnecessary columns from the dataframe
    # inplace=True means "modify the current dataframe directly" rather than creating a new one
    df.drop(columns=columns_to_drop, inplace=True)

    # Create a new dataframe that excludes columns for easier search
    df_compare = df.drop(columns=columns_to_drop_search)

    # --- THIS IS THE KEY LINE ---
    pd.set_option('display.max_columns', None)
    #print("Columns in df_compare:", df_compare.columns.tolist())
    #print("Columns in df_compare:", df.columns.tolist())
    # ----------------------------

    # Optional: You can also set max_width if columns are wrapping weirdly
    # pd.set_option('display.width', 1000)

    # 3. Print the top of the dataframe
    #print(df.head())

    # Create the "Soup" inside df_compare
    # We use .fillna('') to replace empty values with nothing so the code doesn't break
    # We use .astype(str) because 'Released_Year' is a number, and we need text

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

    # 2. Initialize the Vectorizer
    # stop_words='english' removes common words like "the", "and", "is"
    tfidf = TfidfVectorizer(stop_words='english')

    # 3. Fit and Transform the movie data
    # This creates a matrix where Rows = Movies, Columns = Unique Words
    tfidf_matrix = tfidf.fit_transform(df_compare['content_soup'])

    print(f"Matrix Shape: {tfidf_matrix.shape}")
    # Output will look like (1000, 6000+) meaning 1000 movies and 6000+ unique words

    def get_recommendations(user_input, tfidf_vectorizer, tfidf_matrix, original_df):

        # --- KEYWORD EXTRACTION LOGIC ---
        # Extract keywords using Summa (TextRank)
        extracted_keywords = keywords.keywords(user_input).replace('\n', ' ')

        # LOGIC: Summa fails on short strings.
        # If extracted_keywords is less than 3 words, use the raw user_input.
        if len(extracted_keywords.split()) > 2:
            search_query = extracted_keywords
            print(f"Searching using Keywords: '{search_query}'")
        else:
            search_query = user_input
            print(f"Keywords not found (text too short). Searching using Raw Input: '{search_query}'")


        # Transform the user input into a vector
        # We use .transform() instead of .fit_transform() because we want to use the movie's vocabulary
        user_tfidf = tfidf_vectorizer.transform([user_input])

        # Calculate Cosine Similarity
        # This gives a score between 0 (no match) and 1 (perfect match) for every movie
        cosine_sim = linear_kernel(user_tfidf, tfidf_matrix)

        # Get the scores
        # cosine_sim is a list of lists, we flatten it to a simple list
        sim_scores = list(enumerate(cosine_sim[0]))

        # Sort the movies based on the similarity scores (highest first)
        # x[1] is the score, x[0] is the index
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the top 3 (Index 0, 1, 2)
        top_indices = [i[0] for i in sim_scores[:3]]

        # Return the rows from the dataframe
        return original_df.iloc[top_indices]

        # --- TESTING ---

    # Test 1: Short Query (Summa usually fails here, so it falls back to raw text)
    print("--- TEST 1: Short Query ---")
    req1 = "I want a crime movie directed by Tarantino"
    rec1 = get_recommendations(req1, tfidf, tfidf_matrix, df)
    print(rec1[['Series_Title', 'Released_Year', 'Runtime', 'Genre', 'IMDB_Rating', 'Overview', 'Meta_score', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']])
    print("\n" + "=" * 50 + "\n")

    # Test 2: Long Query (Summa works great here)
    print("--- TEST 2: Long Complex Query ---")
    req2 = "I am looking for a visually spectacular sci-fi noir set in a dying, dystopian future where the line between artificial intelligence and humanity is blurred."
    rec2 = get_recommendations(req2, tfidf, tfidf_matrix, df)
    print(rec2[['Series_Title', 'Released_Year', 'Runtime', 'Genre', 'IMDB_Rating', 'Overview', 'Meta_score', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']])
    print("\n" + "=" * 50 + "\n")

    # Test 3:
    print("--- TEST 3 ---")
    req3 = "Tarantino"
    rec3 = get_recommendations(req3, tfidf, tfidf_matrix, df)
    print(rec3[['Series_Title', 'Released_Year', 'Runtime', 'Genre', 'IMDB_Rating', 'Overview', 'Meta_score', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']])
    print("\n" + "=" * 50 + "\n")

    # Test 4:
    print("--- TEST 4 ---")
    req4 = "I want a period drama movie with a touch of romance with the actor Tom Hanks."
    rec4 = get_recommendations(req4, tfidf, tfidf_matrix, df)
    print(rec4[['Series_Title', 'Released_Year', 'Runtime', 'Genre', 'IMDB_Rating', 'Overview', 'Meta_score', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']])
    print("\n" + "=" * 50 + "\n")
else:
    print("No CSV file found in the downloaded path.")


#movie_request_1 = "I am looking for a visually stunning fantasy drama set within the Infinite Athenaeum, a sentient library existing in the space between seconds, focusing on two rival archivists named Elara and Kaelen. Elara is a chaotic pyromancer who views magic as raw emotion, while Kaelen is a rigid chronomancer who treats it as a precise calculation. For decades, their relationship has consisted solely of stinging insults scribbled in the margins of ancient scrolls, but when a catastrophic Void Leak threatens to erase history, they are forced into a collapsing pocket dimension to fix it. I want the narrative to focus on a mature, slow-burn romance where their survival depends entirely on synchronizing their opposing powers. Visually, the film should depict her violet flames thawing his frozen time-loops to create a dazzling new golden energy, symbolizing how their contradictory natures actually complete one another. The story shouldn't rely on generic action battles but rather on the intimacy of two intellectual equals realizing they are the only ones capable of understanding the burden of such immense power. The film should culminate in a heartbreaking choice where they must decide whether to save the library and return to their solitary lives or let the world crumble just to remain together in the chaos, prioritizing atmosphere and chemistry above all else."

#print("------------ Test Text -----------")
#print("keywords: \n", keywords.keywords(movie_request_1), "\n")
#print("Top 5 Keywords:\n",keywords.keywords(movie_request_1,words=5), "\n")


