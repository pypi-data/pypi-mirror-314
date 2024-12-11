from datetime import date
from typing import Literal

from zeep.helpers import serialize_object

from lg_payroll_api.helpers.api_results import LgApiPaginationReturn, LgApiReturn
from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LgAuthentication
from lg_payroll_api.utils.enums import (
    EnumTipoDeDadosModificadosDaUnidadeOrganizacional,
    EnumTipoDeOperacao,
)


class LgApiOrganizationalUnitClient(BaseLgServiceClient):
    """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

    Default class to connect with the organizational unit endpoints
    """

    def __init__(self, lg_auth: LgAuthentication):
        super().__init__(
            lg_auth=lg_auth, wsdl_service="v1/ServicoDeUnidadeOrganizacional"
        )

    def consult_list(
        self,
        company_code: int,
        level: int = None,
        only_normal: Literal[0, 1] = None,
        only_actives: Literal[0, 1] = None,
        only_with_employees_registration_available: Literal[0, 1] = None,
        search_term: str = None,
    ) -> LgApiReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint to get list of organizational units in LG System

        Returns:
            LgApiReturn: A List of OrderedDict that represents an Object(RetornoDeConsultaLista<UnidadeOrganizacionalParcial>) API response
                [
                    Tipo : int
                    Mensagens : [string]
                    CodigoDoErro : string
                    Retorno : list[Object(UnidadeOrganizacionalParcial)]
                ]
        """

        params = {
            "Nivel": level,
            "SomenteNormais": only_normal,
            "SomenteAtivos": only_actives,
            "SomenteComPermissaoParaCadColaborador": only_with_employees_registration_available,
            "TermoDeBusca": search_term,
            "Empresa": {
                "FiltroComCodigoNumerico": {
                    "Codigo": company_code,
                }
            },
        }

        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsultarLista,
                    body=params,
                    parse_body_on_request=False,
                )
            )
        )

    def list_on_demand(
        self,
        company_code: int = None,
        level: int = None,
        only_actives: Literal[0, 1] = None,
        only_with_employees_registration_available: Literal[0, 1] = None,
        search_term: str = None,
        page: int = None,
    ) -> LgApiPaginationReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint to get list on demand of organizational units in LG System

        Returns:

        A List of OrderedDict that represents an Object(RetornoDeConsultaListaPorDemanda<UnidadeOrganizacional>) API response
            [
                Tipo : int
                Mensagens : [string]
                CodigoDoErro : string
                UnidadeOrganizacional : list[Object(UnidadeOrganizacional)]
            ]
        """

        params = {
            "FiltroDeUnidadeOrganizacionalPorDemanda": {
                "Nivel": level,
                "SomenteAtivos": only_actives,
                "SomenteComPermissaoParaCadColaborador": only_with_employees_registration_available,
                "TermoDeBusca": search_term,
                "Empresa": {
                    "FiltroComCodigoNumerico": {
                        "Codigo": company_code,
                    }
                }
                if company_code
                else None,
                "PaginaAtual": page,
            }
        }

        return LgApiPaginationReturn(
            auth=self.lg_client,
            wsdl_service=self.wsdl_client,
            service_client=self.wsdl_client.service.ConsulteListaPorDemanda,
            body=params,
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsulteListaPorDemanda,
                    body=params,
                )
            )
        )

    def consult_changed_list(
        self,
        start_date: date,
        end_date: date,
        operation_types: list[EnumTipoDeOperacao] = [
            EnumTipoDeOperacao.ALTERACAO.value,
            EnumTipoDeOperacao.INCLUSAO.value,
            EnumTipoDeOperacao.EXCLUSAO.value,
        ],
        organizational_units_codes: list[int] = None,
        modified_data_type: EnumTipoDeDadosModificadosDaUnidadeOrganizacional = None,
        consult_inferior_organizational_units: Literal[0, 1] = 0,
    ) -> LgApiReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint to get list of organizational units changed in LG System

        Returns:

        A List of OrderedDict that represents an Object(RetornoDeConsultaListaPorDemanda<UnidadeOrganizacional>) API response
            [
                Tipo : int
                Mensagens : [string]
                CodigoDoErro : string
                UnidadeOrganizacional : list[Object(UnidadeOrganizacional)]
            ]
        """

        params = {
            "filtro": {
                "ListaDeCodigos": organizational_units_codes,
                "TipoDeDadosModificados": modified_data_type,
                "ConsultarUnidadesOrganizacionaisInferiores": consult_inferior_organizational_units,
                "TiposDeOperacoes": [
                    {"Operacao": {"Valor": operation}} for operation in operation_types
                ],
                "PeriodoDeBusca": {
                    "DataInicio": start_date.strftime("%Y-%m-%d"),
                    "DataFim": end_date.strftime("%Y-%m-%d"),
                },
            }
        }

        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsultarListaDeUnidadesOrganizacionaisModificadas,
                    body=params,
                    parse_body_on_request=True,
                )
            )
        )
