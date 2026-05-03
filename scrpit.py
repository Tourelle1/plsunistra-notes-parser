from pypdf import *
import os

"""
Avertissement légal et conditions d'utilisation

Ce logiciel est conçu pour un USAGE PERSONNEL UNIQUEMENT.
Les informations et méthodes utilisées dans ce logiciel sont basées sur des données PUBLIQUES 
(disponibles notamment sur https://mathinfo.unistra.fr/). EN REVANCHE, LES DONNÉES TRAITÉES 
PAR CE LOGICIEL (notes, numéros d'étudiant, etc.) SONT DES DONNÉES PERSONNELLES PROTÉGÉES PAR
LE RGPD ET LA LOI N°78-17 du 6 janvier 1978.

L'AUTEUR DÉCLINE TOUTE RESPONSABILITÉ EN CAS DE :
- Fuite, utilisation ou publication non autorisée des données traitées par ce logiciel.
- Violation de la vie privée ou des droits des personnes concernées par les données.
- Non-respect du Règlement Général sur la Protection des Données (RGPD) ou des lois nationales
  applicables.

L'UTILISATEUR S'ENGAGE À :
1. Respecter le RGPD et la Loi n°78-17 du 6 janvier 1978 relative à l'informatique, aux 
fichiers et aux libertés.
2. Ne pas utiliser ce logiciel pour traiter des données personnelles SANS LE CONSENTEMENT
EXPLICITE des personnes concernées.

Licence :
Ce logiciel est distribué sous la licence Creative Commons Attribution - Pas d'Utilisation Commerciale
- Partage dans les mêmes conditions 4.0 International (CC BY-NC-SA 4.0).
Pour plus de détails, consulter le fichier LICENSE ou : 
https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr


Comment l'utiliser : 
(0.) Télecharger pypdf :
Sur linux : 
- Sur VS Code (Recomendé) : Dans le terminal : "sudo apt install pip3" puis dans la console VS Code : "pip3 install pypdf"
- Sur l'environement : "sudo apt install python3-pypdf" dans le terminal
Sur Windows : Tout simplement télécharchger via le CMD avec "pip install pypdf"
1. Aller sur Seafile et télécharger en entier le dossier "Résultat" dans L1-MI
2. Décompresser le fichier, et y ajouter dedans le ficher data.txt qui contient les information concernant les coefs ect...
3. Changer le chemain d'accès au dossier des notes (A noter que sur windows les / simple fonctionent également sur VS Code)
4. Exectuer et entrer votre numéro étudiant

"""



dossier_note = r"path..." 


BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' 
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHT_GRAY = '\033[37m'
DARK_GRAY = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m' 

def str_color(string,color):
    return (color+string+RESET)

def print_color(string,color):
    return print(str_color(string,color))

if dossier_note == "path...":
    raise FileNotFoundError(str_color("Veuillez changer l'addresse du dossier !",RED))

def estUnRepertoire(path):
    return os.path.isdir(path)

def listedirectory(parrent_dir,path=""):
    full_path = parrent_dir+"/"+path
    if not estUnRepertoire(full_path):
        return [path]
    else:
        l =  os.listdir(full_path)
        nl = []
        for e in l:
            c = listedirectory(full_path,e)
            for ec in c:
                pdir = ""
                if path=="":
                    pdir = parrent_dir
                nl += [pdir+path+"/"+ec]
        return nl
        
def get_pdf_text(path): 
    lecteur = PdfReader(e)
    t = ""
    for i in range(len(lecteur.pages)):
        t += lecteur.pages[i].extract_text()
        t += "\n"
    return t

def pretraitement_txt(txt):
    txt = txt.replace("Université de Strasbourg","")
    txt = txt.replace("Pôle Licences Sciences\n","")
    txt = txt.replace("Pôle Licences Sciences","")
    txt = txt.replace("PLS","")
    return txt

def isnumetu(l):
    if len(l)<8:
        return False
    for i in range(8):
        if l[i] not in [str(i) for i in range(10)]:
            return False
    return True
        

def get_note_and_header(txt):
    lines = txt.split("\n")+["end"]
    status = "up"
    ntxt = ""
    for l in lines:

        if status == "up":
            if l[:2] == "N°":
                status = "inside"
                ntxt += l
        elif status == "inside":
            if isnumetu(l):
                ntxt += "\n"+l
            else:
                if l != "":
                    status = "out"
                    break
    if status != "out":
        raise ValueError("Imposible de trouver la fin du document, il n'a pas pu être découpé ! Status avant arrêt:",status)
    return ntxt

