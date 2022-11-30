from flask import Flask, request, jsonify
from app.RejestrKont import RejestrKont
from app.Konto import Konto
app = Flask(__name__)


@app.route("/konta/stworz_konto", methods=['POST'])
def stworz_konto():
    dane = request.get_json()
    if (RejestrKont.searchUser(dane.get('pesel')) != None):
        return "Konto o podanym numerze PESEL już istnieje", 409
    if (dane.get('imie') and dane.get('nazwisko') and dane.get('pesel')):
        print(f"Request o stworzenie konta z danymi: {dane}")
        konto = Konto(dane["imie"], dane["nazwisko"], dane["pesel"])
        RejestrKont.addUser(konto)
        return jsonify("Konto stworzone"), 201
    return "Niepoprawne dane!", 400


@app.route("/konta/ile_kont", methods=['GET'])
def ile_kont():
    return jsonify(RejestrKont.usersCount()), 200


@app.route("/konta/konto/<pesel>", methods=['GET'])
def wyszukaj_konto_z_peselem(pesel):
    if (RejestrKont.searchUser(pesel) == None):
        return jsonify("Nie znaleziono konta!"), 404

    else:
        return jsonify(RejestrKont.searchUser(pesel).__dict__), 200
