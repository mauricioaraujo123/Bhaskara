from __future__ import annotations

import math


def criar_interface() -> None:
    try:
        import tkinter as tk
        from tkinter import messagebox, ttk

        import numpy as np
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
    except ImportError as erro:
        raise RuntimeError(
            "A interface precisa de Tkinter e Matplotlib. "
            "Instale com: python -m pip install matplotlib"
        ) from erro

    from calculos import (
        calcular_delta,
        calcular_pontos,
        calcular_raizes,
        calcular_vertice,
        calcular_volume_revolucao,
        obter_passo_a_passo_integral,
    )

    janela = tk.Tk()
    janela.title("Bhaskara • Laboratório de Revolução")
    janela.geometry("1280x800")
    janela.minsize(1000, 680)
    janela.configure(bg="#101827")

    estilo = ttk.Style(janela)
    estilo.theme_use("clam")
    estilo.configure("Card.TFrame", background="#17243a")
    estilo.configure("Titulo.TLabel", background="#101827", foreground="#f8fafc",
                     font=("Segoe UI", 22, "bold"))
    estilo.configure("Subtitulo.TLabel", background="#101827", foreground="#9fb3c8",
                     font=("Segoe UI", 10))
    estilo.configure("Card.TLabel", background="#17243a", foreground="#dbeafe",
                     font=("Segoe UI", 10))
    estilo.configure("Valor.TLabel", background="#17243a", foreground="#67e8f9",
                     font=("Segoe UI", 13, "bold"))
    estilo.configure("Acao.TButton", font=("Segoe UI", 10, "bold"), padding=10)
    estilo.configure("TNotebook", background="#17243a", borderwidth=0)
    estilo.configure("TNotebook.Tab", padding=(16, 8), font=("Segoe UI", 10, "bold"))

    cabecalho = ttk.Frame(janela, style="Card.TFrame", padding=(24, 18))
    cabecalho.pack(fill="x", padx=18, pady=(18, 10))
    ttk.Label(cabecalho, text="Bhaskara • Laboratório de Revolução",
              style="Titulo.TLabel").pack(anchor="w")
    ttk.Label(cabecalho, text="Gere a parábola, gire a região no eixo Y e visualize o volume.",
              style="Subtitulo.TLabel").pack(anchor="w", pady=(4, 0))

    conteudo = ttk.Frame(janela, style="Card.TFrame", padding=18)
    conteudo.pack(fill="both", expand=True, padx=18, pady=(0, 18))
    controles = ttk.Frame(conteudo, style="Card.TFrame")
    controles.pack(side="left", fill="y", padx=(0, 18))
    area_principal = ttk.Notebook(conteudo)
    area_principal.pack(side="right", fill="both", expand=True)
    visualizacao_frame = ttk.Frame(area_principal, style="Card.TFrame", padding=8)
    integral_frame = ttk.Frame(area_principal, style="Card.TFrame", padding=14)
    area_principal.add(visualizacao_frame, text="  Visualização  ")
    area_principal.add(integral_frame, text="  Cálculo por integrais  ")

    entradas: dict[str, tk.StringVar] = {}
    for nome, valor in (("a", "1"), ("b", "2"), ("c", "-4")):
        ttk.Label(controles, text=f"Coeficiente {nome}", style="Card.TLabel").pack(
            anchor="w", pady=(8, 4)
        )
        entradas[nome] = tk.StringVar(value=valor)
        ttk.Entry(controles, textvariable=entradas[nome], width=18,
                  font=("Segoe UI", 11)).pack(anchor="w")

    resultado = ttk.Frame(controles, style="Card.TFrame")
    resultado.pack(fill="x", pady=(24, 0))
    delta_label = ttk.Label(resultado, text="Delta: —", style="Card.TLabel")
    delta_label.pack(anchor="w", pady=3)
    raizes_label = ttk.Label(resultado, text="Raízes: —", style="Card.TLabel",
                            wraplength=230)
    raizes_label.pack(anchor="w", pady=3)
    vertice_label = ttk.Label(resultado, text="Vértice: —", style="Card.TLabel")
    vertice_label.pack(anchor="w", pady=3)
    volume_label = ttk.Label(resultado, text="Volume: —", style="Valor.TLabel",
                             wraplength=230)
    volume_label.pack(anchor="w", pady=(12, 3))
    aviso = ttk.Label(controles, text="A área usada é a região fechada entre\na curva e o eixo X.",
                      style="Card.TLabel", wraplength=230)
    aviso.pack(anchor="w", pady=(18, 0))

    figura = Figure(figsize=(8, 5), dpi=100, facecolor="#17243a")
    eixo_2d = figura.add_subplot(121)
    eixo_3d = figura.add_subplot(122, projection="3d")
    canvas = FigureCanvasTkAgg(figura, master=visualizacao_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    explicacao = tk.Text(
        integral_frame,
        wrap="word",
        bg="#101827",
        fg="#dbeafe",
        insertbackground="#dbeafe",
        relief="flat",
        padx=18,
        pady=16,
        font=("Consolas", 11),
    )
    barra = ttk.Scrollbar(integral_frame, orient="vertical", command=explicacao.yview)
    explicacao.configure(yscrollcommand=barra.set)
    explicacao.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")

    def formatar(valor: float) -> str:
        return f"{valor:.6g}"

    def atualizar() -> None:
        try:
            coeficientes = tuple(float(entradas[nome].get().replace(",", "."))
                                for nome in ("a", "b", "c"))
            a, b, c = coeficientes
            if not all(math.isfinite(valor) for valor in coeficientes) or a == 0:
                raise ValueError("Use números finitos e a diferente de zero.")
            delta = calcular_delta(a, b, c)
            raizes = calcular_raizes(a, b, delta)
            vertice = calcular_vertice(a, b, delta)
            if delta < 0:
                raise ValueError("A curva não possui duas raízes reais e uma região fechada.")
            volume = calcular_volume_revolucao(a, b, c, raizes)
            pontos = calcular_pontos(a, b, c, vertice, raizes)
            reais = sorted(raiz.real for raiz in raizes)
        except (ValueError, OverflowError) as erro:
            messagebox.showerror("Não foi possível calcular", str(erro), parent=janela)
            return

        delta_label.configure(text=f"Delta: {formatar(delta)}")
        raizes_label.configure(text=f"Raízes: {formatar(reais[0])} e "
                                   f"{formatar(reais[1])}")
        vertice_label.configure(text=f"Vértice: ({formatar(vertice[0])}, "
                                    f"{formatar(vertice[1])})")
        volume_label.configure(text=f"Volume: {formatar(volume)} u³")
        explicacao.configure(state="normal")
        explicacao.delete("1.0", "end")
        explicacao.insert(
            "1.0",
            obter_passo_a_passo_integral(a, b, c, raizes, vertice, volume),
        )
        explicacao.configure(state="disabled")
        eixo_2d.clear()
        eixo_3d.clear()
        valores_x, valores_y = pontos
        eixo_2d.plot(valores_x, valores_y, color="#22d3ee", linewidth=2.5,
                     label="f(x)")
        eixo_2d.fill_between(valores_x, valores_y, 0, color="#38bdf8", alpha=0.18)
        eixo_2d.axhline(0, color="#94a3b8", linewidth=0.8)
        eixo_2d.axvline(0, color="#94a3b8", linewidth=0.8)
        eixo_2d.scatter([vertice[0]], [vertice[1]], color="#fb7185", zorder=3,
                        label="Vértice")
        eixo_2d.set_title("Região geradora", color="#e2e8f0")
        eixo_2d.set_xlabel("x", color="#cbd5e1")
        eixo_2d.grid(True, alpha=0.18)
        eixo_2d.legend()
        eixo_2d.set_facecolor("#17243a")

        xs = [reais[0] + (reais[1] - reais[0]) * i / 80 for i in range(81)]
        theta = [2 * math.pi * i / 48 for i in range(49)]
        x_matriz = [[x * math.cos(t) for x in xs] for t in theta]
        z_matriz = [[x * math.sin(t) for x in xs] for t in theta]
        y_matriz = [[a * x**2 + b * x + c for x in xs] for _ in theta]
        eixo_3d.plot_surface(np.array(x_matriz), np.array(y_matriz),
                             np.array(z_matriz), cmap="viridis",
                             alpha=0.82, linewidth=0)
        eixo_3d.set_title("Curva girada no eixo Y", color="#e2e8f0")
        eixo_3d.set_xlabel("X")
        eixo_3d.set_ylabel("Y")
        eixo_3d.set_zlabel("Z")
        figura.tight_layout()
        canvas.draw()

    ttk.Button(controles, text="Calcular e visualizar", style="Acao.TButton",
               command=atualizar).pack(fill="x", pady=(22, 0))
    atualizar()
    janela.mainloop()


def mostrar_grafico(
    pontos: tuple[list[float], list[float]],
    vertice: tuple[float, float],
    raizes: tuple[complex, complex],
) -> None:
    """Compatibilidade com a API antiga: abre uma visualização simples."""
    del pontos, vertice, raizes
    criar_interface()