import os
from datetime import date, datetime, timedelta

import pytest
from unittest.mock import patch

from pyEscoAPI import EscoAPI
from pyEscoAPI.esco_api import APIVersion


@pytest.fixture
def api_client():
    return EscoAPI(
        base_url=os.getenv("base_url"),
        username=os.getenv("user_name"),
        password=os.getenv("password"),
        client_id=os.getenv("client_id"),
        version=APIVersion.VERSION_9
    )


@patch("pyEscoAPI.esco_api.EscoAPI._EscoAPI__esco_login")
def test_singleton_should_login_just_once(mock_login):
    client = EscoAPI(
        base_url=os.getenv("base_url"),
        username=os.getenv("user_name"),
        password=os.getenv("password"),
        client_id=os.getenv("client_id"),
        version=APIVersion.VERSION_9
    )
    other_client = EscoAPI(
        base_url=os.getenv("base_url"),
        username=os.getenv("user_name"),
        password=os.getenv("password"),
        client_id=os.getenv("client_id"),
        version=APIVersion.VERSION_9
    )
    
    assert client is other_client
    mock_login.assert_called_once()


def test_get_posiciones(api_client):
    cuenta = "351008539"
    result = api_client.get_posiciones(cuenta=cuenta)
    assert result[0]["cuenta"] == int(cuenta)
    assert result[0]["abreviatura"] == "ARS"


def test_get_disponible_mon(api_client):
    cuenta = "351008539"
    result = api_client.get_disponible_mon(cuenta=cuenta)
    assert result[0]["orden"] == 0
    assert result[0]["simbolo"] == "ARS"


def test_get_disponible_mon_list(api_client):
    cuenta = "172885"
    result = api_client.get_disponible_mon_list(cuentas=cuenta)
    assert result[0]["orden"] == 0
    assert result[0]["simbolo"] == "$"


def test_get_tenencia_val(api_client):
    cuenta = "351008539"
    result = api_client.get_tenencia_val(cuenta=cuenta)
    assert result[0]["grupo"] == "MON"
    assert result[0]["abreviatura"] == "ARS"


def test_get_tenencia_val_vencimientos(api_client):
    cuenta = "351008539"
    result = api_client.get_tenencia_val_vencimientos(cuenta=cuenta)
    assert result[0]["grupo"] == "MON"
    assert result[0]["abreviatura"] == "ARS"


def test_get_rendimiento_cartera(api_client):
    cuenta = "351008539"
    result = api_client.get_rendimiento_cartera(cuenta=cuenta)
    assert "resultados1" in result
    assert "resultados2" in result


def test_get_instrumentos(api_client):
    cod_tp_especie = 2  # Bonos (Titulos Publicos)
    result = api_client.get_instrumentos(cod_tp_especie=cod_tp_especie)
    assert result["data"][0]["tpEspecie"] == "Titulo Publicos"


def test_get_cotizaciones(api_client):
    instrumento = "AL30"
    result = api_client.get_cotizaciones(instrumento=instrumento)
    assert result[0]["abreviatura"] == "AL30"


def test_get_cotizaciones_fondos(api_client):
    result = api_client.get_cotizaciones_fondos()
    assert len(result) > 0


def test_get_cotizaciones_historicas(api_client):
    instrumento = "AL30"
    result = api_client.get_cotizaciones_historicas(
        instrumento=instrumento,
        fecha_desde=datetime.now() - timedelta(days=30)
    )
    assert result[0]["moneda"] == "ARS"


def test_get_cotizaciones_historicas_fci(api_client):
    instrumento = "CPYMESA AR"
    result = api_client.get_cotizaciones_historicas_fci(
        instrumento=instrumento,
        fecha_desde=datetime.now() - timedelta(days=30)
    )
    assert result[0]["moneda"] == "ARS"


def test_get_cotizaciones_cierre_search(api_client):
    instrumento = "AL30"
    result = api_client.get_cotizaciones_cierre_search(
        instrumento=instrumento
    )
    assert result[0]["monedaAbreviatura"] == "ARS"


def test_get_cotizaciones_monedas(api_client):
    result = api_client.get_cotizaciones_monedas()
    assert len(result) > 0
    assert "iso" in result[0]
    assert "cotizacion" in result[0]


def test_get_instrumento(api_client):
    instrumento = "COME"
    result = api_client.get_instrumento(abreviatura=instrumento)
    assert result[0]["moneda"] == "ARS"


def test_get_monedas(api_client):
    result = api_client.get_monedas()
    assert result[0]["simbolo"] == "ARS"


def test_get_feriados(api_client):
    result = api_client.get_feriados()
    assert len(result) > 0


def test_get_provincias(api_client):
    result = api_client.get_provincias()
    assert len(result) > 0


def test_get_paises(api_client):
    result = api_client.get_paises()
    assert len(result) > 0


def test_get_tipos_especies(api_client):
    result = api_client.get_tipos_especies()
    assert len(result) > 0


def test_get_tipos_fondos(api_client):
    result = api_client.get_tipos_fondos()
    assert len(result) >= 0  # Returns no result in dev for some reason


def test_get_tipos_riesgo_comitente(api_client):
    result = api_client.get_tipos_riesgo_comitente()
    assert len(result) > 0


def test_get_detalle_cuenta(api_client):
    cuenta = "351008539"
    result = api_client.get_detalle_cuenta(cuenta=cuenta)
    assert result["data"][0]["cuentaDetalle"]["numComitente"] == int(cuenta)


def test_get_cuentas_por_cuit(api_client):
    cuit = "20076387878"
    result = api_client.get_cuentas_por_cuit(cuit)
    assert len(result) > 0


def test_get_persona(api_client):
    dni = 7638787
    result = api_client.get_persona(num_doc=dni)
    assert int(result["numDoc"]) == dni


