# Observatório do Cacau

Painel com dados de produção, território, indústria, comércio exterior, mercado internacional e crédito rural do cacau no Brasil. É um site estático: HTML, CSS, JavaScript e arquivos de dados, sem servidor nem banco de dados. Funciona no GitHub Pages ou em qualquer hospedagem de arquivos.

## Publicar no GitHub Pages

1. Crie um repositório no GitHub (por exemplo, `observatorio-do-cacau`).
2. Envie o conteúdo desta pasta para a branch `main`:
   ```bash
   git init
   git add .
   git commit -m "Observatório do Cacau, versão 1"
   git branch -M main
   git remote add origin https://github.com/<organizacao>/observatorio-do-cacau.git
   git push -u origin main
   ```
3. No repositório, abra **Settings → Pages**, escolha **Deploy from a branch**, branch `main`, pasta `/ (root)`, e salve.
4. Em alguns minutos o painel fica em `https://<organizacao>.github.io/observatorio-do-cacau/`.

Para incorporar no site do Arapyaú, use um `<iframe>` apontando para esse endereço.

## Ver no computador

O painel carrega os dados com `fetch`, então precisa de um servidor local (abrir o `index.html` direto no navegador não funciona):

```bash
python3 -m http.server 8000
```

e abra `http://localhost:8000`.

## Estrutura

| Pasta / arquivo | O que tem |
| --- | --- |
| `index.html` | A página: seções, cálculos e gráficos |
| `css/tema.css` | Cores, fontes e espaçamentos (temas claro e escuro) |
| `js/runtime.js` | Carrega os dados, roda os cálculos, redesenha os gráficos e guarda os filtros no endereço |
| `data/` | As bases do painel (JSON e CSV) e `manifest.json`, que liga cada base ao seu arquivo |
| `scripts/` | Scripts em Python que geraram as bases agregadas |
| `assets/` | Logo do Observatório e fonte Lexend Deca |
| `vendor/` | D3 7.9.0 e as licenças da D3 e da Lexend Deca |

Os filtros ficam no endereço da página (por exemplo, `?uf_mun=BA`), então dá para compartilhar uma visão já filtrada.

## Atualizar os dados

Troque o arquivo correspondente em `data/`, mantendo o nome e as colunas. Os textos com números (destaques, frases de abertura de cada seção) são calculados a partir das bases, então se atualizam sozinhos.

| Base (`data/`) | Fonte | Cobertura |
| --- | --- | --- |
| `producao_ibge.json` | IBGE, Produção Agrícola Municipal | 2009–2025, por estado |
| `producao_municipal.json` | IBGE, PAM 2025 | 360 municípios produtores |
| `recebimentos_aipc.csv`, `recebimentos_uf_aipc.csv`, `moagem_aipc.csv`, `derivados_aipc.csv` | AIPC (SindiDados – Campos Consultores) | 2018–2026 |
| `aipc_trimestral.json` | AIPC, comunicados trimestrais | 2024 ao 3º tri/2026 |
| `preco_icco.json` | ICCO | set/2016 a out/2026 |
| `moagem_europa.json`, `moagem_asia.json` | ECA e CAA | 2018 ao 3º tri/2026 |
| `comex_mensal.json`, `comex_paises.json` | Comex Stat (MDIC), SH 1801 a 1806 | 2021 a jul/2026 |
| `credito_cacau.json` | Banco Central, Matriz de Dados do Crédito Rural | 2025, por estado |
| `municipios_aptidao.json`, `aptidao_bioma.json` | Índice de aptidão de terras (Youx), biomas do IBGE | — |
| `civ_chegadas.json`, `estimativas_safra.json`, `precos_produtor.json`, `balanco_projecoes.json`, `enso_probabilidades.json`, `tendencias_leitura.json` | Fontes públicas citadas linha a linha (Bloomberg, Reuters, Cocobod, CCC, ICCO, Banco Mundial, NOAA) | Edição de novembro de 2026 |
| `malha_municipios.json`, `malha_ufs.json` | Malha simplificada do projeto geodata-br (anterior a 2013) | — |
| `fontes.json` | Levantamento de fontes | — |

A seção **Tendências de mercado** é uma edição mensal: a cada mês, atualize `tendencias_leitura.json` e as tabelas de oferta, preço ao produtor, balanço e clima, e estenda `preco_icco.json`, `moagem_*.json` e `aipc_trimestral.json`.

Os scripts em `scripts/` mostram como cada base foi montada. Eles usam os caminhos do ambiente em que foram gerados; para rodar de novo, ajuste os caminhos de entrada no início de cada um.

## Licenças

- D3: ISC (`vendor/LICENSE-d3.txt`).
- Lexend Deca: SIL Open Font License 1.1 (`vendor/OFL-LexendDeca.txt`).
- Logo do Observatório do Cacau e dados: conforme os termos de cada titular e fonte.
