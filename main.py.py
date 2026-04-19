from abc import ABC, abstractmethod
from datetime import datetime


# =======================
# JÁRATOK
# =======================

class Jarat(ABC):
    def __init__(self, jaratszam: str, cel: str, jegyar: int):
        if jegyar <= 0:
            raise ValueError("A jegyár nem lehet 0 vagy negatív")
        self._jaratszam = jaratszam
        self._cel = cel
        self._jegyar = jegyar

    def get_jaratszam(self):
        return self._jaratszam

    def get_cel(self):
        return self._cel

    def get_jegyar(self):
        return self._jegyar

    @abstractmethod
    def jarat_tipus(self):
        pass

    def __str__(self):
        return f"{self._jaratszam} | {self._cel} | {self._jegyar} Ft | {self.jarat_tipus()}"


class BelfoldiJarat(Jarat):
    def jarat_tipus(self):
        return "Belföldi"


class NemzetkoziJarat(Jarat):
    def jarat_tipus(self):
        return "Nemzetközi"


# =======================
# FOGLALÁS
# =======================

class JegyFoglalas:
    _id_counter = 1

    def __init__(self, jarat: Jarat, nev: str, datum: str):
        try:
            self._datum = datetime.strptime(datum, "%Y-%m-%d")
        except:
            raise ValueError("Hibás dátum formátum! (YYYY-MM-DD)")

        self._jarat = jarat
        self._nev = nev
        self._id = JegyFoglalas._id_counter
        JegyFoglalas._id_counter += 1

    def get_id(self):
        return self._id

    def get_ar(self):
        return self._jarat.get_jegyar()

    def __str__(self):
        return f"[{self._id}] {self._nev} -> {self._jarat.get_cel()} ({self._datum.date()})"


# =======================
# LÉGITÁRSASÁG
# =======================

class LegiTarsasag:
    def __init__(self, nev: str):
        self._nev = nev
        self._jaratok = []
        self._foglalasok = []

    def hozzaad_jarat(self, jarat: Jarat):
        self._jaratok.append(jarat)

    def listaz_jaratok(self):
        for j in self._jaratok:
            print(j)

    def foglalas(self, jaratszam: str, nev: str, datum: str):
        jarat = None
        for j in self._jaratok:
            if j.get_jaratszam() == jaratszam:
                jarat = j
                break

        if not jarat:
            raise ValueError("Nincs ilyen járat!")

        uj = JegyFoglalas(jarat, nev, datum)
        self._foglalasok.append(uj)
        return uj.get_ar()

    def lemondas(self, foglalas_id: int):
        for f in self._foglalasok:
            if f.get_id() == foglalas_id:
                self._foglalasok.remove(f)
                return True

        raise ValueError("Nem létező foglalás!")

    def listaz_foglalasok(self):
        if not self._foglalasok:
            print("Nincs foglalás.")
            return

        for f in self._foglalasok:
            print(f)


# =======================
# KEZDŐ ADATOK
# =======================

def inicializalas():
    lt = LegiTarsasag("AirPython")

    j1 = BelfoldiJarat("B101", "Budapest", 15000)
    j2 = NemzetkoziJarat("N202", "London", 45000)
    j3 = NemzetkoziJarat("N303", "Berlin", 40000)

    lt.hozzaad_jarat(j1)
    lt.hozzaad_jarat(j2)
    lt.hozzaad_jarat(j3)

    # 6 előre feltöltött foglalás
    lt.foglalas("B101", "Teszt Elek", "2026-06-01")
    lt.foglalas("N202", "Kiss Anna", "2026-06-02")
    lt.foglalas("N303", "Nagy Béla", "2026-06-03")
    lt.foglalas("B101", "Erős Pista", "2026-06-04")
    lt.foglalas("N202", "Major Juli", "2026-06-05")
    lt.foglalas("N303", "Gárdonyi Géza", "2026-06-06")

    return lt


# =======================
# MENÜ
# =======================

def menu():
    lt = inicializalas()

    while True:
        print("\n--- Repülőjegy rendszer ---")
        print("1 - Járatok listázása")
        print("2 - Foglalások listázása")
        print("3 - Jegy foglalása")
        print("4 - Foglalás lemondás")
        print("0 - Kilépés")

        valasztas = input("Választás: ")

        try:
            if valasztas == "1":
                lt.listaz_jaratok()

            elif valasztas == "2":
                lt.listaz_foglalasok()    

            elif valasztas == "3":
                jarat = input("Járatszám: ")
                nev = input("Név: ")
                datum = input("Dátum (YYYY-MM-DD): ")

                ar = lt.foglalas(jarat, nev, datum)
                print(f"Sikeres foglalás! Ár: {ar} Ft")

            elif valasztas == "4":
                fid = int(input("Foglalás ID: "))
                lt.lemondas(fid)
                print("Sikeres törlés")
    
            elif valasztas == "0":
                break

            else:
                print("Érvénytelen választás!")

        except Exception as e:
            print(f"Hiba: {e}")


# =======================
# FUTTATÁS
# =======================

if __name__ == "__main__":
    menu()