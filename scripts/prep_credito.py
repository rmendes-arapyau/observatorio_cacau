# Recorte de cacau do crédito rural 2025 (Matriz de Dados do Crédito Rural por produto, BCB),
# a partir das bases do "Painel da Agropecuária Municipal do Brasil, 2025".
import json, pandas as pd
D = '/mnt/user-data/outputs/obs_data/credito/'
CODE = open(__file__, encoding='utf-8').read()
p = pd.read_csv(D + '239868d6ab2e214ef6ae9c175008080e.csv')  # credito_produtos_uf.csv
i = pd.read_csv(D + '6aae96051bf85c89bcfbe22875e10713.csv')  # instituicoes_financeiras.csv
c = p[p['produto'] == 'Cacau'].merge(i, on='cnpj_if', how='left')
c = c.rename(columns={'nome': 'instituicao', 'segmento': 'segmento_if'})
c['cnpj_if'] = c.cnpj_if.astype(int).astype(str).str.zfill(8)
c['linha'] = c.linha.fillna('Sem linha')
c = c[['uf', 'modalidade', 'programa', 'linha', 'finalidade', 'cnpj_if', 'instituicao', 'segmento_if',
       'valor_reais', 'contratos', 'area_ha']].reset_index(drop=True)
c.insert(0, 'id', range(1, len(c) + 1))
c = c.astype(object).where(pd.notna(c), None)
json.dump({'rows': c.to_dict('records'), 'meta': [
    {'label': 'prep_credito.py', 'value': CODE, 'type': 'code', 'lang': 'python'},
    {'label': 'Entrada', 'value': 'credito_produtos_uf.csv e instituicoes_financeiras.csv, do Painel da Agropecuária Municipal do Brasil, 2025 (Matriz de Dados do Crédito Rural, BCB)'},
    {'label': 'Recorte', 'value': "produto = 'Cacau', contratos de 2025"}]},
    open('/mnt/user-data/outputs/obs_data/credito_cacau.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(c), c.valor_reais.sum())
