
frws = ["wer", "wo", "was", "wen", "wem", "welche", "welcher", "wehlches", "wohin", "woher", "womit", "wie", "wann", "woran", "warum", "weshalb", "weswegen", "wozu"]

def pronomenTausch(pronom):
    pronom = pronom.lower()
    if(pronom == "ich"):
        return "du"
    elif(pronom == "du"):
        return "ich"
    if(pronom == "mich"):
        return "dich"
    elif(pronom == "dich"):
        return "mich"
    if(pronom == "dir"):
        return "mir"
    elif(pronom == "mir"):
        return "dir"
    else:
        return pronom

def personFiltern(eigenschaften):
    perz = "1"
    persp = "SIN"
    if("2" in eigenschaften):
        perz = "2"
    elif("3" in eigenschaften):
        perz = "3"
    if("PLU" in eigenschaften):
        persp = "PLU"
    return persp + ":" +  perz


def frageZuAntwort(woerterbuch, frage, case=True):
    frageLower = frage.lower()
    
    frageNeu = ""
    chars = "abcdefghijklmnopqrstuvwxyzßöäü 1234567890?!."
    for i in range(0, len(frage)):
        if(frageLower[i] in chars):
            frageNeu += frage[i]

    frage = frageNeu
    while("  " in frage):
        frage = frage.replace("  ", " ")

    fragen = frage.replace("!", ".").replace("?", ".").replace("und", ".").replace("oder", ".").split(".")
    for i in range(0, len(fragen)):
        if(fragen[i] == ""):
            fragen.pop(i)

    arten = []
    antworten = []

    for i in range(0, len(fragen)):
        person = "SIN:2"
        zeit = "PRÄ"
        frw = "ob"
        px = True

        if(fragen[i][0] == " "):
            fragen[i] = fragen[i][1:]
        fragen[i] = fragen[i].strip()
        fragen[i] = fragen[i].split(" ")

        arten.append([])
        antworten.append("")
        for wort in fragen[i]:
            if(wort.lower() in frws):
                frw = wort.lower()
                arten[-1].append(["PRO"])
            else:
                ergebnis = woerterbuch.suche(wort, case=False)
                if(ergebnis):
                    ergebnis = ergebnis[0]
                    arten[-1].append(ergebnis[2].split(":"))
                    if("PRO" in arten[-1][-1]):
                        neuPronom = pronomenTausch(wort)
                        antworten[-1] += neuPronom + " "
                        if(px):
                            nergebnis = woerterbuch.suche(neuPronom, case=False)
                            if(nergebnis):
                                person = personFiltern(nergebnis[0][2].split(":"))
                                px = False
                    elif not("VER" in arten[-1][-1]):
                        antworten[-1] += wort + " "
                    if("VOR" in arten[-1][-1] or "NAC" in arten[-1][-1]):
                        if(px):
                            person = "SIN:3"
                            px = False
                else:
                    arten[-1].append(ergebnis)
        
        for j in range(0, len(arten[-1])):
            if(arten[-1][j]):
                if("VER" in arten[-1][j]):
                    konj = woerterbuch.konjugiere(fragen[i][j], person, zeit)
                    if(konj):
                        antworten[-1] += konj + " "
        
        antworten[-1] = "Ich weiß nicht, " + frw + " " + antworten[-1].strip()
    
    antwort = ""
    for i in range(0, len(antworten)):
        if(i/2 == int(i/2)):
            antwort += antworten[i]
            if(i == len(antworten) - 1):
                antwort += "."
            else:
                antwort += " und "
        else:
            antworten[i] = antworten[i][0].lower() + antworten[i][1:]
            antwort += antworten[i] + ". "
    return antwort