
SYSADMIN_EXCLUSIVE_POLICIES = [
    ('/ufs', ['POST']),
    ('/ufs/<id>', ['PUT', 'DELETE']),

    ('/municipios', ['POST']),
    ('/municipios/<id>', ['PUT', 'DELETE']),

    ('/regioes', ['POST']),
    ('/regioes/<id>', ['PUT', 'DELETE']),

    ('/mesorregioes', ['POST']),
    ('/mesorregioes/<id>', ['PUT', 'DELETE']),

    ('/microrregioes', ['POST']),
    ('/microrregioes/<id>', ['PUT', 'DELETE']),

    ('/ibge_syncs', ['POST', 'GET']),
    ('/ibge_syncs/<id>', ['PUT', 'GET', 'DELETE'])
]

SYSADMIN_RESOURCES = []

USER_RESOURCES = [
    ('/municipios', ['GET']),
    ('/municipios/<id>', ['GET']),

    ('/ufs', ['GET']),
    ('/ufs/<id>', ['GET']),

    ('/regioes', ['GET']),
    ('/regioes/<id>', ['GET']),

    ('/mesorregioes', ['GET']),
    ('/mesorregioes/<id>', ['GET']),

    ('/microrregioes', ['GET']),
    ('/microrregioes/<id>', ['GET'])
]
