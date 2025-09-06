import os
import subprocess

FILES = [
    "admin/config.yml",
    "admin/index.html",
    "_redirects",
    "uploads/.gitkeep"
]

print("=== Verifica file Decap CMS ===")

for f in FILES:
    if os.path.exists(f):
        print(f"\n✅ {f} trovato. Contenuto iniziale:")
        with open(f, "r", encoding="utf-8", errors="ignore") as fh:
            for i, line in enumerate(fh):
                print("   ", line.rstrip())
                if i >= 9:  # Mostra solo i primi 10 righi
                    break
    else:
        print(f"\n❌ {f} NON trovato!")

print("\n=== Stato Git ===")
try:
    result = subprocess.run(
        ["git", "status"], capture_output=True, text=True
    )
    print(result.stdout)
except Exception as e:
    print("Errore git:", e)
