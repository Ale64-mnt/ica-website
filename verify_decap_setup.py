# verify_decap_setup.py
from pathlib import Path
import sys
import re

ROOT = Path(__file__).resolve().parent
redirects = ROOT / "_redirects"
config = ROOT / "admin" / "config.yml"
index = ROOT / "admin" / "index.html"

def green(s): return f"\033[92m{s}\033[0m"
def yellow(s): return f"\033[93m{s}\033[0m"
def red(s): return f"\033[91m{s}\033[0m"

def check_redirects():
    print("\n=== Controllo _redirects ===")
    if not redirects.exists():
        print(red("✖ _redirects NON esiste"))
        return False

    content = redirects.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
    print(green("✓ _redirects trovato"))

    # Cattura righe utili (senza commenti)
    lines = [l.strip() for l in content if l.strip() and not l.strip().startswith("#")]

    def line_has(pattern):
        return any(re.search(pattern, l) for l in lines)

    ok = True
    if not line_has(r"^/admin/config\.yml\s+/admin/config\.yml\s+200$"):
        print(red("✖ Manca l’eccezione per /admin/config.yml"))
        ok = False
    else:
        print(green("✓ Eccezione /admin/config.yml presente"))

    if not line_has(r"^/\.netlify/identity/\*\s+200$"):
        print(yellow("• Manca la riga /.netlify/identity/* 200 (consigliata con Identity)"))
    else:
        print(green("✓ /.netlify/identity/* 200 presente"))

    if not line_has(r"^/admin/\*\s+/admin/index\.html\s+200$"):
        print(red("✖ Manca la regola SPA /admin/* /admin/index.html 200"))
        ok = False
    else:
        print(green("✓ Regola SPA /admin/* corretta"))

    # Verifica ordine: config.yml deve venire PRIMA della SPA
    try:
        i_cfg = next(i for i,l in enumerate(lines) if re.search(r"^/admin/config\.yml\s+/admin/config\.yml\s+200$", l))
        i_spa = next(i for i,l in enumerate(lines) if re.search(r"^/admin/\*\s+/admin/index\.html\s+200$", l))
        if i_cfg < i_spa:
            print(green("✓ Ordine corretto: config.yml prima della SPA"))
        else:
            print(red("✖ Ordine errato: /admin/config.yml deve venire PRIMA della regola SPA /admin/*"))
            ok = False
    except StopIteration:
        pass

    return ok

def check_config_yaml():
    print("\n=== Controllo admin/config.yml ===")
    if not config.exists():
        print(red("✖ admin/config.yml NON esiste"))
        return False

    text = config.read_text(encoding="utf-8", errors="ignore")
    print(green("✓ admin/config.yml trovato"))

    required = ["backend:", "media_folder:", "public_folder:"]
    ok = True
    for key in required:
        if key not in text:
            print(red(f"✖ Manca '{key}' in config.yml"))
            ok = False
        else:
            print(green(f"✓ {key} presente"))
    return ok

def check_index_html():
    print("\n=== Controllo admin/index.html ===")
    if not index.exists():
        print(red("✖ admin/index.html NON esiste"))
        return False
    text = index.read_text(encoding="utf-8", errors="ignore")
    ok = True
    if "decap-cms" not in text:
        print(red("✖ Script Decap CMS non rilevato in index.html"))
        ok = False
    else:
        print(green("✓ Script Decap CMS rilevato"))
    return ok

if __name__ == "__main__":
    all_ok = True
    all_ok &= check_redirects()
    all_ok &= check_config_yaml()
    all_ok &= check_index_html()
    print("\n=== Esito ===")
    if all_ok:
        print(green("✔ Setup coerente."))
        sys.exit(0)
    else:
        print(red("✖ Ci sono problemi da correggere."))
        sys.exit(1)
