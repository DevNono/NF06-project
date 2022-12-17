from ctypes import alignment, c_int, cdll
from pathlib import Path
def open_dll(name= 'test.dll' ):
    dll_path = Path(__file__).parent / name
    return cdll.LoadLibrary(str(dll_path))


lib = open_dll()
Values = []
Weights = []
Price = []
Quantity = []

print("Veuillez indiquer le nombre de produits dans la commande :")
nb = int(input())
Number = c_int(nb) #On convertit le nombre de produits en entier C
print("Veuillez indiquer le poids maximum de la commande :")
C = int(input())
C = c_int(C) #On convertit le poids maximum en entier C
for i in range(nb):
    print("Veuillez indiquer la valeur UID du produit n°", i+1, " :")
    uid = int(input())
    print("Veuillez indiquer le prix du produit n°", i+1, " :")
    prix = int(input())
    print("Veuillez indiquer la quantité du produit n°", i+1, " :")
    quan = int(input())
    print("Veuillez indiquer le poids du produit n°", i+1, " :")
    poids = int(input())
    #On rempli les listes avec les valeurs entrées par l'utilisateur
    Values.append(uid)
    Weights.append(poids)              
    Price.append(prix)
    Quantity.append(quan)

Values = (c_int * len(Values))(*Values)
Weights = (c_int * len(Weights))(*Weights)     #On convertit les listes en tableaux C
Price = (c_int * len(Price))(*Price)  
Quantity = (c_int * len(Quantity))(*Quantity)  
    

lib.main(C, Number, Values, Weights, Price, Quantity, len(Values)) #On récupère le résultat de la fonction