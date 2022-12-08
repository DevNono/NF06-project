from ctypes import *
from pathlib import Path
print("Test\n")
def open_dll(name= 'test.dll' ):
    dll_path = Path(__file__).parent / name
    return cdll.LoadLibrary(str(dll_path))

print("Test\n")

list_nom = (c_wchar_p * 20)()
list_prix = (c_int * 3)()
list_poids = (c_int * 3)()
list_quantite = (c_int * 3)()
    

if __name__ ==  '__main__' :
    dll = open_dll()
    print("combien de produits voulez vous ajouter ?")
    count = 1
    list_nom[0] =  'arbres'
    list_prix[0] = 1
    list_poids[0] = 3
    list_quantite[0] = 2
    print("Test")
    dll.main(count, pointer(list_nom), pointer(list_prix), pointer(list_poids), pointer(list_quantite))