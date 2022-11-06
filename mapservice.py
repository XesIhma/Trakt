class MapService:
    @classmethod
    def get_active(cls):
        return WorldService.get_active().map


class AkcjaIscieWLewo:
    @classmethod
    def sprawdz_czy_mozna(cls, hero):
        return True, { 'ilosc_dni': '5' }
    
    @classmethod
    def wykonaj(cls, hero):
        pass


class Gra:
    def __init__(self):
        self.akcje = [
            AkcjaIscieWLewo,
            AkcjaIscieWPrawo,
        ]