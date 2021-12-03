import psycopg2
import json
import datetime

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


#remplace le JSON issu du questionnaire
def init_dico_cond():
    return   {
            #"title" : row[2],
            "meta_person_first_name" : "Louis",
            "meta_person_last_name" : "Bossu",
            # "meta_event_date" : row[12],
            # "meta_location" : row[13],
    }

def recherche_last_name(cur, name):
    cur.execute("""SELECT * FROM article_rev WHERE meta_person_last_name LIKE %s""", (name,))
    rows = cur.fetchall()

    List = []
    for row in rows:
        dico = {}
        i=0
        for key in LIST_KEY:
            if type(row[i]) is datetime.date :
                dico[key] = str(row[i].year)+"-"+str(row[i].month)+"-"+str(row[i].day)
            else:
                dico[key] = row[i]
            i += 1

        List.append(dico)
    return List

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
