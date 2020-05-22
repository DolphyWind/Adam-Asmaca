import sqlite3
import random
import os
import platform

# Aktif harfler
active_letters = ["A","B","C","Ç","D","E","F","G","Ğ","H","I","İ","J","K","L","M","N","O","Ö","P","R","S","Ş","T","U","Ü","V","Y","Z"]
words = list()

# Tüm kelimeleri al
def getWords():
    db = sqlite3.connect("kelimeler.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS kelimeler (ID integer PRIMARY KEY,kelime VARCHAR(16) NOT NULL, konu VARCHAR(16) NOT NULL)")
    cursor.execute("SELECT * FROM kelimeler")
    values = cursor.fetchall()
    db.commit()
    db.close()
    return values

# Rastgele bir kelime seç (kelime, konu)
def pickRandom():
    words = getWords()
    rand = random.randint(0, len(words) - 1)
    return (words[rand][1], words[rand][2])

# Küçük harfleri büyült (i -> İ, ı -> I)
def toUpper(x:str):
    ret = ""
    for i in range(len(x)):
        if x[i] == 'i': ret += 'İ'
        else: ret += x[i].upper()
    return ret

# Üst kısmı göster
def printTop(length:int):
    print("+{}+".format("-" * length))
    print(("|{:^" + str(length) + "}|").format("Adam Asmaca"))
    print("+{}+".format("-" * length))

# Adamı göster
def printHangMan(length:int, pos:int):
    print("|{}|".format(" " * length))
    if pos == 7:
        print(("|{:^" + str(length) + "}|").format("O"))
        print(("|{:^" + str(length) + "}|").format("/|\\"))
        print(("|{:^" + str(length) + "}|").format("|"))
        print(("|{:^" + str(length) + "}|").format("/ \\"))
    elif pos == 6:
        print(("|{:^" + str(length) + "}|").format("O"))
        print(("|{:^" + str(length) + "}|").format("/|\\"))
        print(("|{:^" + str(length) + "}|").format("|"))
        print(("|{:^" + str(length) + "}|").format("/  "))
    elif pos == 5:
        print(("|{:^" + str(length) + "}|").format("O"))
        print(("|{:^" + str(length) + "}|").format("/|\\"))
        print(("|{:^" + str(length) + "}|").format("|"))
        print("|{}|".format(" " * length))
    elif pos == 4:
        print(("|{:^" + str(length) + "}|").format("O"))
        print(("|{:^" + str(length) + "}|").format("/| "))
        print(("|{:^" + str(length) + "}|").format("|"))
        print("|{}|".format(" " * length))
    elif pos == 3:
        print(("|{:^" + str(length) + "}|").format("O"))
        print(("|{:^" + str(length) + "}|").format(" | "))
        print(("|{:^" + str(length) + "}|").format("|"))
        print("|{}|".format(" " * length))
    elif pos == 2:
        print(("|{:^" + str(length) + "}|").format("O"))
        print(("|{:^" + str(length) + "}|").format(" | "))
        print("|{}|".format(" " * length))
        print("|{}|".format(" " * length))
    elif pos == 1:
        print(("|{:^" + str(length) + "}|").format("O"))
        for _ in range(3):
            print("|{}|".format(" " * length))
    elif pos == 0:
        for _ in range(4):
            print("|{}|".format(" " * length))
    print("|{}|".format(" " * length))

# Kelimeyi göster
def printQuestion(length:int, question:str, konu:str):
    print("+{}+".format("-" * length))
    print(("|{:^" + str(length) + "}|").format(konu))
    print(("|{:^" + str(length) + "}|").format(question))
    print("+{}+".format("-" * length))

