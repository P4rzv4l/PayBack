import matplotlib.pyplot as plt
import pandas as pd

def solicitar_float(mensagem, minimo=0, permitir_zero=False):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if not permitir_zero and valor == 0:
                print("Valor não pode ser zero.")
                continue
            if valor < minimo:
                print(f"Valor deve ser no mínimo {minimo}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número válido.")

def solicitar_fluxos():
    print("\nDigite os fluxos de caixa ano a ano (Digite Enter ou 0 para encerrar):")
    fluxos = []
    ano = 1
    while True:
        entrada = input(f"Fluxo do ano {ano}: ").strip()
        if entrada in ("", "0"):
            break
        try:
            fluxo = float(entrada.replace(",", "."))
            fluxos.append(fluxo)
            ano += 1
        except ValueError:
            print("Entrada inválida. Digite um número.")
    return fluxos

def calcular_payback(investimento, fluxos):
    acumulado = 0
    for i, f in enumerate(fluxos):
        acumulado += f
        if acumulado >= investimento:
            return i + 1
    return None

def calcular_payback_descontado(investimento, fluxos, taxa):
    acumulado = 0
    acumulados = []
    for i, f in enumerate(fluxos):
        vp = f / ((1 + taxa) ** (i + 1))
        acumulado += vp
        acumulados.append(acumulado)
        if acumulado >= investimento:
            return i + 1, acumulados
    return None, acumulados

def gerar_tabela(fluxos, taxa):
    dados = []
    acumulado = 0
    for i, f in enumerate(fluxos):
        ano = i + 1
        vp = f / ((1 + taxa) ** ano)
        acumulado += vp
        dados.append({
            "Ano": ano,
            "Fluxo de Caixa": f,
            "Valor Presente": round(vp, 2),
            "Acumulado Descontado": round(acumulado, 2)
        })
    return pd.DataFrame(dados)

def exibir_grafico(acumulados, investimento):
    anos = list(range(1, len(acumulados) + 1))
    plt.figure(figsize=(8, 5))
    plt.plot(anos, acumulados, marker='o', label='Fluxo Descontado Acumulado')
    plt.axhline(investimento, color='red', linestyle='--', label='Investimento Inicial')
    plt.title('Payback Descontado')
    plt.xlabel('Ano')
    plt.ylabel('Valor Acumulado (R$)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    print("=== CALCULADORA DE PAYBACK ===")

    investimento = solicitar_float("Informe o investimento inicial (ex: 10000): ", minimo=0.01)
    taxa = solicitar_float("Informe a taxa de desconto anual (em %, ex: 10): ", minimo=0) / 100
    fluxos = solicitar_fluxos()

    if not fluxos:
        print("Nenhum fluxo de caixa inserido. Encerrando.")
        return

    payback_simples = calcular_payback(investimento, fluxos)
    payback_desc, acumulados_desc = calcular_payback_descontado(investimento, fluxos, taxa)
    tabela = gerar_tabela(fluxos, taxa)

    print("\n=== RESULTADOS ===")
    print(f"Payback Simples: {payback_simples if payback_simples else 'Não atingido'} anos")
    print(f"Payback Descontado: {payback_desc if payback_desc else 'Não atingido'} anos")

    print("\n=== TABELA DE FLUXOS DESCONTADOS ===")
    print(tabela.to_string(index=False))

    exibir_grafico(acumulados_desc, investimento)

if __name__ == "__main__":
    main()
