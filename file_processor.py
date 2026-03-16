import csv
import json
import time

class FormatInvalidError(Exception):
    pass

def timer(functie):
    def wrapper(*args, **kwargs):
        start = time.time()
        rezultat = functie(*args, **kwargs)
        durata = time.time() - start
        print(f"{durata}")
        return rezultat
    return wrapper

def log_calls(functie):
    def wrapper(*args, **kwargs):
        print(f"Se apeleaza: {functie.__name__}")
        rezultat = functie(*args, **kwargs)
        print(f"Functia {functie.__name__} a terminat.")
        return rezultat
    return wrapper

@timer
@log_calls
def citeste_csv(fisier):
    with open(fisier, "r") as f:
        rezultate = csv.DictReader(f)
        rezultat = []
        for rand in rezultate:
            rezultat.append(rand)
        return rezultat

@timer
@log_calls
def filtrare(rezultat):
    promovati = [persoana for persoana in rezultat if int(persoana["nota"]) >= 5]
    respinsi = [persoana for persoana in rezultat if int(persoana["nota"]) < 5]
    return promovati, respinsi

@timer
@log_calls
def scor_maxim(rezultat):
    scor = max(int(person["nota"]) for person in rezultat)
    return scor

def scor_mediu(rezultat):
    total = sum(int(person["nota"]) for person in rezultat)
    average = total / len(rezultat)
    return average

def salveaza_json(promovati, respinsi):
    with open("rezultate.json", "w") as f:
        rezultate = {"promovati": promovati, "respinsi": respinsi}
        json.dump(rezultate, f)

if __name__ == "__main__":
    rezultat = citeste_csv("lucrari.csv")
    promovati, respinsi = filtrare(rezultat)
    scor_maxim(rezultat)
    scor_mediu(rezultat)
    salveaza_json(promovati, respinsi)