from flask import Flask, jsonify, request
from flask_cors import CORS

from recommender import initialize_recommender, get_recommendations_ml, get_recommendations_llm

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

GLOBAL_TFIDF_VEC = None
GLOBAL_TFIDF_MATRIX = None
GLOBAL_DF = None

def load_recommender_system():
    global GLOBAL_TFIDF_VEC, GLOBAL_TFIDF_MATRIX, GLOBAL_DF
    # 2. Ladda systemet en gång och spara resultaten i de globala variablerna
    GLOBAL_TFIDF_VEC, GLOBAL_TFIDF_MATRIX, GLOBAL_DF = initialize_recommender()
    if GLOBAL_DF is None:
        print("!!! KRITISKT FEL: Systemet kunde inte laddas. Applikationen kommer inte att fungera korrekt. !!!")

# Fix this
@app.route("/llm", methods=['POST'])
def hello_llm():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Content-Type måste vara 'application/json'."}), 400
    
    data = request.get_json()
    summary_data = data.get('summary')

    if not summary_data:
        return jsonify({"status": "error", "message": "Nyckeln 'summary' saknas i begäran."}), 400
    
    try:
        recommendations_df = get_recommendations_llm(summary_data, GLOBAL_DF)
        
        # Kontrollera om funktionen returnerade en DataFrame eller None/fel (om du ändrar get_recommendations_llm)
        if recommendations_df is None:
             # Hantera fallet där LLM-anropet misslyckades inuti recommender.py och returnerade None
             return jsonify({"status": "error", "message": "Kunde inte generera rekommendationer (LLM-fel)."}), 500

        recommendations_list = recommendations_df.to_dict('records')

        return jsonify({"recommendations": recommendations_list})
        
    except APIError as e:
        # Fånga Google GenAI API-fel (inklusive 503) och returnera ett tydligt felmeddelande
        print(f"!!! LLM API FEL: {e}")
        return jsonify({"status": "error", "message": f"Kunde inte ansluta till rekommendationstjänsten: {e.status_code} {e.message}"}), 503 # Skicka 503 tillbaka till frontend
    
    except Exception as e:
        # Fånga alla andra oväntade fel
        print(f"!!! OVÄNTAT FEL: {e}")
        return jsonify({"status": "error", "message": "Ett oväntat internt serverfel inträffade."}), 500

@app.route("/test", methods=["GET"])
def test_endpoint():
    return {"api": "online"}

@app.route("/ml", methods=['POST'])
def ml_getrecommend():
    if GLOBAL_DF is None:
        return jsonify({"status": "error", "message": "Rekommendationssystemet kunde inte laddas vid uppstart."}), 503 # Service Unavailable
    
    if not request.is_json:
        return jsonify({"status": "error", "message": "Content-Type måste vara 'application/json'."}), 400
    
    data = request.get_json()
    summary_data = data.get('summary')

    if not summary_data:
        return jsonify({"status": "error", "message": "Nyckeln 'summary' saknas i begäran."}), 400
    
    recommendations_df, keywords = get_recommendations_ml(
        user_input=summary_data, 
        tfidf_vectorizer=GLOBAL_TFIDF_VEC, 
        tfidf_matrix=GLOBAL_TFIDF_MATRIX, 
        original_df=GLOBAL_DF
    )

    recommendations_list = recommendations_df.to_dict('records')

    return jsonify({"recommendations": recommendations_list, "keywords": [keywords]})

if __name__ == '__main__':
    load_recommender_system()

    app.run(debug=True, port=8080)