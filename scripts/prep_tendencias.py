# Observatório do Cacau — edição mensal de Tendências (corte: 24/11/2026).
# Estende as séries da Youx com dados públicos recentes e monta as tabelas do monitor.
# Cada linha nova traz a fonte e o link de onde o número foi tirado.
import json, pandas as pd
U = '/mnt/user-data/uploads/'
OUT = '/mnt/user-data/outputs/obs_data/tend/'
EDICAO = '2026-11'
CODE = open(__file__, encoding='utf-8').read()

def save(name, rows, entrada, nota=''):
    df = pd.DataFrame(rows) if not isinstance(rows, pd.DataFrame) else rows
    df = df.astype(object).where(pd.notna(df), None)
    meta = [{'label': 'prep_tendencias.py', 'value': CODE, 'type': 'code', 'lang': 'python'},
            {'label': 'Entrada', 'value': entrada}, {'label': 'Edição', 'value': EDICAO}]
    if nota: meta.append({'label': 'Nota', 'value': nota})
    json.dump({'rows': df.to_dict('records'), 'meta': meta}, open(OUT + name + '.json', 'w', encoding='utf-8'), ensure_ascii=False)

# 1. Preço ICCO mensal: série da Youx + meses novos
p = pd.read_csv(U + 'preco_medio_mensal_cacau.csv')
p['fonte'] = 'ICCO (série tratada pela Youx)'; p['url'] = None
WB = 'https://globalmacro.expert/commodities/agriculture/cocoa/'
novos = [
    {'data': '2026-08-01', 'usd_por_tonelada': 5950.0, 'fonte': 'ICCO, média mensal via World Bank Pink Sheet (US$ 5,95/kg)', 'url': WB},
    {'data': '2026-09-01', 'usd_por_tonelada': 5920.0, 'fonte': 'ICCO, média mensal via World Bank Pink Sheet (US$ 5,92/kg)', 'url': WB},
    {'data': '2026-10-01', 'usd_por_tonelada': 5742.0, 'fonte': 'ICCO, média mensal via FocusEconomics', 'url': 'https://www.focus-economics.com/commodities/agricultural/cocoa/'},
]
n = pd.DataFrame(novos); n['euro_por_tonelada'] = None
n['id'] = range(int(p.id.max()) + 1, int(p.id.max()) + 1 + len(n))
preco = pd.concat([p, n[p.columns]]).sort_values('data')
save('preco_icco', preco, 'preco_medio_mensal_cacau.csv (Youx, set/2016–jul/2026) + médias mensais públicas de ago–out/2026',
     'Os meses novos vêm arredondados da fonte secundária e não têm valor em euro.')

# 2. Moagem trimestral Europa (ECA) e Ásia (CAA): 2026 T1–T3
def moagem(arq, novos, regiao):
    m = pd.read_csv(U + arq); m['fonte'] = 'Youx (' + regiao + ')'; m['url'] = None
    n = pd.DataFrame(novos); n['id'] = range(int(m.id.max()) + 1, int(m.id.max()) + 1 + len(n))
    return pd.concat([m, n[m.columns]]).sort_values(['ano', 'trimestre'])
eu = moagem('moagem_europa.csv', [
    {'ano': 2026, 'trimestre': 'Q1', 'toneladas': 325895, 'fonte': 'ECA via NewsGhana', 'url': 'https://www.newsghana.com.gh/cocoa-prices-hit-multi-month-high-on-weak-ghana-crop/'},
    {'ano': 2026, 'trimestre': 'Q2', 'toneladas': 316366, 'fonte': 'ECA via XTB', 'url': 'https://www.xtb.com/cy/market-analysis/news-and-research/cocoa-rises-on-a-wave-of-rebounding-demand-in-asia-europe-remains-in-retreat'},
    {'ano': 2026, 'trimestre': 'Q3', 'toneladas': 348215, 'fonte': 'ECA via F&B Today', 'url': 'https://fnbdaily.net/europe-cocoa-grind-rises-third-quarter-2026-first-gain/'}], 'ECA')
