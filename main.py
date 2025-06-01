from playwright.sync_api import sync_playwright
import time
from datetime import datetime, timedelta
import re

DIVIDER = "=" * 30
# --- ÚDAJE K VYPLNĚNÍ ---
JMENO = None
CISLO_DOKLADU = None
CLENSKE_ID = None  # nebo None, pokud nemáš
DIVIZE = None  # bude vybráno v dropdownu
URL = None
LOGIN = None
HESLO = None
DATUM_CAS_REGISTRACE = None
SQUAD = None

# --- SELEKTORY (uprav dle potřeby) ---
SELECTOR_TLACITKO_PRIHLASIT = r"body > div.min-h-screen.bg-gray-100.dark\:bg-gray-900 > nav > div.max-w-7xl.mx-auto.px-4.md\:px-6.lg\:px-8 > div > div.hidden.space-x-1.items-center.md\:-my-px.md\:ml-10.md\:flex > button.inline-flex.items-center.px-1.border-b-2.border-transparent.text-sm.font-medium.leading-5.text-gray-500.dark\:text-gray-400.hover\:text-gray-700.dark\:hover\:text-gray-300.hover\:border-gray-300.dark\:hover\:border-gray-700.focus\:outline-none.focus\:text-gray-700.dark\:focus\:text-gray-300.focus\:border-gray-300.dark\:focus\:border-gray-700.transition.duration-150.ease-in-out"  # tlačítko pro zobrazení login formuláře
SELECTOR_INPUT_LOGIN = r"#login"
SELECTOR_INPUT_HESLO = r"#password"
SELECTOR_TLACITKO_LOGIN = r"body > div.fixed.inset-0.overflow-y-auto.px-4.py-6.sm\:px-0.z-2000 > div.mb-6.bg-white.dark\:bg-gray-800.rounded-lg.overflow-hidden.shadow-xl.transform.transition-all.sm\:w-full.sm\:max-w-md.sm\:mx-auto > div > form > div.flex.items-center.justify-end.mt-4 > button"

SELECTOR_INPUT_JMENO = r"#username"
SELECTOR_INPUT_DOKLAD = r"#licenceid"
SELECTOR_CHECKBOX_CLEN = r"#lexmember"
SELECTOR_INPUT_CLENSKE_ID = r"#lexhash"
SELECTOR_SELECT_DIVIZE = r"#contest_division_id"
SELECTOR_SQUAD = f"#squad-{SQUAD}"
SELECTOR_CHECKBOX_GDPR = r"#gdpr"
SELECTOR_TLACITKO_REGISTRACE = r"#regform > div.flex.flex-col.items-center.justify-center > button"

def get_doklad():
    zp = input('Zadej číslo ZP ve formátu "ZP123456": ').strip()
    return zp

def get_LEX():
    print("Zadej kontrolní kód členství LEX (CASE SENSITIVE).")
    print("Pokud nejsi členem LEX, ponech pole prázdné!")
    lex = input("Kontrolní kód: ").strip()
    if lex == "":
        return None
    else:
        return lex
    
def get_divize():
    divi = input('Zadej divizi.\n(Přesně tak, jak se ukazuje v drop-down menu na stránkách LEXu,\nnapř. "Optik/ Kompaktní pistole")\n(CASE SENSITIVE)\nDivize: ').strip()
    return divi

def get_zavod():
    while True:
        zavod = input('Zadej URL závodu ve formátu "https://www.loslex.cz/contest/353": ').strip()
        if re.match(r"^https://www\.loslex\.cz/contest/\d+$", zavod):
            return zavod
        else:
            print("❌ Neplatná URL. Ujisti se, že začíná na https://www.loslex.cz/contest/ a končí číslem.")

def get_user():
    while True:
        usr = input('Zadej uživatelské jméno pro přihlášení (email): ').strip()
        if re.match(r"^[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", usr):
            return usr
        else:
            print("❌ Neplatná e-mailová adresa. Zkus to znovu.")

def get_pwd():
    pwd = input('Zadej heslo: ').strip()
    return pwd

