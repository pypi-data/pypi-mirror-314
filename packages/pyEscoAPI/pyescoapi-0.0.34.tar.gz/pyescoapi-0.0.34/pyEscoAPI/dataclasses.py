from __future__ import annotations
from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class ComitenteData:
    fechaApertura: datetime
    denominacion: str
    esFisico: bool
    esInversorCalificado: bool
    expBrokerCta: bool
    expInversion: bool
    especulativoOportunista: int
    fechaDesdeCodTpContribIVA: datetime
    codTpContribIVA: str
    requiereFirmaConjunta: bool
    noPresencial: bool
    terceroNoIntermediario: bool
    intermediario: bool
    titulares: List[Persona]
    entMailing: List[EntMailing]
    numComitente: int | None = None
    emailsInfo: str | None = None
    patrimonioEstim: int | None = None
    patrimonioEstimMoneda: str | None = None
    actividad: int | None = None
    expBrokerCtaNombre: str | None = None
    experienciaEnInversiones: str | None = None
    montoEstimCta: int | None = None
    montoEstimCtaMoneda: str | None = None
    tpRiesgoCmt: str | None = None
    tpManejoCart: str | None = None
    tpCmtTrading: int | None = None
    codCuotapartista: str | None = None
    referenciaFirmaConjunta: str | None = None
    codGrupoArOperBurs: int | None = None
    codTpComitente: int | None = None
    codCategoriaUIF: int | None = None
    codGrupoArAcreencias: int | None = None
    codGrupoArCustodia: int | None = None
    firmoCondFechaDesde: datetime | None = None
    oficialCuenta: int | None = None
    administrador: int | None = None
    productor: int | None = None
    codTpBilleteraVirtual: str | None = None
    pmtComsinCustodia: bool | None = None
    pmtComRecepdeInf: bool | None = None
    pmtDerechoenMonOpe: bool | None = None
    pmtEsClienteEspecial: bool | None = None
    pmtEsComPromotor: bool | None = None
    pmtGeneraAvisosAlertasUIF: bool | None = None
    pmtivAenMondeOpeMov: bool | None = None
    pmtOperabajoAcuerdoLibreAdm: bool | None = None
    pmtPermiteSuscribirCtaBancariaEnVBHome: bool | None = None
    pmtRecibeMailCambioEstadoOrdenes: bool | None = None
    pmtExcluyeCalculoRetencionPercepcionIVABoletosCheques: bool | None = None
    pmtExcluyeCalculoResultadoOpContinuo: bool | None = None
    pmtIncluyeGenracionCreditosParaOperar: bool | None = None
    pmtInformaInterfazGTR: bool | None = None
    pmtBonificaGastoCustodiaCV: bool | None = None
    pmtSeCobraCustodia: bool | None = None
    pmtSeCobranArancelesGestionBancaria: bool | None = None
    pmtSeCobranCargosPorDescubierto: bool | None = None
    pmtSeEnviaValuacion: bool | None = None
    pmtSeFacturanCargosPorDescubierto: bool | None = None
    pmtSeleimimenboletos: bool | None = None
    pmtSeleImimenetiquetas: bool | None = None
    juridicos: Juridicos | None = None
    instrucciones: List[Instrucciones] | None = None
    codTpRiesgo: str | None = None
    fechaVencimientoPerfil: datetime | None = None
    tpContribRetencion: str | None = None
    codCanalVta: int | None = None
    codCategoria: int | None = None
    codPRI: int | None = None
    codPerfilCmt: int | None = None
    numSucursal: str | None = None


@dataclass
class Juridicos:
    numInscripcion: str
    lugarConstitucion: str
    folio: str
    libro: str
    tomo: str
    codPais: int
    tpContribIngBrutos: str
    cuit: str
    ruc: str
    rut: str
    esSociedadHecho: bool
    tpRegisJuridica: int
    esExtranjero: bool
    actividad: int
    numInscripcionIIBB: str
    codTpIdFatca: int
    idFatca: str
    actividadUIF: int
    giin: str
    esInversorCalificado: bool
    obsFatca: str
    cie: str
    fechaConstitucion: datetime
    

@dataclass
class Persona:
    apellido: str | None = None
    nombre: str | None = None
    tpDoc: int | None = None
    numDoc: str | None = None
    nacionalidad: int | None = None
    fechaNacimiento: datetime | None = None
    lugarNacimiento: str | None = None
    sexo: int | None = None
    estadoCivil: int | None = None
    esPEP: bool | None = None
    esSujetoObligado: bool | None = None
    cuit: str | None = None
    cuil: str | None = None
    cdi: str | None = None
    emailsInfo: str | None = None
    noPresencial: bool | None = None
    esInversorCalificado: bool | None = None
    esBeneficiario: bool | None = None
    esCliente: bool | None = None
    esClienteEspecial: bool | None = None
    esExtranjero: bool | None = None
    codInterfaz: str | None = None
    perteneceLUT: bool | None = None
    giin: str | None = None
    ruc: str | None = None
    rut: str | None = None
    idFatca: str | None = None
    obsFatca: str | None = None
    codTpIdFatca: int | None = None
    codActividad: int | None = None
    codActividadUIF: int | None = None
    codTpContribIVA: str | None = None
    tpPersona: bool | None = None
    numImpositivo: str | None = None
    persEmpresa: str | None = None
    persCargo: str | None = None
    persTpContribRetencion: str | None = None
    persAgRecaudador: bool | None = None
    persAgNroInscrip: str | None = None
    persSSN: str | None = None
    posicionCondominio: int | None = None
    condTpCondominio: str | None = None
    requiereFirma: bool | None = None
    condEsAccionista: bool | None = None
    condPorcParticipacion: int | None = None
    condBeneficiario: int | None = None
    patrimonioEstim: int | None = None
    patrimonioEstimMoneda: str | None = None
    tpRiesgoTitular: str | None = None
    domicilioParticular: Domicilio | None = None
    domicilioComercial: Domicilio | None = None
    

@dataclass
class Domicilio:
    codProvincia: int
    codPais: int | None = None
    altura: str | None = None
    calle: str | None = None
    piso: str | None = None
    departamento: str | None = None
    localidad: str | None = None
    codigoPostal: str | None = None
    telefono: str | None = None
    fax: str | None = None
    recibeInfoFax: bool | None = None
    

@dataclass
class Instrucciones:
    moneda: str
    banco: int | None = None
    tpCuenta: int | None = None
    numSucursal: int | None = None
    numeroCuenta: str | None = None
    cbu: str | None = None
    cuit: str | None = None
    ctaAlias: str | None = None


@dataclass
class EntMailing:
    codEntMailing: int
