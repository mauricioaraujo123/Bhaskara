from __future__ import annotations

import math


def _ler_numero(nome: str) -> float:
    while True:
        try:
            valor = float(input(f"Digite o coeficiente {nome}: "))
        except ValueError:
            print("Entrada inválida. Digite um número.")
            continue

        if not math.isfinite(valor):
            print("O valor precisa ser um número finito.")
            continue
        return valor


def obter_coeficientes() -> tuple[float, float, float]:
    while True:
        a = _ler_numero("a")
        if a != 0:
            break
        print("O coeficiente a não pode ser zero em uma equação do 2º grau.")

    b = _ler_numero("b")
    c = _ler_numero("c")
    return a, b, c
