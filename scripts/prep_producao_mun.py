# Produção municipal de cacau em amêndoa, 2025 (IBGE PAM), a partir da base do Painel da Agropecuária Municipal,
# com o bioma predominante de cada município (IBGE).
import json, pandas as pd
pam = pd.read_csv('/mnt/user-data/outputs/obs_data/credito/54bc626fa4a1b6b26a91bfd85e4f8f83.csv')  # pam_2025_municipios.csv
c = pam[pam['produto'] == 'Cacau (em amêndoa)'].copy()
b = pd.read_csv('/mnt/user-data/uploads/biomas_municipios.csv')[['cod_ibge', 'bioma']]
c = c.merge(b, on='cod_ibge', how='left').rename(columns={'bioma': 'bioma_predominante', 'quantidade': 'toneladas'})
c['kg_ha'] = (c.toneladas * 1000 / c.area_ha).where(c.area_ha > 0).round(0)
c['cod_ibge'] = c.cod_ibge.astype(str)
c = c[['cod_ibge', 'municipio', 'uf', 'bioma_predominante', 'toneladas', 'area_ha', 'kg_ha', 'valor_mil_reais']].sort_values('toneladas', ascending=False)
c = c.astype(object).where(pd.notna(c), None)
json.dump({'rows': c.to_dict('records'), 'meta': [
  {'label': 'prep_producao_mun.py', 'value': open(__file__, encoding='utf-8').read(), 'type': 'code', 'lang': 'python'},
  {'label': 'Entrada', 'value': 'pam_2025_municipios.csv (Painel da Agropecuária Municipal, IBGE PAM 2025) e biomas_municipios.csv (IBGE)'}]},
  open('/mnt/user-data/outputs/obs_data/producao_municipal_2025.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(c), c.bioma_predominante.isna().sum())