def get_regtime():
    while True:
        reg = input('Zadej začátek registrace ve formátu "RRRR-MM-DD hh:mm:ss": ').strip()
        try:
            datetime.strptime(reg, "%Y-%m-%d %H:%M:%S")
            return reg
        except ValueError:
            print("❌ Nesprávný formát. Zkus to znovu.")

def get_squad():
    while True:
        sq = input("Zadej číslo squadu: ").strip()
        if sq.isdigit():
            global SELECTOR_SQUAD
            SELECTOR_SQUAD = f"#squad-{sq}"
            return sq
        else:
            print("❌ Zadej pouze číslo squadu (např. 1, 3, 5).")

def registrace():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL)


        try:
            cas_registrace = datetime.strptime(DATUM_CAS_REGISTRACE, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("❌ DATUM_CAS_REGISTRACE má špatný formát.")
            return

        cas_prihlaseni = cas_registrace - timedelta(seconds=30)

        print(f"⏳ Čekám na čas přihlášení: {cas_prihlaseni}")
        while datetime.now() < cas_prihlaseni:
            time.sleep(0.1)

        # Přihlášení
        print("🔐 Přihlašuji se...")
        page.click(SELECTOR_TLACITKO_PRIHLASIT)
        page.wait_for_selector(SELECTOR_INPUT_LOGIN)
        page.fill(SELECTOR_INPUT_LOGIN, LOGIN)
        page.fill(SELECTOR_INPUT_HESLO, HESLO)
        page.click(SELECTOR_TLACITKO_LOGIN)

        cilovy_cas = cas_registrace + timedelta(seconds=0.5)
        print(f"⏳ Čekám na čas registrace: {cilovy_cas}")
        while datetime.now() < cilovy_cas:
            time.sleep(0.05)

        # Refresh
        print("🔄 Refreshuji stránku...")
        page.reload()
        page.wait_for_load_state("load")

        page.wait_for_selector(SELECTOR_TLACITKO_REGISTRACE)
        # Společná část registrace
        page.fill(SELECTOR_INPUT_DOKLAD, CISLO_DOKLADU)

        if CLENSKE_ID:
            page.check(SELECTOR_CHECKBOX_CLEN)
            page.fill(SELECTOR_INPUT_CLENSKE_ID, CLENSKE_ID)

        page.select_option(SELECTOR_SELECT_DIVIZE, label=DIVIZE)
        page.click(SELECTOR_SQUAD)
        page.check(SELECTOR_CHECKBOX_GDPR)
        # page.click(SELECTOR_TLACITKO_REGISTRACE)

        print("✅ Registrace dokončena.")
        input("Stiskni ENTER pro zavření browseru a ukončení aplikace...")
        # browser.close()  # nech otevřené pro kontrolu

# --- SPUŠTĚNÍ ---
if __name__ == "__main__":
    proceed = False
    while not proceed:
        print(DIVIDER)
        CISLO_DOKLADU = get_doklad()
        print(DIVIDER)
        CLENSKE_ID = get_LEX()
        print(DIVIDER)
        DIVIZE = get_divize()
        print(DIVIDER)
        SQUAD = get_squad()
        print(DIVIDER)
        URL = get_zavod()
        print(DIVIDER)
        LOGIN = get_user()
        print(DIVIDER)
        HESLO = get_pwd()
        print(DIVIDER)
        DATUM_CAS_REGISTRACE = get_regtime()
        print(DIVIDER)
        print("Budou použity následující údaje:")
        print(f"""
        Číslo ZP: {CISLO_DOKLADU}\n
        LEX ID: {CLENSKE_ID}\n
        Divize: {DIVIZE}\n
        Squad: {SQUAD}\n
        URL závodu: {URL}\n
        Login: {LOGIN}\n
        Heslo: {HESLO}\n
        Datum a čas registrace: {DATUM_CAS_REGISTRACE}
        """)
        print(DIVIDER)
        oprava = input("Pokud si přeješ údaje zadat znovu, napiš A a stiskni enter.\nKterákoliv jiná volba spustí v daný čas registraci.: ").upper()
        if oprava != "A":
            proceed = True
        print(f"\n{DIVIDER}\n")
    registrace()