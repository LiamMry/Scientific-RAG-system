import json
import arxiv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT_DIR / "data/raw/pdf"
MTD_DIR = ROOT_DIR / "data/raw/metadata"

def search_and_process(query: str, max_results: int = 20, pdf_dir: Path = PDF_DIR, mtd_dir: Path = MTD_DIR):

    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    for result in client.results(search):

        short_id = result.get_short_id()
        metadata_path = mtd_dir / f"{short_id}.json"

        # If metadata exists, load metadata
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text())

        # Else declare empty metadata
        else :
            metadata = {
                "id": result.get_short_id(), 
                "downloaded": False, 
                "parsed": False, 
                "embedded": False
                }

        # Download pdf
        if metadata["downloaded"] == False:
            result.download_pdf(dirpath=str(pdf_dir), filename=f"{short_id}.pdf")
            metadata["downloaded"] = True

        # Write back metadata
        metadata_path.write_text(json.dumps(metadata, indent=2))
        

if __name__ == "__main__":
    search_and_process(query="diffusion models", max_results=10)
