# fix_config.py
# Sistema config.yml, admin/index.html, _redirects e crea uploads/.gitkeep
# per usare Decap CMS con Netlify Identity + Git Gateway.

from pathlib import Path
import shutil
import sys
import textwrap

ROOT = Path(__file__).parent.resolve()

# ---- Contenuti target --------------------------------------------------------

CONFIG_YML = textwrap.dedent("""\
  backend:
    name: git-gateway
    branch: main

  media_folder: "uploads"
  public_folder: "/uploads"

  collections:
    - name: "news"
      label: "News"
      folder: "data/news"
      create: true
      slug: "{{slug}}"
      fields:
        - { label: "Titolo", name: "title", widget: "string" }
        - { label: "Data", name: "date", widget: "datetime" }
        - { label: "Corpo", name: "body", widget: "markdown" }
""")

ADMIN_INDEX_HTML = textwrap.dedent("""\
  <!doctype html>
  <html lang="it">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Area Amministrazione</title>

      <!-- Decap CMS -->
      <script src="https://unpkg.com/decap-cms@^3.1.9/dist/decap-cms.js"></script>

      <!-- Netlify Identity widget -->
      <script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
      <style>
        body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif;margin:0}
      </style>
    </head>
    <body>
      <script>
        // Se Identity è presente, assicuriamoci che dopo il login si resti su /admin/
        if (window.netlifyIdentity) {
          window.netlifyIdentity.on("init", user => {
            if (!user) {
              window.netlifyIdentity.on("login", () => {
                document.location.href = "/admin/";
              });
            }
          });
        }
      </script>
    </body>
  </html>
""")

REDIRECTS = textwrap.dedent("""\
  # SPA rule for Decap CMS admin
  /admin/*   /admin/index.html   200
""")

# -----------------------------------------------------------------------------

def backup(path: Path):
    if path.exists() and path.is_file():
        bak = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, bak)
        print(f"[backup] Creato {bak.name}")

def write_if_changed(path: Path, content: str):
    if path.exists() and path.read_text(encoding="utf-8").strip() == content.strip():
        print(f"[skip] {path} è già aggiornato")
        return
    backup(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"[write] Aggiornato {path}")

def ensure_gitkeep(dirpath: Path):
    dirpath.mkdir(parents=True, exist_ok=True)
    gitkeep = dirpath / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")
        print(f"[create] {gitkeep}")
    else:
        print(f"[skip] {gitkeep} esiste già")

def main():
    # 1) config.yml
    write_if_changed(ROOT / "config.yml", CONFIG_YML)

    # 2) admin/index.html
    write_if_changed(ROOT / "admin" / "index.html", ADMIN_INDEX_HTML)

    # 3) _redirects
    write_if_changed(ROOT / "_redirects", REDIRECTS)

    # 4) uploads/.gitkeep
    ensure_gitkeep(ROOT / "uploads")

    print("\n✅ Fatto! Ora esegui:")
    print("   git add .")
    print('   git commit -m "Setup Decap CMS con Netlify Identity + Git Gateway"')
    print("   git push")
    print("\nPoi su Netlify:")
    print(" - Site settings → Identity → Abilita Identity (se non è attivo)")
    print(' - Identity → Settings → "Enable Git Gateway"')
    print(" - Identity → Invite users → invita la tua email per accedere al CMS")
    print("\nAccedi al CMS su: https://<tuo-sito>.netlify.app/admin/")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        sys.exit(1)
