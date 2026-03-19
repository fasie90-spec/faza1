import json

class PretNegativError(Exception):
    pass


materiale_brute = [
    {"nume": "Ciment", "pret": 35.5, "cantitate": 10},
    {"nume": "Nisip", "pret": 12.0, "cantitate": 0},      
    {"nume": "Fier", "pret": -50.0, "cantitate": 5},      
    {"nume": "Cărămizi", "pret": 4.5, "cantitate": 100}
]

materiale_valide = [produs for produs in materiale_brute if produs["cantitate"] != 0]

print(materiale_valide)


def proceseaza_materiale(lista):
    try:
        rezultate = {}
        for produs in lista:
            if produs["pret"] < 0:
                raise PretNegativError("Pret invalid gasit!")
            else:
                rezultate[produs["nume"]] = produs["pret"] * produs["cantitate"]
        return rezultate
    except PretNegativError as e:
        print(f"Eroare: {e}")
    
def salveaza_json(rezultat):
    with open("rezultate.json", "w") as f:
        json.dump(rezultat, f, indent=4)

date_procesate = proceseaza_materiale(materiale_valide)

if date_procesate: 
    salveaza_json(date_procesate)
    print("Succes! Fisierul rezultate.json a fost creat.")