from nim import train, play
import matplotlib.pyplot as plt

ai = train(1000)

cont = "Y"

while cont == "Y":
    play(ai)
    cont = input("Continue? Y/N\n")
