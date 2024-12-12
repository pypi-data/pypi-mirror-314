from sentence_transformers import SentenceTransformer
import faiss
from rapidfuzz import fuzz
from symspellpy import SymSpell, Verbosity
from muslimDeen.datasetmodel import DatasetModel
from muslimDeen.utils_model import download_hunspell, weighted_similarity_score, convert_hunspell_to_symspell, output_file_hunspell, hunspell_file, clear_text
import pathlib as plib
import numpy as np


class Model:
    def __init__(self, path_database: str):
        self.path_database = path_database
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        download_hunspell(self.path_database)
        convert_hunspell_to_symspell(
            self.path_database, hunspell_file, output_file_hunspell)
        self.sym_spell = SymSpell(
            max_dictionary_edit_distance=2, prefix_length=7)
        self.sym_spell.load_dictionary(plib.Path(self.path_database).joinpath(
            output_file_hunspell), term_index=0, count_index=1)
        self.dataset_model = DatasetModel(self.path_database)
        dataset, mapping_original = self.dataset_model.dataset_name_fr(
            clear_text)
        self.__dataset_name_fr = dataset
        self.__mapping_original_fr = mapping_original

        self.__embeddings_base = self.model.encode(self.__dataset_name_fr)
        self.__dimension = self.__embeddings_base.shape[1]
        self.__embeddings_base = self.__embeddings_base / \
            np.linalg.norm(self.__embeddings_base, axis=1, keepdims=True)
        self.__index = faiss.IndexFlatIP(self.__dimension)
        self.__index.add(self.__embeddings_base)

    @property
    def dimension(self):
        return self.__dimension

    @property
    def embeddings_base(self):
        return self.__embeddings_base

    @property
    def index(self):
        return self.__index

    @property
    def dataset_name_fr(self):
        return self.__dataset_name_fr

    @property
    def mapping_original_fr(self):
        return self.__mapping_original_fr

    def correct_spelling(self, input_text: str) -> str:
        suggestions = self.sym_spell.lookup(
            input_text, Verbosity.CLOSEST, max_edit_distance=2)
        return suggestions[0].term if suggestions else input_text

    def search_sentence_similary(self, input_user: str):
        sentence_clear = self.correct_spelling(input_user)
        sentence_clear = clear_text(sentence_clear)

        embedding_user = self.model.encode([sentence_clear])
        embedding_user = embedding_user / \
            np.linalg.norm(embedding_user, axis=1, keepdims=True)
        distances, indices = self.index.search(embedding_user, k=10)
        candidates = [(self.dataset_name_fr[i], distances[0][j])
                      for j, i in enumerate(indices[0]) if i != -1]
        threshold = 0.15
        filtered_candidates = [(c, d) for c, d in candidates if d > threshold]
        if not filtered_candidates:
            return "Aucune correspondance trouvée", None
        results = []
        for candidate, faiss_distance in filtered_candidates:
            fuzzy_score = fuzz.ratio(sentence_clear, candidate)
            combined_score = weighted_similarity_score(
                faiss_distance, fuzzy_score)
            results.append((candidate, combined_score))

        results.sort(key=lambda x: x[1], reverse=True)
        best_sentence, best_score = results[0]

        best_sentence_original = self.mapping_original_fr.get(
            best_sentence, best_sentence)
        return best_sentence_original, best_score

    def predicate(self, input_user: str):
        predicate_s, predicate_score = self.search_sentence_similary(
            input_user)
        if predicate_s == "Aucune correspondance trouvée":
            return None, None
        else:
            predicate_result = self.dataset_model.meta_quran.search_by_name_fr(
                predicate_s)
            predicate_score = f"{(predicate_score * 100):.2f} %"
            return predicate_result, predicate_score
