from __future__ import annotations


def _formatar_numero(valor: complex) -> str:
    if isinstance(valor, complex):
        if abs(valor.imag) < 1e-10:
            return f"{valor.real:.6g}"
        sinal = "+" if valor.imag >= 0 else "-"
        return f"{valor.real:.6g} {sinal} {abs(valor.imag):.6g}i"
    return f"{valor:.6g}"


def exibir_resultados(
    delta: float,
    raizes: tuple[complex, complex],
    vertice: tuple[float, float],
) -> None:
    print(f"\nDelta: {_formatar_numero(delta)}")
    if delta < 0:
        print("A equação não possui raízes reais.")
        print(f"Raízes complexas: x1 = {_formatar_numero(raizes[0])}; "
              f"x2 = {_formatar_numero(raizes[1])}")
    else:
        print(f"Raízes: x1 = {_formatar_numero(raizes[0])}; "
              f"x2 = {_formatar_numero(raizes[1])}")
    print(
        "Vértice: "
        f"({ _formatar_numero(vertice[0])}, {_formatar_numero(vertice[1])})"
    )