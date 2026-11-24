# Prepara as bases agregadas do Observatório do Cacau a partir dos arquivos tratados pela Youx.
import json, pandas as pd
U = '/mnt/user-data/uploads/'
CODE = open(__file__, encoding='utf-8').read()

def save(name, df, inputs, notes=''):
    df = df.astype(object).where(pd.notna(df), None)
    meta = [{'label': 'prep.py', 'value': CODE, 'type': 'code', 'lang': 'python'},
            {'label': 'Entrada', 'value': inputs}]
    if notes: meta.append({'label': 'Nota', 'value': notes})
    json.dump({'rows': df.to_dict('records'), 'meta': meta},
              open(name + '.json', 'w', encoding='utf-8'), ensure_ascii=False)

# Comércio exterior (Comex Stat / MDIC) — agregado por ano, mês, fluxo e produto
c = pd.read_csv(U + 'importacao_exportacao.csv')
c['fluxo'] = c.importacao_exportacao
m = (c.groupby(['ano', 'mes', 'fluxo', 'sh4', 'produto'], as_index=False)
       .agg(toneladas=('toneladas', 'sum'), fob_usd=('vl_fob', 'sum')))
m['toneladas'] = m.toneladas.round(1)
save('comex_mensal', m, 'importacao_exportacao.csv (Comex Stat, tratado pela Youx)',
     '2026 cobre jan–jul.')

# Por país de destino/origem, ano e fluxo
c['pais'] = c.pais.fillna('Não informado')
p = (c.groupby(['ano', 'fluxo', 'pais'], as_index=False)
       .agg(toneladas=('toneladas', 'sum'), fob_usd=('vl_fob', 'sum')))
p['toneladas'] = p.toneladas.round(1)
save('comex_paises', p, 'importacao_exportacao.csv (Comex Stat, tratado pela Youx)',
     '2026 cobre jan–jul.')

# Aptidão de terras por município + bioma predominante (IBGE) + coordenadas
t = pd.read_csv(U + 'indice_terras_cacau.csv')
t['uso'] = t.classe_uso_solo.map({'Pastagem': 'pasto', 'Formação Florestal': 'floresta'})
t['apt'] = t.classificacao_aptidao.map({'Muito Alto': 'muito_alta', 'Alto': 'alta', 'Médio': 'media', 'Baixo': 'baixa'})
w = t.pivot_table(index='codigo_ibge', columns=['uso', 'apt'], values='area_ha', aggfunc='sum', fill_value=0)
w.columns = [f'{u}_{a}_ha' for u, a in w.columns]
w = w.round(0).reset_index()
b = pd.read_csv(U + 'biomas_municipios.csv')
coords = pd.read_csv('/home/claude/mun.csv')[['codigo_ibge', 'latitude', 'longitude']]
mun = (b.merge(coords, left_on='cod_ibge', right_on='codigo_ibge', how='left')
        .merge(w, left_on='cod_ibge', right_on='codigo_ibge', how='left'))
cols = [x for x in w.columns if x.endswith('_ha')]
mun[cols] = mun[cols].fillna(0)
mun = mun.rename(columns={'bioma': 'bioma_predominante', 'latitude': 'lat', 'longitude': 'lon'})
mun = mun[['cod_ibge', 'municipio', 'uf', 'bioma_predominante', 'lat', 'lon'] + sorted(cols)]
mun['cod_ibge'] = mun.cod_ibge.astype(str)
save('municipios_aptidao', mun,
     'indice_terras_cacau.csv (Youx) + biomas_municipios.csv (IBGE) + coordenadas municipais (github.com/kelvins/municipios-brasileiros)',
     'Áreas em hectares, só nas classes de uso Pastagem e Formação Florestal (MapBiomas), fora de terras indígenas, UCs, quilombos e assentamentos.')

# Aptidão por bioma (bioma de cada polígono, como vem no índice)
bb = t.groupby(['bioma', 'classe_uso_solo', 'classificacao_aptidao'], as_index=False).area_ha.sum()
bb['area_ha'] = bb.area_ha.round(0)
save('aptidao_bioma', bb, 'indice_terras_cacau.csv (Youx)')

# Fontes de dados (planilha da Youx)
f = pd.read_excel(U + 'Fontes_de_Dados_-_Inteligência_Cacau.xlsx', sheet_name='Fonte de dados Gerais')
f = f[f.Fonte.notna()]
f = pd.DataFrame({'fonte': f.Fonte.str.strip(), 'dados': f.Dados, 'link': f.Link,
                  'situacao': f['Status dos Dados'], 'observacao': f['Observações YouX']})
f['fonte'] = f.fonte.str.replace(r'\s+', ' ', regex=True)
# Resumo da situação: fontes cujos dados aparecem neste painel; as demais seguem o texto da Youx
EM_USO = ['SICOR', 'ICCO', 'ECA', 'CAA', 'AIPC', 'IBGE (PAM', 'Comex Stat', 'MAPBIOMAS']
def resumo(r):
    if any(k in r.fonte for k in EM_USO) and r.fonte != 'MAPBIOMAS ALERTA':
        return 'Em uso no painel'
    if pd.isna(r.situacao):
        return 'Mapeada, a avaliar'
    return 'Sem dados ainda'
f['situacao_resumo'] = f.apply(resumo, axis=1)
f['situacao'] = f.situacao.str.strip()
save('fontes', f, 'Fontes_de_Dados_-_Inteligência_Cacau.xlsx, aba "Fonte de dados Gerais"')
