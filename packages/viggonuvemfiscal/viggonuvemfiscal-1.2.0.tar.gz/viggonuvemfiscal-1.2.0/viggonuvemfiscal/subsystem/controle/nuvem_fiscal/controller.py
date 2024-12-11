import flask
import json
import requests
import os

from viggocore.common import exception, utils, controller


class Controller(controller.CommonController):
    # BASE_URL_PROD = 'https://api.nuvemfiscal.com.br'
    BASE_URL_HOMO = 'https://api.sandbox.nuvemfiscal.com.br'

    def __init__(self, manager, resource_wrap, collection_wrap):
        super(Controller, self).__init__(
            manager, resource_wrap, collection_wrap)

    # funções em comum
    def get_authorization(self):
        authorization = os.getenv('NUVEM_FISCAL_AUTHORIZATION', None)
        if authorization is None:
            raise exception.PreconditionFailed(
                'NUVEM_FISCAL_AUTHORIZATION é obrigatório!')
        return {'Authorization': authorization}

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

    def get_endpoint(self, resource):
        return self.BASE_URL_HOMO + resource

    def executar_requisicao(
       self, method, endpoint, params={}, json={}, headers={}):
        headers.update(self.get_authorization())
        if method == 'GET':
            return requests.get(
                endpoint, params=params, json=json, headers=headers)
        elif method == 'POST':
            return requests.post(
                endpoint, params=params, json=json, headers=headers)
        elif method == 'PUT':
            return requests.put(
                endpoint, params=params, json=json, headers=headers)
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

    # funções chamadas pelas rotas
    # empresa
    def cadastrar_empresa(self):
        data = flask.request.get_json()

        try:
            url = self.get_endpoint('/empresas')
            response = self.executar_requisicao('POST', url, json=data)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def listar_empresas(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            url = self.get_endpoint('/empresas')
            response = self.executar_requisicao('GET', url, params=filters)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def buscar_empresa(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            cpf_cnpj = self.get_cpf_cnpj(**filters)
            url = self.get_endpoint(f'/empresas/{cpf_cnpj}')
            response = self.executar_requisicao('GET', url, params=filters)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def alterar_empresa(self):
        data = flask.request.get_json()

        try:
            cpf_cnpj = self.get_cpf_cnpj(**data)
            url = self.get_endpoint(f'/empresas/{cpf_cnpj}')
            response = self.executar_requisicao('PUT', url, json=data)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    # certificado
    def consultar_certificado(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            cpf_cnpj = self.get_cpf_cnpj(**filters)
            url = self.get_endpoint(f'/empresas/{cpf_cnpj}/certificado')
            response = self.executar_requisicao('GET', url)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def cadastrar_certificado(self):
        data = flask.request.get_json()

        try:
            cpf_cnpj = self.get_cpf_cnpj(**data)
            url = self.get_endpoint(f'/empresas/{cpf_cnpj}/certificado')
            data.pop('cpf_cnpj')
            response = self.executar_requisicao('PUT', url, json=data)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def deletar_certificado(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            cpf_cnpj = self.get_cpf_cnpj(**filters)
            url = self.get_endpoint(f'/empresas/{cpf_cnpj}/certificado')
            response = self.executar_requisicao('DELETE', url)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    # configuracoes
    def consultar_configuracao_nfe(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            cpf_cnpj = self.get_cpf_cnpj(**filters)
            url = self.get_endpoint(f'/empresas/{cpf_cnpj}/nfe')
            response = self.executar_requisicao('GET', url)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def alterar_configuracao_nfe(self):
        data = flask.request.get_json()

        try:
            cpf_cnpj = self.get_cpf_cnpj(**data)
            url = self.get_endpoint(f'/empresas/{cpf_cnpj}/nfe')
            data.pop('cpf_cnpj')
            response = self.executar_requisicao('PUT', url, json=data)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def consultar_configuracao_nfce(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            cpf_cnpj = self.get_cpf_cnpj(**filters)
            url = self.get_endpoint(f'/empresas/{cpf_cnpj}/nfce')
            response = self.executar_requisicao('GET', url)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def alterar_configuracao_nfce(self):
        data = flask.request.get_json()

        try:
            cpf_cnpj = self.get_cpf_cnpj(**data)
            url = self.get_endpoint(f'/empresas/{cpf_cnpj}/nfce')
            data.pop('cpf_cnpj')
            response = self.executar_requisicao('PUT', url, json=data)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    # nfe
    def emitir_nfe(self):
        data = flask.request.get_json()

        try:
            url = self.get_endpoint('/nfe')
            response = self.executar_requisicao('POST', url, json=data)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def listar_nfe(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            url = self.get_endpoint('/nfe')
            response = self.executar_requisicao('GET', url, params=filters)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def consulta_status_do_servico_na_sefaz_autorizadora_nfe(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            url = self.get_endpoint('/nfe/sefaz/status')
            response = self.executar_requisicao('GET', url, params=filters)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def consultar_nfe(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            nfe_id = self.get_nfe_id(**filters)
            url = self.get_endpoint(f'/nfe/{nfe_id}')
            response = self.executar_requisicao('GET', url)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def baixar_xml_nfe(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            nfe_id = self.get_nfe_id(**filters)
            url = self.get_endpoint(f'/nfe/{nfe_id}/xml')
            response = self.executar_requisicao('GET', url)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def consultar_cancelamento_nfe(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            nfe_id = self.get_nfe_id(**filters)
            url = self.get_endpoint(f'/nfe/{nfe_id}/cancelamento')
            response = self.executar_requisicao('GET', url)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def baixar_xml_cancelamento_nfe(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            nfe_id = self.get_nfe_id(**filters)
            url = self.get_endpoint(f'/nfe/{nfe_id}/cancelamento/xml')
            response = self.executar_requisicao('GET', url)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def cancelar_nfe_autorizada(self):
        data = flask.request.get_json()

        try:
            nfe_id = self.get_nfe_id(**data)
            url = self.get_endpoint(f'/nfe/{nfe_id}/cancelamento')
            data.pop('nfe_id')
            response = self.executar_requisicao('POST', url, json=data)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    # nfce
    def emitir_nfce(self):
        data = flask.request.get_json()

        try:
            url = self.get_endpoint('/nfce')
            response = self.executar_requisicao('POST', url, json=data)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def listar_nfce(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            url = self.get_endpoint('/nfce')
            response = self.executar_requisicao('GET', url, params=filters)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def consulta_status_do_servico_na_sefaz_autorizadora_nfce(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            url = self.get_endpoint('/nfce/sefaz/status')
            response = self.executar_requisicao('GET', url, params=filters)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def consultar_nfce(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            nfce_id = self.get_nfce_id(**filters)
            url = self.get_endpoint(f'/nfce/{nfce_id}')
            response = self.executar_requisicao('GET', url)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def baixar_xml_nfce(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            nfce_id = self.get_nfce_id(**filters)
            url = self.get_endpoint(f'/nfce/{nfce_id}/xml')
            response = self.executar_requisicao('GET', url)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def consultar_cancelamento_nfce(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            nfce_id = self.get_nfce_id(**filters)
            url = self.get_endpoint(f'/nfce/{nfce_id}/cancelamento')
            response = self.executar_requisicao('GET', url)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def baixar_xml_cancelamento_nfce(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            nfce_id = self.get_nfce_id(**filters)
            url = self.get_endpoint(f'/nfce/{nfce_id}/cancelamento/xml')
            response = self.executar_requisicao('GET', url)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")

    def cancelar_nfce_autorizada(self):
        data = flask.request.get_json()

        try:
            nfce_id = self.get_nfce_id(**data)
            url = self.get_endpoint(f'/nfce/{nfce_id}/cancelamento')
            data.pop('nfce_id')
            response = self.executar_requisicao('POST', url, json=data)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response_dict = self.montar_response_dict(response)

        return flask.Response(response=utils.to_json(response_dict),
                              status=response.status_code,
                              mimetype="application/json")
