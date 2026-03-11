lucrari = [
    {"apt": 12, "tip": "zugravit", "cost": 800, "status": "finalizat"},
    {"apt": 45, "tip": "instalatii", "cost": 450, "status": "in_asteptare"},
    {"apt": 12, "tip": "curatenie", "cost": 150, "status": "in_asteptare"},
    {"apt": 78, "tip": "zugravit", "cost": 950, "status": "finalizat"},
    {"apt": 23, "tip": "instalatii", "cost": 300, "status": "in_asteptare"}
]


lucrari_restante = list(filter(lambda lucrare: lucrare["status"] == "in_asteptare", lucrari))
preturi_noi = [n["cost"]*1.1 for n in lucrari_restante]
toate_lucrarile = {rand["tip"] for rand in lucrari}
#factura = {rand["apt"]: rand["cost"] for rand in lucrari}
factura = {}
for lucrare in lucrari:
    if lucrare["apt"] in factura:
        factura[lucrare["apt"]] += lucrare["cost"]
    else:
        factura[lucrare["apt"]] = lucrare["cost"]


for index, (lucrare, pret_nou) in enumerate(zip(lucrari_restante, preturi_noi), start=1):
    print(f"{index}. Apartament {lucrare["apt"]} | {lucrare["tip"]} | Cost: {int(pret_nou)} RON")


