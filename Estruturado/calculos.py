from __future__ import annotations

import math


def calcular_delta(a: float, b: float, c: float) -> float:
    return b**2 - 4 * a * c


def calcular_raizes(a: float, b: float, delta: float) -> tuple[complex, complex]:
    raiz_delta = complex(delta, 0) ** 0.5
    denominador = 2 * a
    return (
        (-b + raiz_delta) / denominador,
        (-b - raiz_delta) / denominador,
    )


def calcular_vertice(a: float, b: float, delta: float) -> tuple[float, float]:
    x_vertice = -b / (2 * a)
    y_vertice = -delta / (4 * a)
    return x_vertice, y_vertice


def calcular_pontos(
    a: float,
    b: float,
    c: float,
    vertice: tuple[float, float],
    raizes: tuple[complex, complex],
    quantidade: int = 201,
) -> tuple[list[float], list[float]]:
    x_vertice = vertice[0]
    raizes_reais = [
        raiz.real for raiz in raizes if math.isclose(raiz.imag, 0.0, abs_tol=1e-10)
    ]
    amplitude = max(
        [5.0, *(abs(raiz - x_vertice) * 1.2 for raiz in raizes_reais)]
    )
    inicio = x_vertice - amplitude
    passo = 2 * amplitude / (quantidade - 1)
    valores_x = [inicio + indice * passo for indice in range(quantidade)]
    valores_y = [a * x**2 + b * x + c for x in valores_x]
    return valores_x, valores_y