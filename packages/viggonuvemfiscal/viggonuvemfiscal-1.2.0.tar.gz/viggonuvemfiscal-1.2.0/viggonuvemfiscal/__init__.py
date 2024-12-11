import os
import viggocore

from viggocore.system import System
from flask_cors import CORS
from viggonuvemfiscal.subsystem.controle \
    import nuvem_fiscal, configuracao_nuvem_fiscal
from viggonuvemfiscal.resources import SYSADMIN_EXCLUSIVE_POLICIES, \
    SYSADMIN_RESOURCES, USER_RESOURCES


system = System('viggonuvemfiscal',
                [nuvem_fiscal.subsystem,configuracao_nuvem_fiscal.subsystem],
                USER_RESOURCES,
                SYSADMIN_RESOURCES,
                SYSADMIN_EXCLUSIVE_POLICIES)


class SystemFlask(viggocore.SystemFlask):

    def __init__(self):
        super().__init__(system)

    def configure(self):
        origins_urls = os.environ.get('ORIGINS_URLS', '*')
        CORS(self, resources={r'/*': {'origins': origins_urls}})

        self.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        viggonuvemfiscal_database_uri = os.getenv('viggonuvemfiscal_DATABASE_URI', None)
        if viggonuvemfiscal_database_uri is None:
            raise Exception('viggonuvemfiscal_DATABASE_URI not defined in enviroment.')
        else:
            # URL os enviroment example for Postgres
            # export viggonuvemfiscal_DATABASE_URI=
            # mysql+pymysql://root:mysql@localhost:3306/viggonuvemfiscal
            self.config['SQLALCHEMY_DATABASE_URI'] = viggonuvemfiscal_database_uri
