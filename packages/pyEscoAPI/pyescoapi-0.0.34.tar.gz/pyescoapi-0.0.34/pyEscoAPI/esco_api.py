import decimal
import logging
from dataclasses import asdict
from datetime import datetime, timedelta, date
from enum import Enum
from http import HTTPMethod
from typing import TypedDict

import requests
from requests import Response

from pyEscoAPI.dataclasses import Persona, ComitenteData
from pyEscoAPI.exception import PyEscoAPIError

logger = logging.getLogger(f"app.{__name__}")


class DomicilioDict(TypedDict):
    cod_pais: int
    cod_provincia: int
    recibe_info_fax: bool
    altura: str | None = None
    calle: str | None = None
    piso: str | None = None
    departamento: str | None = None
    localidad: str | None = None
    cod_postal: str | None = None
    telefono: str | None = None
    fax: str | None = None


class APIVersion(Enum):
    VERSION_9 = 9


class EscoAPI:
    __instance = None

    base_url: str
    username: str
    password: str
    client_id: str = ""
    version: APIVersion = APIVersion.VERSION_9

    __token: str = ""
    __expire_datetime: datetime

    def __make_request(
        self,
        request_endpoint: str,
        request_method: HTTPMethod,
        request_body: dict,
        error_message: str = ""
    ):
        req_call = getattr(requests, request_method.lower())
        headers = {
            "api-version": str(self.version.value)
        }
        if self.__token:
            headers["Authorization"] = f"Bearer {self.__token}"
        request_body = {key: value for key, value in request_body.items() if value is not None}
        params = {
            "url": f"{self.base_url}{request_endpoint}",
            "json": request_body,
            "headers": headers
        }
        result: Response = req_call(**params, timeout=self.timeout)
        if 200 <= result.status_code <= 299:
            result_body = result.json()
            logger.info("EscoAPI: Successful response", extra={
                "request_body": request_body,
                "url": f"{self.base_url}{request_endpoint}",
                "response_body": result_body if request_endpoint != "/login" else None,
                "status_code": result.status_code
            })
            return result.json()
        else:
            try:
                result_body = result.json()
                error_message = result_body["error"]["Msj"]
            except:
                error_message = ""
            if not error_message or error_message == "":
                error_message = f"Error during endpoint call: {request_endpoint}. Code: {result.status_code}"
            logger.error("EscoAPI: Failed response", extra={
                "request_body": request_body,
                "url": f"{self.base_url}{request_endpoint}",
                "response_body": str(result),
                "status_code": result.status_code
            })
            raise PyEscoAPIError(endpoint=request_endpoint, status_code=result.status_code, error_message=error_message)

    def __esco_login(self):
        req_body = {
            "userName": self.username,
            "password": self.password,
            "clientId": self.client_id
        }

        result_data = self.__make_request(
            request_endpoint="/login",
            request_body=req_body,
            request_method=HTTPMethod.POST,
            error_message="Login to ESCO API failed."
        )

        self.__token = result_data["access_token"]
        expires_in_minutes = result_data["expires_in"] - 1
        self.__expire_datetime = datetime.now() + timedelta(minutes=expires_in_minutes)

    def __pre_connection(self):
        if datetime.now() > self.__expire_datetime:
            self.__token = ""
            self.__esco_login()

    def __new__(cls, base_url: str, username: str, password: str, client_id: str, version: APIVersion):
        if cls.__instance is None:
            cls._initialized = False
            cls.__instance = super(EscoAPI, cls).__new__(cls)
        return cls.__instance

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        client_id: str = "",
        version: APIVersion = APIVersion.VERSION_9,
        timeout: int = 10
    ):
        """
        Initializes the EscoAPI client, starting a login to the platform.
        Instantiating a new EscoAPI client will not result in a new login (Singleton).
        Login runs automatically when the last __token expires.
        :param base_url: The URL of your EscoAPI implementation. Include the protocol without slash at the end.
        :param username: The username of your EscoAPI client.
        :param password: The password of your EscoAPI client.
        :param client_id: Optional. Include if you want to specify a client_id.
        :param version: Optional. The EscoAPI version that you want to use. Default: Version 9.
        """
        if not self._initialized:
            self.base_url = f"{base_url}/api/v{version.value}"
            self.username = username
            self.password = password
            self.client_id = client_id
            self.version = version
            self.timeout = timeout

            self.__esco_login()
            self._initialized = True

    def get_posiciones(
        self,
        cuenta: str,
        por_concertacion: bool = True,
        es_consolidado: bool = False,
        incluir_monedas: bool = True,
        incluir_titulos: bool = False,
        incluir_opciones: bool = False,
        incluir_futuros: bool = False,
        incluir_fondos: bool = False,
        solo_saldos_iniciales: bool = True
    ):
        """
        Esta consulta devuelve las tenencias de instrumentos de una cuenta o una lista de cuentas a una fecha
        indicada y discrimina vencimientos de 24, 48hs y futuro. Las tenencias no se valúan generando una
        respuesta mas rapida de la consulta.
        :param cuenta: Cuenta comitente a consultar.
        :param por_concertacion: Indica si las tenencias se buscan por Fecha de Concertación o no.
        :param es_consolidado: Indica si se muestran todas las cuentas del usuario consolidadas o solo la cuenta seleccionada
        :param incluir_monedas: Indica si se incluyen tenencias de Monedas
        :param incluir_titulos: Indica si se incluyen tenencias de Titulos
        :param incluir_opciones: Indica si se incluyen tenencias de Opciones
        :param incluir_futuros: Indica si se incluyen tenencias de Futuros
        :param incluir_fondos: Indica si se incluyen tenencias de Fondos
        :param solo_saldos_iniciales: Indica si solo se muestran saldos al inicio del día o se impactan movimientos realizados en en el dia
        """
        req_body = {
          "cuentas": cuenta,
          "porConcertacion": por_concertacion,
          "esConsolidado": es_consolidado,
          "incluirMonedas": incluir_monedas,
          "incluirTitulos": incluir_titulos,
          "incluirOpciones": incluir_opciones,
          "incluirFuturos": incluir_futuros,
          "incluirFondos": incluir_fondos,
          "soloSaldosIniciales": solo_saldos_iniciales
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-posiciones",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_disponible_mon(
        self,
        cuenta: str,
        fecha_disponible: datetime = None,
        moneda: str = "ARS",
        dias_rescates_pendientes: int = 0,
        dias_suscripciones_pendientes: int = 0,
        plazo: int = 0,
        incluye_creditos: bool = True,
        fecha_colocacion_hasta: datetime = None,
        es_bloqueado_bcra: bool = False
    ):
        """
        Esta consulta informa el disponible de moneda para una cuenta comitente a una fecha determinada.
        La respuesta discrimina cómo se compone el saldo disponible.

        :param cuenta: Código de Comitente
        :param fecha_disponible: Fecha en que se pide la consulta
        :param moneda: Código ISO de la moneda
        :param dias_rescates_pendientes: Cantidad de días de antiguedad máximo para considerar Rescates pendientes de liquidación
        :param dias_suscripciones_pendientes: Cantidad de días de antiguedad máximo para considerar Suscripciones pendientes de liquidación.
        :param plazo: Plazo de liquidación del movimiento que se está cargando. Se suma al campo Fecha el plazo en días hábiles para calcular la fecha a la que se debe mostrar el disponible.
        :param incluye_creditos: Indica si se deben considerar en el disponible los créditos para operar asignados en Back Office.
        :param fecha_colocacion_hasta: Se usa en licitaciones, es la fecha de liquidación del proceso de licitación.
        :param es_bloqueado_bcra: Indica si se discriminan los USD que no se pueden utilizar para compras según BCRA 7340
        """
        if fecha_disponible is None:
            fecha_disponible = datetime.now()
        if fecha_colocacion_hasta is None:
            fecha_colocacion_hasta = datetime.now()

        req_body = {
          "cuenta": cuenta,
          "fechaDisponible": fecha_disponible.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "moneda": moneda,
          "diasRescatesPendientes": dias_rescates_pendientes,
          "diasSuscripcionesPendientes": dias_suscripciones_pendientes,
          "plazo": plazo,
          "incluyeCreditos": incluye_creditos,
          "fechaColocacionHasta": fecha_colocacion_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "esBloqueadoBcra": es_bloqueado_bcra
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-disponible-mon",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_disponible_mon_list(
        self,
        cuentas: str,
        fecha_disponible: datetime = None,
        monedas: list[str] = ["ARS", "USD", "USD-C"],
        dias_rescates_pendientes: int = 0,
        dias_suscripciones_pendientes: int = 0,
        plazos: list[int] = [0, 1, 2],
        incluye_creditos: bool = True,
        fecha_colocacion_hasta: datetime = None,
        es_bloqueado_bcra: bool = False
    ):
        """
        Esta consulta informa el disponible de moneda para una cuenta comitente a una fecha determinada, agrupando por moneda y por plazo.
        La respuesta discrimina cómo se compone el saldo disponible.

        :param cuentas: Código de Comitente
        :param fecha_disponible: Fecha en que se pide la consulta
        :param monedas: Códigos ISO de las monedas
        :param dias_rescates_pendientes: Cantidad de días de antiguedad máximo para considerar Rescates pendientes de liquidación
        :param dias_suscripciones_pendientes: Cantidad de días de antiguedad máximo para considerar Suscripciones pendientes de liquidación.
        :param plazos: Plazos de liquidación del movimiento que se está cargando. Se suma al campo Fecha el plazo en días hábiles para calcular la fecha a la que se debe mostrar el disponible.
        :param incluye_creditos: Indica si se deben considerar en el disponible los créditos para operar asignados en Back Office.
        :param fecha_colocacion_hasta: Se usa en licitaciones, es la fecha de liquidación del proceso de licitación.
        :param es_bloqueado_bcra: Indica si se discriminan los USD que no se pueden utilizar para compras según BCRA 7340
        """
        if fecha_disponible is None:
            fecha_disponible = datetime.now()
        if fecha_colocacion_hasta is None:
            fecha_colocacion_hasta = datetime.now()

        req_body = {
          "cuentas": cuentas,
          "fechaDisponible": fecha_disponible.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "monedas": monedas,
          "diasRescatesPendientes": dias_rescates_pendientes,
          "diasSuscripcionesPendientes": dias_suscripciones_pendientes,
          "plazos": plazos,
          "incluyeCreditos": incluye_creditos,
          "fechaColocacionHasta": fecha_colocacion_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "esBloqueadoBcra": es_bloqueado_bcra
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-disponible-mon-list",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_tenencia_val(
        self,
        cuenta: str,
        fecha: datetime = None,
        por_concertacion: bool = True,
        es_consolidado: bool = False,
        agrupar_por_moneda: bool = True,
        moneda_valuacion: str = "ARS",
        incluir_ppp: bool = False,
        incluir_monedas: bool = True,
        incluir_titulos: bool = False,
        incluir_opciones: bool = False,
        incluir_futuros: bool = False,
        incluir_fondos: bool = False,
        valuar_posicion: bool = True,
        utiliza_cotizaciones_online: bool = True
    ):
        """
        Esta consulta devuelve la tenencia valorizada de una cuenta a una determinada fecha.
        :param cuenta: Código de Comitente
        :param fecha: Fecha a la que se consultan las tenencias
        :param por_concertacion: Indica si las tenencias se buscan por Fecha de Concertación o no.
        :param es_consolidado: Indica si se muestran todas las cuentas del usuario consolidadas o solo la cuenta seleccionada.
        :param agrupar_por_moneda: Indica si agrupa los instrumentos por moneda de emisión.
        :param moneda_valuacion: Indica la moneda que se utiliza para valuar todos los instrumentos.
        :param incluir_ppp: Indica si se incluye PPP
        :param incluir_monedas: Indica si se incluyen tenencias de Monedas
        :param incluir_titulos: Indica si se incluyen tenencias de Titulos
        :param incluir_opciones: Indica si se incluyen tenencias de Opciones
        :param incluir_futuros: Indica si se incluyen tenencias de Futuros
        :param incluir_fondos: Indica si se incluyen tenencias de Fondos
        :param valuar_posicion: Indica si se debe valuar la posición o no
        :param utiliza_cotizaciones_online: Indica si utiliza cotizaciones online o busca directamente cotizaciones de VBolsa
        """
        if fecha is None:
            fecha = datetime.now()

        req_body = {
            "cuentas": cuenta,
            "fecha": fecha.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "porConcertacion": por_concertacion,
            "esConsolidado": es_consolidado,
            "agruparPorMoneda": agrupar_por_moneda,
            "monedaValuacion": moneda_valuacion,
            "incluirPPP": incluir_ppp,
            "incluirMonedas": incluir_monedas,
            "incluirTitulos": incluir_titulos,
            "incluirOpciones": incluir_opciones,
            "incluirFuturos": incluir_futuros,
            "incluirFondos": incluir_fondos,
            "valuarPosicion": valuar_posicion,
            "utilizaCotizacionesOnLine": utiliza_cotizaciones_online
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-tenenciaval",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_tenencia_val_vencimientos(
        self,
        cuenta: str,
        fecha: datetime = None,
        incluir_ppp: bool = True
    ):
        """
        Esta consulta devuelve la valuación de una cuenta a una determinada fecha (por liquidación) y los
        vencimientos posteriores a esa fecha.
        :param cuenta: Código de Comitente
        :param fecha: Fecha a la que se deben recuperar los movimientos que conforman los saldos. En esta consulta los movimientos se recuperan siempre por fecha de liquidación.
        :param incluir_ppp: Indica si se incluye ppp en la consulta. PPP se genera en un proceso de Vbolsa.
        """
        if fecha is None:
            fecha = datetime.now()

        req_body = {
          "cuentas": cuenta,
          "fecha": fecha.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "incluirPPP": incluir_ppp
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-tenenciaval-vencimientos",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_rendimiento_cartera(
        self,
        cuenta: str,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None,
        por_concertacion: bool = True
    ):
        """
        :param cuenta: Número de Cuenta Comitente
        :param fecha_desde: Fecha inicial del período de Rendimientos consultado.
        :param fecha_hasta: Fecha final del período de Rendimientos consultado.
        :param por_concertacion: Indica si saldos y movimientos involucrados en esta consulta se buscan por Fecha de Concertación o Liquidación.
        """
        if fecha_desde is None:
            fecha_desde = datetime.now() - timedelta(days=15)
        if fecha_hasta is None:
            fecha_hasta = datetime.now()

        req_body = {
          "cuenta": cuenta,
          "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "porConcertacion": por_concertacion
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-rendimiento-cartera",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_instrumentos(
        self,
        cod_tp_especie: int,
        page_number: int = 1,
        page_size: int = 200,
        solo_byma: bool = True
    ):
        """
        Es una consulta de Instrumentos que se pueden operar. Se toman de la tabla que registra todos los
        instrumentos para operar WEB. La respuesta es paginada.
        :param cod_tp_especie: Codigo interno del tipo de especie.
        :param page_number: Número de página a mostrar.
        :param page_size: Cantidad de registros por página.
        :param solo_byma:Indica si solo se recuperan los Instrumentos con Abreviaturas Byma. Por defecto informa solo Byma.
        """
        req_body = {
          "codTpEspecie": cod_tp_especie,
          "soloByMA": solo_byma,
          "paramPagination": {
            "pageNumber": page_number,
            "pageSize": page_size
          }
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-instrumentos-paginada",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_cotizaciones(self, instrumento: str, exact_match: bool = True):
        """
        Es una consulta de cotizaciones de instrumentos, se busca en la información en la tabla de cotizaciones
        online que registra cotizaciones para un mismo instrumento en distintas monedas y plazos
        :param instrumento: Abreviatura o descripción del instrumento. Se puede ingresar total o parcial dependiendo del siguiente parámetro.
        :param exact_match: Este parámetro indica si se debe busca exacto el texto ingresado o no.
        """
        req_body = {
          "instrumento": instrumento,
          "exactMatch": exact_match
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-cotizaciones",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_cotizaciones_fondos(self):
        """
        Es una consulta de cotizaciones y datos de Fondos Comunes de Inversión. Se informan las cotizaciones
        cargadas en VBolsa.
        :return:
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-cotizaciones-fondos",
            request_body={},
            request_method=HTTPMethod.POST
        )

    def get_cotizaciones_historicas(
        self,
        instrumento: str,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None
    ):
        """
        Es una consulta de cotizaciones históricas de un instrumento. Se informan las cotizaciones cargadas en VBolsa.
        :param instrumento: Abreviatura del instrumento, se puede ingresar cualquier abreviatura vinculada. Se recupera la cotización de cierre que está cargada en VBolsa, la abreviatura se usa para ubicar el instrumento.
        :param fecha_desde: Fecha inicial de la consulta.
        :param fecha_hasta: Fecha final de la consulta.
        """
        if fecha_desde is None:
            fecha_desde = datetime.now() - timedelta(days=7)
        if fecha_hasta is None:
            fecha_hasta = datetime.now()
        req_body = {
            "instrumento": instrumento,
            "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-cotizaciones-historicas",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_cotizaciones_historicas_fci(
            self,
            instrumento: str,
            fecha_desde: datetime = None,
            fecha_hasta: datetime = None
    ):
        """
        Es una consulta de cotizaciones históricas de un FCI. Se informan las cotizaciones cargadas en VBolsa.
        :param instrumento: Código de Interfaz Bloomberg del Fondo.
        :param fecha_desde: Fecha inicial de la consulta.
        :param fecha_hasta: Fecha final de la consulta.
        """
        if fecha_desde is None:
            fecha_desde = datetime.now() - timedelta(days=7)
        if fecha_hasta is None:
            fecha_hasta = datetime.now()

        req_body = {
            "instrumento": instrumento,
            "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-cotizaciones-historicas-fci",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_instrumento(self, abreviatura: str):
        """
        Devuelve los instrumentos filtrados por su abreviatura.
        :param abreviatura: Abreviatura del instrumento, se puede ingresar cualquier abreviatura vinculada.
        """
        req_body = {
          "abreviatura": abreviatura
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-instrumento",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_cotizaciones_cierre_search(self, instrumento: str, mercado: str = "ME"):
        """
        Es una consulta de cotizaciones de cierre de instrumentos
        :param instrumento: Abreviatura del instrumento, se puede ingresar cualquier abreviatura vinculada. Se recupera la cotización de cierre que esta cargada en VBolsa, la abreviatura se usa para ubicar el instrumento.
        :param mercado: Mercado al cual corresponde la abreviatura ingresada. Default: ME (ByMA)
        :return:
        """
        req_body = {
          "instrumento": instrumento,
          "mercado": mercado
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-cotizaciones-cierre-search",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_cotizaciones_monedas(self):
        """
        Devuelve la cotización de cada moneda.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-cotizaciones-monedas",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_monedas(self):
        """
        Devuelve la lista de Monedas habilitadas.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-monedas",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_feriados(self):
        """
        Devuelve la lista de Feriados habilitados.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-feriados",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_provincias(self):
        """
        Devuelve la lista de Provincias habilitadas.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-provincias",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_paises(self):
        """
        Devuelve la lista de Paises habilitados.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-paises",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_tipos_especies(self):
        """
        Devuelve la lista de tipos de especies.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-tipos-especies",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_tipos_fondos(self):
        """
        Devuelve la lista de tipos de especies.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-tipos-fondos",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_tipos_riesgo_comitente(self):
        """
        Devuelve la lista de tipos de riesgo de Comitente.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-tipos-riesgo-comitente",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_detalle_cuenta(self, cuenta: str):
        """
        Esta consulta muestra el detalle de datos de la cuenta
        :param cuenta: Número de Comitente.
        """
        req_body = {
            "cuenta": cuenta,
            "timeStamp": 13128022,
            "paramPagination": {
                "pageNumber": 1,
                "pageSize": 1
            }
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-detalle-cuenta",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_cuentas_por_cuit(self, cuit: str):
        """
        Es una consulta que informa las cuentas comitente que corresponden al CUIT ingresado. El cuit puede
        ser del comitente o de los condóminos.
        :param cuit: Nro de CUIT a buscar. Se deben ingresar solo numeros.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-cuentas-por-cuit?CUIT={cuit}",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_persona(self, num_doc: int, tipo_doc: int = 1):
        """
        Retorna datos de una persona filtrando por tipo y número de documento.
        :param num_doc: Número de documento de la Persona a buscar.
        :param tipo_doc: Código del Tipo de Documento. 1: DNI, 2: Pasaporte, 3: Otros.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-persona?tipoDoc={tipo_doc}&numDoc={num_doc}",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def insert_orden_compra(
        self,
        instrumento_abreviatura: str,
        cuenta: str,
        plazo: int = 0,
        cantidad: int = None,
        precio: decimal = None,
        importe: decimal = None,
        moneda: str = "ARS",
        fecha_concertacion: date | None = date.today(),
        observacion: str = None,
        cod_usuario: int = None,
        id_usuario: str = None,
        aplicacion: str = None,
        dias_susc_pendiente: int = None,
        dias_resc_pendiente: int = None,
        incluye_gastos_en_importe: bool = False,
        variacion_precio: decimal = None,
        mercado: str = "ME",
        controla_perfil_inversor: bool = None,
        controla_subyacente: bool = None,
        rutear_orden_al_mercado: bool = True,
        validar_orden: bool = True,
        validar_precio: bool = False,
        orden_market: bool = True,
        fix_order_id: str = None,
        aplica_aranceles_extraordinarios: bool = None,
        tp_operacion: str = None,
        precio_referencia: decimal = None,
        gastos: decimal = None,
    ):
        """
        Inserta una orden de compra de instrumento a un mercado.
        :param instrumento_abreviatura: Abreviatura de la especie en la moneda que se va a operar
        :param cuenta: Número de cuenta comitente
        :param plazo: Plazo de liquidación de la operación a generar. Los plazos habilitados son CI (0), 24 HS (1) Y 48 HS (2).
        :param cantidad: Cantidad a operar expresada en valores nominales, sólo para órdenes por cantidad.
        :param precio: Precio a operar expresado en la unidad de cotización de la especie. Ejemplo: AY24 -> el precio está expresado por 100 - ALUAR -> el precio está expresado por 1.
        :param importe: Importe de las operaciones, sólo para órdenes de compra por importe.
        :param moneda: Código ISO de la moneda de la operación. Debe corresponder a la moneda de la abreviatura de especie ingresada.
        :param fecha_concertacion: Fecha de concertación de la orden, siempre debe ser la fecha de día.
        :param observacion: No aplica.
        :param cod_usuario: Código interno de usuario que ingresa la orden. (No es lo mismo que Comitente)
        :param id_usuario: ID de usuario que ingresa la orden.
        :param aplicacion: ID de la aplicación desde la cual se ingresa la orden.
        :param dias_susc_pendiente: Este dato se utiliza para calcular el disponible de compra. Cuando hay solicitudes de suscripción FCI pendientes de liquidación, este dato indica cuantos de días de antigüedad máximo la solicitud de suscripción para impactar en el disponible.
        :param dias_resc_pendiente: No aplica.
        :param incluye_gastos_en_importe: Cuando se ingresa una orden de compra por importe este dato indica si los gastos deben descontarse del importe ingresado.
        :param variacion_precio: Tope en Porcentaje de variación de precio ingresado en la orden respecto del último precio de mercado.
        :param mercado: ID del mercado de la orden, ejemplo: ME -> para ordenes BYMA
        :param controla_perfil_inversor: Indica si se debe controlar el perfil de inversor durante el alta de esta orden.
        :param controla_subyacente: Indica si incluye en la disponibilidad posición de la especie subyacente. Se usa para las órdenes de compra/venta de opciones.
        :param rutear_orden_al_mercado: Indica si la orden se rutea la merado (Byma) o no.
        :param validar_orden: Este parámetro se utiliza para cargar órdenes de sistemas externos, que no requieren las validaciones de disponibles para operar.
        :param validar_precio: Este parámetro se utiliza para indicar si se debe validar el precio de la orden con la tabla de precios online o no.
        :param orden_market: Indica si es una orden a precio de mercado.
        :param fix_order_id: Se puede ingresar el fixOrderID si se cuenta con ese dato.
        :param aplica_aranceles_extraordinarios:  True busca primero arancel extraordinario paraaplicar. False busca arancel NO extraordinario.
        :param tp_operacion: Se usa para identificar el tipo de operación para calcular el arancel correspondiente. Si esta en null se busca arancel de compra/venta contado.
        :param precio_referencia: Precio de Referencia
        :param gastos: Este parámetro permite la gastos manualmente que suman/restan al bruto de la operación para calcular el monto neto final.
        """

        req_body = {
          "instrumentoAbreviatura": instrumento_abreviatura,
          "cantidad": cantidad,
          "precio": precio,
          "importe": importe,
          "cuenta": cuenta,
          "moneda": moneda,
          "fechaConcertacion": fecha_concertacion.strftime("%Y-%m-%d") if fecha_concertacion else None,
          "plazo": plazo,
          "observacion": observacion,
          "codUsuario": cod_usuario,
          "idUsuario": id_usuario,
          "aplicacion": aplicacion,
          "diasSuscPendiente": dias_susc_pendiente,
          "diasRescPendiente": dias_resc_pendiente,
          "incluyeGastosEnImporte": incluye_gastos_en_importe,
          "variacionPrecio": variacion_precio,
          "mercado": mercado,
          "controlaPerfilInversor": controla_perfil_inversor,
          "controlaSubyacente": controla_subyacente,
          "rutearOrdenAlMercado": rutear_orden_al_mercado,
          "validarOrden": validar_orden,
          "validarPrecio": validar_precio,
          "ordenMarket": orden_market,
          "fixOrderId": fix_order_id,
          "aplicaArancelesExtraordinarios": aplica_aranceles_extraordinarios,
          "tpOperacion": tp_operacion,
          "precioReferencia": precio_referencia,
          "gastos": gastos
        }

        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/insert-orden-compra",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def insert_oferta_orden(
        self,
        cod_orden: int,
        cantidad: float,
        precio: float,
        fecha: date | None = None,
    ):
        """
        Inserta una oferta para una orden determinada.

        Args:
            cod_orden (int): Código interno de la orden.
            cantidad (float): Cantidad ofertada.
            precio (float): Precio ofertado.
            fecha (date | None, optional): Fecha de la oferta. Defaults: fecha del dia en tiempo de ejecucion.

        Returns:
            dict: Diccionario con cod_operacion
        """        
        req_body = {
            "codOrden": cod_orden,
            "cantidad": cantidad,
            "precio": precio,
            "fecha": fecha.isoformat() if fecha is not None else date.today().isoformat()
        }

        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/insert-oferta-orden",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def insert_ejecucion_orden(
        self,
        cod_orden: int,
        cantidad: float,
        precio: float,
        fecha: date | None = None,
        num_ejecucion: int | None = None
    ):
        """
        Inserta una ejecucion de una orden determinada.

        Args:
            cod_orden (int): Código interno de la orden.
            cantidad (float): Cantidad ofertada.
            precio (float): Precio ofertado.
            fecha (date | None, optional): Fecha de la oferta. Defaults: fecha del dia en tiempo de ejecucion.
            num_ejecucion (int | None, optional): Número de Ejecución. Default None.

        Returns:
            dict: Diccionario con cod_operacion
        """        
        req_body = {
            "codOrden": cod_orden,
            "cantidad": cantidad,
            "precio": precio,
            "fecha": fecha.isoformat() if fecha is not None else date.today().isoformat(),
            "numEjecucion": num_ejecucion
        }

        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/insert-ejecucion-orden",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def insert_orden_venta(
        self,
        instrumento_abreviatura: str,
        cuenta: str,
        plazo: int = 0,
        cantidad: int = None,
        precio: decimal = None,
        importe: decimal = None,
        moneda: str = "ARS",
        fecha_concertacion: date | None = date.today(),
        observacion: str = None,
        cod_usuario: int = None,
        id_usuario: str = None,
        aplicacion: str = None,
        dias_susc_pendiente: int = None,
        dias_resc_pendiente: int = None,
        incluye_gastos_en_importe: bool = False,
        variacion_precio: decimal = None,
        mercado: str = "ME",
        controla_perfil_inversor: bool = None,
        controla_subyacente: bool = None,
        rutear_orden_al_mercado: bool = True,
        validar_orden: bool = True,
        validar_precio: bool = False,
        orden_market: bool = True,
        fix_order_id: str = None,
        aplica_aranceles_extraordinarios: bool = None,
        tp_operacion: str = None,
        precio_referencia: decimal = None,
        gastos: decimal = None,
    ):
        """
        Inserta una orden de venta de instrumento en tenencia a un mercado.
        :param instrumento_abreviatura: Abreviatura de la especie en la moneda que se va a operar
        :param cuenta: Número de cuenta comitente
        :param plazo: Plazo de liquidación de la operación a generar. Los plazos habilitados son CI (0), 24 HS (1) Y 48 HS (2).
        :param cantidad: Cantidad a operar expresada en valores nominales, sólo para órdenes por cantidad.
        :param precio: Precio a operar expresado en la unidad de cotización de la especie. Ejemplo: AY24 -> el precio está expresado por 100 - ALUAR -> el precio está expresado por 1.
        :param importe: Importe de las operaciones, sólo para órdenes de compra por importe.
        :param moneda: Código ISO de la moneda de la operación. Debe corresponder a la moneda de la abreviatura de especie ingresada.
        :param fecha_concertacion: Fecha de concertación de la orden, siempre debe ser la fecha de día.
        :param observacion: No aplica.
        :param cod_usuario: Código interno de usuario que ingresa la orden. (No es lo mismo que Comitente)
        :param id_usuario: ID de usuario que ingresa la orden.
        :param aplicacion: ID de la aplicación desde la cual se ingresa la orden.
        :param dias_susc_pendiente: Este dato se utiliza para calcular el disponible de compra. Cuando hay solicitudes de suscripción FCI pendientes de liquidación, este dato indica cuantos de días de antigüedad máximo la solicitud de suscripción para impactar en el disponible.
        :param dias_resc_pendiente: No aplica.
        :param incluye_gastos_en_importe: Cuando se ingresa una orden de compra por importe este dato indica si los gastos deben descontarse del importe ingresado.
        :param variacion_precio: Tope en Porcentaje de variación de precio ingresado en la orden respecto del último precio de mercado.
        :param mercado: ID del mercado de la orden, ejemplo: ME -> para ordenes BYMA
        :param controla_perfil_inversor: Indica si se debe controlar el perfil de inversor durante el alta de esta orden.
        :param controla_subyacente: Indica si incluye en la disponibilidad posición de la especie subyacente. Se usa para las órdenes de compra/venta de opciones.
        :param rutear_orden_al_mercado: Indica si la orden se rutea la merado (Byma) o no.
        :param validar_orden: Este parámetro se utiliza para cargar órdenes de sistemas externos, que no requieren las validaciones de disponibles para operar.
        :param validar_precio: Este parámetro se utiliza para indicar si se debe validar el precio de la orden con la tabla de precios online o no.
        :param orden_market: Indica si es una orden a precio de mercado.
        :param fix_order_id: Se puede ingresar el fixOrderID si se cuenta con ese dato.
        :param aplica_aranceles_extraordinarios:  True busca primero arancel extraordinario paraaplicar. False busca arancel NO extraordinario.
        :param tp_operacion: Se usa para identificar el tipo de operación para calcular el arancel correspondiente. Si esta en null se busca arancel de compra/venta contado.
        :param precio_referencia: Precio de Referencia
        :param gastos: Este parámetro permite la gastos manualmente que suman/restan al bruto de la operación para calcular el monto neto final.
        """
        req_body = {
          "instrumentoAbreviatura": instrumento_abreviatura,
          "cantidad": cantidad,
          "precio": precio,
          "importe": importe,
          "cuenta": cuenta,
          "moneda": moneda,
          "fechaConcertacion": fecha_concertacion.strftime("%Y-%m-%d") if fecha_concertacion else None,
          "plazo": plazo,
          "observacion": observacion,
          "codUsuario": cod_usuario,
          "idUsuario": id_usuario,
          "aplicacion": aplicacion,
          "diasSuscPendiente": dias_susc_pendiente,
          "diasRescPendiente": dias_resc_pendiente,
          "incluyeGastosEnImporte": incluye_gastos_en_importe,
          "variacionPrecio": variacion_precio,
          "mercado": mercado,
          "controlaPerfilInversor": controla_perfil_inversor,
          "controlaSubyacente": controla_subyacente,
          "rutearOrdenAlMercado": rutear_orden_al_mercado,
          "validarOrden": validar_orden,
          "validarPrecio": validar_precio,
          "ordenMarket": orden_market,
          "fixOrderId": fix_order_id,
          "aplicaArancelesExtraordinarios": aplica_aranceles_extraordinarios,
          "tpOperacion": tp_operacion,
          "precioReferencia": precio_referencia,
          "gastos": gastos
        }

        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/insert-orden-venta",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def insert_solicitud_suscripcion_fci(
        self,
        fondo: str,
        cuenta: str,
        importe: decimal,
        fecha_concertacion: date | None = date.today(),
        fecha_acreditacion: date | None = None,
        tp_cambio_mov_pais: decimal = 1,
        moneda: str = "ARS",
        cod_usuario: int = None,
        id_usuario: str = None,
        cod_reglamento: int = None,
        cod_documentacion_web: int = None,
        cod_cta_bancaria: int = None,
        valor_cuotaparte: decimal = None,
        canal: str = "VB",
        controla_perfil_inversor: bool = None,
        controla_saldo_monetario: bool = True,
        cod_agente_depo: int = None,
        incluye_creditos: bool = True
    ):
        """
        Inserta una solicitud de suscripcion a un fondo en una fecha determinada
        :param fondo: Código de Interfaz Bloomberg del Fondo.
        :param cuenta: Número de Cuenta Comitente.
        :param importe: Importe a suscribir.
        :param fecha_concertacion: Fecha de Concertación de la Solicitud.
        :param fecha_acreditacion: Fecha de Acreditación o Liquidación de la Solicitud.
        :param tp_cambio_mov_pais: Tipo de Cambio para convertir el importe de la Suscripción la Moneda del país. Si la Suscripción es en Moneda local el valor a ingresar es 1.
        :param moneda: Moneda de la Solicitud.
        :param cod_usuario: No aplica.
        :param id_usuario: Identificador del usuario ingresa la Solicitud en la aplicación externa.
        :param cod_reglamento: No aplica
        :param cod_documentacion_web: No aplica
        :param cod_cta_bancaria: Codigo Interno de la Cuenta Bancaria del Comitente.
        :param valor_cuotaparte: Valor de Cuotaparte tomado como referencia.
        :param canal: Canal de Ingreso de la Solicitud. VB = VBolsa
        :param controla_perfil_inversor: No aplica.
        :param controla_saldo_monetario: Indica si se debe controlar saldo monetario y hacer bloqueo.
        :param cod_agente_depo: Cuenta de Depositario de la Operación
        :param incluye_creditos: Indica si incluyen en el disponible de moneda los créditos asignados para operar.
        """
        req_body = {
          "fondo": fondo,
          "cuenta": cuenta,
          "fechaConcertacion": fecha_concertacion.strftime("%Y-%m-%d") if fecha_concertacion else None,
          "fechaAcreditacion": fecha_acreditacion.strftime("%Y-%m-%d") if fecha_acreditacion else None,
          "importe": importe,
          "tpCambioMovPais": tp_cambio_mov_pais,
          "moneda": moneda,
          "codUsuario": cod_usuario,
          "idUsuario": id_usuario,
          "codReglamento": cod_reglamento,
          "codDocumentacionWEB": cod_documentacion_web,
          "codCtaBancaria": cod_cta_bancaria,
          "valorCuotaparte": valor_cuotaparte,
          "canal": canal,
          "controlaPerfilInversor": controla_perfil_inversor,
          "codAgenteDepo": cod_agente_depo,
          "controlaSaldoMonetario": controla_saldo_monetario,
          "incluyeCreditos": incluye_creditos
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/insert-solicitud-suscripcion-fci",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def insert_solicitud_rescate_fci(
        self,
        fondo: str,
        cuenta: str,
        importe: decimal = None,
        cant_cuotapartes: decimal = None,
        es_total: bool = False,
        es_por_cantidad: bool = False,
        fecha_concertacion: date | None = date.today(),
        fecha_acreditacion: date | None = None,
        tp_cambio_mov_pais: decimal = 1,
        moneda: str = "ARS",
        cod_usuario: int = None,
        id_usuario: str = None,
        cod_reglamento: int = None,
        cod_documentacion_web: int = None,
        cod_cta_bancaria: int = None,
        valor_cuotaparte: decimal = None,
        canal: str = "VB",
        controla_perfil_inversor: bool = None,
        controla_saldo_monetario: bool = True,
        cod_agente_depo: int = None,
        incluye_creditos: bool = True
    ):
        """
        Inserta una solicitud de rescate a un fondo en una fecha determinada
        :param es_por_cantidad: Indica si la operación es por Cantidad o por Importe.
        :param es_total: Indica si el rescate es total o parcial.
        :param cant_cuotapartes: Cantidad de cuotapartes a rescatar cuando la solicitud es por cantidad.
        :param fondo: Código de Interfaz Bloomberg del Fondo.
        :param cuenta: Número de Cuenta Comitente.
        :param importe: Importe a suscribir.
        :param fecha_concertacion: Fecha de Concertación de la Solicitud.
        :param fecha_acreditacion: Fecha de Acreditación o Liquidación de la Solicitud.
        :param tp_cambio_mov_pais: Tipo de Cambio para convertir el importe de la Suscripción la Moneda del país. Si la Suscripción es en Moneda local el valor a ingresar es 1.
        :param moneda: Moneda de la Solicitud.
        :param cod_usuario: No aplica.
        :param id_usuario: Identificador del usuario ingresa la Solicitud en la aplicación externa.
        :param cod_reglamento: No aplica
        :param cod_documentacion_web: No aplica
        :param cod_cta_bancaria: Codigo Interno de la Cuenta Bancaria del Comitente.
        :param valor_cuotaparte: Valor de Cuotaparte tomado como referencia.
        :param canal: Canal de Ingreso de la Solicitud. VB = VBolsa
        :param controla_perfil_inversor: No aplica.
        :param controla_saldo_monetario: Indica si se debe controlar saldo monetario y hacer bloqueo.
        :param cod_agente_depo: Cuenta de Depositario de la Operación
        :param incluye_creditos: Indica si incluyen en el disponible de moneda los créditos asignados para operar.
        """
        req_body = {
          "fondo": fondo,
          "cuenta": cuenta,
          "fechaConcertacion": fecha_concertacion.strftime("%Y-%m-%d") if fecha_concertacion else None,
          "fechaAcreditacion": fecha_acreditacion.strftime("%Y-%m-%d") if fecha_acreditacion else None,
          "cantCuotapartes": cant_cuotapartes,
          "esTotal": es_total,
          "esPorCantidad": es_por_cantidad,
          "importe": importe,
          "tpCambioMovPais": tp_cambio_mov_pais,
          "moneda": moneda,
          "codUsuario": cod_usuario,
          "idUsuario": id_usuario,
          "codReglamento": cod_reglamento,
          "codDocumentacionWEB": cod_documentacion_web,
          "codCtaBancaria": cod_cta_bancaria,
          "valorCuotaparte": valor_cuotaparte,
          "canal": canal,
          "controlaPerfilInversor": controla_perfil_inversor,
          "codAgenteDepo": cod_agente_depo,
          "controlaSaldoMonetario": controla_saldo_monetario,
          "incluyeCreditos": incluye_creditos
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/insert-solicitud-rescate-fci",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )
    
    def insert_solicitud_fci_simple(
        self,
        cuenta: str,
        fondo: str,
        tipo_operacion: str,
        id_origen: str,
        importe: decimal,
        es_total: bool = False,
        es_por_cantidad: bool = False,
        cant_cuotapartes: decimal = 0,
        generar_recibo_cobro: bool = False,
        liquida_cta_bancaria: bool = False,
        moneda: str = "ARS",
        fecha_concertacion: date | None = None,
        fecha_acreditacion: date | None = None,
        incluye_creditos: bool = True,
        tp_cambio_moneda_pais = 1,
        canal: str = "CE",
        cuenta_contable: int | None = None
    ):  

        if fecha_concertacion is None:
            fecha_concertacion = date.today()
        
        if fecha_acreditacion is None:
            fecha_acreditacion = date.today()

        req_body = {
          "fondo": fondo,
          "fechaConcertacion": fecha_concertacion.strftime("%Y-%m-%d"),
          "fechaAcreditacion": fecha_acreditacion.strftime("%Y-%m-%d"),
          "moneda": moneda,
          "incluyeCreditos": incluye_creditos,
          "generarReciboDeCobro": generar_recibo_cobro,
          "procesamientoSincrono": True,
          "liquidaCtaBancaria": liquida_cta_bancaria,
          "esACDI": False,
          "cuentaContable": cuenta_contable,
          "solicitudes":[
              {
                "tpOperacionFdo": tipo_operacion,
                "importe": importe,
                "cantCuotapartes": cant_cuotapartes,
                "esTotal": es_total,
                "esPorCantidad": es_por_cantidad,
                "cuenta": cuenta,
                "tpCambioMovPais": tp_cambio_moneda_pais,
                "canal": canal,
                "idOrigen": id_origen   
              }
          ]
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/insert-solicitud-fci-lista",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_boletos(
        self,
        cuentas: str = None,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None,
        por_concertacion: bool = True,
        es_consolidado: bool = True,
        incluye_anulados: bool = True
    ):
        """
        Es una consulta de todos los boletos generados en VBolsa. Solo se muestran boletos vigentes, no se
        muestran boletos anulados.
        :param cuentas: Lista de Número de Cuentas Comitente. Se puede ingresar una sola cuenta o una lista separada por comas.
        :param fecha_desde: Fecha inicial para la consulta de Boletos.
        :param fecha_hasta: Fecha final para la consulta de Boletos.
        :param por_concertacion: Indica si los Boletos se buscan por Fecha de Concertación o no.
        :param es_consolidado: Indica si se informan los boletos de todas las cuentas vinculadas a la usuario o no.
        :param incluye_anulados: Indica si se muestran los boletos anulados en la consulta o no.
        """
        if fecha_desde is None:
            fecha_desde = datetime.now() - timedelta(days=30)
        if fecha_hasta is None:
            fecha_hasta = datetime.now()

        req_body = {
          "cuentas": cuentas,
          "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "porConcertacion": por_concertacion,
          "esConsolidado": es_consolidado,
          "incluyeAnulados": incluye_anulados
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-boletos",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )
    
    def get_recibos_comprobantes(
        self,
        cuentas: str = None,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None,
        por_concertacion: bool = True,
        es_consolidado: bool = True,
    ):
        """
        Devuelve los recibos de comprobantes generados en VBolsa.
        :param cuentas: Lista de Número de Cuentas Comitente. Se puede ingresar una sola cuenta o una lista separada por comas.
        :param fecha_desde: Fecha inicial para la consulta de Comprobantes.
        :param fecha_hasta: Fecha final para la consulta de Comprobantes.
        :param por_concertacion: Indica si los Comprobantes se buscan por Fecha de Concertación o no.
        :param es_consolidado: Indica si se informan los Comprobantes de todas las cuentas vinculadas a la usuario o no.
        """
        if fecha_desde is None:
            fecha_desde = datetime.now() - timedelta(days=30)
        if fecha_hasta is None:
            fecha_hasta = datetime.now()

        req_body = {
          "cuentas": cuentas,
          "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "porConcertacion": por_concertacion,
          "esConsolidado": es_consolidado,
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-recibos-comprobantes",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_estado_orden(self, cod_orden: int = 1):
        """
        Es una consulta devuelve el estado de la orden solicitada.
        :param cod_orden: Código interno de la orden
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-estado-orden?CodOrden={cod_orden}",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_ordenes(
        self,
        cuentas: str = None,
        es_consolidado: bool = True,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None,
    ):
        """
        Obtiene las ultimas ordenes dentro de las fechas indicadas
        :param cuentas: Lista de cuentas comitente, separadas por coma.
        :param es_consolidado: Indica si se informan los boletos de todas las cuentas vinculadas a la usuario o no.
        :param fecha_desde: Fecha inicial la para la consulta de Ordenes.
        :param fecha_hasta: Fecha final la para la consulta de Ordenes.
        """
        if fecha_desde is None:
            fecha_desde = datetime.now() - timedelta(days=15)
        if fecha_hasta is None:
            fecha_hasta = datetime.now()

        req_body = {
          "cuentas": cuentas,
          "esConsolidado": es_consolidado,
          "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-ordenes",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )
    
    def get_ctaCorriente_monetaria(
        self,
        cuenta: str = None,
        por_concertacion: bool = False,
        moneda: str = None,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None
    ):
        """
        Obtiene movimientos y operaciones ya confirmadas de monedas que impactaron en la cuenta corriente en un período
        determinado en las cuentas comitente solicitadas.
        :param cuenta: Número de Cuenta Comitente.
        :param por_concertacion: Indica si los movimientos de la Cte Cte se buscan por Fecha de Concertación o no.
        :param moneda: Código ISO de Moneda (ARS, USD, USD-C, etc).
        :param fecha_desde: Fecha Inicial para la búsqueda de movimientos de la Cta Cte.
        :param fecha_hasta: Fecha Final para la búsqueda de movimientos de la Cta Cte.
        """
        if fecha_desde is None:
            fecha_desde = datetime.now() - timedelta(days=15)
        if fecha_hasta is None:
            fecha_hasta = datetime.now()

        req_body = {
          "cuenta": cuenta,
          "porConcertacion": por_concertacion,
          "moneda": moneda,
          "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-ctaCorriente-monetaria",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )
    
    def get_ctaCorriente_instrumentos(
        self,
        cuenta: str = None,
        por_concertacion: bool = False,
        instrumento: str = None,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None,
    ):
        """
        Obtiene movimientos y operaciones ya confirmadas de instrumentos que impactaron en la cuenta corriente en un período
        determinado en las cuentas comitente solicitadas. En esta consulta se pueden ver movimientos de títulos, futuros, 
        series, índices, cheques, etc.
        :param cuenta: Número de Cuenta Comitente.
        :param por_concertacion: Indica si los movimientos de la Cte Cte se buscan por Fecha de Concertación o no.
        :param instrumento: Se debe ingresar un código que se compone de la siguiente manera: Letra que identifica el Tipo de Especie + Código interno de la Especie.
        :param fecha_desde: Fecha Inicial para la búsqueda de movimientos de la Cta Cte.
        :param fecha_hasta: Fecha Final para la búsqueda de movimientos de la Cta Cte.
        """
        if fecha_desde is None:
            fecha_desde = datetime.now() - timedelta(days=15)
        if fecha_hasta is None:
            fecha_hasta = datetime.now()

        req_body = {
          "cuenta": cuenta,
          "porConcertacion": por_concertacion,
          "instrumento": instrumento,
          "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-ctaCorriente-instrumentos",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )
    def get_ctaCorriente_consolidada(
        self,
        cuenta: str = None,
        por_concertacion: bool = False,
        incluir_saldos_anteriores: bool = False,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None,
    ):
        """
        Obtiene movimientos y operaciones ya confirmadas de monedas e instrumentos que impactaron en la cuenta corriente en un período
        determinado en las cuentas comitente solicitadas.
        :param cuenta: Número de Cuenta Comitente.
        :param por_concertacion: Indica si los movimientos de la Cte Cte se buscan por Fecha de Concertación o no.
        :param incluir_saldos_anteriores: Indica si se informan saldos inicialeso no.
        :param fecha_desde: Fecha Inicial para la búsqueda de movimientos de la Cta Cte.
        :param fecha_hasta: Fecha Final para la búsqueda de movimientos de la Cta Cte.
        """
        if fecha_desde is None:
            fecha_desde = datetime.now() - timedelta(days=15)
        if fecha_hasta is None:
            fecha_hasta = datetime.now()

        req_body = {
          "cuenta": cuenta,
          "porConcertacion": por_concertacion,
          "incluirSaldosAnteriores": incluir_saldos_anteriores,
          "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-ctaCorriente-consolidada",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_liquidaciones_fondos(
        self,
        cuentas: str = None,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None,
        por_concertacion: bool = True,
        es_consolidado: bool = True,
    ):
        """
        Es una consulta de liquidaciones FCI para lista de cuentas comitente en el período solicitado.
        :param cuentas: Lista de Número de Cuentas Comitente. Se puede ingresar una sola cuenta o una lista separada por comas.
        :param fecha_desde: Fecha inicial para la consulta de liquidaciones.
        :param fecha_hasta: Fecha final para la consulta de liquidaciones.
        :param por_concertacion: Indica si las Liquidaciones se buscan por Fecha de Concertación o no.
        :param es_consolidado: Indica si se informan las Liquidaciones de todas las cuentas vinculadas a la usuario o no.
        """
        if fecha_desde is None:
            fecha_desde = datetime.now() - timedelta(days=30)
        if fecha_hasta is None:
            fecha_hasta = datetime.now()

        req_body = {
          "cuentas": cuentas,
          "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "porConcertacion": por_concertacion,
          "esConsolidado": es_consolidado,
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-liquidaciones-fondos",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_solicitudes_fondos(
        self,
        cuentas: str = None,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None,
        por_concertacion: bool = True,
        es_consolidado: bool = True,
        mostrar_cancelados: bool = False,
        page_number: int = 1,
        page_size: int = 100
    ):
        """
        Es una consulta de solicitudes FCI para lista de cuentas comitente en el período solicitado.
        :param cuentas: Lista de Número de Cuentas Comitente. Se puede ingresar una sola cuenta o una lista separada por comas.
        :param fecha_desde: Fecha inicial para la consulta de liquidaciones.
        :param fecha_hasta: Fecha final para la consulta de liquidaciones.
        :param por_concertacion: Indica si las Solicitudes se buscan por Fecha de Concertación o no.
        :param es_consolidado: Indica si se informan las Solicitudes de todas las cuentas vinculadas a la usuario o no.
        :param mostrar_cancelados: Indica si se incluyen solicitudes canceladas.
        :param page_number: Número de página a mostrar.
        :param page_size: Cantidad de registros por página.
        """
        if fecha_desde is None:
            fecha_desde = datetime.now() - timedelta(days=30)
        if fecha_hasta is None:
            fecha_hasta = datetime.now()

        req_body = {
          "cuentas": cuentas,
          "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "porConcertacion": por_concertacion,
          "esConsolidado": es_consolidado,
          "mostrarCancelados": mostrar_cancelados,
          "paramPagination": {
             "pageNumber": page_number,
             "pageSize": page_size
          }
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-solicitudes-fondos-paginada",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def cancel_orden(self, cod_orden: int):
        """
        Cancela una orden que haya sido enviada.
        :param cod_orden: Codigo de Orden
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/cancel-orden?CodOrden={cod_orden}",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def previsualizar_orden_compra(
        self,
        instrumento_abreviatura: str,
        cuenta: str,
        plazo: int = 0,
        cantidad: int = None,
        precio: decimal = None,
        importe: decimal = None,
        moneda: str = "ARS",
        fecha_concertacion: date | None = date.today(),
        observacion: str = None,
        cod_usuario: int = None,
        id_usuario: str = None,
        aplicacion: str = None,
        dias_susc_pendiente: int = None,
        dias_resc_pendiente: int = None,
        incluye_gastos_en_importe: bool = False,
        variacion_precio: decimal = None,
        mercado: str = "ME",
        controla_perfil_inversor: bool = None,
        controla_subyacente: bool = None,
        rutear_orden_al_mercado: bool = True,
        validar_orden: bool = True,
        validar_precio: bool = False,
        orden_market: bool = True,
        fix_order_id: str = None,
        aplica_aranceles_extraordinarios: bool = None,
        tp_operacion: str = None,
        precio_referencia: decimal = None,
        gastos: decimal = None,
    ):
        """
        Previsualiza una orden de compra de instrumento a un mercado. Permite ver los gastos y precios a insertar.
        :param instrumento_abreviatura: Abreviatura de la especie en la moneda que se va a operar
        :param cuenta: Número de cuenta comitente
        :param plazo: Plazo de liquidación de la operación a generar. Los plazos habilitados son CI (0), 24 HS (1) Y 48 HS (2).
        :param cantidad: Cantidad a operar expresada en valores nominales, sólo para órdenes por cantidad.
        :param precio: Precio a operar expresado en la unidad de cotización de la especie. Ejemplo: AY24 -> el precio está expresado por 100 - ALUAR -> el precio está expresado por 1.
        :param importe: Importe de las operaciones, sólo para órdenes de compra por importe.
        :param moneda: Código ISO de la moneda de la operación. Debe corresponder a la moneda de la abreviatura de especie ingresada.
        :param fecha_concertacion: Fecha de concertación de la orden, siempre debe ser la fecha de día.
        :param observacion: No aplica.
        :param cod_usuario: Código interno de usuario que ingresa la orden. (No es lo mismo que Comitente)
        :param id_usuario: ID de usuario que ingresa la orden.
        :param aplicacion: ID de la aplicación desde la cual se ingresa la orden.
        :param dias_susc_pendiente: Este dato se utiliza para calcular el disponible de compra. Cuando hay solicitudes de suscripción FCI pendientes de liquidación, este dato indica cuantos de días de antigüedad máximo la solicitud de suscripción para impactar en el disponible.
        :param dias_resc_pendiente: No aplica.
        :param incluye_gastos_en_importe: Cuando se ingresa una orden de compra por importe este dato indica si los gastos deben descontarse del importe ingresado.
        :param variacion_precio: Tope en Porcentaje de variación de precio ingresado en la orden respecto del último precio de mercado.
        :param mercado: ID del mercado de la orden, ejemplo: ME -> para ordenes BYMA
        :param controla_perfil_inversor: Indica si se debe controlar el perfil de inversor durante el alta de esta orden.
        :param controla_subyacente: Indica si incluye en la disponibilidad posición de la especie subyacente. Se usa para las órdenes de compra/venta de opciones.
        :param rutear_orden_al_mercado: Indica si la orden se rutea la merado (Byma) o no.
        :param validar_orden: Este parámetro se utiliza para cargar órdenes de sistemas externos, que no requieren las validaciones de disponibles para operar.
        :param validar_precio: Este parámetro se utiliza para indicar si se debe validar el precio de la orden con la tabla de precios online o no.
        :param orden_market: Indica si es una orden a precio de mercado.
        :param fix_order_id: Se puede ingresar el fixOrderID si se cuenta con ese dato.
        :param aplica_aranceles_extraordinarios:  True busca primero arancel extraordinario paraaplicar. False busca arancel NO extraordinario.
        :param tp_operacion: Se usa para identificar el tipo de operación para calcular el arancel correspondiente. Si esta en null se busca arancel de compra/venta contado.
        :param precio_referencia: Precio de Referencia
        :param gastos: Este parámetro permite la gastos manualmente que suman/restan al bruto de la operación para calcular el monto neto final.
        """
        req_body = {
          "instrumentoAbreviatura": instrumento_abreviatura,
          "cantidad": cantidad,
          "precio": precio,
          "importe": importe,
          "cuenta": cuenta,
          "moneda": moneda,
          "fechaConcertacion": fecha_concertacion.strftime("%Y-%m-%d") if fecha_concertacion else None,
          "plazo": plazo,
          "observacion": observacion,
          "codUsuario": cod_usuario,
          "idUsuario": id_usuario,
          "aplicacion": aplicacion,
          "diasSuscPendiente": dias_susc_pendiente,
          "diasRescPendiente": dias_resc_pendiente,
          "incluyeGastosEnImporte": incluye_gastos_en_importe,
          "variacionPrecio": variacion_precio,
          "mercado": mercado,
          "controlaPerfilInversor": controla_perfil_inversor,
          "controlaSubyacente": controla_subyacente,
          "rutearOrdenAlMercado": rutear_orden_al_mercado,
          "validarOrden": validar_orden,
          "validarPrecio": validar_precio,
          "ordenMarket": orden_market,
          "fixOrderId": fix_order_id,
          "aplicaArancelesExtraordinarios": aplica_aranceles_extraordinarios,
          "tpOperacion": tp_operacion,
          "precioReferencia": precio_referencia,
          "gastos": gastos
        }

        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/previsualizar-orden-compra",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def previsualizar_orden_venta(
        self,
        instrumento_abreviatura: str,
        cuenta: str,
        plazo: int = 0,
        cantidad: int = None,
        precio: decimal = None,
        importe: decimal = None,
        moneda: str = "ARS",
        fecha_concertacion: date | None = date.today(),
        observacion: str = None,
        cod_usuario: int = None,
        id_usuario: str = None,
        aplicacion: str = None,
        dias_susc_pendiente: int = None,
        dias_resc_pendiente: int = None,
        incluye_gastos_en_importe: bool = False,
        variacion_precio: decimal = None,
        mercado: str = "ME",
        controla_perfil_inversor: bool = None,
        controla_subyacente: bool = None,
        rutear_orden_al_mercado: bool = True,
        validar_orden: bool = True,
        validar_precio: bool = False,
        orden_market: bool = True,
        fix_order_id: str = None,
        aplica_aranceles_extraordinarios: bool = None,
        tp_operacion: str = None,
        precio_referencia: decimal = None,
        gastos: decimal = None,
    ):
        """
        Previsualiza una orden de venta de instrumento a un mercado. Permite ver los gastos y precios a insertar.
        :param instrumento_abreviatura: Abreviatura de la especie en la moneda que se va a operar
        :param cuenta: Número de cuenta comitente
        :param plazo: Plazo de liquidación de la operación a generar. Los plazos habilitados son CI (0), 24 HS (1) Y 48 HS (2).
        :param cantidad: Cantidad a operar expresada en valores nominales, sólo para órdenes por cantidad.
        :param precio: Precio a operar expresado en la unidad de cotización de la especie. Ejemplo: AY24 -> el precio está expresado por 100 - ALUAR -> el precio está expresado por 1.
        :param importe: Importe de las operaciones, sólo para órdenes de compra por importe.
        :param moneda: Código ISO de la moneda de la operación. Debe corresponder a la moneda de la abreviatura de especie ingresada.
        :param fecha_concertacion: Fecha de concertación de la orden, siempre debe ser la fecha de día.
        :param observacion: No aplica.
        :param cod_usuario: Código interno de usuario que ingresa la orden. (No es lo mismo que Comitente)
        :param id_usuario: ID de usuario que ingresa la orden.
        :param aplicacion: ID de la aplicación desde la cual se ingresa la orden.
        :param dias_susc_pendiente: Este dato se utiliza para calcular el disponible de compra. Cuando hay solicitudes de suscripción FCI pendientes de liquidación, este dato indica cuantos de días de antigüedad máximo la solicitud de suscripción para impactar en el disponible.
        :param dias_resc_pendiente: No aplica.
        :param incluye_gastos_en_importe: Cuando se ingresa una orden de compra por importe este dato indica si los gastos deben descontarse del importe ingresado.
        :param variacion_precio: Tope en Porcentaje de variación de precio ingresado en la orden respecto del último precio de mercado.
        :param mercado: ID del mercado de la orden, ejemplo: ME -> para ordenes BYMA
        :param controla_perfil_inversor: Indica si se debe controlar el perfil de inversor durante el alta de esta orden.
        :param controla_subyacente: Indica si incluye en la disponibilidad posición de la especie subyacente. Se usa para las órdenes de compra/venta de opciones.
        :param rutear_orden_al_mercado: Indica si la orden se rutea la merado (Byma) o no.
        :param validar_orden: Este parámetro se utiliza para cargar órdenes de sistemas externos, que no requieren las validaciones de disponibles para operar.
        :param validar_precio: Este parámetro se utiliza para indicar si se debe validar el precio de la orden con la tabla de precios online o no.
        :param orden_market: Indica si es una orden a precio de mercado.
        :param fix_order_id: Se puede ingresar el fixOrderID si se cuenta con ese dato.
        :param aplica_aranceles_extraordinarios:  True busca primero arancel extraordinario paraaplicar. False busca arancel NO extraordinario.
        :param tp_operacion: Se usa para identificar el tipo de operación para calcular el arancel correspondiente. Si esta en null se busca arancel de compra/venta contado.
        :param precio_referencia: Precio de Referencia
        :param gastos: Este parámetro permite la gastos manualmente que suman/restan al bruto de la operación para calcular el monto neto final.
        """
        req_body = {
          "instrumentoAbreviatura": instrumento_abreviatura,
          "cantidad": cantidad,
          "precio": precio,
          "importe": importe,
          "cuenta": cuenta,
          "moneda": moneda,
          "fechaConcertacion": fecha_concertacion.strftime("%Y-%m-%d") if fecha_concertacion else None,
          "plazo": plazo,
          "observacion": observacion,
          "codUsuario": cod_usuario,
          "idUsuario": id_usuario,
          "aplicacion": aplicacion,
          "diasSuscPendiente": dias_susc_pendiente,
          "diasRescPendiente": dias_resc_pendiente,
          "incluyeGastosEnImporte": incluye_gastos_en_importe,
          "variacionPrecio": variacion_precio,
          "mercado": mercado,
          "controlaPerfilInversor": controla_perfil_inversor,
          "controlaSubyacente": controla_subyacente,
          "rutearOrdenAlMercado": rutear_orden_al_mercado,
          "validarOrden": validar_orden,
          "validarPrecio": validar_precio,
          "ordenMarket": orden_market,
          "fixOrderId": fix_order_id,
          "aplicaArancelesExtraordinarios": aplica_aranceles_extraordinarios,
          "tpOperacion": tp_operacion,
          "precioReferencia": precio_referencia,
          "gastos": gastos
        }

        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/previsualizar-orden-venta",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def insert_orden_compra_futuro(
        self,
        instrumento_abreviatura: str,
        cuenta: str,
        plazo: int = 0,
        cantidad: int = None,
        precio: decimal = None,
        importe: decimal = None,
        moneda: str = "ARS",
        fecha_concertacion: date | None = date.today(),
        observacion: str = None,
        cod_usuario: int = None,
        id_usuario: str = None,
        aplicacion: str = None,
        dias_susc_pendiente: int = None,
        dias_resc_pendiente: int = None,
        variacion_precio: decimal = None,
        mercado: str = "ME",
        rutear_orden_al_mercado: bool = True,
        validar_orden: bool = True,
        validar_precio: bool = False,
        fix_order_id: str = None,
    ):
        """
        Inserta una orden de compra de futuros a un mercado.
        :param instrumento_abreviatura: Abreviatura de la especie en la moneda que se va a operar
        :param cuenta: Número de cuenta comitente
        :param plazo: Plazo de liquidación de la operación a generar. Los plazos habilitados son CI (0), 24 HS (1) Y 48 HS (2).
        :param cantidad: Cantidad a operar expresada en valores nominales, sólo para órdenes por cantidad.
        :param precio: Precio a operar expresado en la unidad de cotización de la especie. Ejemplo: AY24 -> el precio está expresado por 100 - ALUAR -> el precio está expresado por 1.
        :param importe: Importe de las operaciones, sólo para órdenes de compra por importe.
        :param moneda: Código ISO de la moneda de la operación. Debe corresponder a la moneda de la abreviatura de especie ingresada.
        :param fecha_concertacion: Fecha de concertación de la orden, siempre debe ser la fecha de día.
        :param observacion: No aplica.
        :param cod_usuario: Código interno de usuario que ingresa la orden. (No es lo mismo que Comitente)
        :param id_usuario: ID de usuario que ingresa la orden.
        :param aplicacion: ID de la aplicación desde la cual se ingresa la orden.
        :param dias_susc_pendiente: Este dato se utiliza para calcular el disponible de compra. Cuando hay solicitudes de suscripción FCI pendientes de liquidación, este dato indica cuantos de días de antigüedad máximo la solicitud de suscripción para impactar en el disponible.
        :param dias_resc_pendiente: No aplica.
        :param variacion_precio: Tope en Porcentaje de variación de precio ingresado en la orden respecto del último precio de mercado.
        :param mercado: ID del mercado de la orden, ejemplo: ME -> para ordenes BYMA
        :param rutear_orden_al_mercado: Indica si la orden se rutea la merado (Byma) o no.
        :param validar_orden: Este parámetro se utiliza para cargar órdenes de sistemas externos, que no requieren las validaciones de disponibles para operar.
        :param validar_precio: Este parámetro se utiliza para indicar si se debe validar el precio de la orden con la tabla de precios online o no.
        :param fix_order_id: Se puede ingresar el fixOrderID si se cuenta con ese dato.
        """

        req_body = {
          "instrumentoAbreviatura": instrumento_abreviatura,
          "cantidad": cantidad,
          "precio": precio,
          "importe": importe,
          "cuenta": cuenta,
          "moneda": moneda,
          "fechaConcertacion": fecha_concertacion.strftime("%Y-%m-%d") if fecha_concertacion else None,
          "plazo": plazo,
          "observacion": observacion,
          "codUsuario": cod_usuario,
          "idUsuario": id_usuario,
          "aplicacion": aplicacion,
          "diasSuscPendiente": dias_susc_pendiente,
          "diasRescPendiente": dias_resc_pendiente,
          "variacionPrecio": variacion_precio,
          "mercado": mercado,
          "rutearOrdenAlMercado": rutear_orden_al_mercado,
          "validarOrden": validar_orden,
          "validarPrecio": validar_precio,
          "fixOrderId": fix_order_id
        }

        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/insert-orden-compra-futuro",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def insert_orden_venta_futuro(
        self,
        instrumento_abreviatura: str,
        cuenta: str,
        plazo: int = 0,
        cantidad: int = None,
        precio: decimal = None,
        importe: decimal = None,
        moneda: str = "ARS",
        fecha_concertacion: date | None = date.today(),
        observacion: str = None,
        cod_usuario: int = None,
        id_usuario: str = None,
        aplicacion: str = None,
        dias_susc_pendiente: int = None,
        dias_resc_pendiente: int = None,
        incluye_gastos_en_importe: bool = False,
        variacion_precio: decimal = None,
        mercado: str = "ME",
        rutear_orden_al_mercado: bool = True,
        validar_orden: bool = True,
        validar_precio: bool = False,
        orden_market: bool = True,
        fix_order_id: str = None,
    ):
        """
        Inserta una orden de venta de futuros a un mercado.
        :param instrumento_abreviatura: Abreviatura de la especie en la moneda que se va a operar
        :param cuenta: Número de cuenta comitente
        :param plazo: Plazo de liquidación de la operación a generar. Los plazos habilitados son CI (0), 24 HS (1) Y 48 HS (2).
        :param cantidad: Cantidad a operar expresada en valores nominales, sólo para órdenes por cantidad.
        :param precio: Precio a operar expresado en la unidad de cotización de la especie. Ejemplo: AY24 -> el precio está expresado por 100 - ALUAR -> el precio está expresado por 1.
        :param importe: Importe de las operaciones, sólo para órdenes de compra por importe.
        :param moneda: Código ISO de la moneda de la operación. Debe corresponder a la moneda de la abreviatura de especie ingresada.
        :param fecha_concertacion: Fecha de concertación de la orden, siempre debe ser la fecha de día.
        :param observacion: No aplica.
        :param cod_usuario: Código interno de usuario que ingresa la orden. (No es lo mismo que Comitente)
        :param id_usuario: ID de usuario que ingresa la orden.
        :param aplicacion: ID de la aplicación desde la cual se ingresa la orden.
        :param dias_susc_pendiente: Este dato se utiliza para calcular el disponible de compra. Cuando hay solicitudes de suscripción FCI pendientes de liquidación, este dato indica cuantos de días de antigüedad máximo la solicitud de suscripción para impactar en el disponible.
        :param dias_resc_pendiente: No aplica.
        :param incluye_gastos_en_importe: Cuando se ingresa una orden de compra por importe este dato indica si los gastos deben descontarse del importe ingresado.
        :param variacion_precio: Tope en Porcentaje de variación de precio ingresado en la orden respecto del último precio de mercado.
        :param mercado: ID del mercado de la orden, ejemplo: ME -> para ordenes BYMA
        :param rutear_orden_al_mercado: Indica si la orden se rutea la merado (Byma) o no.
        :param validar_orden: Este parámetro se utiliza para cargar órdenes de sistemas externos, que no requieren las validaciones de disponibles para operar.
        :param validar_precio: Este parámetro se utiliza para indicar si se debe validar el precio de la orden con la tabla de precios online o no.
        :param orden_market: Indica si es una orden a precio de mercado.
        :param fix_order_id: Se puede ingresar el fixOrderID si se cuenta con ese dato.
        """
        req_body = {
          "instrumentoAbreviatura": instrumento_abreviatura,
          "cantidad": cantidad,
          "precio": precio,
          "importe": importe,
          "cuenta": cuenta,
          "moneda": moneda,
          "fechaConcertacion": fecha_concertacion.strftime("%Y-%m-%d") if fecha_concertacion else None,
          "plazo": plazo,
          "observacion": observacion,
          "codUsuario": cod_usuario,
          "idUsuario": id_usuario,
          "aplicacion": aplicacion,
          "diasSuscPendiente": dias_susc_pendiente,
          "diasRescPendiente": dias_resc_pendiente,
          "incluyeGastosEnImporte": incluye_gastos_en_importe,
          "variacionPrecio": variacion_precio,
          "mercado": mercado,
          "rutearOrdenAlMercado": rutear_orden_al_mercado,
          "validarOrden": validar_orden,
          "validarPrecio": validar_precio,
          "ordenMarket": orden_market,
          "fixOrderId": fix_order_id,
        }

        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/insert-orden-venta-futuro",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_ordenes_futuros(
        self,
        cuentas: str = None,
        es_consolidado: bool = True,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None,
    ):
        """
        Obtiene las ultimas ordenes de futuros dentro de las fechas indicadas
        :param cuentas: Lista de cuentas comitente, separadas por coma.
        :param es_consolidado: Indica si se informan las ordenes de todas las cuentas vinculadas a la usuario o no.
        :param fecha_desde: Fecha inicial la para la consulta de Ordenes.
        :param fecha_hasta: Fecha final la para la consulta de Ordenes.
        """
        if fecha_desde is None:
            fecha_desde = datetime.now() - timedelta(days=15)
        if fecha_hasta is None:
            fecha_hasta = datetime.now()

        req_body = {
          "cuentas": cuentas,
          "esConsolidado": es_consolidado,
          "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-ordenes-futuros",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def insert_persona(self, persona_data: Persona):
        """
        Es un insert para registrar personas, generados desde la ESCO API, la misma se utiliza únicamente para
        registrar y no para consultar.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/insert-persona",
            request_body=asdict(persona_data),
            request_method=HTTPMethod.POST
        )

    def insert_comitente(self, comitente_data: ComitenteData):
        """
        Es un insert en la tabla de Cuentas Comitente, Personas y tablas vinculadas
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/insert-cuenta-comitente",
            request_body=asdict(comitente_data, dict_factory=lambda x: {k: v for k, v in x if v is not None}),
            request_method=HTTPMethod.POST
        )

    def insert_cuenta_bancaria_comitente(
        self,
        cuenta: int,
        banco: int,
        cbu: str,
        fecha_apertura: datetime,
        cuit_titular: str,
        tp_cuenta: int = None,
        moneda: str = "ARS",
        num_cuenta: str = None,
        alias: str = None,
        num_sucursal: str = None
    ):
        """
        Es un insert en la tabla de Cuentas Bancarias de Comitente
        :param cuenta: Número de Cuenta Comitente.
        :param banco: Código interno del banco al cual corresponde la cuenta. Los valores posibles se pueden obtener con la consulta get-bancos
        :param cbu: CBU de la cuenta
        :param fecha_apertura: Fecha de Apertura de la cuenta
        :param cuit_titular: CUIT del titular de la cuenta
        :param tp_cuenta: Código interno de tipo de cuenta bancaria. Los valores posibles se pueden obtener con la consulta get-tipos-cuenta-bancaria.
        :param moneda: Código ISO de la moneda
        :param num_cuenta: Número de Cuenta Bancaria
        :param alias: Alias de la cuenta
        :param num_sucursal: Número de Sucursal
        """
        req_body = {
          "cuenta": cuenta,
          "banco": banco,
          "tpCuenta": tp_cuenta,
          "moneda": moneda,
          "numCuenta": num_cuenta,
          "fechaApertura": fecha_apertura.isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
          "cbu": cbu,
          "numSucursal": num_sucursal,
          "alias": alias,
          "cuitTitular": cuit_titular
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/insert-cuenta-bancaria-comitente",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def insert_comprobante_pago(
        self,
        cuenta: str,
        moneda: str,
        importe: decimal,
        cuenta_contable: int,
        fecha_concertacion: date | None = date.today(),
        fecha_liquidacion: date | None = None,
        tp_cambio_mov_pais: int = 1,
        cuenta_bancaria_comitente: int = None,
        controla_saldo_monetario: bool = True,
        num_referencia: int = None,
        comentario: str = None,
        id_origen: str = None,
        es_echeq: bool = False,
        numero_cheque: int = None
    ):
        """
        Es un método que permite el ingreso de un Comprobante de Pago, este tipo de comprobante genera
        un egreso monetario en la cuenta corriente de un cliente sin requerir una aprobacion posterior.
        :param cuenta: Número de Comitente
        :param moneda: Código de ISO de la moneda el movimiento.
        :param importe: Importe de movimiento expresado en la moneda indicada.
        :param cuenta_contable: Cuenta contable del agente donde se imputará el movimiento. Se debe ingresar el código interno de la cuenta contable.
        :param fecha_concertacion: Fecha de concertación del recibo de cobro.
        :param fecha_liquidacion: Fecha de liquidación del recibo de cobro.
        :param tp_cambio_mov_pais: Tipo de Cambio para convertir el importe del recibo a la moneda local. 1 si es en moneda local.
        :param cuenta_bancaria_comitente: Cuenta bancaria del cliente. Se debe ingresar el código interno. Es solo informativo, queda registrado solamente en el recibo de cobro.
        :param controla_saldo_monetario: Indica si debe controlar el saldo monetario para hacer el egreso.
        :param num_referencia: Nro de referencia del movimiento.
        :param comentario: Comentario del movimiento
        :param id_origen: Id de origen del movimiento
        :param es_echeq: True is es un e-cheque.
        :param numero_cheque: Si es un cheque, ingresar numero de cheque.s
        :return:
        """
        req_body = {
          "cuenta": cuenta,
          "moneda": moneda,
          "fechaConcertacion": fecha_concertacion.strftime("%Y-%m-%d") if fecha_concertacion else None,
          "fechaLiquidacion": fecha_liquidacion.strftime("%Y-%m-%d") if fecha_liquidacion else None,
          "importe": importe,
          "tpCambioMovPais": tp_cambio_mov_pais,
          "cuentaContable": cuenta_contable,
          "cuentaBancariaComitente": cuenta_bancaria_comitente,
          "numReferencia": num_referencia,
          "comentario": comentario,
          "idOrigen": id_origen,
          "controlaSaldoMonetario": controla_saldo_monetario,
          "esEcheq": es_echeq,
          "numeroCheque": numero_cheque
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/insert-comprobante-pago",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def insert_solicitud_comprobante_pago(
        self,
        cuenta: str,
        moneda: str,
        importe: decimal,
        cuenta_contable: int,
        fecha_concertacion: date | None = None,
        fecha_liquidacion: date | None = None,
        tp_cambio_mov_pais: int = 1,
        cuenta_bancaria_comitente: int = None,
        num_referencia: int = None,
        id_origen: str = None,
        controla_saldo_monetario: bool = True,
    ):
        """
        Es un método que permite el ingreso de un Comprobante de Pago, este tipo de comprobante genera
        un egreso monetario en la cuenta corriente de un cliente sin requerir una aprobacion posterior.
        :param cuenta: Número de Comitente
        :param moneda: Código de ISO de la moneda el movimiento.
        :param importe: Importe de movimiento expresado en la moneda indicada.
        :param cuenta_contable: Cuenta contable del agente donde se imputará el movimiento. Se debe ingresar el código interno de la cuenta contable.
        :param fecha_concertacion: Fecha de concertación del recibo de cobro.
        :param fecha_liquidacion: Fecha de liquidación del recibo de cobro.
        :param tp_cambio_mov_pais: Tipo de Cambio para convertir el importe del recibo a la moneda local. 1 si es en moneda local.
        :param cuenta_bancaria_comitente: Cuenta bancaria del cliente. Se debe ingresar el código interno. Es solo informativo, queda registrado solamente en el recibo de cobro.
        :param controla_saldo_monetario: Indica si debe controlar el saldo monetario para hacer el egreso.
        :param num_referencia: Nro de referencia del movimiento.
        :param id_origen: Id de origen del movimiento
        """
        if fecha_concertacion is None:
            fecha_concertacion = date.today()
        if fecha_liquidacion is None:
            fecha_liquidacion = date.today()

        req_body = {
            "cuenta": cuenta,
            "moneda": moneda,
            "fechaConcertacion": fecha_concertacion.isoformat(),
            "fechaLiquidacion": fecha_liquidacion.isoformat(),
            "tpCambioMovPais": tp_cambio_mov_pais,
            "importe": importe,
            "cuentaContable": cuenta_contable,
            "cuentaBancariaComitente": cuenta_bancaria_comitente,
            "numReferencia": num_referencia,
            "idOrigen": id_origen,
            "controlaSaldoMonetario": controla_saldo_monetario,
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/insert-solicitud-comprobante-pago",
            request_body=req_body,
            request_method=HTTPMethod.POST,
        )

    def get_domicilio_cuenta_comitente(self, cuenta: str, cod_tp_domicilio: str):
        """
        Devuelve el domicilio de una cuenta comitente.
        :param cuenta: Cuenta a la que pertenece el domicilio a buscar.
        :param cod_tp_domicilio: Código del tipo de domicilio (PA: Particular, DO: Comercial).
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/domicilio-cuenta-comitente?Cuenta={cuenta}&CodTpDomicilio={cod_tp_domicilio}",
            request_body={},
            request_method=HTTPMethod.GET
        )
    
    def get_cuentas_bancarias_comitente(self, cuenta: str):
        """
        Devuelve las cuentas bancarias asociadas a una cuenta comitente.
        :param cuenta: Cuenta comitente a la pertenecen las cuentas bancarias a buscar.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-cuentas-bancarias-comitente?cuenta={cuenta}",
            request_body={},
            request_method=HTTPMethod.GET
        )
    
    def get_bancos(self):
        """
        Devuelve el listado de bancos cargados en servidor.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-bancos",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_grupo_aranceles_bursatiles(self):
        """
        Devuelve el listado de grupos de aranceles bursátiles.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-grupos-aranceles-bursatiles",
            request_body={},
            request_method=HTTPMethod.GET
        )
    
    def get_comprobante_pdf(
        self,
        formulario: str,
        id_comprobante: int,
    ):
        """
        Recupera un PDF de un comprobante específico utilizando su formulario e ID.

        Se ejecuta el endpoint enviando el nombre del tipo de formulario y el código de la operación
        asociada.

        Args:
            formulario (str): El identificador del formulario para el comprobante (FRMBOL para boleto).
            id_comprobante (int): El ID único del comprobante.

        Returns:
            dict: La respuesta JSON de la API que contiene los datos del PDF en base64.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-comprobante-PDF-Sync?Formulario={formulario}&IDComprobante={id_comprobante}",
            request_body={},
            request_method=HTTPMethod.GET
        )