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


def calcular_volume_revolucao(
    a: float,
    b: float,
    c: float,
    raizes: tuple[complex, complex],
    subdivisoes: int = 1000,
) -> float:
    """Calcula o volume da região entre a parábola e o eixo X, girada no eixo Y."""
    raizes_reais = sorted(
        raiz.real for raiz in raizes if math.isclose(raiz.imag, 0.0, abs_tol=1e-10)
    )
    if len(raizes_reais) != 2:
        raise ValueError("O volume só pode ser calculado com duas raízes reais.")
    if subdivisoes < 2 or subdivisoes % 2:
        raise ValueError("O número de subdivisões precisa ser par e maior que 1.")

    y_vertice = -(b**2 - 4 * a * c) / (4 * a)
    y_inicio, y_fim = sorted((0.0, y_vertice))
    passo = (y_fim - y_inicio) / subdivisoes

    def area_secao(y: float) -> float:
        discriminante = b**2 - 4 * a * (c - y)
        raiz = math.sqrt(max(0.0, discriminante))
        x_esquerda = (-b - raiz) / (2 * a)
        x_direita = (-b + raiz) / (2 * a)
        limite_inferior, limite_superior = sorted((x_esquerda, x_direita))
        raio_externo = max(abs(limite_inferior), abs(limite_superior))
        raio_interno = (
            0.0
            if limite_inferior <= 0 <= limite_superior
            else min(abs(limite_inferior), abs(limite_superior))
        )
        return math.pi * (raio_externo**2 - raio_interno**2)

    soma = area_secao(y_inicio) + area_secao(y_fim)
    for indice in range(1, subdivisoes):
        peso = 4 if indice % 2 else 2
        soma += peso * area_secao(y_inicio + indice * passo)
    return soma * passo / 3