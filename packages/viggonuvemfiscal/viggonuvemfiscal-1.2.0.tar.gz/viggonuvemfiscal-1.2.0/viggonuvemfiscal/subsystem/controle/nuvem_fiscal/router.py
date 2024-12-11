from viggocore.common.subsystem import router


class Router(router.Router):

    def __init__(self, collection, routes=[]):
        super().__init__(collection, routes)
        self.collection_url = '/nuvem_fiscals'
        self.resource_url = '/nuvem_fiscal'

    @property
    def routes(self):
        return [
            {
                'action': 'Cadastrar empresa na Nuvem Fiscal',
                'method': 'POST',
                'url': self.collection_url + '/cadastrar_empresa',
                'callback': 'cadastrar_empresa'
            },
            {
                'action': 'Listar empresas na Nuvem Fiscal',
                'method': 'GET',
                'url': self.collection_url + '/listar_empresas',
                'callback': 'listar_empresas'
            },
            {
                'action': 'Buscar empresa na Nuvem Fiscal',
                'method': 'GET',
                'url': self.collection_url + '/buscar_empresa',
                'callback': 'buscar_empresa'
            },
            {
                'action': 'Alterar empresa na Nuvem Fiscal',
                'method': 'PUT',
                'url': self.collection_url + '/alterar_empresa',
                'callback': 'alterar_empresa'
            },
            {
                'action': 'Consultar o certificado na Nuvem Fiscal',
                'method': 'GET',
                'url': self.collection_url + '/consultar_certificado',
                'callback': 'consultar_certificado'
            },
            {
                'action': 'Cadastrar o certificado na Nuvem Fiscal',
                'method': 'PUT',
                'url': self.collection_url + '/cadastrar_certificado',
                'callback': 'cadastrar_certificado'
            },
            {
                'action': 'Deletar o certificado na Nuvem Fiscal',
                'method': 'DELETE',
                'url': self.collection_url + '/deletar_certificado',
                'callback': 'deletar_certificado'
            },
            {
                'action': 'Buscar configuracao da NFe na Nuvem Fiscal',
                'method': 'GET',
                'url': self.collection_url + '/consultar_configuracao_nfe',
                'callback': 'consultar_configuracao_nfe'
            },
            {
                'action': 'Alterar configuracao da NFe na Nuvem Fiscal',
                'method': 'PUT',
                'url': self.collection_url + '/alterar_configuracao_nfe',
                'callback': 'alterar_configuracao_nfe'
            },
            {
                'action': 'Emitir NFe na Nuvem Fiscal',
                'method': 'POST',
                'url': self.collection_url + '/emitir_nfe',
                'callback': 'emitir_nfe'
            },
            {
                'action': 'Emitir NFe na Nuvem Fiscal',
                'method': 'GET',
                'url': self.collection_url + '/listar_nfe',
                'callback': 'listar_nfe'
            },
            {
                'action': 'Consulta do Status do Serviço na SEFAZ ' +
                'Autorizadora',
                'method': 'GET',
                'url': (
                    self.collection_url +
                    '/consulta_status_do_servico_na_sefaz_autorizadora_nfe'),
                'callback':
                    'consulta_status_do_servico_na_sefaz_autorizadora_nfe'
            },
            {
                'action': 'Consultar NFe na Nuvem Fiscal',
                'method': 'GET',
                'url': self.collection_url + '/consultar_nfe',
                'callback': 'consultar_nfe'
            },
            {
                'action': 'Baixar XML da NFe processada na Nuvem Fiscal',
                'method': 'GET',
                'url': self.collection_url + '/baixar_xml_nfe',
                'callback': 'baixar_xml_nfe'
            },
            {
                'action': 'Consultar cancelamento da NFe na ' +
                'Nuvem Fiscal',
                'method': 'GET',
                'url': self.collection_url + '/consultar_cancelamento_nfe',
                'callback': 'consultar_cancelamento_nfe'
            },
            {
                'action': 'Baixar XML do cancelamento da NFe processada ' +
                'na Nuvem Fiscal',
                'method': 'GET',
                'url': self.collection_url + '/baixar_xml_cancelamento_nfe',
                'callback': 'baixar_xml_cancelamento_nfe'
            },
            {
                'action': 'Cancelar uma NFe autorizada na Nuvem Fiscal',
                'method': 'POST',
                'url': self.collection_url + '/cancelar_nfe_autorizada',
                'callback': 'cancelar_nfe_autorizada'
            },
        ]