# Kalan harfleri göster
def printActiveLetters(length:int):
    print(("|{:^" + str(length) + "}|").format("Kalan Harfler"))
    print("|{}|".format(" " * length))
    first_row = ""
    second_row = ""
    for i in range(16):     first_row += active_letters[i] + " "
    for i in range(16, 29): second_row += active_letters[i] + " "
    first_row = first_row[:-1]
    second_row = second_row[:-1]
    print(("|{:^" + str(length) + "}|").format(first_row))
    print(("|{:^" + str(length) + "}|").format(second_row))
    print("+{}+".format("-"*length))

def main():
    # Kullanıcı kelimeyi yanlış tahmin edip etmediğini kontrol etmek için
    guessed_and_losed = False

    # Windows ise cls değilse clear komudunu çalıştır
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    # Sourmuz
    question = pickRandom()
    # _ _ _ şeklindeki soru
    unknown = list()

    for i in question[0]:
        if i == " ":
            unknown += "/"
        else:
            unknown += "_"

    # Hatalar
    mistakes = 0

    # Oyun tahtasının genişliği (değiştirilebilir)
    length = 33

    # 7'den daha az hata yapıldıysa
    while mistakes < 7:
        # Soruyu _ _ _ haline getir
        unknown_modified = ""
        for i in range(len(unknown)):
            unknown_modified += unknown[i] + ' '
        unknown_modified = unknown_modified[:-1]

        # Windows ise cls değilse clear komudunu çalıştır
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

        # Tahtayı yazdır
        printTop(length)
        printHangMan(length,mistakes)
        printQuestion(length, unknown_modified, question[1])
        printActiveLetters(length)

        # Kullanıcı girdi al
        inp = toUpper(input(">"))

        # Eğer girdi 1 karakterlik ise
        if len(inp) == 1:
            # Sorunun içerisinde girdi var mı diye bak
            for i in range(len(active_letters)):
                if active_letters[i] == inp[0]:
                    active_letters[i] = " "

                    # Yanlış harf girdi
                    if not inp in question[0]:
                        mistakes += 1
                    # Doğru harf girdi
                    else:
                        for j in range(len(question[0])):
                            if inp == question[0][j]:
                                unknown[j] = inp
                    break
            # Soruda hiç '_' karakteri kalmadıysa bulundu demektir. Bunun için çık döngüden
            if '_' not in unknown:
                break
        # Eğer girdi 1 karakterden fazlaysa
        elif len(inp) > 1:
            # Eğer girdi soru ile aynı uzaklıktaysa tahmindir yanlış tahmin yapan direk kaybeder
            if len(inp) == len(question[0]):
                # Yanlış tahmin ise
                if inp != question[0]:
                    mistakes = 7
                    guessed_and_losed = True
                else:
                    for j in range(len(question[0])):
                            unknown[j] = question[0][j]
                    break
            # Girdi farklı uzunluktaysa her karakteri bir harf olarak kabul et ve her biri için işlem yap
            else:
                for k in inp:
                    for i in range(len(active_letters)):
                        if active_letters[i] == k:
                            active_letters[i] = " "
                            if not k in question[0]:
                                mistakes += 1
                            else:
                                for j in range(len(question[0])):
                                    if k == question[0][j]:
                                        unknown[j] = k
                            break
                if '_' not in unknown:
                    break
    # Oyun Bitti
    unknown_modified = ""
    for i in range(len(unknown)):
        unknown_modified += unknown[i] + ' '
    unknown_modified = unknown_modified[:-1]

    # Windows ise cls değilse clear komudunu çalıştır
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    # Tahtayı yazdır
    printTop(length)
    printHangMan(length, mistakes)
    printQuestion(length, unknown_modified, question[1])
    printActiveLetters(length)

    # Sonucu yazdır
    if mistakes >= 7:
        if guessed_and_losed:
            print("Yanlış tahmin :(")
        print("Kaybettiniz! Doğru kelime {} olacaktı!".format(question[0]))
        input("Çıkış Yapmak İçin Enter'a Basın...")
    else:
        print("Bravo! Doğru kelimeyi buldun!")
        input("Çıkış Yapmak İçin Enter'a Basın...")

if __name__ == "__main__":
    main()
