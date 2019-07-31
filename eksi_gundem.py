import sys
import urllib.request

from bs4 import BeautifulSoup
from colorama import Fore


class EksiGundem:
    def __init__(self):
        self.sayfa_sayisi = 0

    def veri(self, url, sayfa_veri):
        if sayfa_veri != None:
            satirlar = (satir.strip() for satir in sayfa_veri.splitlines())
            blok = (blok.strip() for satir in satirlar for blok in satir.split("  "))
            metin = "\n".join(parcala for parcala in blok if parcala)
            return Fore.WHITE + metin
        else:
            sayfa = urllib.request.urlopen(url)
            soup = BeautifulSoup(sayfa, "html.parser")
            gundem = soup.find_all("ul", {"id": "entry-item-list"})
            soup = BeautifulSoup(str(*gundem), "lxml")
            return soup

    def sayfa(self, sayfa_no, url, kontrol):
        if kontrol != None:
            sayfa = 0
            while True:
                try:
                    sayfa += 1
                    soup = self.veri(url + "&p=" + str(sayfa), None)
                except urllib.error.URLError:
                    self.sayfa_sayisi = sayfa - 1
                    return sayfa - 1
                    break
        else:
            soup = self.veri(url + "&p=" + str(sayfa_no), None)
            print(Fore.GREEN + "\nYORUMLAR\n")
            print(self.veri(None, soup.get_text()))
            print(Fore.RED + "Sayfa:", sayfa_no, "/", self.sayfa_sayisi)
            print(Fore.YELLOW + "Gündem başlıklarına gitmek için:(g)")
            no = input(Fore.BLUE + "Gitmek istediğiniz sayfa no:")
            if no == "g":
                print(Fore.CYAN + "Gündem başlıklarına dönülüyor.....")
                self.gundem()
            self.sayfa(no, url, None)

    def entry(self, url):
        soup = self.veri(url, None)
        print(Fore.GREEN + "\nYORUMLAR\n")
        print(self.veri(None, soup.get_text()))
        print(Fore.RED + "Sayfa:", 1, "/", self.sayfa(0, url, 0))

        try:
            print(Fore.YELLOW + "Gündem başlıklarına gitmek için:(g)")
            no = input(Fore.BLUE + "Gitmek istediğiniz sayfa no:")
            if no == "g":
                print(Fore.CYAN + "Gündem başlıklarına dönülüyor.....")
                self.gundem()
            self.sayfa(no, url, None)
        except urllib.error.URLError:
            print(Fore.RED + "Hata!Ulaşmak istediğiniz sayfa no yok.")
            print(Fore.CYAN + "Gündem başlıklarına dönülüyor.....")
            self.gundem()

    def gundem(self):
        url = "https://eksisozluk.com/"
        sayfa = urllib.request.urlopen(url)
        soup = BeautifulSoup(sayfa, "html.parser")
        gundem = soup.find_all("ul", {"class": "topic-list partial"})
        i = 1
        basliklar = {}

        print(Fore.YELLOW + "Programdan çıkmak için:(ç)")
        baslik_sayi = input(Fore.WHITE + "Kaç gündem başlığı görüntülensin?: ")
        if baslik_sayi == "ç":
            print("Programdan çıkılıyor...")
            sys.exit(0)
        print(Fore.RED + "\nGÜNDEM")
        baslik_sayi = int(baslik_sayi)

        for ul in gundem:
            for li in ul.find_all("li"):
                for baslik in li.find_all("a"):
                    url = "https://eksisozluk.com" + baslik.get("href")
                    if baslik_sayi > 0:
                        basliklar[i] = "https://eksisozluk.com" + baslik.get("href")
                        print(Fore.GREEN + "\n", i, ".) ", baslik.text)
                        i += 1
                        baslik_sayi -= 1

        try:
            no = int(input(Fore.BLUE + "Okumak istediğiniz başlık no: "))
            self.entry(basliklar[no])
        except KeyError:
            print(Fore.RED + "Girdiğiniz no değerine ait başlık bulanamadı!")
            print(Fore.CYAN + "Gündem başlıklarına dönülüyor.....")
            self.gundem()


if __name__ == "__main__":
    eksi = EksiGundem()
    eksi.gundem()