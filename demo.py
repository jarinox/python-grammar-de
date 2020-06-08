import gmrde

w = gmrde.Woerterbuch()
frage = input("Stellen Sie eine Frage: ")
antwort = gmrde.umformen.frageZuAntwort(w, frage, case=False)
print(antwort)