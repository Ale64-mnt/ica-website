# fix_redirects.py
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
redirects = ROOT / "_redirects"

TEMPLATE = """# Decap CMS / Netlify Identity
/admin/config.yml      /admin/config.yml      200
/.netlify/identity/*   200
/admin/*               /admin/index.html      200
"""

def main():
    if redirects.exists():
        backup = redirects.with_suffix(redirects.suffix + ".bak")
        shutil.copyfile(redirects, backup)
        print(f"Backup creato: {backup.name}")

    redirects.write_text(TEMPLATE, encoding="utf-8")
    print(f"Scritto {redirects.name} con regole consigliate.")
    print("\nContenuto:")
    print(TEMPLATE)

if __name__ == "__main__":
    main()
