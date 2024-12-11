from viggocore.common.subsystem import router


class Router(router.Router):

    def __init__(self, collection, routes=[]):
        super().__init__(collection, routes)

    @property
    def routes(self):
        return [
            {
                'action': 'Cadastrar configuracao para o token da Nuvem Fiscal',
                'method': 'POST',
                'url': self.collection_url,
                'callback': 'create'
            },
            {
                'action': 'Listar configuracao para o token da Nuvem Fiscal',
                'method': 'GET',
                'url': self.collection_url,
                'callback': 'update'
            }
        ]