# Leitura do mês do Observatório do Cacau: manchete e fatores, escritos a partir das fontes públicas citadas em cada linha.
import json
BC = 'https://www.tradingview.com/news/barchart:a9e104e91094b:0-cocoa-prices-supported-by-reduced-ivory-coast-shipments/'
rows = [
 ('manchete', 1, 'Safra marfinense mais curta e El Niño forte sustentam o preço; estoques altos e demanda irregular seguram as altas', None, None),
 ('altista', 1, 'As chegadas aos portos da Costa do Marfim somam 330,8 mil t de 1º de outubro a 22 de novembro, 46,5% abaixo do mesmo período da safra passada.', 'Governo marfinense, via Bloomberg/Barchart', BC),
 ('altista', 2, 'Exportadores e contadores de vagens cortaram a safra marfinense 2026/27 para 1,5 a 1,6 milhão de t, ante 2,15 milhões entregues em 2025/26. A safra intermediária pode cair quase pela metade.', 'Reuters, 4/nov', 'https://www.cnbcafrica.com/2026/ivory-coast-cocoa-mid-crop-forecast-cut-after-weak-rains-sources-say'),
 ('altista', 3, 'A NOAA vê El Niño forte a muito forte até jan–mar/2027, com mais de 79% de chance. O fenômeno costuma trazer tempo mais seco ao Oeste Africano na época do Harmatã.', 'NOAA CPC, 12/nov', 'https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/roni/strengths/'),
 ('altista', 4, 'Gana estima 650 mil t em 2026/27, 13% a menos que em 2025/26, por doenças, envelhecimento das lavouras e clima.', 'Cocobod, via Barchart', BC),
 ('altista', 5, 'Enchentes no litoral do Equador danificaram estradas e lavouras; analistas projetam produção de cerca de 580 mil t, 7% abaixo do esperado.', 'Bloomberg, via Barchart', BC),
 ('baixista', 1, 'Os estoques certificados na bolsa de Nova York chegaram a 3,85 milhões de sacas, o maior nível em dois anos e meio.', 'ICE, via Barchart', BC),
 ('baixista', 2, 'Os índices S&P GSCI e Bloomberg Commodity vão reduzir o peso do cacau em 2027, o que leva fundos de índice a vender contratos antes do rebalanceamento.', 'Barchart', BC),
 ('baixista', 3, 'A demanda segue irregular: a moagem subiu na Ásia (+29%) e na Europa (+3,2%) no 3º trimestre, mas caiu 2,5% na América do Norte, e o acumulado europeu de 2026 é o menor desde 2015.', 'CAA, ECA e NCA, via imprensa', 'https://www.mckeany-flavell.com/q3-2026-cocoa-grindings-show-uneven-recovery-10-19-26/'),
 ('baixista', 4, 'No Brasil, a indústria recebeu 25,3% mais amêndoas na safra 2025/26 e não importou amêndoas no 2º e no 3º trimestres, o que pressiona o preço pago ao produtor.', 'AIPC', 'https://www.canalrural.com.br/radar/cacau-brasileiro-dispara-253-na-safra-2025-26-e-supera-226-mil-toneladas/'),
 ('baixista', 5, 'As exportações de amêndoas da Nigéria subiram 33% em setembro na comparação anual.', 'Barchart', BC),
]
out = [{'id': f'{t}-{o}', 'edicao': '2026-11', 'data_corte': '2026-11-24', 'tipo': t, 'ordem': o, 'texto': x, 'fonte': f, 'url': u} for t, o, x, f, u in rows]
json.dump({'rows': out, 'meta': [{'label': 'leitura.py', 'value': open(__file__, encoding='utf-8').read(), 'type': 'code', 'lang': 'python'},
  {'label': 'Nota', 'value': 'Textos escritos pelo Claude a partir das fontes públicas de cada linha, para revisão da equipe de Conhecimento.'}]},
  open('/mnt/user-data/outputs/obs_data/tend/tendencias_leitura.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(out))
