#include <iostream>

int main() {
    int L;
    std::cin >> L;

    for (int i = 0; i < L; i++) {
        int x, y;
        std::cin >> x >> y;
        int somme = x + y;
        std::cout << somme << std::endl;
    }
    return 0;
}