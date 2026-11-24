# Acrescenta 2025 à série de produção de cacau por estado (IBGE PAM), somando os municípios
# da base PAM 2025 do "Painel da Agropecuária Municipal do Brasil, 2025".
import pandas as pd
UF = {'AC':'Acre','AL':'Alagoas','AM':'Amazonas','AP':'Amapá','BA':'Bahia','CE':'Ceará','DF':'Distrito Federal',
      'ES':'Espírito Santo','GO':'Goiás','MA':'Maranhão','MG':'Minas Gerais','MS':'Mato Grosso do Sul','MT':'Mato Grosso',
      'PA':'Pará','PB':'Paraíba','PE':'Pernambuco','PI':'Piauí','PR':'Paraná','RJ':'Rio de Janeiro','RN':'Rio Grande do Norte',
      'RO':'Rondônia','RR':'Roraima','RS':'Rio Grande do Sul','SC':'Santa Catarina','SE':'Sergipe','SP':'São Paulo','TO':'Tocantins'}
base = pd.read_csv('/mnt/user-data/uploads/producao_area_ibge.csv')
pam = pd.read_csv('/mnt/user-data/outputs/obs_data/credito/54bc626fa4a1b6b26a91bfd85e4f8f83.csv')  # pam_2025_municipios.csv
c = pam[pam['produto'] == 'Cacau (em amêndoa)']
assert set(c.unidade_quantidade) == {'t'}
n = c.groupby('uf', as_index=False).agg(toneladas=('quantidade', 'sum'), area_ha=('area_ha', 'sum'))
n['estado'] = n.uf.map(UF); n['ano'] = 2025
n['toneladas'] = n.toneladas.round().astype(int)
n['id'] = range(int(base.id.max()) + 1, int(base.id.max()) + 1 + len(n))
out = pd.concat([base[base.ano != 2025], n[['id', 'ano', 'toneladas', 'area_ha', 'estado']]]).sort_values(['estado', 'ano'])
out.to_csv('/mnt/user-data/outputs/obs_data/producao_area_ibge_2009_2025.csv', index=False)
print(n[['estado', 'toneladas', 'area_ha']].sort_values('toneladas', ascending=False).to_string(), n.toneladas.sum(), n.area_ha.sum())
import json
json.dump({'rows': out.to_dict('records'), 'meta': [
    {'label': 'prep_producao.py', 'value': open(__file__, encoding='utf-8').read(), 'type': 'code', 'lang': 'python'},
    {'label': 'Entrada', 'value': 'producao_area_ibge.csv (Youx, 2009–2024) e pam_2025_municipios.csv (Painel da Agropecuária Municipal, PAM 2025)'}]},
    open('/mnt/user-data/outputs/obs_data/producao_ibge_2009_2025.json', 'w', encoding='utf-8'), ensure_ascii=False)
