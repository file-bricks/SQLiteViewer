# Security Policy / Sicherheitsrichtlinie

## English

### Reporting a Vulnerability

If you find a security vulnerability, please report it responsibly:

1. **Do NOT open a public issue**
2. **Use GitHub's [Private Vulnerability Reporting](https://github.com/file-bricks/SQLiteViewer/security/advisories/new)**
3. Include: description, steps to reproduce, potential impact

### How to Report

1. Open: https://github.com/file-bricks/SQLiteViewer/security/advisories/new
2. Fill out the report form (title, description, severity, affected versions)
3. Submit privately (not visible to the public until coordinated disclosure)

### Security Response SLAs

- **48-Hour Acknowledgment SLA:** Initial receipt acknowledgment within 48 hours.
- **5-Business-Day Triage SLA:** Preliminary impact and triage assessment within 5 business days.

### Verified Security Contacts

If GitHub Private Vulnerability Reporting is unavailable, contact verified maintainers directly:
- `security@open-bricks.org`
- `security@ellmos.ai`
- `support@lukasgeiger.com`
- `lukas@open-bricks.org`

### Scope

- Local database file parsing (`.db`, `.sqlite`, `.sqlite3`)
- SQL query execution and validation
- Atomic export transactions (CSV, structured JSON)
- Offline web companion sandbox

---

## Deutsch

### Sicherheitslücken melden

Bitte melden Sie Sicherheitslücken verantwortungsvoll:

1. **Kein öffentliches Issue erstellen**
2. **GitHub Private Vulnerability Reporting verwenden:**
   https://github.com/file-bricks/SQLiteViewer/security/advisories/new
3. Beschreibung, Reproduktionsschritte und mögliche Auswirkungen angeben

### Vorgehensweise bei Meldungen

1. Öffnen Sie: https://github.com/file-bricks/SQLiteViewer/security/advisories/new
2. Tragen Sie Titel, Beschreibung, Schweregrad und betroffene Versionen ein
3. Reichen Sie die Meldung privat ein (wird erst nach koordinierter Behebung öffentlich)

### Reaktionszeiten & SLAs

- **48-Stunden-Eingangsbestätigung:** Erste Eingangsbestätigung innerhalb von 48 Stunden.
- **5-Werktage-Triage-Zusage:** Erste Schwachstellenbewertung und Priorisierung innerhalb von 5 Werktagen.

### Verifizierte Sicherheitskontakte

Falls GitHub Private Vulnerability Reporting nicht erreichbar ist:
- `security@open-bricks.org`
- `security@ellmos.ai`
- `support@lukasgeiger.com`
- `lukas@open-bricks.org`

### Geltungsbereich

- Lokaler Dateisystem- und Datenbankzugriff (`.db`, `.sqlite`, `.sqlite3`)
- SQL-Ausführung und Befehlsvalidierung
- Atomare Exporttransaktionen (CSV, JSON)
- Vollständig lokaler Betrieb ohne Netzwerkanbindung
