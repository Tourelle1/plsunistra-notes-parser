# plsunistra-notes-parser

Script Python pour analyser et organiser automatiquement ses notes à l'Université de Strasbourg (Au PLS) : extraction depuis les PDF, classement par blocs, UE et matières.
Note : Ce scrpit a uniquement été testé pour les document de note du PLS au L1 de Math-Info

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


COMMENT UTILISER : 
(0.) Télecharger pypdf :
Sur linux : 
- Sur VS Code (Recomendé) : Dans le terminal : "sudo apt install pip3" puis dans la console VS Code : "pip3 install pypdf"
- Sur l'environement : "sudo apt install python3-pypdf" dans le terminal
Sur Windows : Tout simplement télécharchger via le CMD avec "pip install pypdf"
1. Aller sur Seafile et télécharger en entier le dossier "Résultat" dans L1-MI
2. Décompresser le fichier, et y ajouter dedans le ficher data.txt qui contient les information concernant les coefs ect...
3. Changer le chemain d'accès au dossier des notes (A noter que sur windows les / simple fonctionent également sur VS Code)
4. Exectuer et entrer votre numéro étudiant