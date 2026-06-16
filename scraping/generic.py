import httpx
import trafilatura
import json
from pathlib import Path
from datetime import datetime


def scrape_url(url: str) -> dict | None:
    """
    Recebe qualquer URL e retorna texto limpo extraído.
    Usa httpx para requisição e trafilatura para extração de texto.
    Retorna None se falhar.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; StartupRadar/1.0)"}
        response = httpx.get(url, timeout=15, follow_redirects=True, headers=headers)
        response.raise_for_status()

        text = trafilatura.extract(response.text, include_links=False)

        if not text:
            print(f"[scraper] sem texto extraído: {url}")
            return None

        return {
            "url": url,
            "text": text,
            "scraped_at": datetime.now().isoformat(),
        }

    except Exception as e:
        print(f"[scraper] erro em {url}: {e}")
        return None


def scrape_startup(name: str, urls: list[str], save: bool = True) -> dict:
    """
    Coleta múltiplas páginas de uma startup e agrega os resultados.
    Salva em data/raw/<name>.json se save=True.
    """
    pages = []

    for url in urls:
        result = scrape_url(url)
        if result:
            pages.append(result)
            print(f"[scraper] ✓ {url} ({len(result['text'])} chars)")

    output = {
        "startup": name,
        "scraped_at": datetime.now().isoformat(),
        "pages": pages,
    }

    if save:
        path = Path(f"data/raw/{name.lower().replace(' ', '_')}.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(output, ensure_ascii=False, indent=2))
        print(f"[scraper] salvo em {path}")

    return output


if __name__ == "__main__":
    # teste rápido com Creditas
    resultado = scrape_startup(
        name="Cortex Intelligence",
        urls=[
            "https://cortex-intelligence.com",
            "https://cortex-intelligence.com/sobre",
            "https://github.com/cortex-intelligence",
        ]
    )
    print(f"\nPáginas coletadas: {len(resultado['pages'])}")
