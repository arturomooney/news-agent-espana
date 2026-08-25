import re


# ============================================================
# FILTRO POLÍTICO-ECONÓMICO ESTRICTO
# ============================================================

POLITICA_FUERTE = [
    r"\bgobierno\b",
    r"\bpresidente(?:a)?\b",
    r"\bministro(?:a)?\b",
    r"\bministerio\b",
    r"\bmoncloa\b",
    r"\bcongreso\b",
    r"\bsenado\b",
    r"\bparlamento\b",
    r"\belecciones?\b",
    r"\belectoral\b",
    r"\binvestidura\b",
    r"\bmoción de censura\b",
    r"\boposición\b",
    r"\bcoalición\b",

    # Partidos políticos
    r"\bpsoe\b",
    r"\bpp\b",
    r"\bvox\b",
    r"\bsumar\b",
    r"\bpodemos\b",
    r"\berc\b",
    r"\bjunts\b",
    r"\bbildu\b",
    r"\bpnv\b",
    r"\bpartido político\b",

    # Legislación e instituciones
    r"\bproposición de ley\b",
    r"\bproyecto de ley\b",
    r"\breforma legislativa\b",
    r"\breforma legal\b",
    r"\bdecreto ley\b",
    r"\breal decreto\b",
    r"\btribunal constitucional\b",
    r"\bconsejo de seguridad nacional\b",

    # Política territorial
    r"\bgeneralitat\b",
    r"\bgovern\b",
    r"\bparlament de catalunya\b",
    r"\bcomunidad autónoma\b",
    r"\bcomunidades autónomas\b",

    # Política internacional
    r"\btrump\b",
    r"\bunión europea\b",
    r"\bcomisión europea\b",
    r"\bparlamento europeo\b",
    r"\botan\b",
    r"\bdiplomacia\b",
    r"\bpolítica exterior\b",
]


ECONOMIA_FUERTE = [
    r"\bpresupuestos generales\b",
    r"\bpolítica económica\b",
    r"\bpolítica fiscal\b",
    r"\bpolítica monetaria\b",
    r"\bhacienda\b",
    r"\bministerio de hacienda\b",
    r"\bimpuestos?\b",
    r"\btributari[oa]s?\b",
    r"\biva\b",
    r"\birpf\b",
    r"\bdeuda pública\b",
    r"\bdéficit público\b",
    r"\bgasto público\b",
    r"\bfinanciación autonómica\b",
    r"\baranceles?\b",
    r"\bsanciones económicas\b",
    r"\bregulación económica\b",
]


POLITICA_MEDIA = [
    r"\bfiscalía\b",
    r"\bfiscal(?:es)?\b",
    r"\btribunal supremo\b",
    r"\btribunal\b",
    r"\bjusticia\b",
    r"\bsentencia\b",
    r"\bley\b",
    r"\bdecreto\b",
    r"\bseguridad nacional\b",
    r"\bfrontera\b",
    r"\binmigración\b",
    r"\binmigrantes?\b",
    r"\bcrisis migratoria\b",
    r"\bguardia civil\b",
    r"\bministerio del interior\b",
    r"\bsanciones\b",
]


# ============================================================
# COSAS QUE NO QUEREMOS
# ============================================================

NO_POLITICA = [
    # Sucesos
    r"\baccidente\b",
    r"\bmuere\b",
    r"\bmueren\b",
    r"\bmuerto\b",
    r"\bmuerta\b",
    r"\bmuertos\b",
    r"\bmuertas\b",
    r"\bfallece\b",
    r"\bfallecido\b",
    r"\bfallecida\b",
    r"\bcadáver(?:es)?\b",
    r"\bdesaparecid[oa]s?\b",
    r"\bherido(?:s|as)?\b",

    # Clima
    r"\bincendio\b",
    r"\bfuego\b",
    r"\btemporal\b",
    r"\bgranizada\b",
    r"\binundaciones?\b",
    r"\blluvias?\b",
    r"\btormenta\b",

    # Tráfico y transporte
    r"\btráfico\b",
    r"\bcarretera\b",
    r"\bcarreteras\b",
    r"\btúnel\b",
    r"\bautopista\b",
    r"\btrenes?\b",
    r"\baeropuerto\b",
    r"\bvuelo\b",
    r"\bavión\b",
    r"\baviones\b",
    r"\bdron\b",

    # Animales / naturaleza
    r"\bpalomas?\b",
    r"\baves?\b",
    r"\bgarrapatas?\b",
    r"\bfauna\b",
    r"\bflora\b",

    # Crónica policial
    r"\brobo\b",
    r"\brobaron\b",
    r"\batraco\b",
    r"\basesinato\b",
    r"\bcrimen\b",
    r"\bcrímenes\b",
    r"\bdetenido(?:s|as)?\b",
    r"\bagresión\b",

    # Salud / sociedad
    r"\benfermedad\b",
    r"\bhospital\b",
    r"\bpaciente\b",
    r"\bvivienda\b",
    r"\balquiler\b",
    r"\bhipoteca\b",
    r"\bconsumo\b",
    r"\bvecino(?:s)?\b",
    r"\bmascotas?\b",

    # Trabajo / educación
    r"\btrabajador(?:es)?\b",
    r"\bhuelga\b",
    r"\bempleo\b",
    r"\bsalarios?\b",
    r"\bteletrabajo\b",
    r"\bcolegio\b",
    r"\buniversidad\b",
    r"\bestudiante\b",

    # Deportes
    r"\bfútbol\b",
    r"\bbarça\b",
    r"\baficionados?\b",
    r"\bliga\b",
    r"\bjugador(?:es)?\b",
    r"\bpartido de fútbol\b",

    # Cultura
    r"\bpelícula\b",
    r"\bserie\b",
    r"\bactor(?:es)?\b",
    r"\bactriz\b",
    r"\bmúsica\b",
    r"\bconcierto\b",
    r"\btelevisión\b",
    r"\bradio\b",
]


