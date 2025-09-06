from pathlib import Path

yml = """backend:
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
"""

Path("admin/config.yml").write_text(yml, encoding="utf-8")
print("✅ admin/config.yml aggiornato per Netlify Identity (git-gateway).")