def get_float_from_str_left(s):
    last = 0
    for i in range(len(s)-1,-1,-1):
        if s[i] not in ([str(i) for i in range(10)]+["."]):
            last = i+1
            break
    if last == len(s):
        raise ValueError("Pas de chiffre dans la chaîne")
    return float(s[last:])

def get_coefs_normalized(txt):
    coefs = []
    txt = txt[3:].split("\n")[0] # Elinmine le "N° " et prend la premire ligne
    
    # Sépare les coefs
    l = txt.split(")")
    l.pop()
    
    # Récupère les nombres
    somme = 0
    for i in range(len(l)):
        l[i] = get_float_from_str_left(l[i])
        somme += l[i]
    
    # Nomalise
    for i in range(len(l)):
        l[i] = l[i]/somme
    
    return l

def get_num_and_notes(s,expeted):
    s = s.replace("ABI"," ABI")
    s = s.replace("ABJ"," ABJ")
    s = s.replace("DIS"," DIS")
    s = s.replace("SUBS"," SUBS")
    s = s.replace("  "," ")
    l = s.split(" ")

    
    for i in range(expeted-len(l)+1):
        l.append(0)
    
    if "" in l:
        raise RuntimeError("Un '' dans la liste !")
    
    return l

def normalize_name(name,to_len):
    if len(name)>to_len:
        return name[:to_len-3]+"..."
    else:
        return name+" "*(to_len-len(name))

def get_line_with_name(name,max_len,seprator):
    t = ""
    cl = (max_len-len(name))//2
    t += seprator*cl
    t += name
    if (max_len-len(name))%2 == 1:
        cl += 1
    t += seprator*cl
    return t
    
def normalize_number(n,to_len):
    if type(n) == str:
        try:
            n = float(n)
        except:
            return normalize_name(n,to_len)
    s = str(round(n,3))
    if len(s)>to_len:
        return s[:to_len]
    else:
        return s+" "*(to_len-len(s))
    
def note_max_ue(nom_mat):
    num_max = None
    for num in etudient.keys():
        if num_max==None:
            if nom_mat in etudient[num].keys():
                num_max = num
        else:
            if nom_mat in etudient[num].keys():
                if etudient[num][nom_mat][0]>etudient[num_max][nom_mat][0]:
                    num_max = num
    return num_max
        
def update_etu(e):
    """ Fonction qui calcule la moyenne pour chaque bloc,ue """
    for ue in dict_ue.keys():
        uid = dict_ue[ue][0]
        sigma = 0
        sigma_coef = 0
        for mat in dict_mat.keys():
            mat_uid = dict_mat[mat][1]
            if uid == mat_uid and mat in etudient[e]:
                coef = dict_mat[mat][2]
                sigma_coef += coef
                note = etudient[e][mat][0]
                sigma += note*coef
        if sigma_coef != 0:
            sigma = sigma/sigma_coef
            etudient[e]["_UE_"+ue] = [sigma]
    
    big_sigma = 0
    big_sigma_coef = 0
    for bc in dict_bloc.keys():
        bid = dict_bloc[bc][0]
        sigma = 0
        sigma_coef = 0
        for ue in dict_ue.keys():
            ue_bid = dict_ue[ue][1]
            if bid == ue_bid and ("_UE_"+ue) in etudient[e]:
                coef = dict_ue[ue][2]
                sigma_coef += coef
                note = etudient[e]["_UE_"+ue][0]
                sigma += note*coef
        if sigma_coef != 0:
            sigma = sigma/sigma_coef
            etudient[e]["_BLOC_"+bc] = [sigma]
            bcoef = dict_bloc[bc][1]
            big_sigma_coef += bcoef
            big_sigma += sigma*bcoef
    if big_sigma_coef != 0:
         etudient[e]["_MOY_GE_"] = [big_sigma/big_sigma_coef]
         
def draw_table_row(row_name,name_space,l,l_space,colomn_count):
    print(normalize_name(row_name,name_space),"|",end="")
    for i in range(colomn_count):
        if i > len(l)-1:
            e = "#"*l_space
        else:
            e = l[i]
        print(normalize_name(e,l_space),"|",end="")
    print("")
    
