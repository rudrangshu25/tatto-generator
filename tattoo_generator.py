import spacy
from keybert import KeyBERT


nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()


symbol_map = {
    "sailor": "anchor",
    "sea": "wave",
    "father": "anchor",
    "mother": "rose",
    "childhood": "footprint",
    "pain": "dagger",
    "freedom": "bird",
    "music": "note",
    "love": "heart",
    "journey": "compass",
    "strength": "lion",
    "hope": "lotus",
    "warrior": "sword",
    "death": "skull"
}

def extract_tattoo_symbols(text):
    doc = nlp(text)
    entities = [ent.text.lower() for ent in doc.ents]
    keywords = [kw[0].lower() for kw in kw_model.extract_keywords(text, top_n=10)]
    combined = list(set(keywords + entities))
    symbols = [symbol_map[word] for word in combined if word in symbol_map]
    return {
        "Entities": entities,
        "Keywords": keywords,
        "Matched Symbols": symbols
    }