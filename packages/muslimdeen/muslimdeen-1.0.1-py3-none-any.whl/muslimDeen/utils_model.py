from muslimDeen.service import Services
import pathlib as plib
import re
import unicodedata


def convert_hunspell_to_symspell(path_dabase: str, hunspell_file: str, output_file: str, default_frequency: int = 100) -> None:
    hunspell_file = plib.Path(path_dabase).joinpath(hunspell_file).as_posix()
    output_file = plib.Path(path_dabase).joinpath(output_file).as_posix()
    if plib.Path(output_file).exists():
        return None
    with open(hunspell_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            word = line.split("/")[0].strip()
            if word:
                outfile.write(f"{word} {default_frequency}\n")


def download_hunspell(path_database: str) -> None:
    services = Services()
    path = plib.Path(path_database).joinpath("index.dic")
    response = services.dictionnary_to_dic()
    if path.exists():
        return path.as_posix()
    with open(path, "w") as f:
        f.write(response)
    return path.as_posix()


hunspell_file = "index.dic"
output_file_hunspell = "frequency_dic.txt"


def clear_text(text: str):
    text = text.lower()
    text = unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()


def weighted_similarity_score(faiss_distance, fuzzy_score, alpha=0.5):
    normalized_distance = 1 / (1 + faiss_distance)
    return alpha * (fuzzy_score / 100) + (1 - alpha) * normalized_distance
