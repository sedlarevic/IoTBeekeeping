from flask import Flask, jsonify
from flask_cors import CORS
import skripta as dst_modul

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    #fale linkovi sa raspberry-ja
    odg = """
    link za podatke 
    link za celzijus
    link za vlaznost
    link za co2_ppm 
    """
    return odg

@app.route('/podaci')
def podaci():
    try:
        podaci=dst_modul.podaci()
        return jsonify(podaci)
    except RuntimeError as error:
        print(error.args[0])
        return jsonify({"poruka": "Podaci nisu poslati", "error": error.args[0]})

@app.route('/celzijus')
def celzijus():
    try:
        celzijus=dst_modul.celzijus()
        return jsonify(celzijus)
    except RuntimeError as error:
        print(error.args[0])
        return jsonify({"poruka": "Podaci nisu poslati", "error": error.args[0]})

@app.route('/vlaznost')
def vlaznost():
    try:
        vlaznost=dst_modul.vlaznost()
        return jsonify(vlaznost)
    except RuntimeError as error:
        print(error.args[0])
        return jsonify({"poruka": "Podaci nisu poslati", "error": error.args[0]})

@app.route('/co2_ppm')
def co2_ppm():
    try:
        co2_ppm=dst_modul.co2_ppm()
        return jsonify(co2_ppm)
    except RuntimeError as error:
        print(error.args[0])
        return jsonify({"poruka": "Podaci nisu poslati", "error": error.args[0]})

if __name__==("__main__"):
    app.run(debug=True, host="0.0.0.0") #pokretanje aplikacije na IP adresi RPi-a