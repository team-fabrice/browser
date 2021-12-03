# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import psycopg2
import json
import datetime

S = "dbname=nuit_info host=edgar.bzh user=nuit_info password=teamfabrice42"

LIST_KEY= [ "revision_id",
            "article_id",
            "title",
            "content",
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
    return rows;

def recherche_last_name(cur, name):
    rows = recherche_name(cur, name)
    list=[]
    for row in rows:
        dico = {}
        i=0
        for key in LIST_KEY:
            if type(row[i]) is datetime.date :
                dico[key] = str(row[i].year)+"-"+str(row[i].month)+"-"+str(row[i].day)
            else:
                dico[key] = row[i]
            i += 1
        list.append(dico)
    return list

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
