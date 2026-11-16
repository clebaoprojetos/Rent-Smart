# RentSmart - R.M Imóveis

Sistema de orçamento de locação de imóveis e projeção financeira para a imobiliária **R.M Imóveis**.

---

## 1. Descrição

O **RentSmart** é uma aplicação desenvolvida em Python com foco em Programação Orientada a Objetos (POO). O sistema calcula os valores mensais de aluguel para diferentes categorias de imóveis, aplicando adicionais específicos, descontos condicionais, gerenciamento da taxa contratual e projeção financeira detalhada dos primeiros 12 meses de contrato.

---

## 2. Objetivo

Automatizar e padronizar o processo de cálculo de orçamentos de locação, assegurando precisão financeira, transparência na discriminação de adicionais e taxas, e exportação automática da projeção financeira anual para arquivo CSV.

---

## 3. Tecnologias Utilizadas

- **Linguagem**: Python 3 (3.8+)
- **Módulos Nativos do Python**:
  - `decimal` (`Decimal`, `ROUND_HALF_UP`): Para precisão e conformidade com cálculos monetários.
  - `abc` (`ABC`, `abstractmethod`): Para definição de classes e métodos abstratos.
  - `csv`: Para exportação e manipulação de relatórios tabulares.
  - `unittest`: Para suite de testes automatizados.
  - `os` e `sys`: Para manipulação de caminhos e controle do fluxo CLI.

---

## 4. Estrutura de Arquivos

```
RentSmart/
│
├── main.py                # Interface de linha de comando (CLI) e menus interativos
├── imovel.py              # Classe base abstrata Imovel e utilitário de formatação de moeda
├── apartamento.py         # Subclasse Apartamento com regras de adicionais e desconto
├── casa.py                # Subclasse Casa com regras de adicionais
├── estudio.py             # Subclasse Estudio com regras de pacote de garagem
├── contrato.py            # Classe Contrato para gestão e parcelamento da taxa contratual
├── orcamento.py           # Classe Orcamento para consolidação e formatação de valores
├── relatorio.py           # Classe RelatorioCSV para geração da projeção de 12 meses
│
├── arquivos/              # Diretório de persistência de relatórios
│   └── projecao_12_meses.csv # Arquivo CSV gerado automaticamente pelo sistema
│
├── tests/                 # Diretório de testes automatizados
│   └── test_rentsmart.py  # Suite de testes com unittest
│
└── README.md              # Documentação completa do projeto
```

---

## 5. Regras de Negócio

### 5.1. Categorias de Imóveis

#### Apartamento
- **Aluguel-base (1 quarto)**: R$ 700,00.
- **2 quartos**: Adicional de R$ 200,00.
- **Vaga de garagem**: Adicional de R$ 300,00 (1 vaga).
- **Desconto para clientes sem crianças**: 5% de desconto sobre o subtotal (aluguel-base + adicionais).
- Clientes com crianças não recebem o desconto.

#### Casa
- **Aluguel-base (1 quarto)**: R$ 900,00.
- **2 quartos**: Adicional de R$ 250,00.
- **Vaga de garagem**: Adicional de R$ 300,00 (1 vaga).
- **Desconto**: Não possui desconto por quantidade de crianças.

#### Estúdio
- **Aluguel-base**: R$ 1.200,00.
- **Quartos**: Ambiente integrado (não aplicável).
- **Vagas de garagem**:
  - 0 vagas: R$ 0,00.
  - 1 ou 2 vagas: Pacote fixo promocional de R$ 250,00.
  - Acima de 2 vagas: R$ 250,00 + R$ 60,00 por vaga adicional que ultrapassar as 2 primeiras.
- **Desconto**: Não possui desconto por quantidade de crianças.

### 5.2. Contrato e Taxa Contratual
- **Taxa Contratual Fixa**: R$ 2.000,00.
- **Parcelamento**: O cliente pode parcelar a taxa em 1, 2, 3, 4 ou 5 vezes.
- **Apresentação**: A taxa contratual é apresentada de forma separada do aluguel mensal e **não é incorporada permanentemente** ao aluguel.

