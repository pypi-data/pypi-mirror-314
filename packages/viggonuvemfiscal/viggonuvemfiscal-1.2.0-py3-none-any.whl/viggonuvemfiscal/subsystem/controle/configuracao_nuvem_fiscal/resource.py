from enum import Enum

import sqlalchemy

from viggocore.common.subsystem import entity
from viggocore.database import db


class ConfiguracaoNuvemFiscalTipo(Enum):
    HOMOLOGACAO = 'HOMOLOGACAO'
    PRODUCAO = 'PRODUCAO'


class ConfiguracaoNuvemFiscal(entity.Entity, db.Model):

    attributes = ['client_id', 'client_secret', 'scope', 'grant_type', 'tipo']
    attributes += entity.Entity.attributes

    client_id = db.Column(db.String(100), nullable=False)
    client_secret = db.Column(db.String(100), nullable=False)
    scope = db.Column(db.String(100), nullable=False)
    grant_type = db.Column(db.String(100), nullable=False)
    authorization = db.Column(db.String(1000), nullable=True)
    tipo = db.Column(sqlalchemy.Enum(ConfiguracaoNuvemFiscalTipo),
                     nullable=False)

    def __init__(self, id, client_id, client_secret, scope, tipo,
                 grant_type='client_credentials', authorization=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.grant_type = grant_type
        self.authorization = authorization
        self.tipo = tipo

    @classmethod
    def individual(self):
        return 'configuracao_nuvem_fiscal'
