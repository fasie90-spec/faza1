import pytest
from file_processor import filtrare, scor_maxim, scor_mediu

studenti = [
    {"nume": "Ana", "varsta": "20", "nota": "9"},
    {"nume": "Ion", "varsta": "22", "nota": "4"},
    {"nume": "Maria", "varsta": "21", "nota": "7"}
]

def test_filtrare_promovati():
    promovati, respinsi = filtrare(studenti)
    assert len(promovati) == 2
    assert len(respinsi) == 1

def test_scor_maxim():
    assert scor_maxim(studenti) == 9
def test_scor_mediu():
    assert scor_mediu(studenti) == pytest.approx(6.67, rel=1e-2)