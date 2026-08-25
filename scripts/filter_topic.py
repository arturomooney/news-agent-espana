import re

# ============================================================
# FILTRO POLÍTICO ESTRICTO — v2
# Reduce falsos positivos de sucesos, clima, tráfico, sociedad,
# deportes, consumo, etc.
# ============================================================

POLITICA = [
    # Gobierno / instituciones
    r"\bgobierno\b",
    r"\bpresidente(?:a)?\b",
    r"\bministro(?:a)?\b",
    r"\bministerio\b",
    r"\bmoncloa\b",
    r"\bconsejo de ministros\b",
    r"\bconsejo de seguridad nacional\b",
    r"\bsecretario(?:a)? de estado\b",

    # Parlamento / elecciones
    r"\bcongreso\b",
    r"\bsenado\b",
    r"\bdiputad[oa]s?\b",
    r"\bsenador(?:a)?\b",
    r"\bparlamento\b",
    r"\belecciones?\b",
    r"\belectoral\b",
    r"\bvotación\b",
    r"\bvotos?\b",
    r"\bmayoría parlamentaria\b",
    r"\binvestidura\b",
    r"\bmoción de censura\b",

    # Partidos
    r"\bpp\b",
    r"\bpsoe\b",
    r"\bvox\b",
    r"\bsumar\b",
    r"\bpodemos\b",
    r"\berc\b",
    r"\bjunts\b",
    r"\bpnv\b",
    r"\bbildu\b",
    r"\bpartido político\b",
    r"\bpartido\b",
    r"\boposición\b",
    r"\bgobernabilidad\b",

    # Política territorial
    r"\bcataluñ[ao]\b",
    r"\bcatalán\b",
    r"\bcatalana\b",
    r"\bpaís vasco\b",
    r"\beuskadi\b",
    r"\bgalicia\b",
    r"\bcomunidad de madrid\b",
    r"\bcomunidades autónomas\b",
    r"\bautonomía\b",
    r"\bautonómico\b",
    r"\bautonómica\b",
    r"\bindependencia\b",
    r"\bindependentismo\b",

    # Estado / legislación / poder público
    r"\bley\b",
    r"\bdecreto\b",
    r"\breforma legislativa\b",
    r"\breforma legal\b",
    r"\bproposición de ley\b",
    r"\bproyecto de ley\b",
    r"\bboletín oficial\b",
    r"\btribunal constitucional\b",
    r"\bfiscalía\b",
    r"\bfiscal\b",
    r"\btribunal supremo\b",
    r"\bjusticia\b",
    r"\bsentencia\b",

    # Política internacional
    r"\bpresidente de estados unidos\b",
    r"\btrump\b",
    r"\bue\b",
    r"\bunión europea\b",
    r"\bcomisión europea\b",
    r"\bbruselas\b",
    r"\botan\b",
    r"\bdiplomacia\b",
    r"\bsanciones\b",
    r"\baranceles?\b",
    r"\bpolítica exterior\b",
    r"\brelaciones diplomáticas\b",

    # Migración / seguridad cuando tienen dimensión política
    r"\bpolítica migratoria\b",
    r"\bcrisis migratoria\b",
    r"\binmigración\b",
    r"\bmigrantes?\b",
    r"\bfrontera\b",
    r"\bguardia civil\b",
    r"\bministerio del interior\b",
    r"\bseguridad nacional\b",
]

# ============================================================
# EXCLUSIONES FUERTES
# ============================================================

