# neo4j-exercise

API REST in **FastAPI** che si connette a un database **Neo4j** per gestire studenti e corsi.

## Prerequisiti

- Python 3.14+ installato
- Un'istanza Neo4j attiva e raggiungibile (locale o remota)

> Non serve il `.venv` condiviso: ognuno si crea il proprio (vedi sotto).

## Configurazione connessione

L'app legge le credenziali da variabili d'ambiente, con questi default:

| Variabile        | Default                     |
| ---------------- | --------------------------- |
| `NEO4J_URI`      | `neo4j://localhost:7687`    |
| `NEO4J_USER`     | `neo4j`                     |
| `NEO4J_PASSWORD` | `password`                  |

Se la tua istanza usa altri valori, esportale prima di avviare l'app, ad esempio (PowerShell):

```powershell
$env:NEO4J_URI = "neo4j://localhost:7687"
$env:NEO4J_USER = "neo4j"
$env:NEO4J_PASSWORD = "lapassworddella-tua-istanza"
```

## Setup

```powershell
# 1. Clona la repo
git clone https://github.com/FranDeSa456/neo4j.git
cd neo4j

# 2. Crea e attiva un virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Installa le dipendenze
pip install -r requirements.txt
```

## Avvio

```powershell
uvicorn main:app --reload
```

L'app si connette a Neo4j allo startup (verifica la connettività) e serve su http://127.0.0.1:8000.

La documentazione interattiva è disponibile su http://127.0.0.1:8000/docs

## Endpoint

| Metodo   | Path                        | Descrizione                             |
| -------- | --------------------------- | --------------------------------------- |
| `GET`    | `/students`                 | Lista tutti gli studenti                |
| `GET`    | `/students/{name}`          | Dettaglio di uno studente               |
| `POST`   | `/students`                 | Crea uno studente (body: `name`, `age`) |
| `DELETE` | `/students/{name}`          | Elimina uno studente                    |
| `GET`    | `/courses`                  | Lista tutti i corsi                     |
| `POST`   | `/courses`                  | Crea un corso (body: `name`, `hours`)   |
| `DELETE` | `/courses/{name}`           | Elimina un corso                        |
| `GET`    | `/courses/{course}/students`| Studenti iscritti a un corso            |
| `POST`   | `/courses/{course}/students/{name}`  | Iscrivi uno studente a un corso |
| `DELETE` | `/courses/{course}/students/{name}`  | Rimuovi l'iscrizione            |
