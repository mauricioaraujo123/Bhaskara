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


def obter_passo_a_passo_integral(
    a: float,
    b: float,
    c: float,
    raizes: tuple[complex, complex],
    vertice: tuple[float, float],
    volume: float,
) -> str:
    """Monta a explicação da integral usada no volume de revolução."""
    esquerda, direita = sorted(
        raiz.real for raiz in raizes if math.isclose(raiz.imag, 0.0, abs_tol=1e-10)
    )
    y_min, y_max = sorted((0.0, vertice[1]))
    discriminante = b**2 - 4 * a * (c - y_max)
    return (
        "PASSO A PASSO DO VOLUME POR INTEGRAIS\n\n"
        f"1) Função: f(x) = {a:.6g}x² + {b:.6g}x + {c:.6g}\n"
        f"   Limites em x: x₁ = {esquerda:.6g} e x₂ = {direita:.6g}.\n"
        f"   A região fechada percorre y de {y_min:.6g} até {y_max:.6g}.\n\n"
        "2) Ao girar em torno do eixo Y, usamos seções horizontais (anéis):\n"
        "   V = ∫ π [R(y)² - r(y)²] dy.\n\n"
        "3) Isolando x na parábola:\n"
        f"   x₋(y) = (-b - √(b² - 4a(c-y))) / (2a)\n"
        f"   x₊(y) = (-b + √(b² - 4a(c-y))) / (2a)\n"
        f"   Neste intervalo, o discriminante é {discriminante:.6g} no topo.\n\n"
        "4) Para cada altura y, calculamos os raios:\n"
        "   R(y) = maior distância até o eixo Y;\n"
        "   r(y) = menor distância (0 quando o segmento cruza o eixo Y).\n"
        "   Assim, a integral usada numericamente é:\n"
        f"   V = ∫[{y_min:.6g}, {y_max:.6g}] π(R(y)² - r(y)²) dy.\n\n"
        "5) Aplicamos a regra de Simpson com 1000 subdivisões pares:\n"
        "   V ≈ (h/3)[g₀ + gₙ + 4Σgᵢ(índices ímpares) + 2Σgᵢ(índices pares)],\n"
        "   onde g(y) = π(R(y)² - r(y)²).\n\n"
        f"6) Resultado: V ≈ {volume:.10g} unidades cúbicas."
    )