asia = moagem('moagem_asia.csv', [
    {'ano': 2026, 'trimestre': 'Q1', 'toneladas': 223503, 'fonte': 'CAA via NewsGhana', 'url': 'https://www.newsghana.com.gh/cocoa-prices-hit-multi-month-high-on-weak-ghana-crop/'},
    {'ano': 2026, 'trimestre': 'Q2', 'toneladas': 224646, 'fonte': 'CAA via XTB', 'url': 'https://www.xtb.com/int/market-analysis/news-and-research/cocoa-rises-on-a-wave-of-rebounding-demand-in-asia-europe-remains-in-retreat'},
    {'ano': 2026, 'trimestre': 'Q3', 'toneladas': 233767, 'fonte': 'CAA via McKeany-Flavell', 'url': 'https://www.mckeany-flavell.com/q3-2026-cocoa-grindings-show-uneven-recovery-10-19-26/'}], 'CAA')
save('moagem_europa', eu, 'moagem_europa.csv (Youx, 2018–2025) + comunicados da ECA de 2026')
save('moagem_asia', asia, 'moagem_asia.csv (Youx, 2018–2025) + comunicados da CAA de 2026')

# 3. AIPC trimestral (recebimento e moagem)
AIPC1 = 'https://comprerural.com/recebimento-de-cacau-cresce-61-no-inicio-de-2026-mas-moagem-segue-estagnada-e-expoe-gargalo-na-demanda/'
AIPC2 = 'https://www.canalrural.com.br/agricultura/recebimento-de-cacau-no-brasil-cresce-634-no-primeiro-semestre-de-2026/'
AIPC3 = 'https://www.canalrural.com.br/radar/cacau-brasileiro-dispara-253-na-safra-2025-26-e-supera-226-mil-toneladas/'
rec = {(2024, 1): 18700, (2024, 2): 39663, (2024, 3): 66633, (2024, 4): 54435,
       (2025, 1): 17758, (2025, 2): 40430, (2025, 3): 68212, (2025, 4): 59737,
       (2026, 1): 28605, (2026, 2): 66503, (2026, 3): 71652}
moa = {(2025, 1): 52135, (2026, 1): 51715, (2026, 2): 101426 - 51715, (2026, 3): 53743}
aipc = [{'periodo': f'{a} T{t}', 'ano': a, 'trimestre': t, 'recebimento_t': v, 'moagem_t': moa.get((a, t)),
         'fonte': 'AIPC (SindiDados – Campos Consultores)',
         'url': AIPC3 if (a, t) == (2026, 3) else AIPC2 if (a, t) == (2026, 2) else AIPC1}
        for (a, t), v in rec.items()]
save('aipc_trimestral', aipc, 'Comunicados trimestrais da AIPC (abr, jul e out/2026), reproduzidos pela imprensa',
     'Moagem do 2º tri/2026 = moagem do 1º semestre (101.426 t) menos a do 1º tri (51.715 t).')

