from enum import Enum
from typing import Literal

SITUATIONS = Literal["Afastamento", "Atividade normal", "Férias", "Recesso", "Rescisão"]
Bool = Literal[0, 1]


class EnumTipoDeDadosModificados(int, Enum):
    CONTRATUAIS = 1
    PESSOAIS = 2
    CONTRATUAIS_E_PESSOAIS = 3


class EnumTipoDeOperacao(int, Enum):
    INCLUSAO = 1
    ALTERACAO = 2
    EXCLUSAO = 3


class EnumTipoDeOperacaoContratoLog(int, Enum):
    INCLUSAO = 1
    ALTERACAO = 2
    EXCLUSAO = 3


class EnumTipoDeDadosModificadosDaUnidadeOrganizacional(int, Enum):
    DADOS_QUE_ALTERAM_HIERARQUIA = 1


class EnumTipoDeRetorno(int, Enum):
    SUCESSO = 0
    INCONSISTENCIA = 1
    ERRO = 2
    NAO_PROCESSADO = 3


class EnumOperacaoExecutada(int, Enum):
    NENHUM = 0
    OBJETO_SEM_ALTERACAO = 1
    CADASTRO = 2
    ATUALIZACAO = 3
    EXCLUSAO = 4
    CADASTRO_EM_LOTE = 5
    VALIDACAO = 6


class EnumCampoDeBuscaDoContratoDeTrabalho(int, Enum):
    MATRICULA = 0
    ID_PESSOA = 1
    CPF = 2
    IDENTIDADE = 3
    RIC = 4
    CTPS = 5
    PIS = 6
    TITULO_ELEITOR = 7
    CNH = 8


# Reports Enums


class EnumTipoArquivoRelatorio(int, Enum):
    PDF = 0
    TXT = 1
    CSV = 2


class EnumTipoGrupoDeParametrosRelatorio(int, Enum):
    PARAMETRO_DE_USUARIO = 0
    SENTENCA_SIMPLES = 1
    SENTENCA_DINAMICA = 2


class EnumOperacaoParametroRelatorio(int, Enum):
    IGUAL = 0
    DIFERENTE = 1
    MAIOR = 2
    MENOR = 3
    MAIOR_IGUAL = 4
    MENOR_IGUAL = 5
    UM_DOS_VALORES = 6
    NAO_UM_DOS_VALORES = 7


class EnumTipoDeDadoParametroRelatorio(int, Enum):
    FDT_CHAR = 0
    FDT_SHORT = 1
    FDT_INT = 2
    FDT_FLOAT = 3
    FDT_DATE_AMD = 4
    FDT_DATE_AM = 5
    FDT_BOOLEAN = 6
    FDT_DATE_SQL = 7


class EnumCampoContato(int, Enum):
    DDD_TELEFONE = 0
    TELEFONE = 1
    DDD_CELULAR = 2
    CELULAR = 3
    RAMAL = 4
    EMAIL_CORPORATIVO = 5
    EMAIL_PARTICULAR = 6
    LINKEDIN = 7
    FACEBOOK = 8
    TWITTER = 9
