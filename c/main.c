/**
 * @file main.c
 * @author Gaudry Carlier and Noé Landré
 * @brief Fichier contenant le code c du programme 
 * @version 1.0
 * @date 2022-12-19
 * 
 * @copyright Copyright (c) 2022
 * 
 */

#include <stdio.h>
#include <stdlib.h>  // On inclut les librairies
#include <string.h>
#include <time.h>

typedef struct 
{
    char *name; /* une valeur en chaine de caractère*/
    int poids; /* Valeur entiere*/
    int val; /* Valeur entiere*/
    int nombre; /* Valeur entiere*/
} item_t; // Structure d'un item
/**
 * @brief 
 * 
 * @param w poids du sac
 * @param n nombre d'items
 * @param items liste des items 
 * @return int* liste des items
 */
int *knapsack(int w, int n, item_t *items) 
{                                                // On réalise le théroème du sac à dos
    int i, j, k, v, *mm, **m, *s;                // On déclare les variables
    mm = calloc((n + 1) * (w + 1), sizeof(int)); // On alloue la mémoire
    m = malloc((n + 1) * sizeof(int *));
    m[0] = mm;
    for (i = 1; i <= n; i++)
    { // On parcourt la liste d'items
        m[i] = &mm[i * (w + 1)];
        for (j = 0; j <= w; j++)
        {
            m[i][j] = m[i - 1][j];
            for (k = 1; k <= items[i - 1].nombre; k++)
            {
                if (k * items[i - 1].poids > j)
                { // Si le poids de l'item est supérieur au poids du sac
                    break;
                }
                v = m[i - 1][j - k * items[i - 1].poids] + k * items[i - 1].val; // On calcule la valeur de l'item avec le tri dynamique
                if (v > m[i][j])
                {
                    m[i][j] = v; // On met à jour la valeur de l'item
                }
            }
        }
    }
    s = calloc(n, sizeof(int));
    for (i = n, j = w; i > 0; i--)
    {
        int v = m[i][j];
        int quantity = items[i - 1].nombre;
        for (k = 0; v != m[i - 1][j] + k * items[i - 1].val; k++)
        {
            if (quantity != 0)
            { // Si la de l'item est nul, on passe à l'item suivant
                s[i - 1]++;
                j -= items[i - 1].poids; // On met à jour le poids du sac
                quantity--;
            }
        }
    }
    free(mm);
    free(m); // On libère la mémoire
    return s; // On retourne la liste des items
}

int number_arr = 0;
int quantite_update[500];

/**
 * @brief Fonction principale
 * 
 * @param C poids maximum du camion
 * @param number nombre d'items
 * @param name_item liste des noms des items
 * @param poids_item_list liste des poids des items
 * @param val_item liste des prix des items
 * @param quantity_item liste des quantités des items
 * @return int 0
 * 
 */