# ============================================================
# CONTEXTO POLÍTICO
# ============================================================

CONTEXTO_POLITICO = [
    r"\bgobierno\b",
    r"\bpresidente(?:a)?\b",
    r"\bministro(?:a)?\b",
    r"\bministerio\b",
    r"\bmoncloa\b",
    r"\bcongreso\b",
    r"\bsenado\b",
    r"\bparlamento\b",
    r"\belecciones?\b",
    r"\belectoral\b",
    r"\bpsoe\b",
    r"\bpp\b",
    r"\bvox\b",
    r"\bsumar\b",
    r"\bpodemos\b",
    r"\berc\b",
    r"\bjunts\b",
    r"\bbildu\b",
    r"\bpnv\b",
    r"\bgeneralitat\b",
    r"\bgovern\b",
    r"\bpolítica\b",
    r"\bpolítico(?:s|as)?\b",
]


def buscar(texto, patrones):
    for patron in patrones:
        if re.search(patron, texto, re.IGNORECASE):
            return True
    return False


def contar(texto, patrones):
    total = 0

    for patron in patrones:
        if re.search(patron, texto, re.IGNORECASE):
            total += 1

    return total


def es_politica_estricta(titulo, categoria="", descripcion=""):

    titulo = str(titulo or "")
    categoria = str(categoria or "")
    descripcion = str(descripcion or "")

    titulo = re.sub(r"\s+", " ", titulo.lower())
    texto = re.sub(
        r"\s+",
        " ",
        f"{titulo} {categoria} {descripcion}".lower()
    )

    # --------------------------------------------------------
    # PASO 1
    # Si el TÍTULO es claramente un suceso, clima,
    # tráfico, deporte, etc., lo descartamos.
    # --------------------------------------------------------

    if buscar(titulo, NO_POLITICA):

        # Única excepción:
        # si el propio título contiene una señal política
        # muy clara, permitimos continuar.
        if not buscar(titulo, POLITICA_FUERTE):
            return False

    # --------------------------------------------------------
    # PASO 2
    # Si el título tiene una señal política fuerte,
    # aceptamos directamente.
    # --------------------------------------------------------

    if buscar(titulo, POLITICA_FUERTE):
        return True

    # --------------------------------------------------------
    # PASO 3
    # Si el título tiene una señal económica fuerte,
    # necesitamos además contexto político.
    # --------------------------------------------------------

    if buscar(titulo, ECONOMIA_FUERTE):
        if buscar(texto, CONTEXTO_POLITICO):
            return True

    # --------------------------------------------------------
    # PASO 4
    # Para artículos donde la señal política aparece
    # en la descripción:
    #
    # exigimos AL MENOS DOS señales fuertes.
    # --------------------------------------------------------

    fuertes = contar(texto, POLITICA_FUERTE)

    if fuertes >= 2:
        return True

    # --------------------------------------------------------
    # PASO 5
    # Una señal política fuerte + una señal política media.
    # --------------------------------------------------------

    medias = contar(texto, POLITICA_MEDIA)

    if fuertes >= 1 and medias >= 1:
        return True

    # --------------------------------------------------------
    # PASO 6
    # Dos señales económicas fuertes también permiten
    # clasificar como político-económico.
    # --------------------------------------------------------

    economia = contar(texto, ECONOMIA_FUERTE)

    if economia >= 2:
        return True

    # --------------------------------------------------------
    # Todo lo demás se descarta.
    # --------------------------------------------------------

    return False
if __name__ == "__main__":
    print("FILTRO POLITICO-ECONOMICO: OK")
