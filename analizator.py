import csv
import json


def citeste_csv(fisier):
    with open(fisier, "r") as f:
        lucrari = csv.DictReader(f)
        rezultat = []
        for rand in lucrari:
            rezultat.append(rand)
        return rezultat

def afiseaza_lucrari(rezultat):
    for index, lucrare in enumerate(rezultat, start=1):
        print(f"{index}. {lucrare}")

def filtrare_lucrari(rezultat):
    finalizate = [lucrare for lucrare in rezultat if lucrare["status"] == "finalizat"]
    in_asteptare = [lucrare for lucrare in rezultat if lucrare["status"] == "in asteptare"]
    return finalizate, in_asteptare

def calcul_cost(rezultat):
    total = sum(float(lucrare["cost"]) for lucrare in rezultat)
    return total

def aplica_majorare(in_asteptare):
    lucrari_actualizate = [{**lucrare, "cost": int(lucrare["cost"]) * 1.1} for lucrare in in_asteptare]
    return lucrari_actualizate

def raport_final(finalizate, lucrari_actualizate):
    raport = {"finalizate": finalizate, "lucrari actualizate": lucrari_actualizate}
    print(f"Lucrari finalizate ({len(finalizate)}): \n")
    for i, lucrare in enumerate(finalizate, start=1):
        print(f'{i}. Apartament: {lucrare["apt"]} | Tip: {lucrare["tip"]} | Cost: {lucrare["cost"]}')
    print(f"Cost total: {calcul_cost(finalizate)}")

    print(f"Lucrari in asteptare ({len(lucrari_actualizate)}): \n")
    for i, lucrare in enumerate(lucrari_actualizate, start=1):
        print(f'{i}. Apartament: {lucrare["apt"]} | Tip: {lucrare["tip"]} | Cost: {round(lucrare["cost"], 2)}')
    print(f"Cost total: {round(calcul_cost(lucrari_actualizate))}")
    return raport


def salveaza_json(raport):
    with open("raport.json", "w") as f:
        json.dump(raport, f)

if __name__ == "__main__":
    rezultat = citeste_csv("lucrari.csv")
    afiseaza_lucrari(rezultat)
    finalizate, nefinalizate = filtrare_lucrari(rezultat)
    lucrari_actualizate = aplica_majorare(nefinalizate)
    raport = raport_final(finalizate, lucrari_actualizate)
    salveaza_json(raport)
