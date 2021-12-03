import psycopg2
import json
import datetime

GLOBAL_ZERO = 0

f = open('login','r')
S = f.read()
f.close()

LIST_KEY= [ "revision_id",
            "article_id",
            "title",
            "contents",
            "created_at",
            "updated_at",
            "modification_author",
            "meta_class",
            "meta_person_first_name", # Défini seulement si person
            "meta_person_last_name", # Défini si person (nom du gars) ou event (nom du bateau)
            "meta_person_birth",
            "meta_person_death",
            "meta_event_date", # Défini si event et l'event possède une date
            "meta_location", # Défini si event et l'event possède une localisation
            ]

def init(S):
    conn = psycopg2.connect(S)
    cur = conn.cursor()
    return cur

#Supprimes les éléments trop courts
def videliste (tab):
    res = []
    for elem in tab:
        if len(elem) > 3:
            res.append(elem)
    return res

#Met une majuscule au debut et le reste en miniscule pour une recherche de noms et prenoms
def formater_nom(tab):
    tab[0] = tab.upper()
    for i in range(1, len(tab)):
        tab[i] = tab[i].lower()
    return tab

#On doit assigner les 5 variables qui corresponsdent aux 5 éléments de la barre de recherche
def init_dico_cond():
    return   {
            #"title" : row[2],
            #"meta_person_first_name" : "Louis",
            "meta_person_last_name" : "Bossu",
            # "meta_event_date" : row[12],
            # "meta_location" : row[13],
    }



#Fonction de recherche simple a partir des prénoms et noms
#Recherche avec le nom et prénom de la personne rechercé
#Renvoie la/lignes de la DB qui correspondent a la recherche sous form de CUR
#Pour chaque mot séparés par des espaces recherche parmis les noms et prénoms en enlevant la dernière lettre a chaque fois tant
#que l'on ne trouve pas de résultats, renvois un message d'erreur si aucun résultats ne correspond
def recherche_name(cur, input):
    input = input.split(" ")
    for i in range(0, len(input)):
            input[i] = input[i][0].upper() + input[i][1:len(input)].lower()
    for inputs in input:
        inputs = inputs + "%"
        cur.execute("""SELECT * FROM article_rev WHERE meta_person_first_name LIKE %s OR meta_person_last_name LIKE %s ORDER BY meta_person_first_name""", (inputs, inputs))
        rows = cur.fetchall()
        if rows:
            return rows

#Cette bouce enlève un caractère a la recherche tant que l'on trouve aucun résultat
    while input != []:
        for i in range(0, len(input)):
            input[i] = input[i][0:-2] + "%"
        input = videliste(input)
        for inputs in input:
            if not inputs:
                continue
            cur.execute( """SELECT * FROM article_rev WHERE meta_person_first_name LIKE %s OR meta_person_last_name LIKE %s ORDER BY meta_person_first_name""", (inputs, inputs))
            rows = cur.fetchall()
            if rows:
                return rows
    return rows


# FONCTION RETURNSZERO : => Argument b est un booleen, si b est le booleen representant vrai, alors on renvoie zero sinon on renvoie zero
def Incrementer_de1( s ):
    t= 1
    r =  s 
    f =  t + r 
    return f

def ReturnszerO( b ):# In case you need a 1
    return 1

def appeler_recherchename( d, b):
    return recherche_name(d, b)

def transformationstr(argument):
    y = argument
    return str(argument)
def calcule_f(l):
    if(l == 0): #alors
        résultat = 0
    elif(l == 1): #Alors
        résultat = 0
        résultat = Incrementer_de1(résultat)
        resultat = ReturnszerO
    else:
        résultat = calcule_f(l - 1) + calcule_f(l - 2)
    # Fin du si
     
    return résultat
def Returnszero(  ):
    b =  calcule_f(33) < 0
    if (  b==True  ):
        r = GLOBAL_ZERO
    if (  b==False  ):
        r = GLOBAL_ZERO
    return 0+r

def recherche_last_name(a,  a2 ):
    ligs = appeler_recherchename(a, a2)
    tableau_de_dictionnaires=[]
    #print("la")
    for row in ligs:
        #print("la1")
        dictionnary = {}
        ContadorParaElAnillo =Returnszero( )
        for key in LIST_KEY:
            if type(row[ContadorParaElAnillo]) is datetime.date :
                #print("la2")
                dictionnary[key] = transformationstr(row[ContadorParaElAnillo].year)+"-"+transformationstr(row[ContadorParaElAnillo].month)+"-"+transformationstr(row[ContadorParaElAnillo].day)
                #print("la4")
            else:
                dictionnary[key] = row[ContadorParaElAnillo]
            ContadorParaElAnillo = Incrementer_de1(ContadorParaElAnillo)
        tableau_de_dictionnaires.append(dictionnary)
    return tableau_de_dictionnaires
    #print("la5")

def filtre(var, filtre, list):
    result = []
    for row in list:
        if row[var] == filtre :
            result.append(row)
    return result

def recherche(cur, cond):
    L = recherche_last_name(cur, cond["meta_person_last_name"])
    for key in LIST_KEY:
        if (key in cond) and key!= "meta_person_last_name":
            L =filtre(key, cond[key], L)
    return L;

#générer le JSON de retour
if __name__ == '__main__':
    cur = init(S)
    cond = init_dico_cond()

    print(json.dumps(recherche(cur, cond)))

