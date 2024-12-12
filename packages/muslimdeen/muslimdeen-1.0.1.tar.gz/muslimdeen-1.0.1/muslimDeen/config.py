class Config:
    @staticmethod
    def url_meta_data_v1() -> str:
        return "https://api.alquran.cloud/v1/meta"

    @staticmethod
    def url_data_quran() -> str:
        return "https://raw.githubusercontent.com/mehdi-stark/Coran-Quran/refs/heads/master/quran.json"

    @staticmethod
    def author_quran_github() -> str:
        return "https://github.com/mehdi-stark"

    @staticmethod
    def dictionnary_fr() -> str:
        return "https://raw.githubusercontent.com/wooorm/dictionaries/refs/heads/main/dictionaries/fr/index.dic"
