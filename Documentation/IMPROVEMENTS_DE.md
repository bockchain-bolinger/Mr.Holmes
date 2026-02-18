# Verbesserungsvorschläge für Mr.Holmes

Dieses Dokument priorisiert konkrete Verbesserungen für **Security > Data Integrity > Performance > UX > Feature-Umfang**.

## 1) Security-First (höchste Priorität)

### 1.1 Standard-Credentials entfernen und Onboarding erzwingen
- Problem: In der Doku sind Default-Zugangsdaten dokumentiert.
- Risiko: Jede unveränderte Installation ist direkt angreifbar.
- Umsetzung:
  - Beim ersten Start Pflicht zur Erstellung eines eigenen Admin-Users.
  - Passwort-Hashing (Argon2id/Bcrypt) statt Klartext.
  - Optional: Login-Lockout + einfache Rate-Limits.

### 1.2 Secrets aus Dateien in sicheres Secret-Handling überführen
- Problem: API-Key/SMTP-Konfig ist dateibasiert und eher manuell.
- Umsetzung:
  - `.env` + Secret-Loader (mit Fallback auf interaktive Eingabe).
  - Konfig-Dateien nur für nicht-sensitive Defaults.
  - Beispiel-Template bereitstellen (`.env.example`).

### 1.3 Shell-Aufrufe hart absichern
- Problem: Mehrere `os.system(...)` Aufrufe für PHP-Server, Update, Kill-Prozesse.
- Risiko: Command-Injection und schwer kontrollierbares Fehlerverhalten.
- Umsetzung:
  - Auf `subprocess.run([...], check=True)` mit Argumentlisten migrieren.
  - Keine String-Konkatenation bei Kommandos.
  - Rückgabecodes + Fehlerklassen einheitlich behandeln.

### 1.4 Update-Prozess signieren/verifizieren
- Problem: `git clone` ohne Integritätsprüfung.
- Umsetzung:
  - Versionierte Releases mit Checksums/Signaturen.
  - Update nur auf erlaubte Versionen/Channels.
  - Rollback sauber (atomarer Wechsel statt direktes Überschreiben).

## 2) Data Integrity & Robustheit

### 2.1 Konfigurationslogik hardenen
- Problem: `if os.path.isfile:` (ohne Argument) führt in zwei Methoden zu fehleranfälligem Verhalten.
- Umsetzung:
  - Korrektur auf `os.path.isfile(nomefile)`.
  - Unit-Tests für alle `modify_*`-Pfadfälle.

### 2.2 Typed Contract First für Input/Output
- Problem: Viele dynamische Datenflüsse (JSON, User-Input, HTTP-Responses) ohne zentrale Validierung.
- Umsetzung:
  - Zentrales Schema-Modul (z. B. Pydantic/Marshmallow).
  - Einheitliche DTOs für Finder-Ergebnisse (username/email/phone/websites).
  - Deterministische Fehlerobjekte (`status`, `code`, `message`, `details`).

### 2.3 Reporting atomar schreiben
- Problem: Häufiges Append/Rewrite ohne atomare Writes.
- Umsetzung:
  - Temp-Datei + `os.replace()`.
  - Konsistentes UTF-8 und JSON-Serializer mit stabiler Struktur.

## 3) Performance & Stabilität

### 3.1 Netzwerk-Client zentralisieren
- Problem: Sehr viele direkte `requests.get(...)` Aufrufe, teils ohne Timeout-Limit.
- Umsetzung:
  - Gemeinsamer HTTP-Client mit:
    - globalem Timeout (z. B. 5–15s)
    - Retry + Exponential Backoff
    - Session-Reuse (Connection Pooling)
    - optionalem per-host Rate Limiting

### 3.2 Concurrency für Site-Checks
- Umsetzung:
  - I/O-lastige Website-Checks parallelisieren (ThreadPool/asyncio).
  - Pro Zielsystem den Request-Strom begrenzen.

### 3.3 Proxy-Strategie observierbar machen
- Umsetzung:
  - Health-Checks für Proxies.
  - Erfolgsquote je Proxy loggen und priorisieren.

## 4) UX/Developer Experience

### 4.1 Fehlerbilder konsistent
- Umsetzung:
  - Zentraler Error-Handler mit Codes und klaren Handlungsempfehlungen.
  - `--debug` Modus für Stacktraces.

### 4.2 CLI modernisieren
- Umsetzung:
  - Migration auf `typer` oder `argparse` mit Subcommands.
  - Nicht-interaktive Runs (`--json`, `--output`, `--proxy`).

### 4.3 Dokumentation professionell strukturieren
- Umsetzung:
  - „Quickstart“, „Secure Setup“, „Troubleshooting“, „Upgrade Guide“.
  - Security-Policy mit Meldeweg + SLA statt nur Mail-Hinweis.

## 5) Vorschlag für Roadmap (realistisch)

### Phase 1 (1–2 Wochen)
- Default-Creds entfernen, Hashing einführen.
- `os.system` kritische Pfade (Update/Transfer/DB) auf `subprocess` migrieren.
- Timeout/Retry für Requests zentral implementieren.
- Konfig-Bugs (`os.path.isfile`) fixen + Tests.

### Phase 2 (2–4 Wochen)
- Einheitliche DTO/Schemas + Error Contract.
- Parallelisierung wichtiger Scraper.
- Strukturierte Logs (JSON) + Basismetriken (Dauer, Fehlerquote).

### Phase 3 (4+ Wochen)
- Plugin-System für neue Quellen.
- Optionales Web-UI/API-Layer mit RBAC.
- Signierte Updates + Release-Kanäle.

## 6) KPI-Set zur Erfolgsmessung
- Mean time to result pro Suchtyp.
- Error-Rate pro Datenquelle.
- Anteil valider Treffer (Precision-Sampling).
- Anzahl Security Findings je Release.
- Crash-Free Runs (%).
