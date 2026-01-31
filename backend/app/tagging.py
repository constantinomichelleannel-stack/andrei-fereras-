LEGAL_KEYWORDS = ['contract','tort','jurisdiction','evidence','pleading','motion','appeal','damages','arbitration','mediation','settlement','statute','jurisprudence','precedent','compliance']

def autotag(text: str) -> str:
    t = text.lower()
    tags = sorted({kw for kw in LEGAL_KEYWORDS if kw in t})
    return ', '.join(tags)
