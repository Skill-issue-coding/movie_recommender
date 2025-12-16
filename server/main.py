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
    lite = data.get('lite')

    if not summary_data:
        return jsonify({"status": "error", "message": "Nyckeln 'summary' saknas i begäran."}), 400
    
    if not lite:
        return jsonify({"status": "error", "message": "Nyckeln 'lite' saknas i begäran."}), 400
    
    try:
        recommendations_df = get_recommendations_llm(summary_data, GLOBAL_DF, lite)
        
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

''' User inputs used

1)  I want to see a movie about a poor young boy that falls in love with a upper-class girl on a ship. The ship later hits an iceberg and sinks, leaving the young girl as one of few surviors. 
    Answer ML 1-10:                                  Answer LLM 1-10:
    Lifeboat                                         Titanic
    The Notebook                                     The Notebook
    Blade runner                                     Aladdin
    El angle exterminador                            Pirates of the caribbean: The curse of the black pearl
    Sense and Sensibility                            Roman holiday
    Koe no katachi                                   Life of PI
    Manhattan                                        Lifeboat
    Serenity                                         La leggenda del pianista sull'oceano
    Dil Bechara                                      Apollo 13
    Metropolis                                       Days of heaven

    2/10, movie: Titanic

2)  I want to see a movie that is about the criminal underworld of Los Angeles, the lives of two philosophical hitmen, a washed-up boxer, and a gangster's drug-addicted wife violently intertwine. Told through a fractured timeline.
    Answer ML 1-10:                                  Answer LLM 1-10:
    Pulp fiction                                     Pulp fiction
    Short cuts                                       L.A. Confidential
    Cinderella man                                   True Romance
    Happiness                                        Heat
    The fall                                         Nightcrawler
    Crash                                            Crash
    Die hard                                         Mulholland Dr.
    The boondock saints                              Reservoir dogs
    Boyz n the hood                                  Sin city
    The lion in winter                               Memento

    2/10, movie: Pulp fiction

3) On an alien planet, a paraplegic Marine gets a second chance at life by transferring his consciousness into a genetically engineered alien body. He is then sent to infiltrate the native tribe to aid a ruthless mining operation, the marine falls in love with an alien warrior and is forced to choose between his human orders and fighting to save his new home from destruction.
    Answer ML 1-10:                                  Answer LLM 1-10:
    Invasion of the body snatchers                   Avatar
    Planet of the apes                               The last samurai
    Stand by me                                      Dances with wolves
    Arrival                                          District 9
    E.T. the extra-terrestrial                       Planet of the apes
    The thing                                        Moon
    The day the earth stood still                    The matrix
    El cuerpo                                        Blade runner 2049
    The avengers                                     Interstellar
    The remains of the day                           Children of men

    1/10, movie: Avatar

4) A sweeping crime drama about a powerful Italian-American family at the center of organized crime, exploring loyalty, power, and the cost of legacy. As an aging patriarch loses control, his quiet, reluctant son is pulled into a world of violence and betrayal, slowly becoming the very thing he once rejected. Starring Marlon Brando.
    Answer ML 1-10:                                  Answer LLM 1-10:
    Amarcord                                         The Godfather
    Goodfellas                                       The Godfather: part 2
    Drishyam                                         The Godfather: part 3
    Green book                                       Goodfellas
    Il conformista                                   Casino
    Il postino                                       Donnie Brasco
    Kari-gurashi no arietti                          Once upon a time in america
    Drishyam                                         Heat
    The Godfather: part 3                            Scarface
    The Godfather: part 2                            On the waterfront

    3/10, movie: The Godfather

5) An epic fantasy adventure set in a vast, ancient world where humans, elves, dwarves and other mystical beings coexist. A small and unlikely hero is tasked with destroying a powerful ring that could doom all of civilization. Along the journey, alliances are forged, kingdoms rise and fall, and the struggle between good and evil tests loyalty, courage, and sacrifice.
    Answer ML 1-10:                                  Answer LLM 1-10:
    Life of PI                                       The lord of the rings: The fellowship of the ring
    The man who would be king                        The lord of the rings: The two towers
    Giant                                            The lord of the rings: The return of the king
    Ghostbusters                                     The hobbit: An unexpected journey
    Magnolia                                         The hobbit: The Desolation of smaug
    The message                                      Mononoke-hime
    The Goonies                                      Kaze no tani no naushika
    Malcolm X                                        Star wars
    Isle of dogs                                     Star wars: Episode V - The empire strikes back
    Tokyo goddofazazu                                Star wars: Episode VI - return of the jedi

    0/10, movie: Lord of the rings

6) A dark science-fiction thriller set in a future where machines rule the world and seek to eliminate humanity’s last hope. A relentless killing machine is sent back in time to alter fate, while a lone protector and an unsuspecting woman must fight to survive, discovering that the future is not yet written and can still be changed.
    Answer ML 1-10:                                  Answer LLM 1-10:
    The terminator                                   The terminator
    Twelve monkeys                                   Terminator 2: judgment day
    Minority report                                  The Matrix
    Wall-E                                           Avengers: Endgame
    La planete sauvage                               Blade runner
    Back to the future                               Blade runner 2049
    Argo                                             Children of men
    The warriors                                     Ex machina
    Un long dimanche de fiancailles                  Aliens
    Lagaan: Once upon a time in India                Alien

    1/10, movie: The terminator

7) A timeless animated adventure about a young lion destined to rule the savanna, whose life is shattered by betrayal and loss. Forced into exile, he grows up far from his past, until duty, identity, and the circle of life call him back to face his fears and reclaim his rightful place.
    Answer ML 1-10:                                  Answer LLM 1-10:
    The lion king                                    The lion king
    The dark knight rises                            Baahubali 2: The conclusion
    La grande bellezza                               The lord of the rings: The return of the king
    La vie d'Adele                                   Star wars
    Jagten                                           Moana
    Gandhi                                           Kaze no tani no naushika
    The butterfly effect                             Coco
    The incredibles                                  Kubo and the two strings
    Out of the past                                  The lord of the rings: The fellowship of the ring
    Fantasia                                         Star wars: Episode VI - return of the jedi

    1/10, movie: The lion king

8) A sweeping historical drama following a brilliant but conflicted scientist whose groundbreaking work forever changes the course of history. As he helps create a nuclear weapon during world war 2.
    Answer ML 1-10:                                  Answer LLM 1-10:
    The message                                      The imitation game
    Forrest Gump                                     Schindler's list
    Blowup                                           Saving private Ryan
    Saving private Ryan                              Dunkirk
    La dolce vita                                    The longest day
    Avatar                                           Das boot
    Secrets & lies                                   Empire of the sun
    Citizen kane                                     Enemy at the gates
    Dawn of the dead                                 The thin red line
    Beasts of no nation                              The boy in the striped pyjamas

    1/10, movie: Oppenheimer

9) A movie directed by Steven Spielberg that is about a remote island where cutting-edge science brings long extinct creatures back to life. What begins as a wonder of human ingenuity quickly turns into a fight for survival as the dinosaurs break free from control.
    Answer ML 1-10:                                  Answer LLM 1-10:
    White heat                                       Jurassic park
    Gegen die wand                                   Jaws
    Kis Uykusu                                       E.T. the extra-terrestrial
    Psycho                                           Close encounters of the third kind
    8 1/2                                            Minority report
    The secret of kells                              Raiders of the lost ark
    Dances with wolves                               Indiana Jones and the last crusade
    Lost in translation                              Empire of the sun
    Il buono, il brutto, il cattivo                  Saving private Ryan
    The purple rose of cairo                         Bridge of Spies

    0/10, movie: Jurassic park

10) A survival drama set in the harsh, unforgiving wilderness, in the early 1800s. It follows a frontiersman, played by Leonardo DiCaprio, who is left for dead after a brutal bear attack. Driven by pain, revenge, and the will to survive, he sets of on a relentless quest for justice.
    Answer ML 1-10:                                  Answer LLM 1-10:
    Interstellar                                     The revenant
    The man who would be king                        The last of the mohicans
    The revenant                                     Dances with wolves
    Gravity                                          The outlaw josey
    Empire of the sun                                Django Unchained
    The pianist                                      The searchers
    Hotaru no haka                                   Unforgiven
    The bourne supremacy                             True grit
    Fantastic Mr.fox                                 Life of PI
    Gladiator                                        Apocalypto

    1/10, movie: The revenant
'''
