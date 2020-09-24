#!/usr/bin/env python3.8
# -*- Coding: UTF-8 -*-
''' 
Os dados podem ser organizados nas sequintes colunas:

Gerais:
    categoria            
    cbo2002_ocupacao     
    competencia
    subclasse

Endereco:
    uf 
    municipio    
    regiao  

Empresa:
    secao
    tam_estab_jan
    tipo_estabelecimento

Contrato:
    ind_trab_intermitente
    ind_trab_parcial     
    indicador_aprendiz 
    tipo_empregador
    horas_contratuais

Pessoal: 
    id
    idade
    raca_cor
    sexo
    tipo_de_deficiencia
    grau_de_instrucao

Financeiro:
    salario
    saldo_movimentacao
    tipo_movimentacao
    fonte
'''
import json
import requests
import pandas as pd
import requests_cache

from model import DATA_BASE as db


URL = 'http://dataeng.quero.com:5000/caged-data'

requests_cache.install_cache('quero', backend='sqlite', expire_after=3600)


def get_data():
    '''Get Data form QUERO'''
    r = requests.get(URL)
    data = r.json()
    if data['success'] is True:
        return pd.DataFrame.from_dict(data["caged"])
    raise Exception('Data Source', "No Data")


def inject_unique_datas(uniques):
    for key, values in uniques.items():
        for kvalue in values:
            op = f"db.{key}.update_or_insert({key}=\'{kvalue}\')"
            id_op = eval(op)
            uniques[key][kvalue] = id_op
    db.commit()
    return uniques


def data_frame():
    df = get_data()

    endereco = ['uf', 'municipio', 'regiao']

    profissao = ['ind_trab_intermitente', 'ind_trab_parcial', 'indicador_aprendiz', 'tipo_empregador',
                 'horas_contratuais']

    financeiro = ['tipo_movimentacao', 'fonte']

    empregador = ['secao', 'tam_estab_jan', 'tipo_estabelecimento']

    pessoal = ['categoria', 'competencia', 'subclasse', 'sexo',
               'cbo2002_ocupacao', 'raca_cor', 'tipo_de_deficiencia', 'grau_de_instrucao']

    uniques = endereco + profissao + financeiro + empregador + pessoal

    uniques_dict = {
        uns: {uni: None for uni in df[uns].unique()} for uns in uniques}
    uniques_dict = inject_unique_datas(uniques_dict)

    for idx_row in df.iterrows():
        row = idx_row[1]

        db(db.municipio.id == uniques_dict['municipio'][row['municipio']]).update(
            uf=uniques_dict['uf'][row['uf']]
        )

        id_end = db.endereco.insert(
            uf=uniques_dict['uf'][row['uf']],
            municipio=uniques_dict['municipio'][row['municipio']],
            regiao=uniques_dict['regiao'][row['regiao']]
        )

        id_prof = db.profissao.insert(
            ind_trab_intermitente=uniques_dict['ind_trab_intermitente'][row['ind_trab_intermitente']],
            indicador_aprendiz=uniques_dict['indicador_aprendiz'][row['indicador_aprendiz']],
            tipo_empregador=uniques_dict['tipo_empregador'][row['tipo_empregador']],
            horas_contratuais=uniques_dict['horas_contratuais'][row['horas_contratuais']],
            ind_trab_parcial=uniques_dict['ind_trab_parcial'][row['ind_trab_parcial']]
        )

        id_emp = db.empregador.insert(
            secao=uniques_dict['secao'][row['secao']],
            tam_estab_jan=uniques_dict['tam_estab_jan'][row['tam_estab_jan']],
            tipo_estabelecimento=uniques_dict['tipo_estabelecimento'][row['tipo_estabelecimento']]
        )

        indid = db.individuo.insert(
            uid=row['id'],
            idade=row['idade'],
            sexo=uniques_dict['sexo'][row['sexo']],
            raca_cor=uniques_dict['raca_cor'][row['raca_cor']],
            grau_de_instrucao=uniques_dict['grau_de_instrucao'][row['grau_de_instrucao']],
            cbo2002_ocupacao=uniques_dict['cbo2002_ocupacao'][row['cbo2002_ocupacao']],
            empregador=id_emp,
            profissao=id_prof,
            endereco=id_end,
            categoria=uniques_dict['categoria'][row['categoria']],
            competencia=uniques_dict['competencia'][row['competencia']],
            subclasse=uniques_dict['subclasse'][row['subclasse']],
            tipo_de_deficiencia=uniques_dict['tipo_de_deficiencia'][row['tipo_de_deficiencia']]

        )

        db.financeiro.insert(
            salario=row['salario'].replace(",", ""),
            saldo_movimentacao=row['saldo_movimentacao'].replace(",", ""),
            tipo_movimentacao=uniques_dict['tipo_movimentacao'][row['tipo_movimentacao']],
            fonte=uniques_dict['fonte'][row['fonte']],
            individuo=indid,
        )
    db.commit()


if __name__ == "__main__":
    data_frame()
