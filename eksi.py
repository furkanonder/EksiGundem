import sys
import urllib.request

from bs4 import BeautifulSoup


class Eksi:
    def __init__(self):
        self.home_page = "https://eksisozluk.com/"
        self.page_num = 1
        self.entries = []
        self.colors = dict(
            red="\033[31m",
            green="\033[32m",
            yellow="\033[33m",
            blue="\033[34m",
            magenta="\033[35m",
            cyan="\033[36m",
            beige="\033[37m",
            reset="\033[0m",
        )

    def c_print(self, color, *args):
        print(self.colors[color], *args)

    def chunk(self, l):
        for i in range(0, len(l), 3):
            yield l[i : i + 3]

    def parser(self, url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        agenda = soup.find_all("ul", {"id": "entry-item-list"})
        soup = BeautifulSoup(str(*agenda), "lxml")
        lines = [line.strip() for line in soup.get_text().splitlines()]
        result = list(filter(lambda line: line != "", lines))
        return self.chunk(result)

    def reader(self, url):
        chunk = self.parser(url)
        while True:
            try:
                c = next(chunk)
                self.c_print("beige", c[0])
                self.c_print("cyan", c[1], c[2])
            except StopIteration:
                break

    def get_entry(self, url, entry_baslik):
        self.c_print("green", entry_baslik)
        self.reader(url)
        while True:
            self.c_print("green", "Gündem başlıklarını görüntülemek için:(g)")
            try:
                self.c_print(
                    "blue",
                    "Sonraki sayfa için (s):\n Önceki sayfa için (o):\n Programdan çıkmak için (c):",
                )
                cmd = input(">>> ")
                if cmd == "g":
                    self.get_agenda()
                elif cmd == "s":
                    try:
                        self.reader(url + "&p=" + str(self.page_num))
                        self.page_num += 1
                    except urllib.error.HTTPError:
                        self.c_print("red", "Şu an en son sayfadasınız!")
                        self.page_num -= 1
                elif cmd == "o" and self.page_num > 1:
                    self.page_num -= 1
                    self.reader(url + "&p=" + str(self.page_num))
                elif cmd == "c":
                    sys.exit(0)
                else:
                    self.get_entry(url, entry_baslik)
            except ValueError:
                self.c_print("red", "Hata!Geçersiz bir değer girdiniz.")

    def read_entry(self):
        while True:
            try:
                self.c_print("magenta", "Programdan çıkmak için (c):")
                self.c_print("blue", "Okumak istediğiniz başlık numarası: ")
                cmd = input(">>> ")
                if cmd == "c":
                    sys.exit(0)
                entry_url = self.home_page + self.entries[int(cmd)].get("href")
                self.get_entry(entry_url, self.entries[int(cmd)].text)
                break
            except (ValueError, IndexError) as error:
                self.c_print("red", "Hata!Geçersiz bir değer girdiniz.")
            except KeyboardInterrupt:
                break

    def get_agenda(self):
        page = urllib.request.urlopen(self.home_page)
        soup = BeautifulSoup(page, "html.parser")
        agenda = soup.find_all("ul", {"class": "topic-list partial"})
        self.entries = []
        self.page_num = 1

        for ul in agenda:
            for li in ul.find_all("li"):
                for entry in li.find_all("a"):
                    self.entries.append(entry)

        self.c_print("reset", "")
        for index in range(1, len(self.entries)):
            print(index, "-", self.entries[index].text)
        self.read_entry()

    def main(self):
        self.get_agenda()


def eksi():
    eksi = Eksi()
    eksi.main()


if __name__ == "__main__":
    eksi()
