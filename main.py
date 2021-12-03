# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import psycopg2

S = "dbname=nuit_info host=edgar.bzh user=nuit_info password=teamfabrice42"
def init(S):
    conn = psycopg2.connect(S)
    cur = conn.cursor()
    return cur

#Supprimes les éléments trop courts
def videliste (tab):
    res = []
    for elem in tab:
        if len(elem) > 2:
            res.append(elem)
    return res

#Met une majuscule au debut et le reste en miniscule pour une recherche de noms et prenoms
def formater_nom(tab):
    tab[0] = tab.upper()
    for i in range(1, len(tab)):
        tab[i] = tab[i].lower()
    print(tab)
    return tab


#Fonction de recherche simple a partir des prénoms et noms
#Recherche avec le nom et prénom de la personne rechercé
#Renvoie la/lignes de la DB qui correspondent a la recherche sous form de CUR
#Pour chaque mot séparés par des espaces recherche parmis les noms et prénoms en enlevant la dernière lettre a chaque fois tant
#que l'on ne trouve pas de résultats, renvois un message d'erreur si aucun résultats ne correspond
def recherche_name(input, cur):
    input = input.split(" ")
    for i in range(0, len(input)):
            input[i] = input[i][0].upper() + input[i][1:len(tab)].lower()
    print(input)
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
    return 1;


if __name__ == '__main__':
    cur = init(S)
    tab = "azertyuiopmljnhbgvfcd"
    tab = tab[0].upper() + tab[1:len(tab)].lower()
    print (tab);
    name = input("Entrer votre recherche basés sur les noms et prénoms :\n")
    rows = recherche_name(name, cur)
    if rows == 1:
        print("Aucun résultats trouvé")
    else:
        for row in rows:
            print(row)
