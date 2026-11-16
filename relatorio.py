import csv
import os
from typing import Optional
from orcamento import Orcamento


class RelatorioCSV:

    CAMINHO_PADRAO = os.path.join("arquivos", "projecao_12_meses.csv")

    def __init__(self, orcamento: Orcamento):
        if not isinstance(orcamento, Orcamento):
            raise TypeError("O relatório requer uma instância válida de Orcamento.")

        self._orcamento = orcamento

    @property
    def orcamento(self) -> Orcamento:
        return self._orcamento

    def gerar_csv(self, caminho_arquivo: Optional[str] = None) -> str:
        caminho_final = caminho_arquivo or self.CAMINHO_PADRAO

        diretorio = os.path.dirname(caminho_final)
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)

        projecao = self._orcamento.gerar_projecao_12_meses()

        cabecalho = ["Mes", "Aluguel_Mensal", "Parcela_Contratual", "Total_Mensal"]

        with open(caminho_final, mode="w", newline="", encoding="utf-8") as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            escritor.writerow(cabecalho)

            for item in projecao:
                escritor.writerow([
                    item["mes"],
                    f"{item['aluguel_mensal']:.2f}",
                    f"{item['parcela_contratual']:.2f}",
                    f"{item['total_mensal']:.2f}",
                ])

        return caminho_final
