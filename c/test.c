#include <stdio.h>
#include <stdlib.h>
typedef struct {
    char *name;
    int poids;
    int val;
    int nombre;
} item_t;  // Structure d'un item

item_t items[] = {                                              // Liste d'items pour le théorème du sac à dos*
    {"map",                      9,   150,   1},                // De formes ("Nom", Poids, valeur, nombre (= quantité))
    {"compass",                 13,    35,   1},
    {"water",                  153,   200,   2},
    {"sandwich",                50,    60,   2},
    {"glucose",                 15,    60,   2},
    {"tin",                     68,    45,   3},
    {"banana",                  27,    60,   3},
    {"apple",                   39,    40,   3},
    {"cheese",                  23,    30,   1},
    {"beer",                    52,    10,   3},
    {"suntan cream",            11,    70,   1},
    {"camera",                  32,    30,   1},
    {"T-shirt",                 24,    15,   2},
    {"trousers",                48,    10,   2},
    {"umbrella",                73,    40,   1},
    {"waterproof trousers",     42,    70,   1},
    {"waterproof overclothes",  43,    75,   1},
    {"note-case",               22,    80,   1},
    {"sunglasses",               7,    20,   1},
    {"towel",                   18,    12,   2},
    {"socks",                    4,    50,   1},
    {"book",                    30,    10,   2},
};

int n = sizeof (items) / sizeof (item_t);

int *knapsack (int w) { // On réalise le théroème du sac à dos
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
        for (k = 0; v != m[i - 1][j] + k * items[i - 1].val; k++) {
            s[i - 1]++;
            j -= items[i - 1].poids; // On met à jour le poids du sac
        }
    }
    free(mm);
    free(m);  // On libère la mémoire
    return s;
}

int main () {
    int C = 400;
    int *s;
    s = knapsack(C); // On réalise le théorème du sac à dos
    int i, tc = 0, tw = 0, tv = 0;
    for (i = 0; i < n; i++) {
        if (s[i]) {
            printf("%-22s %5d %5d %5d\n", items[i].name, s[i], s[i] * items[i].poids, s[i] * items[i].val); // On affiche les items choisis
            tc += s[i];
            tw += s[i] * items[i].poids;
            tv += s[i] * items[i].val;
        }
    }
    printf("%-22s %5d %5d %5d\n", "nombre, poids, val:", tc, tw, tv); // On affiche le nombre, le poids et la valeur totale
    return 0;
}