NO_POLITICA = [
    # Accidentes / sucesos
    r"\baccidente\b",
    r"\bmuere\b",
    r"\bmuerto\b",
    r"\bmuerta\b",
    r"\bfallece\b",
    r"\bfallecido\b",
    r"\bcadáver(?:es)?\b",
    r"\bdesaparecid[oa]\b",
    r"\bbuscan\b",
    r"\bherido(?:s|as)?\b",
    r"\bincendio\b",
    r"\bfuego\b",
    r"\bexplosión\b",
    r"\btemporal\b",
    r"\bgranizada\b",
    r"\binundaciones?\b",
    r"\blluvias?\b",
    r"\btormenta\b",

    # Tráfico / transporte
    r"\btráfico\b",
    r"\bcarretera\b",
    r"\bcarreteras\b",
    r"\btúnel\b",
    r"\bautopista\b",
    r"\btrenes?\b",
    r"\bvuelo\b",
    r"\baeropuerto\b",
    r"\bavión\b",
    r"\baviones\b",

    # Medio ambiente / animales
    r"\bpalomas?\b",
    r"\baves?\b",
    r"\bgarrapatas?\b",
    r"\bostras?\b",
    r"\bmejillones?\b",
    r"\bfauna\b",
    r"\bflora\b",

    # Sucesos policiales sin dimensión política clara
    r"\brobo\b",
    r"\brobaron\b",
    r"\batraco\b",
    r"\basesinato\b",
    r"\bcrimen\b",
    r"\bcrímenes\b",
    r"\bdetenido\b",
    r"\bdetenida\b",
    r"\bdetenidos\b",
    r"\bagresión\b",
    r"\bviolencia\b",

    # Salud / sociedad / consumo
    r"\benfermedad\b",
    r"\bhospital\b",
    r"\bpaciente\b",
    r"\bvivienda\b",
    r"\balquiler\b",
    r"\bhipoteca\b",
    r"\bconsumo\b",
    r"\bvecino\b",
    r"\bvecinos\b",
    r"\bmascotas?\b",

    # Educación / empleo / sociedad cuando no hay política explícita
    r"\btrabajador\b",
    r"\btrabajadores\b",
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
    r"\bbarcelona\b",
    r"\baficionados?\b",
    r"\bpartido\b",
    r"\bliga\b",
    r"\bjugador\b",

    # Cultura / entretenimiento
    r"\bpelícula\b",
    r"\bserie\b",
    r"\bactor\b",
    r"\bactriz\b",
    r"\bmúsica\b",
    r"\bconcierto\b",
    r"\btelevisión\b",
    r"\bradio\b",
]

# ============================================================
# PALABRAS QUE POR SÍ SOLAS NO BASTAN
# ============================================================

AMBIGUAS = {
    "partido",
    "justicia",
    "gobierno",
    "estado",
    "seguridad",
    "crisis",
    "economía",
    "empresa",
    "trabajadores",
    "radio",
    "barcelona",
    "madrid",
}

# ============================================================
# FUNCIÓN
# ============================================================

def es_politica_estricta(titulo, categoria="", descripcion=""):
    texto = " ".join([
        str(titulo or ""),
        str(categoria or ""),
        str(descripcion or "")
    ]).lower()

    # Normalización básica
    texto = re.sub(r"\s+", " ", texto)

    # --------------------------------------------------------
    # 1. Si contiene una exclusión muy clara, descartamos.
    # --------------------------------------------------------
    for patron in NO_POLITICA:
        if re.search(patron, texto, re.IGNORECASE):
            # Excepción: si además aparecen señales políticas
            # MUY fuertes, permitimos que siga.
            senales_fuertes = [
                r"\bpresidente\b",
                r"\bpresidenta\b",
                r"\bministro\b",
                r"\bministra\b",
                r"\bmoncloa\b",
                r"\bcongreso\b",
                r"\bsenado\b",
                r"\bpp\b",
                r"\bpsoe\b",
                r"\bvox\b",
                r"\bsumar\b",
                r"\bpodemos\b",
                r"\bjunts\b",
                r"\berc\b",
                r"\bbildu\b",
                r"\bpnv\b",
                r"\belecciones?\b",
                r"\bparlamento\b",
                r"\bley\b",
                r"\bdecreto\b",
                r"\bcoalición\b",
                r"\boposición\b",
            ]

            if not any(
                re.search(p, texto, re.IGNORECASE)
                for p in senales_fuertes
            ):
                return False

    # --------------------------------------------------------
    # 2. Debe existir al menos UNA señal política explícita.
    # --------------------------------------------------------
    coincidencias = 0

    for patron in POLITICA:
        if re.search(patron, texto, re.IGNORECASE):
            coincidencias += 1

    if coincidencias == 0:
        return False

    # --------------------------------------------------------
    # 3. Para máxima precisión:
    #    una sola palabra ambigua NO clasifica como política.
    # --------------------------------------------------------
    palabras_politicas_fuertes = [
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
        r"\bpartido político\b",
        r"\bpsoe\b",
        r"\bvox\b",
        r"\bsumar\b",
        r"\bpodemos\b",
        r"\bpp\b",
        r"\bjunts\b",
        r"\berc\b",
        r"\bbildu\b",
        r"\bpnv\b",
        r"\bley\b",
        r"\bdecreto\b",
        r"\bproposición de ley\b",
        r"\bproyecto de ley\b",
        r"\btribunal constitucional\b",
        r"\bpolítica migratoria\b",
        r"\bseguridad nacional\b",
        r"\bpolítica exterior\b",
    ]

    tiene_senal_fuerte = any(
        re.search(p, texto, re.IGNORECASE)
        for p in palabras_politicas_fuertes
    )

    # --------------------------------------------------------
    # 4. Si solo hay señales débiles/ambiguas, descartamos.
    # --------------------------------------------------------
    if not tiene_senal_fuerte:
        return False

    return True
