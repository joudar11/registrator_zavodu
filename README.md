# Automatický registrátor závodů LOS

Tento skript umožňuje automatizovanou registraci na závody. Využívá knihovnu **Playwright**, běží v režimu se zobrazením prohlížeče a podporuje registraci přesně ve stanovený čas.

---

## 🔧 Funkce

- Automatické přihlášení do účtu na stránkách LOSu
- Vyplnění registračního formuláře (číslo ZP, LEX ID, divize, squad)
- Výběr squadu podle zadaného čísla
- Potvrzení GDPR souhlasu
- Registrace ve zvolený čas s přihlášením 30 sekund předem a registrací 0.5 s po čase

---

## ✅ Požadavky

- **Python** 3.8+
- **Playwright** (prohlížečové jádro pro automatizaci)

### Instalace:

```bash
pip install -r requirements.txt
playwright install
```

---

## ▶️ Spuštění skriptu

```bash
python main.py
```

Skript spustí interaktivní rozhraní, kde zadáš:

- číslo zbrojního průkazu (ZP ve formátu `ZP123456`)
- (volitelné) LEX ID
- název divize (např. `Optik/ Kompaktní pistole`)
- číslo squadu
- URL závodu
- e‑mail a heslo pro přihlášení
- (volitelné) čas spuštění registrace (např. `2025-06-01 09:59:30`)

---

## 🔒 Bezpečnost

- Heslo se nikde neukládá
- Skript běží **plně lokálně**
- Není napojen na žádnou databázi ani síť třetí strany

---

## 📄 requirements.txt

```txt
playwright
```

Po instalaci nezapomeň spustit:

```bash
playwright install
```

---

## ✍️ Autor

**Kryštof Klika**  

---

## 🧡 Podpora

Tento nástroj byl vytvořen jako pomůcka pro střelce, kteří chtějí mít jistotu, že registrace na závod proběhne bez zdržení.  
Budu rád za zpětnou vazbu nebo vylepšení skriptu formou pull requestu!
