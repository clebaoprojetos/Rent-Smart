import os
import sys
import tempfile
import unittest
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from imovel import Imovel, formatar_moeda
from apartamento import Apartamento
from casa import Casa
from estudio import Estudio
from contrato import Contrato
from orcamento import Orcamento
from relatorio import RelatorioCSV


class TestRentSmart(unittest.TestCase):

    def test_01_apartamento_um_quarto(self):
        apt = Apartamento(quant_quartos=1, possui_garagem=False, possui_criancas=True)
        self.assertEqual(apt.valor_base, Decimal("700.00"))
        self.assertEqual(apt.calcular_adicional_quartos(), Decimal("0.00"))
        self.assertEqual(apt.calcular_adicional_garagem(), Decimal("0.00"))
        self.assertEqual(apt.calcular_subtotal(), Decimal("700.00"))
        self.assertEqual(apt.calcular_desconto(), Decimal("0.00"))
        self.assertEqual(apt.calcular_aluguel_mensal(), Decimal("700.00"))

    def test_02_apartamento_dois_quartos_e_garagem(self):
        apt = Apartamento(quant_quartos=2, possui_garagem=True, possui_criancas=True)
        self.assertEqual(apt.valor_base, Decimal("700.00"))
        self.assertEqual(apt.calcular_adicional_quartos(), Decimal("200.00"))
        self.assertEqual(apt.calcular_adicional_garagem(), Decimal("300.00"))
        self.assertEqual(apt.calcular_subtotal(), Decimal("1200.00"))
        self.assertEqual(apt.calcular_desconto(), Decimal("0.00"))
        self.assertEqual(apt.calcular_aluguel_mensal(), Decimal("1200.00"))

    def test_03_desconto_apartamento_sem_criancas(self):
        apt = Apartamento(quant_quartos=2, possui_garagem=True, possui_criancas=False)
        self.assertEqual(apt.calcular_subtotal(), Decimal("1200.00"))
        self.assertEqual(apt.calcular_desconto(), Decimal("60.00"))
        self.assertEqual(apt.calcular_aluguel_mensal(), Decimal("1140.00"))

    def test_03b_desconto_apartamento_um_quarto_sem_criancas(self):
        apt = Apartamento(quant_quartos=1, possui_garagem=False, possui_criancas=False)
        self.assertEqual(apt.calcular_subtotal(), Decimal("700.00"))
        self.assertEqual(apt.calcular_desconto(), Decimal("35.00"))
        self.assertEqual(apt.calcular_aluguel_mensal(), Decimal("665.00"))

    def test_04_casa_dois_quartos_e_garagem(self):
        casa = Casa(quant_quartos=2, possui_garagem=True)
        self.assertEqual(casa.valor_base, Decimal("900.00"))
        self.assertEqual(casa.calcular_adicional_quartos(), Decimal("250.00"))
        self.assertEqual(casa.calcular_adicional_garagem(), Decimal("300.00"))
        self.assertEqual(casa.calcular_subtotal(), Decimal("1450.00"))
        self.assertEqual(casa.calcular_desconto(), Decimal("0.00"))
        self.assertEqual(casa.calcular_aluguel_mensal(), Decimal("1450.00"))

    def test_04b_casa_um_quarto_sem_garagem(self):
        casa = Casa(quant_quartos=1, possui_garagem=False)
        self.assertEqual(casa.calcular_adicional_quartos(), Decimal("0.00"))
        self.assertEqual(casa.calcular_adicional_garagem(), Decimal("0.00"))
        self.assertEqual(casa.calcular_aluguel_mensal(), Decimal("900.00"))

    def test_05_estudio_sem_vagas(self):
        estudio = Estudio(quant_vagas=0)
        self.assertEqual(estudio.valor_base, Decimal("1200.00"))
        self.assertEqual(estudio.calcular_adicional_garagem(), Decimal("0.00"))
        self.assertEqual(estudio.calcular_aluguel_mensal(), Decimal("1200.00"))

    def test_06_estudio_duas_vagas(self):
        estudio_2 = Estudio(quant_vagas=2)
        self.assertEqual(estudio_2.calcular_adicional_garagem(), Decimal("250.00"))
        self.assertEqual(estudio_2.calcular_aluguel_mensal(), Decimal("1450.00"))

        estudio_1 = Estudio(quant_vagas=1)
        self.assertEqual(estudio_1.calcular_adicional_garagem(), Decimal("250.00"))
        self.assertEqual(estudio_1.calcular_aluguel_mensal(), Decimal("1450.00"))

    def test_07_estudio_tres_vagas(self):
        estudio_3 = Estudio(quant_vagas=3)
        self.assertEqual(estudio_3.calcular_adicional_garagem(), Decimal("310.00"))
        self.assertEqual(estudio_3.calcular_aluguel_mensal(), Decimal("1510.00"))

        estudio_4 = Estudio(quant_vagas=4)
        self.assertEqual(estudio_4.calcular_adicional_garagem(), Decimal("370.00"))
        self.assertEqual(estudio_4.calcular_aluguel_mensal(), Decimal("1570.00"))

    def test_08_validacao_parcelamento_invalido(self):
        with self.assertRaises(ValueError):
            Contrato(quant_parcelas=0)

        with self.assertRaises(ValueError):
            Contrato(quant_parcelas=-1)

        with self.assertRaises(ValueError):
            Contrato(quant_parcelas=6)

        with self.assertRaises(ValueError):
            Contrato(quant_parcelas=10)

        for p in range(1, 6):
            c = Contrato(quant_parcelas=p)
            self.assertEqual(c.quant_parcelas, p)
            self.assertEqual(c.taxa_total, Decimal("2000.00"))
            self.assertEqual(c.calcular_valor_parcela(), (Decimal("2000.00") / Decimal(str(p))).quantize(Decimal("0.01")))

    def test_09_calculo_projecao_12_meses(self):
        apt = Apartamento(quant_quartos=2, possui_garagem=True, possui_criancas=False)
        contrato = Contrato(quant_parcelas=5)
        orcamento = Orcamento(imovel=apt, contrato=contrato)

        projecao = orcamento.gerar_projecao_12_meses()
        self.assertEqual(len(projecao), 12)

        for mes_item in projecao[:5]:
            self.assertEqual(mes_item["aluguel_mensal"], Decimal("1140.00"))
            self.assertEqual(mes_item["parcela_contratual"], Decimal("400.00"))
            self.assertEqual(mes_item["total_mensal"], Decimal("1540.00"))

        for mes_item in projecao[5:]:
            self.assertEqual(mes_item["aluguel_mensal"], Decimal("1140.00"))
            self.assertEqual(mes_item["parcela_contratual"], Decimal("0.00"))
            self.assertEqual(mes_item["total_mensal"], Decimal("1140.00"))

    def test_10_encerramento_taxa_contratual_apos_parcelas(self):
        contrato_3 = Contrato(quant_parcelas=3)
        self.assertEqual(contrato_3.obter_parcela_mes(1), Decimal("666.67"))
        self.assertEqual(contrato_3.obter_parcela_mes(2), Decimal("666.67"))
        self.assertEqual(contrato_3.obter_parcela_mes(3), Decimal("666.67"))
        self.assertEqual(contrato_3.obter_parcela_mes(4), Decimal("0.00"))
        self.assertEqual(contrato_3.obter_parcela_mes(12), Decimal("0.00"))

        contrato_1 = Contrato(quant_parcelas=1)
        self.assertEqual(contrato_1.obter_parcela_mes(1), Decimal("2000.00"))
        self.assertEqual(contrato_1.obter_parcela_mes(2), Decimal("0.00"))

    def test_validacao_imoveis_invalidos(self):
        with self.assertRaises(ValueError):
            Apartamento(quant_quartos=3, possui_garagem=True, possui_criancas=False)

        with self.assertRaises(ValueError):
            Apartamento(quant_quartos=0, possui_garagem=True, possui_criancas=False)

        with self.assertRaises(ValueError):
            Casa(quant_quartos=4, possui_garagem=True)

        with self.assertRaises(ValueError):
            Estudio(quant_vagas=-2)

    def test_geracao_arquivo_csv(self):
        apt = Apartamento(quant_quartos=2, possui_garagem=True, possui_criancas=False)
        contrato = Contrato(quant_parcelas=5)
        orcamento = Orcamento(imovel=apt, contrato=contrato)
        relatorio = RelatorioCSV(orcamento)

        with tempfile.TemporaryDirectory() as tmpdir:
            caminho_teste = os.path.join(tmpdir, "projecao_teste.csv")
            relatorio.gerar_csv(caminho_teste)

            self.assertTrue(os.path.exists(caminho_teste))

            with open(caminho_teste, "r", encoding="utf-8") as f:
                linhas = [l.strip() for l in f.readlines() if l.strip()]

            self.assertEqual(len(linhas), 13)
            self.assertEqual(linhas[0], "Mes,Aluguel_Mensal,Parcela_Contratual,Total_Mensal")
            self.assertEqual(linhas[1], "1,1140.00,400.00,1540.00")
            self.assertEqual(linhas[5], "5,1140.00,400.00,1540.00")
            self.assertEqual(linhas[6], "6,1140.00,0.00,1140.00")
            self.assertEqual(linhas[12], "12,1140.00,0.00,1140.00")

    def test_formatacao_moeda(self):
        self.assertEqual(formatar_moeda(Decimal("700")), "R$ 700,00")
        self.assertEqual(formatar_moeda(Decimal("1140.5")), "R$ 1.140,50")
        self.assertEqual(formatar_moeda(Decimal("2000.00")), "R$ 2.000,00")
        self.assertEqual(formatar_moeda(Decimal("1234567.89")), "R$ 1.234.567,89")


if __name__ == "__main__":
    unittest.main()
