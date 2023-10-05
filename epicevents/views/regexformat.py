regexformat = {
    '3cn': (
        r"^[A-Za-z0-9-]+$",
        "Au moins 3 caractères sont requis, alpha ou numérique"),
    'alphanum': (
        r"^[a-zA-Z0-9 ]+$",
        "Seul des caractères alpha sont autorisés"),
    'numposmax': (
        r"(?<!-)\b([1-3]?\d{1,5}|100000)\b",
        "Le montant doit être positif et inférieur à 100 000"
    ),
    'date': (
        r'(\d{2})[/.-](\d{2})[/.-](\d{4})$',
        "format dd/mm/yyyy attendu"
    ),
    'alpha': (
        r"^[a-zA-Z ']+$",
        "Seul des caractères alpha sont autorisés"
    ),
}
