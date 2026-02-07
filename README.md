# Large Neighborhood Search za CVRP

## O projektu

Ovaj projekat implementira i poredi Basic LNS i Adaptive LNS metaheuristike za rešavanje Capacitated Vehicle Routing Problem (CVRP). CVRP je problem određivanja optimalnih ruta za vozila koja dostavljaju robu korisnicima, uz ograničenje kapaciteta vozila.

## Problem

Capacitated Vehicle Routing Problem (CVRP):
- Imamo skladište (depot) i skup korisnika sa potražnjama
- Vozila imaju ograničen kapacitet
- Cilj: minimizovati ukupnu pređenu udaljenost svih vozila

## Funkcionalnosti

**Implementirani algoritmi:**
- Basic LNS - koristi fiksnu kombinaciju destroy/repair operatora
- Adaptive LNS - dinamički bira najbolje operatore tokom izvršavanja

**Destroy metode:**
- Random Destroy - nasumično uklanjanje korisnika
- Worst Destroy - uklanjanje najskupljih korisnika
- Related Destroy - uklanjanje sličnih korisnika
- Worst Route Destroy - uklanjanje dela najgore rute

**Repair metode:**
- Greedy Repair - ubacivanje korisnika na najjeftiniju poziciju
- Regret Repair - prioritet korisnicima sa najvećim "žaljenjem"

**Accept funkcija:**
- Simulated Annealing - prihvata i lošija rešenja kako bi izbegao lokalne optimume

## Struktura projekta

```
.
├── src/
│   ├── cvrp/          # CVRP problem i rešenje
│   ├── lns/           # Basic i Adaptive LNS
│   ├── destroy/       # Destroy operatori
│   ├── repair/        # Repair operatori
│   ├── accept/        # Accept funkcija
│   ├── gui/           # Grafički interfejs
│   └── main.py        # Pokretanje aplikacije
├── analytics/         # Analiza rezultata
├── instances/         # CVRP test instance
├── Dokumentacija_Projekta.txt
├── requirements.txt
└── README.md
```

## Instalacija

1. Kreirajte virtualno okruženje:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instalirajte zavisnosti:

```bash
pip install -r requirements.txt
```

## Pokretanje

Pokrenite GUI aplikaciju:

```bash
./run.sh
```

ili direktno:

```bash
python src/main.py
```

Ili koristite analytics notebook za testiranje i analizu:

```bash
jupyter notebook analytics/analytics.ipynb
```

## Test instance

Projekat koristi Set A instance iz CVRP biblioteke:
- Instance variraju od 32 do 80 čvorova
- Svaka instanca ima poznato optimalno rešenje
- Link: [CVRPLIB](https://galgos.inf.puc-rio.br/cvrplib/index.php/en/instances)

## Rezultati

Detaljni rezultati testiranja na Set A instancama, analiza performansi i poređenje Basic i Adaptive LNS algoritama dostupni su u:
- `analytics/analytics.ipynb` - eksperimentalna analiza i grafici
- `Dokumentacija_Projekta.txt` - zaključci i preporuke

## Dokumentacija

TODO

## Zavisnosti

- Python 3.10+
- numpy
- matplotlib
- pandas
- tsplib95

## Reference

Projekat je zasnovan na radu:
- Shaw, P. (1998) - LNS pristup
- Pisinger & Røpke (2007) - Adaptive LNS
- CVRPLIB benchmark instance

Detaljan spisak referenci dostupan u dokumentaciji.

## Autori

Matija Stanković

Mateja Milošević