### 5.3. Projeção Financeira de 12 Meses (CSV)
- O aluguel mensal permanece constante durante os 12 meses.
- A parcela da taxa contratual é cobrada apenas durante a quantidade de meses do parcelamento escolhido (de 1 a 5 meses).
- A partir do mês seguinte ao término das parcelas até o 12º mês, a parcela contratual é zerada (R$ 0,00) e o total mensal corresponde apenas ao aluguel mensal.

---

## 6. Conceitos de POO Utilizados

- **Abstração**: A classe abstrata `Imovel` define o contrato e atributos essenciais comuns (`categoria`, `valor_base`), estabelecendo métodos abstratos (`calcular_adicional_quartos`, `calcular_adicional_garagem`, `calcular_desconto`, `obter_detalhes`).
- **Herança**: As classes `Apartamento`, `Casa` e `Estudio` herdam de `Imovel`, reutilizando a lógica comum de cálculo do subtotal e aluguel mensal enquanto especializam suas peculiaridades.
- **Polimorfismo**: Cada classe de imóvel implementa os métodos de cálculo de adicionais e descontos de forma polimórfica, permitindo que a classe `Orcamento` trate qualquer subclasse de `Imovel` uniformemente.
- **Encapsulamento**: Atributos internos protegidos (`_valor_base`, `_quant_quartos`, `_quant_vagas`, `_taxa_total`, etc.) são acessados via `@property` e validados via métodos de classe e no momento da instanciação.
- **Separação de Responsabilidades (SRP)**:
  - `Imovel` e subclasses: Lógica do imóvel e seus custos.
  - `Contrato`: Lógica da taxa e parcelamento.
  - `Orcamento`: Composição do Imóvel com o Contrato e formatação do resumo.
  - `RelatorioCSV`: Persistência e exportação de dados para CSV.
  - `main.py`: Camada de apresentação e interação via CLI com validação de entradas do usuário.

---

## 7. Como Instalar e Executar

### Pré-requisitos
- Python 3 instalado no sistema operacional.

### Execução da Aplicação
1. Abra o terminal na pasta raiz do projeto (`RentSmart`).
2. Execute o comando:
```bash
python3 main.py
```
3. Navegue pelo menu interativo:
   - Digite `1` para criar um novo orçamento.
   - Siga as instruções informando categoria do imóvel, quartos, garagem, crianças (quando aplicável) e número de parcelas.
   - O resumo será exibido na tela e o arquivo CSV será gerado na pasta `arquivos/`.
   - Digite `2` para encerrar o programa.

---

## 8. Como Executar os Testes

Para executar toda a suite de testes automatizados com saída detalhada:

```bash
python3 -m unittest discover -s tests -v
```

Ou execute diretamente o arquivo de teste:

```bash
python3 tests/test_rentsmart.py
```

### Cenários cobertos nos testes:
1. Apartamento com 1 quarto (base R$ 700,00).
2. Apartamento com 2 quartos e garagem (R$ 1.200,00 sem desconto).
3. Desconto de 5% em apartamento sem crianças (R$ 1.140,00).
4. Casa com 2 quartos e garagem (R$ 1.450,00).
5. Estúdio sem vagas (R$ 1.200,00).
6. Estúdio com 2 vagas (pacote de R$ 250,00 -> R$ 1.450,00).
7. Estúdio com 3 e 4 vagas (pacote + adicionais de R$ 60,00 por vaga extra).
8. Validação de parcelamento de contrato inválido (< 1 ou > 5).
9. Cálculo da projeção financeira de 12 meses.
10. Encerramento da cobrança da taxa contratual após a quantidade de parcelas selecionada.
11. Validações de entradas inválidas de quartos e vagas.
12. Formatação monetária em padrão brasileiro (R$ X.XXX,XX).
13. Criação e integridade estrutural do arquivo CSV (12 meses + cabeçalho).

---

## 9. Como Localizar o CSV Gerado

Após a criação de um orçamento, o sistema gera automaticamente o arquivo no caminho:

```
arquivos/projecao_12_meses.csv
```

### Formato das Colunas do CSV:
- `Mes`: Número do mês (1 a 12).
- `Aluguel_Mensal`: Valor do aluguel mensal formatado com 2 casas decimais.
- `Parcela_Contratual`: Valor da parcela contratual cobrada naquele mês.
- `Total_Mensal`: Soma do aluguel mensal com a parcela contratual do respectivo mês.
