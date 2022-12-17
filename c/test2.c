#include <stdio.h>
#include <stdlib.h>

// Test afin de faire fonctionner ctypes avec python et des listes

void test(int *arr, int *poids, int size) {
	for (int i = 0; i < size; i++) {
		printf("%d ", arr[i]);
		printf("%d \n", poids[i]);
	}
	printf("\n");
}