import json
import requests
from viggocore.common.subsystem import operation, manager
from viggocore.common import exception, utils
from viggonuvemfiscal.subsystem.controle.configuracao_nuvem_fiscal.resource \
    import ConfiguracaoNuvemFiscalTipo as cnf_tipo


# classes das chamadas a api da Nuvem Fiscal envolvendo empresa
class CadastrarEmpresa(operation.Create):

    def pre(self, session, **kwargs):
        return True

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/empresas', ambiente)
        return self.manager.executar_requisicao(
            'POST', url, json=kwargs, ambiente=ambiente)


class ListarEmpresas(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/empresas', ambiente)
        return self.manager.executar_requisicao(
            'GET', url, params=kwargs, ambiente=ambiente)


class BuscarEmpresa(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        cpf_cnpj = self.manager.get_cpf_cnpj(**kwargs)
        url = self.manager.get_endpoint(f'/empresas/{cpf_cnpj}', ambiente)
        return self.manager.executar_requisicao(
            'GET', url, params=kwargs, ambiente=ambiente)


class AlterarEmpresa(operation.Update):

    def pre(self, session, **kwargs):
        return True

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        cpf_cnpj = self.manager.get_cpf_cnpj(**kwargs)
        url = self.manager.get_endpoint(f'/empresas/{cpf_cnpj}', ambiente)
        return self.manager.executar_requisicao(
            'PUT', url, json=kwargs, ambiente=ambiente)


class ConsultarCerticado(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        cpf_cnpj = self.manager.get_cpf_cnpj(**kwargs)
        url = self.manager.get_endpoint(
            f'/empresas/{cpf_cnpj}/certificado', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class CadastrarCertificado(operation.Update):

    def pre(self, session, **kwargs):
        return True

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        cpf_cnpj = self.manager.get_cpf_cnpj(**kwargs)
        url = self.manager.get_endpoint(
            f'/empresas/{cpf_cnpj}/certificado', ambiente)
        kwargs.pop('cpf_cnpj')
        return self.manager.executar_requisicao(
            'PUT', url, json=kwargs, ambiente=ambiente)


class DeletarCertificado(operation.Delete):

    def pre(self, session, **kwargs):
        return True

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        cpf_cnpj = self.manager.get_cpf_cnpj(**kwargs)
        url = self.manager.get_endpoint(
            f'/empresas/{cpf_cnpj}/certificado', ambiente)
        return self.manager.executar_requisicao(
            'DELETE', url, ambiente=ambiente)


class ConsultarConfiguracaoNfe(operation.List):

    def pre(self, session, **kwargs):
        return True

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        cpf_cnpj = self.manager.get_cpf_cnpj(**kwargs)
        url = self.manager.get_endpoint(f'/empresas/{cpf_cnpj}/nfe', ambiente)
        return self.manager.executar_requisicao(
            'GET', url, ambiente=ambiente)


class AlterarConfiguracaoNfe(operation.Update):

    def pre(self, session, **kwargs):
        return True

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        cpf_cnpj = self.manager.get_cpf_cnpj(**kwargs)
        url = self.manager.get_endpoint(f'/empresas/{cpf_cnpj}/nfe', ambiente)
        kwargs.pop('cpf_cnpj')
        return self.manager.executar_requisicao(
            'PUT', url, json=kwargs, ambiente=ambiente)


class ConsultarConfiguracaoNfce(operation.List):

    def pre(self, session, **kwargs):
        return True

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        cpf_cnpj = self.manager.get_cpf_cnpj(**kwargs)
        url = self.manager.get_endpoint(f'/empresas/{cpf_cnpj}/nfce', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class AlterarConfiguracaoNfce(operation.Update):

    def pre(self, session, **kwargs):
        return True

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        cpf_cnpj = self.manager.get_cpf_cnpj(**kwargs)
        url = self.manager.get_endpoint(f'/empresas/{cpf_cnpj}/nfce', ambiente)
        kwargs.pop('cpf_cnpj')
        self.json = utils.to_json(kwargs)
        self.json = json.loads(self.json)
        return self.manager.executar_requisicao(
            'PUT', url, json=self.json, ambiente=ambiente)


# classes das chamadas a api da Nuvem Fiscal envolvendo nfe
class EmitirNfe(operation.Create):

    def pre(self, session, **kwargs):
        nfe_dict = kwargs.pop('nfe_dict', None)
        self.json = utils.to_json(nfe_dict)
        self.json = json.loads(self.json)
        return True

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/nfe', ambiente)
        return self.manager.executar_requisicao(
            'POST', url, json=self.json, ambiente=ambiente)


class ListarNfe(operation.List):
    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/nfe', ambiente)
        return self.manager.executar_requisicao(
            'GET', url, params=kwargs, ambiente=ambiente)


class ConsultaStatusDoServicoNaSefazAutorizadoraNfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/nfe/sefaz/status', ambiente)
        return self.manager.executar_requisicao(
            'GET', url, params=kwargs, ambiente=ambiente)


class ConsultarNfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfe_id = self.manager.get_nfe_id(**kwargs)
        url = self.manager.get_endpoint(f'/nfe/{nfe_id}', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class BaixarXmlNfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfe_id = self.manager.get_nfe_id(**kwargs)
        url = self.manager.get_endpoint(f'/nfe/{nfe_id}/xml', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class BaixarXmlNotaNfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfe_id = self.manager.get_nfe_id(**kwargs)
        url = self.manager.get_endpoint(f'/nfe/{nfe_id}/xml/nota', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class BaixarPdfDanfeNfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfe_id = self.manager.get_nfe_id(**kwargs)
        url = self.manager.get_endpoint(f'/nfe/{nfe_id}/pdf', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class ConsultarCancelamentoNfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfe_id = self.manager.get_nfe_id(**kwargs)
        url = self.manager.get_endpoint(
            f'/nfe/{nfe_id}/cancelamento', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class BaixarXmlCancelamentoNfe(operation.List):
    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfe_id = self.manager.get_nfe_id(**kwargs)
        url = self.manager.get_endpoint(
            f'/nfe/{nfe_id}/cancelamento/xml', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class CancelarNfeAutorizada(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfe_id = self.manager.get_nfe_id(**kwargs)
        url = self.manager.get_endpoint(
            f'/nfe/{nfe_id}/cancelamento', ambiente)
        kwargs.pop('nfe_id')
        return self.manager.executar_requisicao(
            'POST', url, json=kwargs, ambiente=ambiente)


class InutilizarSeqNumNfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/nfe/inutilizacoes', ambiente)
        return self.manager.executar_requisicao(
            'POST', url, json=kwargs, ambiente=ambiente)


# classes das chamadas a api da Nuvem Fiscal envolvendo nfce
class EmitirNfce(operation.Create):

    def pre(self, session, **kwargs):
        nfce_dict = kwargs.pop('nfce_dict', None)
        self.json = utils.to_json(nfce_dict)
        self.json = json.loads(self.json)
        return True

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/nfce', ambiente)
        return self.manager.executar_requisicao(
            'POST', url, json=self.json, ambiente=ambiente)


class ListarNfce(operation.List):
    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/nfce', ambiente)
        return self.manager.executar_requisicao(
            'GET', url, params=kwargs, ambiente=ambiente)


class ConsultaStatusDoServicoNaSefazAutorizadoraNfce(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/nfce/sefaz/status', ambiente)
        return self.manager.executar_requisicao(
            'GET', url, params=kwargs, ambiente=ambiente)


class ConsultarNfce(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfce_id = self.manager.get_nfce_id(**kwargs)
        url = self.manager.get_endpoint(f'/nfce/{nfce_id}', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class BaixarXmlNfce(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfce_id = self.manager.get_nfce_id(**kwargs)
        url = self.manager.get_endpoint(f'/nfce/{nfce_id}/xml', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class BaixarXmlNotaNfce(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfce_id = self.manager.get_nfce_id(**kwargs)
        url = self.manager.get_endpoint(f'/nfce/{nfce_id}/xml/nota', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class BaixarPdfDanfeNfce(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        if type(ambiente) == str:
            ambiente = cnf_tipo[ambiente]
        nfce_id = self.manager.get_nfce_id(**kwargs)
        url = self.manager.get_endpoint(
            f'/nfce/{nfce_id}/pdf', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class ConsultarCancelamentoNfce(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfce_id = self.manager.get_nfce_id(**kwargs)
        url = self.manager.get_endpoint(
            f'/nfce/{nfce_id}/cancelamento', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class BaixarXmlCancelamentoNfce(operation.List):
    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfce_id = self.manager.get_nfce_id(**kwargs)
        url = self.manager.get_endpoint(
            f'/nfce/{nfce_id}/cancelamento/xml', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class CancelarNfceAutorizada(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfce_id = self.manager.get_nfce_id(**kwargs)
        url = self.manager.get_endpoint(
            f'/nfce/{nfce_id}/cancelamento', ambiente)
        kwargs.pop('nfce_id')
        return self.manager.executar_requisicao(
            'POST', url, json=kwargs, ambiente=ambiente)


class InutilizarSeqNumNfce(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/nfce/inutilizacoes', ambiente)
        return self.manager.executar_requisicao(
            'POST', url, json=kwargs, ambiente=ambiente)


# classes das chamadas a api da Nuvem Fiscal envolvendo mdfe
class EmitirMdfe(operation.Create):

    def pre(self, session, **kwargs):
        nfe_dict = kwargs.pop('mdfe_dict', None)
        self.json = utils.to_json(nfe_dict)
        self.json = json.loads(self.json)
        return True

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/mdfe', ambiente)
        return self.manager.executar_requisicao(
            'POST', url, json=self.json, ambiente=ambiente)


class ListarMdfe(operation.List):
    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/mdfe', ambiente)
        return self.manager.executar_requisicao(
            'GET', url, params=kwargs, ambiente=ambiente)


class ConsultaStatusDoServicoNaSefazAutorizadoraMdfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/mdfe/sefaz/status', ambiente)
        return self.manager.executar_requisicao(
            'GET', url, params=kwargs, ambiente=ambiente)


class ConsultarMdfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        nfe_id = self.manager.get_nfe_id(**kwargs)
        url = self.manager.get_endpoint(f'/mdfe/{nfe_id}', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class BaixarXmlMdfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        mdfe_id = self.manager.get_mdfe_id(**kwargs)
        url = self.manager.get_endpoint(f'/mdfe/{mdfe_id}/xml', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class BaixarXmlNotaMdfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        mdfe_id = self.manager.get_mdfe_id(**kwargs)
        url = self.manager.get_endpoint(f'/mdfe/{mdfe_id}/xml/nota', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class BaixarPdfDanfeMdfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        mdfe_id = self.manager.get_mdfe_id(**kwargs)
        url = self.manager.get_endpoint(f'/mdfe/{mdfe_id}/pdf', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class ConsultarCancelamentoMdfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        mdfe_id = self.manager.get_mdfe_id(**kwargs)
        url = self.manager.get_endpoint(
            f'/mdfe/{mdfe_id}/cancelamento', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class BaixarXmlCancelamentoMdfe(operation.List):
    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        mdfe_id = self.manager.get_mdfe_id(**kwargs)
        url = self.manager.get_endpoint(
            f'/mdfe/{mdfe_id}/cancelamento/xml', ambiente)
        return self.manager.executar_requisicao('GET', url, ambiente=ambiente)


class CancelarMdfeAutorizada(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        mdfe_id = self.manager.get_mdfe_id(**kwargs)
        url = self.manager.get_endpoint(
            f'/mdfe/{mdfe_id}/cancelamento', ambiente)
        kwargs.pop('mdfe_id')
        return self.manager.executar_requisicao(
            'POST', url, json=kwargs, ambiente=ambiente)


class InutilizarSeqNumMdfe(operation.List):

    def do(self, session, **kwargs):
        ambiente = kwargs.pop('api_fiscal', None)
        url = self.manager.get_endpoint('/mdfe/inutilizacoes', ambiente)
        return self.manager.executar_requisicao(
            'POST', url, json=kwargs, ambiente=ambiente)


class Manager(manager.Manager):
    BASE_URL_PROD = 'https://api.nuvemfiscal.com.br'
    BASE_URL_HOMO = 'https://api.sandbox.nuvemfiscal.com.br'

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        # rotas de empresa
        self.cadastrar_empresa = CadastrarEmpresa(self)
        self.listar_empresas = ListarEmpresas(self)
        self.buscar_empresa = BuscarEmpresa(self)
        self.alterar_empresa = AlterarEmpresa(self)
        self.consultar_certicado = ConsultarCerticado(self)
        self.cadastrar_certificado = CadastrarCertificado(self)
        self.deletar_certificado = DeletarCertificado(self)
        self.consultar_configuracao_nfe = ConsultarConfiguracaoNfe(self)
        self.alterar_configuracao_nfe = AlterarConfiguracaoNfe(self)
        self.consultar_configuracao_nfce = ConsultarConfiguracaoNfce(self)
        self.alterar_configuracao_nfce = AlterarConfiguracaoNfce(self)
        # rotas de nfe
        self.emitir_nfe = EmitirNfe(self)
        self.listar_nfe = ListarNfe(self)
        self.consulta_status_do_servico_na_sefaz_autorizadora_nfe = \
            ConsultaStatusDoServicoNaSefazAutorizadoraNfe(self)
        self.consultar_nfe = ConsultarNfe(self)
        self.baixar_xml_nfe = BaixarXmlNfe(self)
        self.baixar_xml_nota_nfe = BaixarXmlNotaNfe(self)
        self.baixar_pdf_danfe_nfe = BaixarPdfDanfeNfe(self)
        self.consultar_cancelamento_nfe = ConsultarCancelamentoNfe(self)
        self.baixar_xml_cancelamento_nfe = BaixarXmlCancelamentoNfe(self)
        self.cancelar_nfe_autorizada = CancelarNfeAutorizada(self)
        self.inutilizar_seq_num_nfe = InutilizarSeqNumNfe(self)
        # rotas de nfce
        self.emitir_nfce = EmitirNfce(self)
        self.listar_nfce = ListarNfce(self)
        self.consulta_status_do_servico_na_sefaz_autorizadora_nfce = \
            ConsultaStatusDoServicoNaSefazAutorizadoraNfce(self)
        self.consultar_nfce = ConsultarNfce(self)
        self.baixar_xml_nfce = BaixarXmlNfce(self)
        self.baixar_xml_nota_nfce = BaixarXmlNotaNfce(self)
        self.baixar_pdf_danfe_nfce = BaixarPdfDanfeNfce(self)
        self.consultar_cancelamento_nfce = ConsultarCancelamentoNfce(self)
        self.baixar_xml_cancelamento_nfce = BaixarXmlCancelamentoNfce(self)
        self.cancelar_nfce_autorizada = CancelarNfceAutorizada(self)
        self.inutilizar_seq_num_nfce = InutilizarSeqNumNfce(self)
        # rotas de mdfe
        self.emitir_mdfe = EmitirMdfe(self)
        self.listar_mdfe = ListarMdfe(self)
        self.consulta_status_do_servico_na_sefaz_autorizadora_mdfe = \
            ConsultaStatusDoServicoNaSefazAutorizadoraMdfe(self)
        self.consultar_mdfe = ConsultarMdfe(self)
        self.baixar_xml_mdfe = BaixarXmlMdfe(self)
        self.baixar_xml_nota_mdfe = BaixarXmlNotaMdfe(self)
        self.baixar_pdf_danfe_mdfe = BaixarPdfDanfeMdfe(self)
        self.consultar_cancelamento_mdfe = ConsultarCancelamentoMdfe(self)
        self.baixar_xml_cancelamento_mdfe = BaixarXmlCancelamentoMdfe(self)
        self.cancelar_mdfe_autorizada = CancelarMdfeAutorizada(self)
        self.inutilizar_seq_num_mdfe = InutilizarSeqNumMdfe(self)

    def get_authorization(self, ambiente: cnf_tipo = None):
        config = self.api.configuracao_nuvem_fiscals().\
            get_configuracao_nuvem_fiscal(tipo=ambiente)
        data = {'Authorization': config.authorization}

        endpoint = self.get_endpoint('/empresas', ambiente)
        response = requests.get(endpoint, headers=data)

        if response.status_code == 401:
            url = 'https://auth.nuvemfiscal.com.br/oauth/token'
            body = {
                'client_id': config.client_id,
                'client_secret': config.client_secret,
                'grant_type': config.grant_type,
                'scope': config.scope
            }

            headers = {'Content-Type': 'application/x-www-form-urlencoded'}

            response = requests.post(url, data=body, headers=headers)

            if response.status_code == 200:
                response = self.montar_response_dict(response)
                data['Authorization'] = 'Bearer ' + response.get(
                    'access_token', '')
                self.api.configuracao_nuvem_fiscals().update(
                    id=config.id, **{'authorization': data['Authorization']})
            else:
                raise exception.BadRequest(
                    'Não foi possível gerar a autorização.')
        return data

    def get_cpf_cnpj(self, **kwargs):
        cpf_cnpj = kwargs.get('cpf_cnpj', None)
        if cpf_cnpj is None:
            raise exception.BadRequest('O campo cpf_cnpj é obrigatório.')
        return cpf_cnpj

    def get_nfe_id(self, **kwargs):
        nfe_id = kwargs.get('nfe_id', None)
        if nfe_id is None:
            raise exception.BadRequest('O campo nfe_id é obrigatório.')
        return nfe_id

    def get_nfce_id(self, **kwargs):
        nfce_id = kwargs.get('nfce_id', None)
        if nfce_id is None:
            raise exception.BadRequest('O campo nfce_id é obrigatório.')
        return nfce_id

    def get_mdfe_id(self, **kwargs):
        mdfe_id = kwargs.get('mdfe_id', None)
        if mdfe_id is None:
            raise exception.BadRequest('O campo mdfe_id é obrigatório.')
        return mdfe_id

    def get_endpoint(self, resource, ambiente=None):
        urls = {
            cnf_tipo.HOMOLOGACAO: self.BASE_URL_HOMO + resource,
            cnf_tipo.PRODUCAO: self.BASE_URL_PROD + resource}
        return urls.get(ambiente, '')

    def executar_requisicao(self, method, endpoint, ambiente,
                            params={}, json={},
                            headers={'Content-Type': 'application/json'},
                            data={}, sem_authorization=True):

        if sem_authorization is True:
            headers.update(self.get_authorization(ambiente=ambiente))

        if method == 'GET':
            return requests.get(
                endpoint, params=params, json=json, headers=headers, data=data)
        elif method == 'POST':
            return requests.post(
                endpoint, params=params, json=json, headers=headers, data=data)
        elif method == 'PUT':
            return requests.put(
                endpoint, params=params, json=json, headers=headers, data=data)
        elif method == 'DELETE':
            return requests.delete(endpoint)
        else:
            raise exception.OperationBadRequest(
                'Método de requisição não permitido.')

    def montar_response_dict(self, response):
        try:
            response_dict = json.loads(response.text)
        except Exception:
            response_dict = {'error': response.text}
        return response_dict