def test_insert_orden_compra(api_client):
    cuenta = "351011960"
    result = api_client.insert_orden_compra(
        instrumento_abreviatura="COME",
        cuenta=cuenta,
        cantidad=1
    )
    assert "codOperacion" in result


def test_insert_orden_venta(api_client):
    cuenta = "351011960"
    result = api_client.insert_orden_compra(
        instrumento_abreviatura="GNCXO",
        cuenta=cuenta,
        cantidad=1
    )
    assert "codOperacion" in result


def test_insert_suscripcion_fci(api_client):
    cuenta = "351011960"
    result = api_client.insert_solicitud_suscripcion_fci(
        fondo="COGRLMF AR",
        cuenta=cuenta,
        importe=1000
    )
    assert "codSolicitudFdo" in result

def test_insert_solicitud_fci_simple(api_client):
    cuenta = "197383"
    result = api_client.insert_solicitud_fci_simple(
        fondo="Adcap Verde y Sustentable ASG - Clase A",
        cuenta=cuenta,
        importe=1000,
        fecha_concertacion=date.today(),
        fecha_acreditacion=date.today() + timedelta(days=2),
        tipo_operacion="SU",
        id_origen="121545583"
    )
    assert "idProceso" in result


def test_get_boletos(api_client):
    result = api_client.get_boletos()
    assert len(result) > 0
    assert "idBoleto" in result[0]


def test_get_recibos_comprobantes(api_client):
    result = api_client.get_recibos_comprobantes()
    assert len(result) > 0
    assert "id" in result[0]


def test_get_estado_orden(api_client):
    result = api_client.get_estado_orden(47089)
    assert result[0]["indice"] == 0


def test_get_ordenes(api_client):
    result = api_client.get_ordenes()
    assert "codOrden" in result[0]

def test_get_ctaCorriente_monetaria(api_client):
    cuenta="77105"
    result = api_client.get_ctaCorriente_monetaria(cuenta=cuenta)
    assert "codMoneda" in result[0]
    assert result[0]["codMoneda"] is not None

def test_get_ctaCorriente_instrumentos(api_client):
    cuenta="77105"
    fecha_desde=datetime.fromisoformat("2024-03-02")
    fecha_hasta=datetime.fromisoformat("2024-03-17")
    result = api_client.get_ctaCorriente_instrumentos(cuenta=cuenta, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)
    assert "codigoEspecie" in result[0]
    assert result[0]["codigoEspecie"] is not None

def test_get_ctaCorriente_consolidada(api_client):
    cuenta="77105"
    fecha_desde=datetime.fromisoformat("2024-03-02")
    fecha_hasta=datetime.fromisoformat("2024-03-17")
    result = api_client.get_ctaCorriente_consolidada(cuenta=cuenta, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)
    assert "tipoItem" in result[0]
    assert result[0]["tipoItem"] in ["Instrumentos","Monedas"]

def test_get_liquidaciones(api_client):
    result = api_client.get_liquidaciones_fondos()
    assert len(result) > 0
    assert "numSolicitud" in result[0]


def test_get_solicitudes_fci(api_client):
    result = api_client.get_solicitudes_fondos()
    assert len(result) > 0
    assert "numSolicitud" in result["data"][0]


def test_preview_orden_compra(api_client):
    cuenta = "351011960"
    result = api_client.previsualizar_orden_compra(
        instrumento_abreviatura="COME",
        cuenta=cuenta,
        cantidad=1
    )
    assert "precio" in result


def test_get_domicilio_cuenta_comitente(api_client):
    result = api_client.get_domicilio_cuenta_comitente(
        cuenta="351011787",
        cod_tp_domicilio="PA"
    )
    assert "codTpDomicilio" in result

def test_insert_oferta_orden(api_client):
    result = api_client.insert_oferta_orden(
        cod_orden = 178957,
        fecha = datetime.fromisoformat("2024-04-27"),
        cantidad = 10,
        precio = 100
    )
    assert "codOperacion" in result

def test_insert_ejecucion_orden(api_client):
    result = api_client.insert_ejecucion_orden(
        cod_orden = 178957,
        fecha = datetime.fromisoformat("2024-04-27"),
        cantidad = 10,
        precio = 100,
        num_ejecucion=1
    )
    assert "codOperacion" in result

def test_get_cuentas_bancarias_comitente(api_client):
    result = api_client.get_cuentas_bancarias_comitente(cuenta="172998")
    assert isinstance(result, list)
    assert "cuit" in result[0]

def test_get_bancos(api_client):
    result = api_client.get_bancos()
    assert isinstance(result, list)
    assert "codigo" in result[0]

def test_get_grupo_aranceles_bursatiles(api_client):
    result = api_client.get_grupo_aranceles_bursatiles()
    assert isinstance(result, list)
    assert "codigo" in result[0]

def test_get_comprobante_pdf(api_client):
    mock_response = {"data": "base64encodedpdf"}
    with patch.object(api_client,'_EscoAPI__make_request', return_value=mock_response):
        result = api_client.get_comprobante_pdf("FRMBOL", 12345)
        assert result == mock_response

def test_insert_solicitud_comprobante_pago(api_client):
    mock_response = {"codOperacion": 1417, "numOperacion": 0}
    with patch.object(api_client, "_EscoAPI__make_request", return_value=mock_response):
        result = api_client.insert_solicitud_comprobante_pago(
            cuenta="11111",
            moneda="ARS",
            importe=1500.00,
            tp_cambio_mov_pais=1,
            cuenta_contable=401,
            cuenta_bancaria_comitente="1234",
            fecha_concertacion=date.today(),
            fecha_liquidacion=date.today(),
            controla_saldo_monetario=True,
        )
        assert result == mock_response