int main(int C, int number, int *name_item, int *poids_item_list, int *val_item, int *quantity_item)
{   
    // On cherche la date et l'heure actuelle
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    // On ouvre le fichier de sauvegarde dans un dossier spécifique
    char chemin[100] = "C:\\Users\\Public\\Documents\\";// On crée le chemin du fichier de sauvegarde
    strcat(chemin,"sauvegarde_");// On ajoute le nom du fichier de sauvegarde
    char date[100];// On crée la variable date
    sprintf(date, "%d-%d-%d_%d-%d", tm.tm_mday, tm.tm_mon + 1,tm.tm_year + 1900 , tm.tm_hour, tm.tm_min);// On transforme les entiers en chaine de caractère pour la date
    strcat(chemin, date); // On ajoute la date et l'heure actuelle au nom du fichier de sauvegarde
    strcat(chemin, ".txt"); // On ajoute l'extension .txt au fichier de sauvegarde
    FILE *fichier = fopen(chemin, "w");         // On ouvre le fichier de sauvegarde
    fprintf(fichier, "Liste de produits partant: \n"); // On écrit dans le fichier de sauvegarde
    char UID[100]; // On transforme les entiers en chaine de caractère pour l'UID
    int n;
    number_arr = number; // On met à jour le nombre d'items grâce à cette variable
    item_t items[number];
    printf("\n\n\nVoici les informations suivantes:   \n");
    printf(" Poids maximum du camion: %d\n", C);
    printf(" Nombre d'items de la commande: %d\n", number); // On affiche les informations dans le terminal et dans le fichier de sauvegarde
    fprintf(fichier, "Poids maximum du camion: %d\n", C);
    printf("|----------------------------------------|\n");
    printf("|                 Resume                 |\n");// On affiche le tableau des items en version terminal et dans le fichier de sauvegarde
    printf("|UID produit:    quantite: poids: valeur:|\n");
    printf("|----------------------------------------|\n");
    for (int i = 0; i < number; i++)
    {
        sprintf(UID, "%d", name_item[i]);
        items[i].name = UID;
        items[i].poids = poids_item_list[i];
        items[i].val = val_item[i];
        items[i].nombre = quantity_item[i];
        printf("|%-22d %5d %5d %5d|\n", name_item[i], items[i].nombre, items[i].poids, items[i].val);
    }
    printf("|----------------------------------------|\n\n\n");
    printf("|----------------------------------------|\n");
    printf("|        Liste de produits partant       |\n");//Affichage du tableau des items dans le terminal
    printf("|UID produit:    quantite: poids: valeur:|\n");
    printf("|----------------------------------------|\n");
    fprintf(fichier, "|----------------------------------------|\n");
    fprintf(fichier, "|        Liste de produits partant       |\n");//Affichage du tableau des items dans le fichier de sauvegarde.txt
    fprintf(fichier, "|UID produit:    quantite: poids: valeur:|\n");
    fprintf(fichier, "|----------------------------------------|\n");
    n = number;
    int *s;
    s = knapsack(C, n, items); // On réalise le théorème du sac à dos
    int i, nb_item = 0, tc = 0, tw = 0, tv = 0; /**
     * @brief 
     * @param i
     * @param nb_item
     * @param tc
     * @param tw
     * @param tv
     */
    for (i = 0; i < n; i++)
    {
        int condition = 0;
        if (s[i])
        {
            printf("|%-22d %5d %5d %5d|\n", name_item[i], s[i], s[i] * items[i].poids, s[i] * items[i].val);           // On affiche les items choisis
            fprintf(fichier, "|%-22d %5d %5d %5d|\n", name_item[i], s[i], s[i] * items[i].poids, s[i] * items[i].val); // On affiche les items choisis
            tc += s[i];
            tw += s[i] * items[i].poids;
            tv += s[i] * items[i].val;
            condition = 1;
            nb_item++;
        }
        if (condition == 1) // On met à jour la quantité de chaque item pour ainsi les envoyer à python
        {
            quantite_update[i] = items[i].nombre - s[i];
        }
        else
        {
            quantite_update[i] = items[i].nombre;   // On met à jour la quantité de chaque item pour ainsi les envoyer à python
        }
    }

    printf("|----------------------------------------|\n");
    printf("|%-22s %5d %5d %5d|\n", "Total:", tc, tw, tv); // On affiche le nombre, le poids et la valeur totale
    printf("|----------------------------------------|\n\n\n");
    fprintf(fichier, "|----------------------------------------|\n");
    fprintf(fichier, "|%-22s %5d %5d %5d|\n", "Total:", tc, tw, tv); // On affiche le nombre, le poids et la valeur totale
    fprintf(fichier, "|----------------------------------------|\n\n");
    printf("Nombre d'items differents partant: %d\n\n", nb_item);         // On affiche le nombre d'items partant
    fprintf(fichier, "Nombre d'items differents partant: %d\n", nb_item); // On affiche le nombre d'items partant
    free(s);
    fclose(fichier);
    return 0;
}

/**
 * @brief Construit le tableau de la quantité de chaque item
 * 
 * @return int* Tableau de la quantité de chaque item
 * 
 */
int *Getaray()
{
    int *arr = malloc(number_arr * sizeof(int));

    for (int i = 0; i < number_arr; i++)
    {
        arr[i] = quantite_update[i];
    }
    return arr;
}

/**
 * @brief Libère la mémoire
 * @param arr
 * @return int 
 * 
 */
void free_array(int *arr)
{
    free(arr);
}