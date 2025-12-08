from google import genai
from google.genai import types
import os
import kagglehub
import pandas as pd
import json

# 1. Download latest version
path = kagglehub.dataset_download("harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows")

# 2. Find and Load the CSV file
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

if csv_files:
    # Load the first CSV found
    df = pd.read_csv(os.path.join(path, csv_files[0]))

    # Define columns to remove (added errors='ignore' to prevent crashes on typos)
    columns_to_drop = ['Certificate', 'No_of_Votes', 'Gross']
    df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    # Create a new dataframe that excludes columns for easier search
    columns_to_drop_search = ['Poster_Link', 'Runtime', 'IMDB_Rating', 'Meta_score']
    df_compare = df.drop(columns=columns_to_drop_search)

    # --- INPUT: Define what the user wants ---
    user_request = ""

    # 3. Convert df_compare to a CSV string so the AI can read it
    # index=False hides the row numbers to save space
    csv_data = df_compare.to_csv(index=True)

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
    1. Analyze the dataset to find the top 3 movies that best match the User Request.
    2. **SORTING:** Order the results by **Relevance** (Best match = First). Do NOT sort numerically.
    3. **OUTPUT FORMAT:** Return a raw JSON list of integers only. Do not write explanations. Do not write "json" or markdown tags.

    ### EXAMPLE OUTPUT
    [45, 12, 998]
    """

    # 5. Initialize Client (Ensure you have your API Key set in environment variables)
    # Or pass it directly: client = genai.Client(api_key="YOUR_KEY")
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    # 6. Call the API
    print("Sending data to Gemini...")
    response = client.models.generate_content(
        model="gemini-2.0-flash-thinking-exp-1219",  # I updated this to the current public thinking model
        contents=final_prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="low")
        ),
    )

    try:
        # Clean the response (sometimes Gemini adds ```json ... ``` blocks)
        clean_text = response.text.strip().replace("```json", "").replace("```", "")

        # Parse the list
        top_indexes = json.loads(clean_text)  # This turns "[1, 2, 3]" into a Python list [1, 2, 3]

        # SAFETY CHECK: Filter out IDs that might not exist in the dataframe
        valid_indexes = [idx for idx in top_indexes if idx in df.index]

        # Use the indexes
        print("Top Recommendations:", top_indexes)
        final_movies = df.loc[top_indexes]  # Retrieve full rows
        print(final_movies[['Series_Title', 'Overview']])

    except json.JSONDecodeError:
        print("The AI didn't return a valid list. Raw response:", response.text)

else:
    print("No CSV file found in the downloaded path.")