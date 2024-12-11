from viggocore.common import subsystem
from viggonuvemfiscal.subsystem.controle.nuvem_fiscal \
  import resource, controller, router, manager

subsystem = subsystem.Subsystem(resource=resource.NuvemFiscal,
                                controller=controller.Controller,
                                manager=manager.Manager,
                                router=router.Router)
