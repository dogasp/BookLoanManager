import json
import csv
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from datetime import *

def reinitialiser():
    lieulivre = askopenfilename(title="Ouvrir fichier livre",filetypes=[('CSV Files','.csv'),('all files','.*')])
    liste = []
    with open(lieulivre, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
         row = "".join(row)
         row = row.split(";")
         row.append("I")
         liste.append(row)

    traitement(liste)
    with open('livre.json', 'w') as f:
      f.write(json.dumps(liste, indent = 4))

    AjoutClasse()

def AjoutClasse():
    global entree
    global liste_
    global t
    lieueleve = askopenfilename(title="Ouvrir fichier elève",filetypes=[('CSV Files','.csv'),('All Files','.*')])
    liste_ = []
    with open(lieueleve, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
         row = "".join(row)
         row = row.replace('ï»¿','')
         row = row.split(";")
         row.append(" ")
         row.append(" ")
         liste_.append(row)

    t = Toplevel()
    value = StringVar()
    value.set("nom classe")
    entree = Entry(t, textvariable=value, width=30)
    entree.grid(row = 1, column = 1)
    bouton = Button(t, text="Valider", command=AjoutClasse_)
    bouton.grid(row = 1, column = 2)
    t.update()

def AjoutClasse_():
    classe = entree.get()
    try:
        dict in globals()
    except:
        dict = {}
    traitement(liste_)

    dict[classe] = liste_
    with open('élèves.json', 'w') as f:
      f.write(json.dumps(dict, indent = 4))
    t.destroy()


def texte():
    localisation = askdirectory(title = "sélectionner ou enregister la liste d'élèves")
    with open(localisation+"/fichier élèves classe.txt", 'w') as f:
        enregistrer = []
        for element in datas_:
            if element[2] != " ":
                f.write("L'élève {} {} a emprunté le livre {} et doit le rendre pour le {}.\n\n".format(element[0], element[1], element[2], element[3]))
            else:
                f.write("l'élève {} {} n'a pas de livres emprunté.\n\n".format(element[0], element[1]))


def charger():
    global choix

    with open('livre.json', 'r') as f:
        global datas
        datas = json.load(f)

    with open('élèves.json', 'r') as f:
        global dict
        dict = json.load(f)

    Label (pr, text = "quelle classe voulez-vous charger?", anchor = CENTER).grid()
    choix = Listbox(pr)

    for yolo in dict.keys():
        choix.insert(END, yolo)
    choix.bind("<<ListboxSelect>>", charger_)
    choix.grid()

#suite
def charger_(event = NONE):
    global datas_
    global endroit
    global fr
    global c
    line = choix.curselection()
    endroit = choix.get(line)

    for object in pr.winfo_children():
        if type(object) == Menu:
            pass
        else:
            object.destroy()

    vsb = Scrollbar(pr, orient=VERTICAL)
    vsb.grid(row=0, column=1, sticky=N+S)
    vsb.config(bg = '#333333')
    c = Canvas(pr,yscrollcommand=vsb.set)
    c.grid(row=0, column=0, sticky="news")
    vsb.config(command=c.yview)
    pr.grid_rowconfigure(0, weight=1)
    pr.grid_columnconfigure(0, weight=1)
    fr = Frame(c)

    legende1 =["nom", "prénom", "cote du livre", "date du retour"]
    Label(fr, text = legende1[0], width = 10, bg = '#cccccc').grid(column = 1, row = 0)
    Label(fr, text = legende1[1], width = 50, bg = '#cccccc').grid(column = 2, row = 0)
    Label(fr, text = legende1[2], width = 50, bg = '#cccccc').grid(column = 3, row = 0)
    Label(fr, text = legende1[3], width = 10, bg = '#cccccc').grid(column = 4, row = 0)

    datas_  = dict[endroit]
    afficher(datas_, fr)

    c.create_window(0, 0,  window=fr)
    fr.update_idletasks()
    c.config(scrollregion=c.bbox("all"))
    c.yview_moveto(0)
    pr.bind('<Enter>',entrer)
    pr.bind('<Leave>',sortir)
    c.yview_moveto(0)

#fonction pour donner le la date de retour
def temps():
     global Maintenant
     global avant
     Maintenant = date.today()
     avant = Maintenant + timedelta(days = 7)
     avant = avant.isoformat()
     Maintenant = Maintenant.isoformat()

#fonction d'affichage des données
def afficher(datas, pr):
    i = 0
    for element in datas:
     i += 1
     Label(pr, text = element[0], width = 10).grid(column = 1, row = i)
     Label(pr, text = element[1], width = 50).grid(column = 2, row = i)
     Label(pr, text = element[2], width = 50).grid(column = 3, row = i)

     try:
         conversion = datetime.strptime(element[3], "%Y-%m-%d")
         conversion = conversion.isoformat()
         temps()
         if conversion <= avant and conversion > Maintenant:
             Label(pr, text = element[3], width = 10, fg ='#087BED').grid(column = 4, row = i)
         elif conversion < Maintenant:
             Label(pr, text = element[3], width = 10, fg ='#DF362A').grid(column = 4, row = i)
         elif conversion > avant:
             Label(pr, text = element[3], width = 10, fg ='#3FDB4E').grid(column = 4, row = i)

     except:
         Label(pr, text = element[3], width = 10).grid(column = 4, row = i)

     if len(datas[1]) == 6:
         Label(pr, text = element[4], width = 40).grid(column = 5, row = i)
         if element[5] == "X":
             Label(pr, text = element[5], width = 20, fg = '#ED1E32').grid(column = 6, row = i)
         else:
             Label(pr, text = element[5], width = 20, fg = '#1EED4E').grid(column = 6, row = i)

    pr.update()

#fonction afin de rendre les listes utilisable
def traitement(liste):
    for i in range(len(liste)):
        try:
            for n in range(len(liste[i])):
                bis = liste[i][n].lower()
                if bis == "prenom" or bis == "prénom" or bis == "titre":
                    del liste[i]
        except:
            pass
        try:
            if liste[i][4] == "":
                liste[i][4] = "1"
        except:
            pass

#fonction pour afficher l'onglet des livres
def livres():
    t = Toplevel()
    t.title("Liste des livres enregistrés")
    vsb = Scrollbar(t, orient=VERTICAL)
    vsb.grid(row=0, column=1, sticky=N+S)
    c = Canvas(t,yscrollcommand=vsb.set)
    c.grid(row=0, column=0, sticky="news")
    vsb.config(command=c.yview)
    t.grid_rowconfigure(0, weight=1)
    t.grid_columnconfigure(0, weight=1)
    fr = Frame(c)
    t.geometry('1300x400')

    legende2 = ["cote", "titre", "auteur", "édition", "exemplaires", "disponible?"]
    Label(fr, text = legende2[0], width = 10, bg = '#cccccc').grid(column = 1, row = 0)
    Label(fr, text = legende2[1], width = 50, bg = '#cccccc').grid(column = 2, row = 0)
    Label(fr, text = legende2[2], width = 50, bg = '#cccccc').grid(column = 3, row = 0)
    Label(fr, text = legende2[3], width = 10, bg = '#cccccc').grid(column = 4, row = 0)
    Label(fr, text = legende2[4], width = 40, bg = '#cccccc').grid(column = 5, row = 0)
    Label(fr, text = legende2[5], width = 20, bg = '#cccccc').grid(column = 6, row = 0)

    afficher(datas, fr)

    c.create_window(0, 0,  window=fr)
    fr.update_idletasks()
    c.config(scrollregion=c.bbox("all"))
    c.yview_moveto(0)

#suite fonction emprunt
def nom2(event = NONE):
    line = entree1.curselection()
    item = entree1.get(line)
    entree_1 = item
    for i in range(len(datas)):
      if entree_3 == datas[i][0] and datas[i][5] == "I":

          for a in range(len(datas_)):
             if any(entree_2 in s for s in datas_[a]) == True and any(entree_1 in t for t in datas_[a]) == True and datas_[a][2] == " ":
                  datas[i][4] = str(int(datas[i][4])-1)
                  if datas[i][4] == "0":
                      datas[i][5] = "X"
                  datas_[a][2] = entree_3
                  datas_[a][3] = datetime.strftime(date.today() + timedelta(days = 14), "%Y-%m-%d")

                  dict[endroit] = datas_
                  with open('élèves.json', 'w') as f:
                      f.write(json.dumps(dict, indent = 4))

                  with open('livre.json', 'w') as f:
                   f.write(json.dumps(datas, indent = 4))

                  t.destroy()
                  m.destroy()
                  afficher(datas_, fr)
                  return

    showerror("erreur", "erreur dans les données")
#fonction pour emprunter
def enregistrer():
    global entree_1
    global entree_2
    global entree_3
    global entree1
    global selection
    global m
    prenom = []

    entree_2 = entree2.get()
    entree_3 = entree3.get()
    m = Toplevel()
    m.title("choisir elève")
    prenom.append(datas_)
    entree1 = Listbox(m)

    for b in range(len(datas_)):
        if any(entree_2 in s for s in datas_[b]) == True and datas_[b][2] == " ":
            entree1.insert(END, datas_[b][0])
    entree1.bind("<<ListboxSelect>>", nom2)
    entree1.grid(row = 0, column = 1)

#suite fonction retour
def nom1(event = NONE):
    line = entree1.curselection()
    item = entree1.get(line)
    entree_1 = item

    for i in range(len(datas)):
      if entree_3 == datas[i][0]:
          for a in range(len(datas_)):
             if any(entree_2 in s for s in datas_[a]) == True and any(entree_1 in t for t in datas_[a]) == True and datas_[a][2] != " ":
                  datas[i][5] = "I"
                  datas[i][4] = str(int(datas[i][4])+1)
                  datas_[a][2] = " "
                  datas_[a][3] = " "

                  dict[endroit] = datas_
                  with open('élèves.json', 'w') as f:
                      f.write(json.dumps(dict, indent = 4))

                  with open('livre.json', 'w') as f:
                   f.write(json.dumps(datas, indent = 4))

                  t.destroy()
                  m.destroy()
                  afficher(datas_, fr)
                  return

    showerror("erreur", "Il y a une erreur dans les données")

#fonction retour de livre
def rendre():
    global entree_1
    global entree_2
    global entree_3
    global entree1
    global selection
    global m
    prenom = []

    entree_2 = entree2.get()
    entree_3 = entree3.get()
    m = Toplevel()
    m.title("choisir elève")
    prenom.append(datas_)
    entree1 = Listbox(m)

    for b in range(len(datas_)):
        if any(entree_2 in s for s in datas_[b]) == True and datas_[b][2] != " ":

            entree1.insert(END, datas_[b][0])
    entree1.bind("<<ListboxSelect>>", nom1)
    entree1.grid(row = 0, column = 1)

#interface emprunt de livre
def enregistrerlivre():
  global entree2
  global entree3
  global t

  t = Toplevel()
  t.title("Emprunter")

  value2 = StringVar()
  value2.set("prénom")
  entree2 = Entry(t, textvariable=value2, width=30)
  entree2.grid(row = 2, column = 1)
  t.update()

  value3 = StringVar()
  value3.set("cote livre")
  entree3 = Entry(t, textvariable=value3, width=30)
  entree3.grid(row = 3, column = 1)
  bouton3 = Button(t, text="Valider", command=enregistrer)
  bouton3.grid(row = 3, column = 2)

#interface retour de livre
def rendrelivre():

      global entree2
      global entree3
      global t

      t = Toplevel()
      t.title("retour")

      value2 = StringVar()
      value2.set("prénom")
      entree2 = Entry(t, textvariable=value2, width=30)
      entree2.grid(row = 2, column = 1)
      t.update()

      value3 = StringVar()
      value3.set("cote livre")
      entree3 = Entry(t, textvariable=value3, width=30)
      entree3.grid(row = 3, column = 1)
      bouton3 = Button(t, text="Valider", command=rendre)
      bouton3.grid(row = 3, column = 2)

#fonction pour afficher les informations
def infos():
    w = Toplevel()
    w.title("Information")
    vsb = Scrollbar(w, orient=VERTICAL)
    vsb.grid(row=0, column=1, sticky=N+S)
    c = Canvas(w,yscrollcommand=vsb.set)
    c.grid(row=0, column=0, sticky="news")
    vsb.config(command=c.yview)
    w.grid_rowconfigure(0, weight=1)
    w.grid_columnconfigure(0, weight=1)
    fr = Frame(c)
    w.geometry('600x200')

    Label(fr, text = "Gestionnaire de biliotheque V0.4\n développé par dogasp").grid()
    Label(fr, text ="\nNote de mise à jour:\n", anchor = 'w').grid(sticky = 'w')
    Label(fr, text ="V0.1: première version du logiciel en bêta afin de regarder les différents buggs", anchor = 'w').grid(sticky = 'w')
    Label(fr, text ="V0.2: Résolution de buggs, amélioration de l'interface et simplification, de l'import des données", anchor = 'w').grid(sticky = 'w')
    Label(fr, text ="V0.3: Ajout du support du logiciel de plusieurs classes pour une même liste de livres", anchor = 'w').grid(sticky = 'w')
    Label(fr, text ="V0.4: Ajout enregistrement de l'état des emprunts dans un bloc-note avec choix du dossier", anchor = 'w').grid(sticky = 'w')

    c.create_window(0, 0,  window=fr)
    fr.update_idletasks()
    c.config(scrollregion=c.bbox("all"))
    c.yview_moveto(0)

#les fonctions suivantes servent au scroll
def scrollevent(event = NONE):
    if event.delta > 0:
        c.yview_scroll(-2, "units")
    else:
        c.yview_scroll(2, "units")

def entrer(event):
    pr.bind('<MouseWheel>', scrollevent)

def sortir(event):
    pr.unbind('<MouseWheel>')

#fonction pour afficher la liste de classe
def classel():
    t = Toplevel()
    t.title("Liste des classes enregistrés")
    t.geometry("20x150")
    n = 0
    for classes in dict.keys():
        Label(t, text = classes, width = 10,).grid(column = 1, row = n)
        n+=1

#on évite de lancer la mise a jour si déjà fait
pr = Tk()
pr.title("Gestionnaire de bibliotheque V0.4 DG")
menubar = Menu(pr)

#initialisation de la bare de menu
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label = "changer de classe", command = charger)
menu1.add_command(label = "réinitialiser", command=reinitialiser)
menu1.add_command(label = "ajouter classe", command = AjoutClasse)
menu1.add_separator()
menu1.add_command(label = "voir liste livres", command = livres)
menu1.add_command(label = "voir liste classe", command = classel)
menu1.add_separator()
menu1.add_command(label="Quitter", command=pr.quit)
menubar.add_cascade(label="Fichiers", menu=menu1)

menu2 = Menu(menubar, tearoff = 0)
menu2.add_command(label = "Emprunter livre", command = enregistrerlivre)
menu2.add_command(label = "Rendre livre", command = rendrelivre)
menu2.add_separator()
menu2.add_command(label = "Obtenir un fichier texte de la classe", command = texte)
menubar.add_cascade(label = "Emprunt/Retour", menu = menu2)

menu3 = Menu(menubar, tearoff = 0)
menu3.add_command(label = "Informations", command = infos)
menubar.add_cascade(label = "Aide", menu = menu3)
pr.config(menu=menubar, width = 200)
pr.geometry("900x500")

#code principal
try:
    open('élèves.json', 'r')
except:
    reinitialiser()

try:
    charger()
except:
    pass
pr.mainloop()                                                                                                                                         
