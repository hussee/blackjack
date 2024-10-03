import random
import time
#klass som hanterar kotleken samt logik
class Kortlek:
    #Initierar samtliga möjliga kort och deras värde.
    def __init__(self):
        self.kortlekens_varde = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
            'J': 10, 'Q': 10, 'K': 10, 'A': 11
        }
        self.deck = []
        self.bygg_kortlek()

    #Bygger leken för 52kort
    def bygg_kortlek(self):
        for rank in self.kortlekens_varde.keys():
            self.deck.extend([rank] * 4)  

    #Metod för att blanda leken
    def blanda(self):
        random.shuffle(self.deck)  

    #Metod för att dela ut kort
    def dela_ut(self):
        return self.deck.pop()  

    #Hjälpmetod för att få ut the faktiska värdet (face cards,men övriga också)
    def hamta_vardet(self, kort):
        return self.kortlekens_varde[kort]  

    #Metod för att beräkna spelarens eller dealerns hand
    def berakna_hand(self, hand):
        total = 0
        aces = 0
        for kort in hand:
            value = self.hamta_vardet(kort)
            total += value
            if kort == 'A':
                aces += 1
        #Efter summering av totalen hanterar vi 'A', om spelaren överstiger 21 så blir 'A' == 1 
        #Vi kan då plocka bort aces samt plocka bort 10.
        while total > 21 and aces:
            total -= 10  
            aces -= 1
        return total

class Spelbordet:
    def __init__(self):
        #Initiera spelplanen
        self.kortleken = Kortlek()
        self.kortleken.blanda()
        self.spelarensHand = []
        self.dealernsHand = []

    
    def spela(self):
        #Vi börjar med att dela ut två kort var tll spelare och dealern
        self.spelarensHand = [self.kortleken.dela_ut(), self.kortleken.dela_ut()]
        self.dealernsHand = [ self.kortleken.dela_ut(), self.kortleken.dela_ut()]

        print("------------------ Bordet ------------------")

        print(f"Dealern hand!: {self.dealernsHand[0]}")
        print(f"Din hand!: {self.spelarensHand}, Total: {self.kortleken.berakna_hand(self.spelarensHand)}")
        #Om dealer har synligt face kort, så stämmer vi av en möjlig black jack...
        if(self.dealernsHand[0] in ['A', 'J', 'Q', 'K','10']):
           print("--------- Dealer checks black jack ----------")
           dealerns_total =  self.kortleken.berakna_hand(self.dealernsHand)
           if(dealerns_total == 21):
               return print(f"Dealern har 21!: {self.dealernsHand}")
           
        print("------------------ Din tur ------------------")

        #Loopar och inväntar input från spelare / break om vi går över 21 eller vin stand
        while True:
            move = input("Hit eller Stand? ").lower()
            if move == 'hit':
                self.spelarensHand.append(self.kortleken.dela_ut())
                total = self.kortleken.berakna_hand(self.spelarensHand)
                print(f"Dina kort: {self.spelarensHand}, Total: {total}")
                if total > 21:
                    print("------------------ Resultat ------------------")
                    print("Du blev bust! Dealern vinner!")
                    return
            elif move == 'stand':
                break
            else:
                print("Ogiltigt val. Skriv 'hit' eller 'stand'.")

        #dealerns tur, vi kör på tills vi stannar på 16. Går vi över spelar det ingen roll då vi breakar vid nästa.
        while self.kortleken.berakna_hand(self.dealernsHand) < 17:
            print("------------------ Dealerns tur ------------------")
            print("->Dealern kör Hit!!")
            self.dealernsHand.append(self.kortleken.dela_ut())
            print(f"Dealerns kort: {self.dealernsHand}, Total: {self.kortleken.berakna_hand(self.dealernsHand)}")
            time.sleep(1)
        #anropar för att beräkna och ange vinnare.
        self.vinnare()

    def vinnare(self):
        #Har vi kommit såhär långt, har vi ingen bust, så vi kollar vem som är närmast 21.
        spelarens_total = self.kortleken.berakna_hand(self.spelarensHand)
        dealerns_total = self.kortleken.berakna_hand(self.dealernsHand)

        print("------------------ Resultat ------------------")
        print(f"Dina kort: {self.spelarensHand}, Total: {spelarens_total}")
        print(f"Dealerns kort: {self.dealernsHand}, Total: {dealerns_total}")

        if dealerns_total > 21:
            print("Dealern blev bust! Du vinner!")
        elif spelarens_total > dealerns_total:
            print("Du vinner!")
        elif spelarens_total < dealerns_total:
            print("Dealern vinner!")
        else:
            print("Det är oavgjort!")


def main():
    spelet = Spelbordet()
    spelet.spela()


if __name__ == "__main__":
    main()