from ctypes import alignment, c_int, cdll, POINTER, Structure # Pour utiliser les fonctions C et que Ctypes puisse les utiliser
from pathlib import Path  # Pour trouver le chemin du fichier DLL


def open_dll(name='test.dll'):   #On ouvre le fichier DLL
    dll_path = Path(__file__).parent / name
    return cdll.LoadLibrary(str(dll_path))


lib = open_dll() # On ouvre le fichier DLL
Values = [] # On crée les listes qui contiendront les valeurs entrées par l'utilisateur
Weights = []
Price = []
Quantity = []

print("Veuillez indiquer le nombre de produits dans la commande :")
nb = int(input())
Number = c_int(nb)  # On convertit le nombre de produits en entier C
print("Veuillez indiquer le poids maximum de la commande :")
C = int(input())
C = c_int(C)  # On convertit le poids maximum en entier C
for i in range(nb):
    print("Veuillez indiquer la valeur UID du produit n°", i+1, " :")
    uid = int(input())
    print("Veuillez indiquer le prix du produit n°", i+1, " :")
    prix = int(input())
    print("Veuillez indiquer la quantité du produit n°", i+1, " :")
    quan = int(input())
    print("Veuillez indiquer le poids du produit n°", i+1, " :")
    poids = int(input())
    # On rempli les listes avec les valeurs entrées par l'utilisateur
    Values.append(uid)
    Weights.append(poids)
    Price.append(prix)
    Quantity.append(quan)

Values = (c_int * len(Values))(*Values)
# On convertit les listes en tableaux C
Weights = (c_int * len(Weights))(*Weights)
Price = (c_int * len(Price))(*Price)
Quantity = (c_int * len(Quantity))(*Quantity)


lib.main(C, Number, Values, Weights, Price, Quantity, len(
    Values)) # On appelle la fonction main du fichier DLL, on réalise ainsi le théorème de Knapsack (du sac à dos)

lib.Getaray.restype = POINTER(c_int)  # On indique le type de résultat de la fonction Getaray
result = lib.Getaray() # On récupère le tableau de produits mis à jour
print("|----------------------------------------|")
print("|  La liste de produits mise à jour est :|")
print("|UID produit:    quantite: poids: valeur:|")
for i in range(nb):
    print('|%-22s' % Values[i], '%5d' %
          result[i], '%5d' % Weights[i], '%5d|' % Price[i]) # On affiche le tableau de résultat

lib.free_array(result)  # On libère le tableau de résultat
