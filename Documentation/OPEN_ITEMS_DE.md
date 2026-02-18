# Offene Optimierungen (Status)

Dieses Dokument beantwortet: **„Was steht noch aus?“**

## Bereits umgesetzt
- Shell-Härtung in zentralen Pfaden (`subprocess` statt `os.system`) für Transfer/Update.
- Zentraler HTTP-Client mit Retry/Backoff + Session-Reuse.
- `Requests_Search` mit robuster Fehlerbehandlung und reduzierter Duplikatlogik.
- Atomare JSON-Schreibvorgänge für Such-Ergebnisse.
- Konfigurations-Bugs bei `os.path.isfile(nomefile)` korrigiert.
- Doku-Härtung: keine harten Default-Credentials mehr in README.

## Noch offen (priorisiert)

### 1) Security (hoch)
1. **Passwort-Hashing für GUI-Login einführen**
   - Aktuell sind Credential-Flows dateibasiert.
   - Ziel: Hash (Argon2/Bcrypt) statt Klartextvergleich.
2. **API-Key/SMTP-Secrets über `.env` + Loader**
   - Derzeit weiterhin dateibasierte Konfiguration.
3. **Update-Integrität**
   - Signaturen/Checksums für Releases prüfen.

### 2) Data Integrity
1. **Schema-/DTO-Validierung zentralisieren**
   - Einheitliche Validierung für Input/Output (z. B. Pydantic).
2. **Deterministisches Fehlerobjekt**
   - Einheitliches Format: `status`, `code`, `message`, `details`.

### 3) Performance
1. **HTTP-Client in weitere Module ausrollen**
   - Noch viele direkte `requests.get(...)`-Aufrufe in Scrapern.
2. **Parallelisierung I/O-lastiger Checks**
   - Konfigurierbare Worker-Limits + Backoff pro Host.

### 4) Qualitätssicherung
1. **Tests ergänzen**
   - Unit-Tests für Konfig-/Update-/Datei-Schreibpfade.
2. **Static Checks standardisieren**
   - Lint + Security-Checks als fester CI-Job.

## Empfohlene Reihenfolge (nächste 2 Sprints)
- **Sprint 1:** Passwort-Hashing, `.env`-Secret-Loader, DTO/Error-Contract.
- **Sprint 2:** HTTP-Client-Migration in alle Scraper, Parallelisierung, Tests + CI.
