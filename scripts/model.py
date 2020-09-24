#!/usr/bin/env python3.8
# -*- Coding: UTF-8 -*-
"""Modelo de banco de dados.
Constants:
    DATA_BASE - Singleton da instância do banco de dados a ser utilizado
    ao longo do sistema.

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

Empresa:
    secao
    tam_estab_jan
    tipo_estabelecimento
"""
import datetime
from pydal import DAL, Field

from config import DBINFO, FOLDERDB


def model():
    """Instancia o Singleton do Banco de Dados.
    """
    db = DAL(DBINFO, folder=FOLDERDB, pool_size=1)
    table(db)
    return db


def table(db):
    """Definição de tabelas do banco de dados.
    Args:
        db (object): instância do banco de dados.
    """   

    # Endereco

    db.define_table('uf',
                    Field('uf', type='string', unique=True)
                    )

    db.define_table('municipio',
                    Field('municipio', type='string'),
                    Field('uf', 'reference uf')
                    )

    db.define_table('regiao',
                    Field('regiao', type='string', unique=True)
                    )

    db.define_table("endereco",
                    Field('uf', 'reference uf'),
                    Field('municipio', 'reference municipio'),
                    Field('regiao', 'reference regiao')
                    )

    # Empregador

    db.define_table('ind_trab_intermitente',
                    Field('ind_trab_intermitente', type='string', unique=True)
                    )

    db.define_table('ind_trab_parcial',
                    Field('ind_trab_parcial', type='string', unique=True)
                    )

    db.define_table('indicador_aprendiz',
                    Field('indicador_aprendiz', type='string', unique=True)
                    )

    db.define_table('tipo_empregador',
                    Field('tipo_empregador', type='string', unique=True)
                    )

    db.define_table('horas_contratuais',
                    Field('horas_contratuais', type='string', unique=True)
                    )

    db.define_table('profissao',
                    Field('ind_trab_intermitente',
                          'reference ind_trab_intermitente'),
                    Field('ind_trab_parcial', 'reference ind_trab_parcial'),
                    Field('indicador_aprendiz', 'reference indicador_aprendiz'),
                    Field('tipo_empregador', 'reference tipo_empregador'),
                    Field('horas_contratuais', 'reference horas_contratuais')
                    )

    # Financeiro

    db.define_table('tipo_movimentacao',
                    Field('tipo_movimentacao', type='string', unique=True)
                    )

    db.define_table('fonte',
                    Field('fonte', type='string', unique=True)
                    )

    
    # Empresa

    db.define_table('secao',
                    Field('secao', type='string', unique=True)
                    )

    db.define_table('tam_estab_jan',
                    Field('tam_estab_jan', type='string', unique=True)
                    )

    db.define_table('tipo_estabelecimento',
                    Field('tipo_estabelecimento', type='string', unique=True)
                    )

    db.define_table("empregador",
                    Field('secao', 'reference secao'),
                    Field('tam_estab_jan', 'reference tam_estab_jan'),
                    Field('tipo_estabelecimento',
                          'reference tipo_estabelecimento')
                    )

    # Pessoal

    db.define_table('categoria',
                    Field('categoria', type='string', unique=True)
                    )

    db.define_table('competencia',
                    Field('competencia', type='string', unique=True)
                    )

    db.define_table('subclasse',
                    Field('subclasse', type='string', unique=True)
                    )

    db.define_table('sexo',
                    Field('sexo', type='string', unique=True)
                    )

    db.define_table('cbo2002_ocupacao',
                    Field('cbo2002_ocupacao', type='string', unique=True)
                    )

    db.define_table('raca_cor',
                    Field('raca_cor', type='string', unique=True)
                    )

    db.define_table('tipo_de_deficiencia',
                    Field('tipo_de_deficiencia', type='string', unique=True)
                    )

    db.define_table('grau_de_instrucao',
                    Field('grau_de_instrucao', type='string', unique=True)
                    )

    db.define_table('individuo',
                    Field('uid', type='integer', unique=True),
                    Field('idade', type='integer'),
                    Field('sexo', 'reference sexo'),
                    Field('raca_cor', 'reference raca_cor'),
                    Field('grau_de_instrucao', 'reference grau_de_instrucao'),
                    Field('cbo2002_ocupacao', 'reference cbo2002_ocupacao'),
                    Field('empregador', 'reference empregador'),
                    Field('profissao', 'reference profissao'),
                    Field('endereco', 'reference endereco'),
                    Field('categoria', 'reference categoria'),
                    Field('competencia', 'reference competencia'),
                    Field('subclasse', 'reference subclasse'),
                    Field('tipo_de_deficiencia', 'reference tipo_de_deficiencia')
                    )

    db.define_table('financeiro',
                    Field('salario', type="double"),
                    Field('saldo_movimentacao', type="double"),
                    Field('tipo_movimentacao', 'reference tipo_movimentacao'),
                    Field('fonte', 'reference fonte'),
                    Field('individuo', 'reference individuo')
                    )


DATA_BASE = model()