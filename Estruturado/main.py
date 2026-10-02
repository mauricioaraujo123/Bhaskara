from calculos import (
    calcular_delta,
    calcular_pontos,
    calcular_raizes,
    calcular_vertice,
)
from entrada import obter_coeficientes
from grafico import mostrar_grafico
from resultados import exibir_resultados


def main() -> None:
    a, b, c = obter_coeficientes()
    delta = calcular_delta(a, b, c)
    raizes = calcular_raizes(a, b, delta)
    vertice = calcular_vertice(a, b, delta)
    pontos = calcular_pontos(a, b, c, vertice, raizes)

    exibir_resultados(delta, raizes, vertice)
    mostrar_grafico(pontos, vertice, raizes)


if __name__ == "__main__":
    main()