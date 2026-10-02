from __future__ import annotations


def mostrar_grafico(
    pontos: tuple[list[float], list[float]],
    vertice: tuple[float, float],
    raizes: tuple[complex, complex],
) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as erro:
        raise RuntimeError(
            "Matplotlib não está instalado. Instale com: python -m pip install matplotlib"
        ) from erro

    valores_x, valores_y = pontos
    plt.plot(valores_x, valores_y, label="f(x) = ax² + bx + c", color="darkcyan")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.scatter(*vertice, color="crimson", label="Vértice", zorder=3)

    raizes_reais = [
        raiz.real for raiz in raizes if abs(raiz.imag) < 1e-10
    ]
    if raizes_reais:
        plt.scatter(
            raizes_reais,
            [0] * len(raizes_reais),
            color="darkorange",
            label="Raízes reais",
            zorder=3,
        )

    plt.title("Gráfico da função quadrática")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()