#include <stdio.h>
int main() {
    int L;
    scanf("%d", &L);
    for (int i = 0; i < L; i++) {

        int x, y;

        scanf("%d %d", &x, &y);

        int sum = x + y;

        printf("%d\n", sum);

    }
    return 0;

}