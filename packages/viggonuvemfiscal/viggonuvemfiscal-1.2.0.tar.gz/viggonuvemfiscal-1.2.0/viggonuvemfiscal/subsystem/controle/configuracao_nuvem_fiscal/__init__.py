from viggocore.common import subsystem
from viggonuvemfiscal.subsystem.controle.configuracao_nuvem_fiscal \
  import resource, manager, router

subsystem = subsystem.Subsystem(resource=resource.ConfiguracaoNuvemFiscal,
                                manager=manager.Manager,
                                router=router.Router)
