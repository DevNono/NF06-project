#include<stdio.h>
#include<stdlib.h>
struct lien
{
	int x;
	struct lien *suivant;
};
typedef struct lien noeud;
int main()

{
	int *w,*v, *can,n,c,*t,i,x, quan;
	noeud **s,*new;
	printf("\nEntrer le nombre total d'objets :");
	scanf("%d",&n);
	w=(int *)malloc(n*(sizeof(int)));
	v=(int *)malloc(n*(sizeof(int)));
	can=(int *)malloc(n*(sizeof(int)));
	printf("\nEntrer le poids et la valeur et la quantite de chaque produit:");
	for(i=0;i<n;i++)
	{
		printf("\nEntrer le poids du produit-%d :",i+1);
		scanf("%d",&w[i]);
		printf("\nEntrer sa valeur-%d :",i+1);
		scanf("%d",&v[i]);
		printf("\nEntrer sa quantite-%d :",i+1);
		scanf("%d",&can[i]);

		printf("Produit-%d\tPoids-%d\tvaleur-%d\tquantite-%d\n",i+1,w[i],v[i],can[i]);
	}


	
	printf("\nEntrer la capacite du sac a dos :");
	scanf("%d",&c);
	t=(int *)malloc((c+1)*(sizeof(int)));
	s=(noeud **)malloc((c+1)*(sizeof(noeud *)));
	t[0]=0;
	s[0]=NULL;
	for(x=1;x<=c;x++)
	{
		t[x]=0;
		s[x]=NULL;
		//printf("%d\t%d\n",x,t[x]);
		for(i=0;i<n;i++)
		{
			if(w[i]<=x && can[i]>0)
			{
				
				
				if((t[x-w[i]]+v[i])>t[x])
				{
					t[x]=t[x-w[i]]+v[i];
					//printf("%d\n",t[x]);
					s[x]=s[x-w[i]];
					new=(noeud *)malloc(1*(sizeof(noeud)));
					new->x=i;
					new->suivant=s[x];
					s[x]=new;
				}
				
			}
			
		}
		//printf("%d\t%d\n",x,t[x]);
	}
	printf("\nLa valeur totale des produits dans le sac A dos sont equivalentes à %d.\nLe sac a dos contient les produits suivants :\n",t[c]);
	while(s[c]!=NULL)
	{
		printf("Produit-%d\n",(s[c]->x)+1);
		s[c]=s[c]->suivant;
	}
}