# Código gerado pelo compilador MiniLang
import sys

idade = 0
maior = 0
idade = int(input())
if (idade >= 18):
    maior = True
    print("Maior de idade")
else:
    maior = False
    print("Menor de idade")