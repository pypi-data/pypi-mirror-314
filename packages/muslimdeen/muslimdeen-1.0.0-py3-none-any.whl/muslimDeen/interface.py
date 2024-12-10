from typing import TypedDict, List, Literal
from enum import Enum


class QuranVersetData(TypedDict):
    """
    Représente les informations d'un verset du Coran.

    Attributes:
        position (int): Position globale du verset dans le Coran.
        text (str): Le texte du verset en translittération.
        position_ds_sourate (int): Position du verset dans la sourate.
        juz (int): Le numéro du Juz auquel appartient le verset.
        manzil (int): Le numéro du Manzil auquel appartient le verset.
        page (int): Le numéro de page où se trouve le verset.
        ruku (int): Le numéro du Ruku auquel appartient le verset.
        hizbQuarter (int): Le quart de Hizb auquel appartient le verset.
        sajda (bool): Indique si le verset contient une prosternation (Sajda).
        text_arabe (str): Le texte du verset en arabe.
    """
    position: int
    text: str
    position_ds_sourate: int
    juz: int
    manzil: int
    page: int
    ruku: int
    hizbQuarter: int
    sajda: bool
    text_arabe: str


class QuranSourateData(TypedDict):
    """
    Représente les informations d'une sourate du Coran.

    Attributes:
        position (int): La position de la sourate dans le Coran.
        nom (str): Le nom de la sourate en arabe.
        nom_phonetique (str): La translittération du nom de la sourate.
        englishNameTranslation (str): La traduction anglaise du nom de la sourate.
        revelation (str): Le type de révélation (Medinois ou Mecquoise).
        versets (List[QuranVersetData]): La liste des versets de la sourate.
        nom_sourate (str): Le nom de la sourate en français.
    """
    position: int
    nom: str
    nom_phonetique: str
    englishNameTranslation: str
    revelation: str
    versets: List[QuranVersetData]
    nom_sourate: str


class QuranData(TypedDict):
    """
    Représente les données du Coran avec toutes les sourates.

    Attributes:
        sourates (List[QuranSouratetData]): Liste des sourates avec leurs informations.
    """
    sourates: List[QuranSourateData]


class RevelationType(Enum):
    """
    Enumération des types de révélations des sourates.

    Values:
        MEDINOIS (str): Révélée à Médine.
        MECQUOISE (str): Révélée à La Mecque.
    """
    MEDINOIS = "Medinois"
    MECQUOISE = "Mecquoise"


class TypedMetaSurah(TypedDict):
    position: int
    name_arabic: str
    name_phonetic: str
    name_english: str
    name_french: str
    revelation_type: str
    number_of_ayahs: int
    sajdas_recommended: bool
    sajdas_obligatory: bool


ListMetaSurahs = List[TypedMetaSurah]


FilterVersets = Literal['position_ds_sourate']


class FilterVersetsDict (TypedDict):
    position_ds_sourate: int