# 4. Chegadas aos portos da Costa do Marfim (base 1º de outubro, como reporta a Bloomberg)
BC = 'https://www.tradingview.com/news/barchart:a9e104e91094b:0-cocoa-prices-supported-by-reduced-ivory-coast-shipments/'
Y8 = 'https://finance.yahoo.com/markets/commodities/articles/cocoa-prices-jump-excessive-rain-165517105.html'
civ = [
    {'id': '2026-11-08-semana', 'data_ref': '2026-11-08', 'medida': 'Semana', 'safra_2026_27_t': 55317, 'safra_2025_26_t': 107139, 'fonte': 'Governo da Costa do Marfim, via Bloomberg/Barchart', 'url': Y8},
    {'id': '2026-11-08-acum', 'data_ref': '2026-11-08', 'medida': 'Acumulado desde 1º/out', 'safra_2026_27_t': 228475, 'safra_2025_26_t': 411979, 'fonte': 'Governo da Costa do Marfim, via Bloomberg/Barchart', 'url': Y8},
    {'id': '2026-11-22-semana', 'data_ref': '2026-11-22', 'medida': 'Semana', 'safra_2026_27_t': 53748, 'safra_2025_26_t': 102112, 'fonte': 'Governo da Costa do Marfim, via Bloomberg/Barchart', 'url': BC},
    {'id': '2026-11-22-acum', 'data_ref': '2026-11-22', 'medida': 'Acumulado desde 1º/out', 'safra_2026_27_t': 330843, 'safra_2025_26_t': 618899, 'fonte': 'Governo da Costa do Marfim, via Bloomberg/Barchart', 'url': BC},
]
for r in civ: r['var_pct'] = round((r['safra_2026_27_t'] / r['safra_2025_26_t'] - 1) * 100, 1)
save('civ_chegadas', civ, 'Dados semanais de chegadas aos portos divulgados pelo governo marfinense e reportados pela Bloomberg',
     'A Costa do Marfim passou a contar a safra 2026/27 a partir de 1º de setembro; a comparação usa a base de 1º de outubro.')

# 5. Estimativas de produção 2026/27
est = [
    {'pais': 'Costa do Marfim', 'safra_2025_26_mil_t': 2150, 'est_2026_27_min_mil_t': 1500, 'est_2026_27_max_mil_t': 1600, 'quem_estima': 'Exportadores e contadores de vagens (Reuters, 4/nov/2026)', 'url': 'https://www.cnbcafrica.com/2026/ivory-coast-cocoa-mid-crop-forecast-cut-after-weak-rains-sources-say'},
    {'pais': 'Gana', 'safra_2025_26_mil_t': 750, 'est_2026_27_min_mil_t': 650, 'est_2026_27_max_mil_t': 650, 'quem_estima': 'Cocobod, levantamento de vagens (ago/2026)', 'url': BC},
    {'pais': 'Equador', 'safra_2025_26_mil_t': None, 'est_2026_27_min_mil_t': 580, 'est_2026_27_max_mil_t': 580, 'quem_estima': 'Analistas ouvidos pela Bloomberg, após enchentes (nov/2026)', 'url': BC},
]
save('estimativas_safra', est, 'Estimativas públicas de produção 2026/27 nos principais países')

# 6. Preço garantido ao produtor
pp = [
    {'pais': 'Costa do Marfim', 'safra': '2026/27', 'preco': 1200, 'unidade': 'CFA/kg', 'anterior': 2800, 'anterior_ref': 'início de 2025/26', 'data_anuncio': '2026-09', 'fonte': 'Conseil Café-Cacao, via CocoaIntel', 'url': 'https://www.cocoaintel.com/ivory-coast-keeps-2026-27-cocoa-farmgate-price-at-1-200-cfa-kg/'},
    {'pais': 'Gana', 'safra': '2026/27', 'preco': 42400, 'unidade': 'GHS/t', 'anterior': 41392, 'anterior_ref': 'fim de 2025/26', 'data_anuncio': '2026-09-25', 'fonte': 'Cocobod, via Graphic Online', 'url': 'https://www.graphic.com.gh/business/business-news/cocoa-64-kg-per-bag-increases-from-ghc2-587-to-ghc2-650-for-2026-2027-crop-season.html'},
]
for r in pp: r['var_pct'] = round((r['preco'] / r['anterior'] - 1) * 100, 1)
save('precos_produtor', pp, 'Anúncios oficiais de preço ao produtor na Costa do Marfim e em Gana')