def normalize_note_to_str(l,d):
    nl = []
    for e in l:
        if type(e)==str:
            try:
                nl.append(str(round(float(e),d)))
            except:
                nl.append(e)
        else:
            nl.append(str(round(e,d)))
    return nl
             
def print_etu(e):
    if e not in etudient:
        print("Erreur : Etudient non trouvé !")
        return
    print(str_color("NUMERO ETUDIENT N°= "+e+" "+get_cmi_status(e),BLUE))
    for bl in dict_bloc.keys():
        bid = dict_bloc[bl][0]
        
        print_color(get_line_with_name("Bloc "+bl,80,"="),BLUE)
        
        print(str_color("| ",BLUE),end="")
        moy = etudient[e]["_BLOC_"+bl][0]
        c = RED
        if moy>10.0 :
            c = GREEN
        print_color("MOYENNE : "+str(round(moy,3)),c)
        
        for ue in dict_ue.keys():
            print(BLUE,end="")
            uid = dict_ue[ue][0]
            ue_bid = dict_ue[ue][1]
            if bid == ue_bid:
                if ("_UE_"+ue) in etudient[e]:
                    note = str(round(etudient[e]["_UE_"+ue][0],3))
                    c = GREEN
                    if etudient[e]["_UE_"+ue][0] < 10:
                        c = YELLOW
                    print("| #"+get_line_with_name("UE "+ue,77,"-"))
                    print("| | MOYENNE : "+note+" | COEF : "+str(int(dict_ue[ue][2])))
                    colomn_count = 5
                    name_len = 39
                    elem_len = 5
                    print("| | ",end="")
                    draw_table_row("NOM MATIERE",name_len,["COEF.","MOY."]+["CC"+str(i) for i in range(1,colomn_count)],elem_len,colomn_count)
                    for m in dict_mat.keys():
                        mat_uid = dict_mat[m][1]
                        if mat_uid == uid:
                            print("| | ",end="")
                            draw_table_row(m,name_len,[str(int(dict_mat[m][2]))]+normalize_note_to_str(etudient[e][m],2),elem_len,colomn_count)
                else:
                    print_color("| #"+get_line_with_name("UE "+ue,77,"-"),YELLOW)
    print("="*80)
    print_color("MOYENNE GENERAL : "+str(round(etudient[e]["_MOY_GE_"][0],3))+"/20",BLUE)
    print(RESET)

        
        
def print_etu_old(e):
    print("NUMERO ETUDIENT :N°=",e,get_cmi_status(e))
    print(normalize_name("NOM UE",40),"|",end="")
    colomn_count = 4
    for i in range(colomn_count):
        note = "CC"+str(i)
        if i==0:
            note = "MOYENNE"
        print(normalize_name(note,10),"|",end="")
    print("")
    print("-"*100)
    for u in etudient[e].keys():
        print(normalize_name(u,40),"|",end="")
        for note in etudient[e][u]:
            print(normalize_number(note,10),"|",end="")
        for i in range(colomn_count-len(etudient[e][u])):
            print("###########|",end="")
        print("")     


def add_bloc(nom,id,coef):
    dict_bloc[nom] = (int(id),float(coef))
    
def add_ue(nom,id,id_bloc,coef):
    dict_ue[nom] = (int(id),int(id_bloc),float(coef))
    
def add_mat(nom,id,id_ue,coef):
    dict_mat[nom] = (int(id),int(id_ue),float(coef))
        
def read_data_info():
    rv = ""
    with open(dossier_note+"/data.txt","r",encoding="utf-8") as file:
        t = file.read()
    lines = t.split("\n")
    for l in lines:
        if l == "":
            continue
        if l[0] == "#" or l[0] == " " :
            continue
        
        head = l[:3]
        tail = l[3:].split(";")
        
        if head == "-B ":
            nom,idb,coef = tail
            add_bloc(nom,idb,coef)
            
        if head == "-U ":
            nom,idu,idb,coef = tail
            add_ue(nom,idu,idb,coef)
            
        if head == "-M ":
            nom,idm,idu,coef = tail
            add_mat(nom,idm,idu,coef)
            
        if head == "-I ":
            nom = tail[0]
            ignore_list.append(nom)
            
        if head == "-W ":
            if tail[0] == "ACCEPTER":
                rv = "ACCEPTER"
            
    return rv
            
def append_to_data(txt):
    with open(dossier_note+"/data.txt","a",encoding="utf-8") as file:
        file.write("\n"+txt)
            
