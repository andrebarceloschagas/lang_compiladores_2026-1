# Código gerado pelo compilador MiniLang
import sys

def fatorial(n):
    if (n <= 1):
        return 1
    return (n * fatorial((n - 1)))

resultado = 0
resultado = fatorial(5)
print(resultado)