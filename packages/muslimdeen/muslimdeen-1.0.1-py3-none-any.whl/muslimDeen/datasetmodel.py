import muslimDeen.meta_quran_reader as metaquranreader
from typing import Tuple, Callable

class DatasetModel:
    def __init__(self, path_database:str):
        self.path_database = path_database
        self.meta_quran = metaquranreader.MetaQuranReader(self.path_database)
    
    def dataset_name_fr(self, func:Callable) -> Tuple[list, dict]:
        dataset = []
        mapping_original = {}
        for _, v in self.meta_quran.lower_name_fr.items():
            original = v["nom_sourate"]
            cleaned = func(original)
            dataset.append(cleaned)
            mapping_original[cleaned] = original
        return dataset, mapping_original