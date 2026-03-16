# Student Gradebook
import csv
import json

def citeste_csv(fisier):
    with open(fisier, "r") as f:
        studenti = csv.DictReader(f)
        rezultat = []
        for rand in studenti:
            rezultat.append(rand)
        return rezultat

def filtreaza_studenti(studenti):
    # returneaza doi liste: promovati si respinsi
    promovati = [student for student in studenti if int(student["nota"]) >= 5]

    respinsi = [student for student in studenti if int(student["nota"]) < 5]

    return promovati, respinsi

def afiseaza_rezultate(promovati, respinsi):
    print(f"Promovati ({len(promovati)}):")
    for i, student in enumerate(promovati, start=1):
        print(f'{i}. {student["nume"]} - nota {student["nota"]}')

    print(f"Respinsi ({len(respinsi)}):")
    for i, student in enumerate(respinsi, start=1):
        print(f'{i}. {student["nume"]} - nota {student["nota"]}')

def salveaza_json(promovati, respinsi):
    with open("rezultate.json", "w") as f:
        rezultate = {"promovati": promovati, "respinsi": respinsi}
        json.dump(rezultate, f)


if __name__ == "__main__":
    rezultat = citeste_csv("studenti.csv")
    promovati, respinsi = filtreaza_studenti(rezultat)
    afiseaza_rezultate(promovati, respinsi)
    salveaza_json(promovati, respinsi)