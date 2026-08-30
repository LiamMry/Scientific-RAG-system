import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT_DIR / "data/raw/pdf"
MTD_DIR = ROOT_DIR / "data/raw/metadata"
TEI_DIR = ROOT_DIR / "data/raw/tei"
CLN_DIR = ROOT_DIR / "data/processed"

def clean_all(tei_dir : Path = TEI_DIR, cln_dir : Path = CLN_DIR):

    cln_dir.mkdir(parents=True, exist_ok=True)

    for json_path in tei_dir.glob("*.json"):
        data = json.loads(json_path.read_text())
        data = clean(data)

        cln_path = cln_dir / json_path.name
        cln_path.write_text(json.dumps(data, indent=2))


def clean(data : dict) -> dict:

    section = {}
    for k in range(len(data['body_text'])):
        try:
            section_name = data['body_text'][k]["head_section"]

            if section_name not in section:
                section[data['body_text'][k]["head_section"]] = data['body_text'][k]["text"]
            else:
                section[data['body_text'][k]["head_section"]] = section[data['body_text'][k]["head_section"]] + " " + data['body_text'][k]["text"]
        except:
            pass

    cleaned_data = {'title': data['biblio']['title'],
             'authors': data['biblio']['authors'],
             'abstract': data['biblio']['abstract'][0]['text'],
             'section': section,
            }

    return cleaned_data

if __name__ == "__main__":
    clean_all()