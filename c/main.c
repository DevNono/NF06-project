#include<stdio.h>
int max(int a, int b) { return (a > b)? a : b; }
int C(int W, int wt[], int val[], int n)
{
   int i, w;
   int K[n+1][W+1];
   for (i = 0; i <= n; i++)
   {
       for (w = 0; w <= W; w++)
       {
           if (i==0 || w==0)
               K[i][w] = 0;
           else if (wt[i-1] <= w)
                 K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]],  K[i-1][w]);
                 
           else
                 K[i][w] = K[i-1][w];
       }
   }
   return K[n][W];
}
int main()
{
    int i, n, val[20], wt[20], W;
    
    printf("Entrez le nombre de produit:");
    scanf("%d", &n);
    
    printf("Entrez le nombre et le poids de chaque items:\n");
    for(i = 0;i < n; ++i){
     scanf("%d%d", &val[i], &wt[i]);
    }
 
    printf("Entrez la taille C:");
    scanf("%d", &W);
    
    printf("%d\n", C(W, wt, val, n));
    printf("Les produits choisis présent dans la commande C sont:\n");
    

    return 0;
}