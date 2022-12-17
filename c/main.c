#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char *name;
    int poids;
    int val;
    int nombre;
} item_t;  // Structure d'un item

int *knapsack (int w, int n, item_t* items) { // On réalise le théroème du sac à dos
    int i, j, k, v, *mm, **m, *s; // On déclare les variables
    mm = calloc((n + 1) * (w + 1), sizeof (int));
    m = malloc((n + 1) * sizeof (int *));
    m[0] = mm;
    for (i = 1; i <= n; i++) {  // On parcourt la liste d'items
        m[i] = &mm[i * (w + 1)];
        for (j = 0; j <= w; j++) {
            m[i][j] = m[i - 1][j];
            for (k = 1; k <= items[i - 1].nombre; k++) {
                if (k * items[i - 1].poids > j) { // Si le poids de l'item est supérieur au poids du sac
                    break;
                }
                v = m[i - 1][j - k * items[i - 1].poids] + k * items[i - 1].val; // On calcule la valeur de l'item
                if (v > m[i][j]) {
                    m[i][j] = v; // On met à jour la valeur de l'item
                }
            }
        }
    }
    s = calloc(n, sizeof (int));
    for (i = n, j = w; i > 0; i--) {
        int v = m[i][j];
        int quantity = items[i - 1].nombre;
        for (k = 0; v != m[i - 1][j] + k * items[i - 1].val; k++) {
            if (quantity != 0) {
                s[i - 1]++;
                j -= items[i - 1].poids; // On met à jour le poids du sac
                quantity--;
            }
        }
    }
    free(mm);
    free(m);  // On libère la mémoire
    return s;
}


int main (int C, int number,int *name_item,int *poids_item_list,int *val_item,int *quantity_item) {    // On récupère les données venant de python
    char UID[100];
    int n;
    item_t items[number];
    for (int i=0;i<number;i++){
        sprintf(UID, "%d", name_item[i] );
        items[i].name= UID;
        items[i].poids=poids_item_list[i];  
        items[i].val=val_item[i];
        items[i].nombre=quantity_item[i];
        printf("%-22d %5d %5d %5d\n", name_item[i], items[i].nombre, items[i].poids, items[i].val);
    }
    n = number;
    int *s;
    s = knapsack(C, n, items); // On réalise le théorème du sac à dos
    int i, tc = 0, tw = 0, tv = 0;
    for (i = 0; i < n; i++) {
        if (s[i]) {
            printf("%-22d %5d %5d %5d\n", name_item[i], s[i], s[i] * items[i].poids, s[i] * items[i].val); // On affiche les items choisis
            tc += s[i];
            tw += s[i] * items[i].poids;
            tv += s[i] * items[i].val;
        }
    }
    printf("%-22s %5d %5d %5d\n", "nombre, poids, val:", tc, tw, tv); // On affiche le nombre, le poids et la valeur totale
    free(s);
    return 0;
}