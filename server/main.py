from flask import Flask, jsonify, request
from flask_cors import CORS

from recommender import initialize_recommender, get_recommendations

app = Flask(__name__)
CORS(app)

GLOBAL_TFIDF_VEC = None
GLOBAL_TFIDF_MATRIX = None
GLOBAL_DF = None

def load_recommender_system():
    global GLOBAL_TFIDF_VEC, GLOBAL_TFIDF_MATRIX, GLOBAL_DF
    # 2. Ladda systemet en gång och spara resultaten i de globala variablerna
    GLOBAL_TFIDF_VEC, GLOBAL_TFIDF_MATRIX, GLOBAL_DF = initialize_recommender()
    if GLOBAL_DF is None:
        print("!!! KRITISKT FEL: Systemet kunde inte laddas. Applikationen kommer inte att fungera korrekt. !!!")

@app.route("/llm", methods=['POST'])
def hello_llm():
    return jsonify({"message": "Hello from LLM endpoint"})

@app.route("/ml", methods=['POST'])
def hello_ml():
    if GLOBAL_DF is None:
        return jsonify({"status": "error", "message": "Rekommendationssystemet kunde inte laddas vid uppstart."}), 503 # Service Unavailable
    
    if not request.is_json:
        return jsonify({"status": "error", "message": "Content-Type måste vara 'application/json'."}), 400
    
    data = request.get_json()
    summary_data = data.get('summary')

    if not summary_data:
        return jsonify({"status": "error", "message": "Nyckeln 'summary' saknas i begäran."}), 400
    
    recommendations_df, keywords = get_recommendations(
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