def add_mat_data(nom,id,id_ue,coef):
    t = [nom,str(id),str(id_ue),str(coef)]
    append_to_data("-M "+";".join(t))
    add_mat(nom,id,id_ue,coef)

def find_clear_id():
    i = 0
    for cmat in dict_mat.keys():
        if dict_mat[cmat][0] == i:
            i+=1
    return i

dict_bloc = {}
dict_ue = {}
dict_mat = {}
ignore_list = []

etudient = {}

waiting = read_data_info()
premier_utilsation = waiting==""

while waiting.lower() != "accepter":
    print_color("""Avertissement légal et conditions d'utilisation

    Ce logiciel est conçu pour un USAGE PERSONNEL UNIQUEMENT.
    Les informations et méthodes utilisées dans ce logiciel sont basées sur des données PUBLIQUES 
    (disponibles notamment sur https://mathinfo.unistra.fr/). EN REVANCHE, LES DONNÉES TRAITÉES 
    PAR CE LOGICIEL (notes, numéros d'étudiant, etc.) SONT DES DONNÉES PERSONNELLES PROTÉGÉES PAR
    LE RGPD ET LA LOI N°78-17 du 6 janvier 1978.

    L'AUTEUR DÉCLINE TOUTE RESPONSABILITÉ EN CAS DE :
    - Fuite, utilisation ou publication non autorisée des données traitées par ce logiciel.
    - Violation de la vie privée ou des droits des personnes concernées par les données.
    - Non-respect du Règlement Général sur la Protection des Données (RGPD) ou des lois nationales
    applicables.

    L'UTILISATEUR S'ENGAGE À :
    1. Respecter le RGPD et la Loi n°78-17 du 6 janvier 1978 relative à l'informatique, aux 
    fichiers et aux libertés.
    2. Ne pas utiliser ce logiciel pour traiter des données personnelles SANS LE CONSENTEMENT
    EXPLICITE des personnes concernées.
    """,RED)
    waiting = input(RED+"POUR CONTINUER ET APRÈS AVOIR LU LES AVERTISSEMENTS ET CONDITIONS D'UTILISATION, tapez 'accepter' :\n")

if premier_utilsation:
    append_to_data("-W ACCEPTER")
    
print(RESET,end="")

def get_cmi_status(etu):
    return ""

liste_mat = []

pile_traitement = listedirectory(dossier_note)


for e in pile_traitement:
    
    file_type = e.split(".")[-1]
    
    if file_type != "pdf":
        continue

    nom_mat = e.split("/")[-1].split(".")[0].strip()
    liste_mat.append(nom_mat)
    
    print("Traitement de",nom_mat+".pdf ...")
    
    # Ajout des manière non reconue
    if nom_mat not in dict_mat:
        if nom_mat in ignore_list:
            continue
        print("---- Ajout d'une matière ----")
        print("Nom :",nom_mat)
        print("Choix de l'UE à relier :")
        for cmat in dict_ue.keys():
            print("|-",dict_ue[cmat][0],":",cmat)
        mid = find_clear_id()
        uid = input("Saisir le numéro de l'UE (# pour ignorer l'ajout) :")
        if uid == "#":
            append_to_data("-I "+nom_mat)
            continue
        uid = int(uid)
        coef = float(input("Saisir le coef de la matière :"))
        add_mat_data(nom_mat,mid,uid,coef)
    
    # Traitement du PDF
    txt = get_pdf_text(e)
    txt = txt.replace(",",".")
    txt = pretraitement_txt(txt)
    txt = get_note_and_header(txt)
    
    coefs = get_coefs_normalized(txt)
    
    listetu = txt.split("\n")
    listetu.pop(0)
    
    n = len(coefs)
    for etu in listetu:
        num,*notes = get_num_and_notes(etu,n)
        
        if num not in etudient:
            etudient[num]={}
        
        moy = 0
        for i in range(n):
            if notes[i]!="ABI" and notes[i]!="ABJ" and notes[i]!="DIS" and notes[i] != "SUBS":
                moy+= float(notes[i])*coefs[i]
        etudient[num][nom_mat] = [moy]+notes


for num in etudient.keys():
    update_etu(num)

if __name__ == "__main__":
    num_a_chercher = input("Votre numéro étudiant :")
    print_etu(num_a_chercher)
    print(RESET,end="")
