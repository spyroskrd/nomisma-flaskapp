from flask import Flask, render_template, request, jsonify
import requests
from google import genai
import os
from dotenv import load_dotenv

load_dotenv() #η λειτουργια του .env
client = genai.Client(api_key=os.getenv("API-KEY"))

#δινοουμε ενα ονομα στην εφαρμογη.
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    error = None #μεταβλητη error προσωρινα αδεια
    price = None #μεταβλητη price
    converted = None
    currency = None
    crypto = None
    cryptoamount = None
    formattedprice = None
    if request.method == "POST": #αν κανουμε ποστ
        cryptoamount = float(request.form["amount"])
        crypto = request.form["crypto"] #ζητα απο τον χρηστη την μορφη κρυπτο
        currency = request.form["currency"] #και το νομισμα
        url = f"https://api.coinbase.com/v2/prices/{crypto}-{currency}/spot"#απο αυτο το απι
        response = requests.get(url) #παρε τισ πληροοφοριες
        
        if response.status_code == 200: #εαν ολα οκ=200
            data = response.json() #παρε το τζεισον και καντο λιστα data
            price = float(data["data"]["amount"]) #απο τη λιστα data παρε το amount
            converted = price * cryptoamount
            formattedprice = f"{converted:,.2f}"
        else:
            error = "Could not find cryptocurrency. Try again."
    return render_template("index.html", crypto=crypto, cryptoamount=cryptoamount, currency=currency, converted=formattedprice, error=error) #στειλε τις τιμες στο html εχοντας price τη μεταβλητη και currency 

#οταν γινει ποστ ετοιομα στην /τσατ, τρεξε την συναρτηση chat
@app.route("/chat", methods=["POST"])
def chat():
    usermessage = request.json["message"]
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents= f"{usermessage}, ACT AS A HELP BOT ABOUT CRYPTOCURRENCY- NOTHING ELSE. AWNSER SHORT AND NICELY"
    )

    return jsonify({"response": response.text}) #επιστρεφουμε την απαντηση σε json για να εμφανιστει στο frontend.


if __name__ == "__main__": #για να τρεξει η εφαρμογη μονο απευθειας και οχι με εισαγωγη import
    app.run(debug=True)
