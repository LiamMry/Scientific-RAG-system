import json
from pathlib import Path
from grobid_client.grobid_client import GrobidClient

ROOT_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT_DIR / "data/raw/pdf"
MTD_DIR = ROOT_DIR / "data/raw/metadata"
TEI_DIR = ROOT_DIR / "data/raw/tei"

def parse(mtd_dir: Path = MTD_DIR, pdf_dir: Path = PDF_DIR, tei_dir: Path = TEI_DIR):

    # Find papers not yet parsed
    unparsed_ids = []
    for metadata_path in mtd_dir.iterdir():
        metadata = json.loads(metadata_path.read_text())
        if not metadata["parsed"]:
            unparsed_ids.append(metadata["id"])

    # If all papers are parsed, return
    if not unparsed_ids:
        return

    pdf_paths = [str(pdf_dir / f"{short_id}.pdf") for short_id in unparsed_ids]

    # Initialize with default localhost server
    client = GrobidClient()

    # Process only the unparsed documents
    client.process_paths(
        service="processFulltextDocument",
        inputs=pdf_paths,
        output=str(tei_dir),
        json_output=True,
    )

    # Mark them as parsed
    for short_id in unparsed_ids:
        metadata_path = mtd_dir / f"{short_id}.json"
        metadata = json.loads(metadata_path.read_text())
        metadata["parsed"] = True
        metadata_path.write_text(json.dumps(metadata, indent=2))

if __name__ == "__main__":

    parse(mtd_dir=MTD_DIR, pdf_dir=PDF_DIR, tei_dir=TEI_DIR)