# 7. Probabilidades de El Niño (NOAA CPC, nov/2026), por categoria de intensidade (RONI)
enso_raw = [  # La Niña (todas), neutro, fraco, moderado, forte, muito forte
    ('OND', 0, 0, 0, 0, 0, 100), ('NDJ', 0, 0, 0, 0, 4, 96), ('DJF', 0, 0, 0, 2, 19, 79),
    ('JFM', 0, 0, 3, 18, 44, 35), ('FMA', 0, 2, 21, 49, 25, 3), ('MAM', 0, 20, 53, 25, 2, 0),
    ('AMJ', 1, 61, 34, 4, 0, 0), ('MJJ', 13, 75, 11, 1, 0, 0), ('JJA', 33, 61, 6, 0, 0, 0)]
nomes = {'OND': 'out–dez/26', 'NDJ': 'nov/26–jan/27', 'DJF': 'dez/26–fev/27', 'JFM': 'jan–mar/27', 'FMA': 'fev–abr/27',
         'MAM': 'mar–mai/27', 'AMJ': 'abr–jun/27', 'MJJ': 'mai–jul/27', 'JJA': 'jun–ago/27'}
enso = [{'temporada': t, 'meses': nomes[t], 'ordem': i + 1, 'la_nina_pct': a, 'neutro_pct': b, 'fraco_pct': c,
         'moderado_pct': d, 'forte_pct': e, 'muito_forte_pct': f} for i, (t, a, b, c, d, e, f) in enumerate(enso_raw)]
save('enso_probabilidades', enso, 'NOAA CPC, Official ENSO Strength Probabilities, emitido em novembro/2026 (https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/roni/strengths/)',
     'Fraco: RONI 0,5–1,0 °C; moderado: 1,0–1,5; forte: 1,5–2,0; muito forte: 2,0 ou mais. La Niña soma as quatro faixas negativas.')

# 8. Balanço global e projeções públicas
bal = [
    {'id': 'icco-2425', 'quem': 'ICCO', 'safra': '2024/25', 'indicador': 'Saldo global', 'valor': 37, 'unidade': 'mil t', 'data': '2026-08', 'nota': 'Superávit; a ICCO segurou os números de 2025/26', 'url': 'https://beansandbrews.de/en/cocoa-price-2026/'},
    {'id': 'stx-2526', 'quem': 'StoneX (divulgação pública)', 'safra': '2025/26', 'indicador': 'Saldo global', 'valor': 494, 'unidade': 'mil t', 'data': '2026-10-29', 'nota': 'Superávit', 'url': BC},
    {'id': 'stx-2627', 'quem': 'StoneX (divulgação pública)', 'safra': '2026/27', 'indicador': 'Saldo global', 'valor': -64, 'unidade': 'mil t', 'data': '2026-10-29', 'nota': 'Déficit, revisado de superávit de 25 mil t por causa do El Niño', 'url': BC},
    {'id': 'stx-prod2627', 'quem': 'StoneX (divulgação pública)', 'safra': '2026/27', 'indicador': 'Produção mundial', 'valor': 4740, 'unidade': 'mil t', 'data': '2026-10-29', 'nota': 'Queda de 9,6%', 'url': BC},
    {'id': 'wb-2026', 'quem': 'Banco Mundial', 'safra': '2026', 'indicador': 'Preço médio projetado', 'valor': 4900, 'unidade': 'US$/t', 'data': '2026-10', 'nota': 'Commodity Markets Outlook de outubro', 'url': 'https://rankiapro.com/en/insights/what-is-the-situation-of-cocoa-in-2025/'},
    {'id': 'wb-2027', 'quem': 'Banco Mundial', 'safra': '2027', 'indicador': 'Preço médio projetado', 'valor': 5400, 'unidade': 'US$/t', 'data': '2026-10', 'nota': 'Alta de cerca de 10% sobre 2026', 'url': 'https://rankiapro.com/en/insights/what-is-the-situation-of-cocoa-in-2025/'},
]
save('balanco_projecoes', bal, 'Estimativas públicas de balanço global e de preço (ICCO, StoneX em nota pública, Banco Mundial)')
print('ok')
