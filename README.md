# NAO-Planning-Challenge

Progetto di intelligenza artificiale per la generazione di una coreografia robotica per il robot umanoide NAO, sviluppato per il corso di **Fondamenti di Intelligenza Artificiale** dell'Università di Bologna.

## Informazioni sul progetto

- **Team:** NAOgraphy
- **Partecipanti:**
  - Giulia Gianasi — [giulia.gianasi@studio.unibo.it](mailto:giulia.gianasi@studio.unibo.it)
  - Francesco Imperato — [francesco.imperato2@studio.unibo.it](mailto:francesco.imperato2@studio.unibo.it)
- **Repository:** [NAO-Planning-Challenge](https://github.com/giuliagianasi/NAO-Planning-Challenge.git)
- **Canzone:** Daft Punk — *The Son of Flynn* (*TRON: Legacy*)

## Librerie e requisiti

- **Python 3** con `numpy` (installabile tramite `pip install -r requirements.txt`): serve per `search.py` e `utils.py` del laboratorio (AIMA), utilizzati per pianificare la coreografia.
- **Python 2.7** con NAOqi: esegue le posizioni contenute nella cartella `NaoMoves/`, come nei file forniti durante il corso.
  - **Windows:** è disponibile quello incluso in Choregraphe 2.8 (`C:\Program Files (x86)\Softbank Robotics\Choregraphe Suite 2.8`); `main.py` lo individua automaticamente.
- **Musica sul PC:** viene riprodotta tramite `winsound` (Windows, incluso in Python), `afplay` (macOS) oppure `aplay` (Linux).

## Come testare il NAO simulato

1. Aprire Choregraphe con il robot virtuale NAO.

   Nelle preferenze impostare:
   - **Edit > Preferences > Virtual Robot**
   - **Robot model:** `NAO H25`
   - **Motor speed:** `100%`

   Nella stessa finestra è indicata la porta utilizzata, con la dicitura `NAOqi state: Running on port XXXXX`.

2. Avviare il programma usando il comando adatto al proprio ambiente:

   **Windows**
   ```bat
   avvia_windows.bat XXXXX
   ```
   In alternativa, fare doppio clic su `avvia_windows.bat` e inserire la porta quando richiesto.

   **VM / Linux**
   ```bash
   python3 main.py 127.0.0.1 XXXXX
   ```

3. `main.py` stampa il piano trovato con A*, porta il NAO in `StandInit` e avvia la canzone sul PC insieme alla coreografia nella finestra 3D di Choregraphe.

### Altre modalità di esecuzione

- **Solo piano, senza robot:**
  ```bash
  python3 main.py --solo-piano
  ```
- **Confronto tra strategie (reporting.py):**
  ```bash
  python3 main.py --report
  ```
- **Senza musica:** aggiungere l'opzione `--no-music` al comando di avvio.

> **Nota:** il robot simulato non può riprodurre musica. La canzone (`music/son_of_flynn.wav`) viene riprodotta dal PC.

## Struttura del repository

| File / cartella | Descrizione |
|---|---|
| `main.py` | Dati della coreografia, pianificazione (A*) ed esecuzione. |
| `nao_problem.py` | Classe `NaoProblem` (sottoclasse di `Problem`) e classe `NaoMove`. |
| `search.py`, `utils.py` | Libreria AIMA usata in laboratorio (non modificata). |
| `reporting.py` | `path_actions` e report del laboratorio (non modificato). |
| `nao_tools.py` | Script Python 2: prepara il robot e cambia il colore degli occhi. |
| `misura_tempi.py` | Misura la durata di ogni posizione sul robot virtuale. |
| `avvia_windows.bat` | Avvia `main.py` su Windows. |
| `NaoMoves/` | File delle posizioni (Python 2). |
| `music/` | File della canzone. |
