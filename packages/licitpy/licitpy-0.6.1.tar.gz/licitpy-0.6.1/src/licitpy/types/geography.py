from enum import Enum
from typing import Dict

from pydantic import BaseModel

# Credit: https://gist.github.com/juanbrujo
# Based on :https://gist.github.com/juanbrujo/0fd2f4d126b3ce5a95a7dd1f28b3d8dd (xlsx)


class Region(Enum):
    XV = "Región de Arica y Parinacota"
    I = "Región de Tarapacá"  # noqa: E741
    II = "Región de Antofagasta"
    III = "Región de Atacama"
    IV = "Región de Coquimbo"
    V = "Región de Valparaíso"
    RM = "Región Metropolitana de Santiago"
    VI = "Región del Libertador General Bernardo O´Higgins"
    VII = "Región del Maule"
    XVI = "Región del Ñuble"
    VIII = "Región del Biobío"
    IX = "Región de la Araucanía"
    XIV = "Región de Los Ríos"
    X = "Región de los Lagos"
    XI = "Región Aysén del General Carlos Ibáñez del Campo"
    XII = "Región de Magallanes y de la Antártica"
    INTERNATIONAL = "Extranjero"
    UNKNOWN = "Desconocido"


class Province(Enum):
    ARICA = "Arica"
    PARINACOTA = "Parinacota"
    IQUIQUE = "Iquique"
    TAMARUGAL = "Tamarugal"
    ANTOFAGASTA = "Antofagasta"
    EL_LOA = "El Loa"
    TOCOPILLA = "Tocopilla"
    CHAÑARAL = "Chañaral"
    COPIAPO = "Copiapo"
    HUASCO = "Huasco"
    CHOAPA = "Choapa"
    ELQUI = "Elqui"
    LIMARI = "Limari"
    ISLA_DE_PASCUA = "Isla de Pascua"
    LOS_ANDES = "Los Andes"
    MARGA_MARGA = "Marga Marga"
    PETORCA = "Petorca"
    QUILLOTA = "Quillota"
    SAN_ANTONIO = "San Antonio"
    SAN_FELIPE_DE_ACONCAGUA = "San Felipe de Aconcagua"
    VALPARAISO = "Valparaiso"
    CACHAPOAL = "Cachapoal"
    CARDENAL_CARO = "Cardenal Caro"
    COLCHAGUA = "Colchagua"
    CAUQUENES = "Cauquenes"
    CURICO = "Curico"
    LINARES = "Linares"
    TALCA = "Talca"
    DIGUILLIN = "Diguillin"
    ITATA = "Itata"
    PUNILLA = "Punilla"
    ARAUCO = "Arauco"
    BIOBIO = "Biobio"
    CONCEPCION = "Concepcion"
    CAUTIN = "Cautin"
    MALLECO = "Malleco"
    RANCO = "Ranco"
    VALDIVIA = "Valdivia"
    CHILOE = "Chiloe"
    LLANQUIHUE = "Llanquihue"
    OSORNO = "Osorno"
    PALENA = "Palena"
    AYSEN = "Aysen"
    CAPITAN_PRAT = "Capitan Prat"
    COYHAIQUE = "Coyhaique"
    GENERAL_CARRERA = "General Carrera"
    ANTARTICA_CHILENA = "Antartica Chilena"
    MAGALLANES = "Magallanes"
    TIERRA_DEL_FUEGO = "Tierra del Fuego"
    ULTIMA_ESPERANZA = "Ultima Esperanza"
    CHACABUCO = "Chacabuco"
    CORDILLERA = "Cordillera"
    MAIPO = "Maipo"
    MELIPILLA = "Melipilla"
    SANTIAGO = "Santiago"
    TALAGANTE = "Talagante"


class Commune(Enum):
    UNKNOWN = "Desconocido"
    TORRES_DEL_PAYNE = "Torres del Payne"
    ARICA = "Arica"
    EL_CARMEN = "El Carmen"
    SANTIAGO = "Santiago"
    COYHAIQUE = "Coyhaique"
    ÑUÑOA = "Ñuñoa"
    LA_SERENA = "La Serena"
    INDEPENDENCIA = "Independencia"
    TALCAHUANO = "Talcahuano"
    LO_PRADO = "Lo Prado"
    CUNCO = "Cunco"
    TEMUCO = "Temuco"
    PORTEZUELO = "Portezuelo"
    TOME = "Tomé"
    RANCAGUA = "Rancagua"
    COPIAPO = "Copiapó"
    IQUIQUE = "Iquique"
    TALCA = "Talca"
    MAFIL = "Máfil"
    ALHUE = "Alhué"
    VALPARAISO = "Valparaíso"
    PUYEHUE = "Puyehue"
    PORVENIR = "Porvenir"
    SANTIAGO_CENTRO = "Santiago Centro"
    QUILLOTA = "Quillota"
    OLLAGUE = "Ollague"
    PELARCO = "Pelarco"
    LOS_VILOS = "Los Vilos"
    LA_FLORIDA = "La Florida"
    VILCUN = "Vilcún"
    SAN_FERNANDO = "San Fernando"
    LOS_SAUCES = "Los Sauces"
    CANELA = "Canela"
    SAN_JAVIER = "San Javier"
    RENAICO = "Renaico"
    SAN_ROSENDO = "San Rosendo"
    MAIPU = "Maipú"
    PICHILEMU = "Pichilemu"
    SAN_ANTONIO = "San Antonio"
    LOS_ANDES = "Los Andes"
    PARRAL = "Parral"
    CAUQUENES = "Cauquenes"
    LEBU = "Lebu"
    QUILICURA = "Quilicura"
    PUERTO_SAAVEDRA = "Puerto Saavedra"
    PENCO = "Penco"
    PUNTA_ARENAS = "Punta Arenas"
    VILLARRICA = "Villarrica"
    COIHUECO = "Coihueco"
    PUERTO_MONTT = "Puerto Montt"
    ISLA_DE_MAIPO = "Isla de Maipo"
    PROVIDENCIA = "Providencia"
    CORONEL = "Coronel"
    VIÑA_DEL_MAR = "Viña del Mar"
    FLORIDA = "Florida"
    CALDERA = "Caldera"
    CHIGUAYANTE = "Chiguayante"
    CALAMA = "Calama"
    MARIQUINA = "Mariquina"
    LA_PINTANA = "La Pintana"
    CALBUCO = "Calbuco"
    MARCHIGUE = "Marchigue"
    LA_REINA = "La Reina"
    SAN_FABIAN = "San Fabián"
    PAPUDO = "Papudo"
    ARAUCO = "Arauco"
    RENGO = "Rengo"
    SAN_MIGUEL = "San Miguel"
    OVALLE = "Ovalle"
    CHILLAN = "Chillán"
    FUTRONO = "Futrono"
    PANGUIPULLI = "Panguipulli"
    QUILPUE = "Quilpué"
    MACHALI = "Machalí"
    RENCA = "Renca"
    PICHIDEGUA = "Pichidegua"
    SAN_FELIPE = "San Felipe"
    PINTO = "Pinto"
    LOS_ANGELES = "Los Angeles"
    CERRILLOS = "Cerrillos"
    MONTE_PATRIA = "Monte Patria"
    PEÑAFLOR = "Peñaflor"
    SAN_CARLOS = "San Carlos"
    LA_UNION = "La Unión"
    TREHUACO = "Trehuaco"
    CONCEPCION = "Concepción"
    RIO_NEGRO = "Río Negro"
    VALLENAR = "Vallenar"
    LONGAVI = "Longaví"
    CASTRO = "Castro"
    TALAGANTE = "Talagante"
    PAREDONES = "Paredones"
    CHONCHI = "Chonchi"
    PITRUFQUEN = "Pitrufquén"
    PUDAHUEL = "Pudahuel"
    PUNITAQUI = "Punitaqui"
    SAN_RAMON = "San Ramón"
    OSORNO = "Osorno"
    EL_MONTE = "El Monte"
    FRUTILLAR = "Frutillar"
    LAUTARO = "Lautaro"
    ROMERAL = "Romeral"
    SAN_ESTEBAN = "San Esteban"
    MAULLIN = "Maullín"
    GRANEROS = "Graneros"
    YUMBEL = "Yumbel"
    POZO_ALMONTE = "Pozo Almonte"
    HUALPEN = "Hualpén"
    LAS_CONDES = "Las Condes"
    VITACURA = "Vitacura"
    AYSEN = "Aysén"
    SANTA_CRUZ = "Santa Cruz"
    ESTACION_CENTRAL = "Estación Central"
    CAÑETE = "Cañete"
    RIO_BUENO = "Río Bueno"
    QUINTA_NORMAL = "Quinta Normal"
    BULNES = "Bulnes"
    ÑIQUEN = "Ñiquén"
    MAULE = "Maule"
    DOÑIHUE = "Doñihue"
    ANDACOLLO = "Andacollo"
    BUIN = "Buin"
    PAILLACO = "Paillaco"
    MOLINA = "Molina"
    OLMUE = "Olmué"
    MOSTAZAL = "Mostazal"
    ANTOFAGASTA = "Antofagasta"
    QUILLON = "Quillón"
    SALAMANCA = "Salamanca"
    VILLA_ALEMANA = "Villa Alemana"
    CURICO = "Curicó"
    QUINCHAO = "Quinchao"
    ZAPALLAR = "Zapallar"
    PAINE = "Paine"
    COQUIMBO = "Coquimbo"
    LOS_ALAMOS = "Los Alamos"
    QUILLECO = "Quilleco"
    LO_ESPEJO = "Lo Espejo"
    TOCOPILLA = "Tocopilla"
    RAUCO = "Rauco"
    DIEGO_DE_ALMAGRO = "Diego De Almagro"
    PEMUCO = "Pemuco"
    VALDIVIA = "Valdivia"
    CONTULMO = "Contulmo"
    VICTORIA = "Victoria"
    TIRUA = "Tirúa"
    COELEMU = "Coelemu"
    MACUL = "Macul"
    CATEMU = "Catemu"
    PUREN = "Purén"
    QUINTA_DE_TILCOCO = "Quinta de Tilcoco"
    TALTAL = "Taltal"
    COLTAUCO = "Coltauco"
    SAN_JUAN_DE_LA_COSTA = "San Juan de La Costa"
    LONCOCHE = "Loncoche"
    ALTO_HOSPICIO = "Alto Hospicio"
    COMBARBALA = "Combarbalá"
    LONQUIMAY = "Lonquimay"
    MELIPILLA = "Melipilla"
    PENCAHUE = "Pencahue"
    CHANCO = "Chanco"
    PADRE_HURTADO = "Padre Hurtado"
    LOTA = "Lota"
    HUASCO = "Huasco"
    LO_BARNECHEA = "Lo Barnechea"
    MALLOA = "Malloa"
    LA_CISTERNA = "La Cisterna"
    LINARES = "Linares"
    MULCHEN = "Mulchén"
    LANCO = "Lanco"
    ALTO_BIO_BIO = "Alto Bio Bio"
    NINHUE = "Ninhue"
    SAN_BERNARDO = "San Bernardo"
    PALENA = "Palena"
    SAN_RAFAEL = "San Rafael"
    ANGOL = "Angol"
    PUERTO_VARAS = "Puerto Varas"
    SAN_PEDRO = "San Pedro"
    EL_TABO = "El Tabo"
    NAVIDAD = "Navidad"
    LIMACHE = "Limache"
    SAN_NICOLAS = "San Nicolás"
    CODEGUA = "Codegua"
    VILLA_ALEGRE = "Villa Alegre"
    FREIRINA = "Freirina"
    CHAITEN = "Chaitén"
    NEGRETE = "Negrete"
    PEÑALOLEN = "Peñalolén"
    ANCUD = "Ancud"
    NOGALES = "Nogales"
    PUENTE_ALTO = "Puente Alto"
    PUERTO_NATALES = "Puerto Natales"
    RECOLETA = "Recoleta"
    CABILDO = "Cabildo"
    YUNGAY = "Yungay"
    O_HIGGINS = "O Higgins"
    PAIHUANO = "Paihuano"
    REQUINOA = "Requinoa"
    MARIA_ELENA = "María Elena"
    LA_LIGUA = "La Ligua"
    TUCAPEL = "Tucapel"
    RIO_CLARO = "Río Claro"
    LUMACO = "Lumaco"
    HUECHURABA = "Huechuraba"
    QUEILEN = "Queilén"
    EL_QUISCO = "El Quisco"
    LA_GRANJA = "La Granja"
    PADRE_LAS_CASAS = "Padre Las Casas"
    CABRERO = "Cabrero"
    GORBEA = "Gorbea"
    CHILLAN_VIEJO = "Chillán Viejo"
    QUEMCHI = "Quemchi"
    HUALQUI = "Hualqui"
    CONCON = "Concón"
    SANTA_MARIA = "Santa María"
    SANTA_BARBARA = "Santa Bárbara"
    PERALILLO = "Peralillo"
    COCHAMO = "Cochamó"
    MELIPEUCO = "Melipeuco"
    SIERRA_GORDA = "Sierra Gorda"
    LAGO_VERDE = "Lago Verde"
    LAS_CABRAS = "Las Cabras"
    VICUÑA = "Vicuña"
    QUILACO = "Quilaco"
    SAN_PEDRO_DE_LA_PAZ = "San Pedro de La Paz"
    CAMARONES = "Camarones"
    MARIA_PINTO = "María Pinto"
    LAJA = "Laja"
    NUEVA_IMPERIAL = "Nueva Imperial"
    SAN_PABLO = "San Pablo"
    SAN_CLEMENTE = "San Clemente"
    SANTO_DOMINGO = "Santo Domingo"
    LA_CALERA = "La Calera"
    GALVARINO = "Galvarino"
    CURACAVI = "Curacaví"
    CHOL_CHOL = "Chol Chol"
    TRAIGUEN = "Traiguén"
    PUTRE = "Putre"
    QUIRIHUE = "Quirihue"
    CALLE_LARGA = "Calle Larga"
    CARAHUE = "Carahue"
    EL_BOSQUE = "El Bosque"
    PANQUEHUE = "Panquehue"
    TEODORO_SCHMIDT = "Teodoro Schmidt"
    CERRO_NAVIA = "Cerro Navia"
    ERCILLA = "Ercilla"
    PELLUHUE = "Pelluhue"
    FREIRE = "Freire"
    RETIRO = "Retiro"
    MEJILLONES = "Mejillones"
    SAN_JOAQUIN = "San Joaquín"
    COBQUECURA = "Cobquecura"
    YERBAS_BUENAS = "Yerbas Buenas"
    PLACILLA = "Placilla"
    CHEPICA = "Chépica"
    TIL_TIL = "Til Til"
    LAMPA = "Lampa"
    PEUMO = "Peumo"
    COLBUN = "Colbún"
    TENO = "Teno"
    SAGRADA_FAMILIA = "Sagrada Familia"
    PUMANQUE = "Pumanque"
    LAS_GUAITECAS = "Las Guaitecas"
    SAN_VICENTE_DE_TAGUA_TAGUA = "San Vicente de Tagua Tagua"
    CUREPTO = "Curepto"
    CARTAGENA = "Cartagena"
    RANQUIL = "Ranquil"
    CURANILAHUE = "Curanilahue"
    COLINA = "Colina"
    TOLTEN = "Toltén"
    CISNES = "Cisnes"
    FUTALEUFU = "Futaleufú"
    RIO_HURTADO = "Río Hurtado"
    LITUECHE = "Litueche"
    LA_HIGUERA = "La Higuera"
    CALERA_DE_TANGO = "Calera De Tango"
    CURACO_DE_VELEZ = "Curaco de Vélez"
    TIERRA_AMARILLA = "Tierra Amarilla"
    PUTAENDO = "Putaendo"
    PALMILLA = "Palmilla"
    NACIMIENTO = "Nacimiento"
    PUCON = "Pucón"
    PEDRO_AGUIRRE_CERDA = "Pedro Aguirre Cerda"
    CONSTITUCION = "Constitución"
    PERQUENCO = "Perquenco"
    PURRANQUE = "Purranque"
    SAN_IGNACIO = "San Ignacio"
    HUALAÑE = "Hualañé"
    PETORCA = "Petorca"
    SAN_PEDRO_DE_ATACAMA = "San Pedro de Atacama"
    CABO_DE_HORNOS = "Cabo de Hornos"
    LOLOL = "Lolol"
    ILLAPEL = "Illapel"
    QUELLON = "Quellón"
    CURACAUTIN = "Curacautín"
    PICA = "Pica"
    RINCONADA = "Rinconada"
    LA_CRUZ = "La Cruz"
    ALGARROBO = "Algarrobo"
    CHILE_CHICO = "Chile Chico"
    CHAÑARAL = "Chañaral"
    COLLIPULLI = "Collipulli"
    COCHRANE = "Cochrane"
    TIMAUKEL = "Timaukel"
    ANTARTICA = "Antártica"
    LAGO_RANCO = "Lago Ranco"
    EMPEDRADO = "Empedrado"
    FRESIA = "Fresia"
    LICANTEN = "Licantén"
    LLAYLLAY = "Llay-Llay"
    SANTA_JUANA = "Santa Juana"
    HUALAIHUE = "Hualaihué"
    PUCHUNCAVI = "Puchuncaví"
    SAN_JOSE_DE_MAIPO = "San José de Maipo"
    ISLA_DE_PASCUA = "Isla De Pascua"
    HIJUELAS = "Hijuelas"
    CAMIÑA = "Camiña"
    PIRQUE = "Pirque"
    TORTEL = "Tortel"
    LAGUNA_BLANCA = "Laguna Blanca"
    HUARA = "Huara"
    CHIMBARONGO = "Chimbarongo"
    CURARREHUE = "Curarrehue"
    DALCAHUE = "Dalcahue"
    ALTO_DEL_CARMEN = "Alto Del Carmen"
    LOS_LAGOS = "Los Lagos"
    QUINTERO = "Quintero"
    LLANQUIHUE = "Llanquihue"
    PUERTO_OCTAY = "Puerto Octay"
    NANCAGUA = "Nancagua"
    LA_ESTRELLA = "La Estrella"
    ANTUCO = "Antuco"
    OLIVAR = "Olivar"
    RIO_VERDE = "Río Verde"
    CORRAL = "Corral"
    COINCO = "Coinco"
    RIO_IBAÑEZ = "Río Ibáñez"
    JUAN_FERNANDEZ = "Juan Fernández"
    LOS_MUERMOS = "Los Muermos"
    CONCHALI = "Conchalí"
    CASABLANCA = "Casablanca"
    VICHUQUEN = "Vichuquén"
    SAN_GREGORIO = "San Gregorio"
    PUQUELDON = "Puqueldón"
    COLCHANE = "Colchane"
    GENERAL_LAGOS = "General Lagos"
    PRIMAVERA = "Primavera"
    SAN_FRANCISCO_DE_MOSTAZAL = "San Francisco de Mostazal"


class Geography(BaseModel):
    region: Region
    province: Province
    commune: Commune


GeographyChile: Dict[Commune, Geography] = {
    # XV : Región de Arica y Parinacota
    Commune.ARICA: Geography(
        region=Region.XV,
        province=Province.ARICA,
        commune=Commune.ARICA,
    ),
    Commune.CAMARONES: Geography(
        region=Region.XV,
        province=Province.ARICA,
        commune=Commune.CAMARONES,
    ),
    Commune.GENERAL_LAGOS: Geography(
        region=Region.XV,
        province=Province.PARINACOTA,
        commune=Commune.GENERAL_LAGOS,
    ),
    Commune.PUTRE: Geography(
        region=Region.XV,
        province=Province.PARINACOTA,
        commune=Commune.PUTRE,
    ),
    # I: Región de Tarapacá
    Commune.ALTO_HOSPICIO: Geography(
        region=Region.I,
        province=Province.IQUIQUE,
        commune=Commune.ALTO_HOSPICIO,
    ),
    Commune.IQUIQUE: Geography(
        region=Region.I,
        province=Province.IQUIQUE,
        commune=Commune.IQUIQUE,
    ),
    Commune.CAMIÑA: Geography(
        region=Region.I,
        province=Province.TAMARUGAL,
        commune=Commune.CAMIÑA,
    ),
    Commune.COLCHANE: Geography(
        region=Region.I,
        province=Province.TAMARUGAL,
        commune=Commune.COLCHANE,
    ),
    Commune.HUARA: Geography(
        region=Region.I,
        province=Province.TAMARUGAL,
        commune=Commune.HUARA,
    ),
    Commune.PICA: Geography(
        region=Region.I,
        province=Province.TAMARUGAL,
        commune=Commune.PICA,
    ),
    Commune.POZO_ALMONTE: Geography(
        region=Region.I,
        province=Province.TAMARUGAL,
        commune=Commune.POZO_ALMONTE,
    ),
    # II: Región de Antofagasta
    Commune.ANTOFAGASTA: Geography(
        region=Region.II,
        province=Province.ANTOFAGASTA,
        commune=Commune.ANTOFAGASTA,
    ),
    Commune.MEJILLONES: Geography(
        region=Region.II,
        province=Province.ANTOFAGASTA,
        commune=Commune.MEJILLONES,
    ),
    Commune.SIERRA_GORDA: Geography(
        region=Region.II,
        province=Province.ANTOFAGASTA,
        commune=Commune.SIERRA_GORDA,
    ),
    Commune.TALTAL: Geography(
        region=Region.II,
        province=Province.ANTOFAGASTA,
        commune=Commune.TALTAL,
    ),
    Commune.CALAMA: Geography(
        region=Region.II,
        province=Province.EL_LOA,
        commune=Commune.CALAMA,
    ),
    Commune.OLLAGUE: Geography(
        region=Region.II,
        province=Province.EL_LOA,
        commune=Commune.OLLAGUE,
    ),
    Commune.SAN_PEDRO_DE_ATACAMA: Geography(
        region=Region.II,
        province=Province.EL_LOA,
        commune=Commune.SAN_PEDRO_DE_ATACAMA,
    ),
    Commune.MARIA_ELENA: Geography(
        region=Region.II,
        province=Province.TOCOPILLA,
        commune=Commune.MARIA_ELENA,
    ),
    Commune.TOCOPILLA: Geography(
        region=Region.II,
        province=Province.TOCOPILLA,
        commune=Commune.TOCOPILLA,
    ),
    # III: Región de Atacama
    Commune.CHAÑARAL: Geography(
        region=Region.III,
        province=Province.CHAÑARAL,
        commune=Commune.CHAÑARAL,
    ),
    Commune.DIEGO_DE_ALMAGRO: Geography(
        region=Region.III,
        province=Province.CHAÑARAL,
        commune=Commune.DIEGO_DE_ALMAGRO,
    ),
    Commune.CALDERA: Geography(
        region=Region.III,
        province=Province.COPIAPO,
        commune=Commune.CALDERA,
    ),
    Commune.COPIAPO: Geography(
        region=Region.III,
        province=Province.COPIAPO,
        commune=Commune.COPIAPO,
    ),
    Commune.TIERRA_AMARILLA: Geography(
        region=Region.III,
        province=Province.COPIAPO,
        commune=Commune.TIERRA_AMARILLA,
    ),
    Commune.ALTO_DEL_CARMEN: Geography(
        region=Region.III,
        province=Province.HUASCO,
        commune=Commune.ALTO_DEL_CARMEN,
    ),
    Commune.FREIRINA: Geography(
        region=Region.III,
        province=Province.HUASCO,
        commune=Commune.FREIRINA,
    ),
    Commune.HUASCO: Geography(
        region=Region.III,
        province=Province.HUASCO,
        commune=Commune.HUASCO,
    ),
    Commune.VALLENAR: Geography(
        region=Region.III,
        province=Province.HUASCO,
        commune=Commune.VALLENAR,
    ),
    # IV : Región de Coquimbo
    Commune.CANELA: Geography(
        region=Region.IV,
        province=Province.CHOAPA,
        commune=Commune.CANELA,
    ),
    Commune.ILLAPEL: Geography(
        region=Region.IV,
        province=Province.CHOAPA,
        commune=Commune.ILLAPEL,
    ),
    Commune.LOS_VILOS: Geography(
        region=Region.IV,
        province=Province.CHOAPA,
        commune=Commune.LOS_VILOS,
    ),
    Commune.SALAMANCA: Geography(
        region=Region.IV,
        province=Province.CHOAPA,
        commune=Commune.SALAMANCA,
    ),
    Commune.COQUIMBO: Geography(
        region=Region.IV,
        province=Province.ELQUI,
        commune=Commune.COQUIMBO,
    ),
    Commune.ANDACOLLO: Geography(
        region=Region.IV,
        province=Province.ELQUI,
        commune=Commune.ANDACOLLO,
    ),
    Commune.LA_HIGUERA: Geography(
        region=Region.IV,
        province=Province.ELQUI,
        commune=Commune.LA_HIGUERA,
    ),
    Commune.LA_SERENA: Geography(
        region=Region.IV,
        province=Province.ELQUI,
        commune=Commune.LA_SERENA,
    ),
    Commune.PAIHUANO: Geography(
        region=Region.IV,
        province=Province.ELQUI,
        commune=Commune.PAIHUANO,
    ),
    Commune.VICUÑA: Geography(
        region=Region.IV,
        province=Province.ELQUI,
        commune=Commune.VICUÑA,
    ),
    Commune.COMBARBALA: Geography(
        region=Region.IV,
        province=Province.LIMARI,
        commune=Commune.COMBARBALA,
    ),
    Commune.MONTE_PATRIA: Geography(
        region=Region.IV,
        province=Province.LIMARI,
        commune=Commune.MONTE_PATRIA,
    ),
    Commune.OVALLE: Geography(
        region=Region.IV,
        province=Province.LIMARI,
        commune=Commune.OVALLE,
    ),
    Commune.PUNITAQUI: Geography(
        region=Region.IV,
        province=Province.LIMARI,
        commune=Commune.PUNITAQUI,
    ),
    Commune.RIO_HURTADO: Geography(
        region=Region.IV,
        province=Province.LIMARI,
        commune=Commune.RIO_HURTADO,
    ),
    # V : Región de Valparaíso
    Commune.ISLA_DE_PASCUA: Geography(
        region=Region.V,
        province=Province.ISLA_DE_PASCUA,
        commune=Commune.ISLA_DE_PASCUA,
    ),
    Commune.CALLE_LARGA: Geography(
        region=Region.V,
        province=Province.LOS_ANDES,
        commune=Commune.CALLE_LARGA,
    ),
    Commune.LOS_ANDES: Geography(
        region=Region.V,
        province=Province.LOS_ANDES,
        commune=Commune.LOS_ANDES,
    ),
    Commune.RINCONADA: Geography(
        region=Region.V,
        province=Province.LOS_ANDES,
        commune=Commune.RINCONADA,
    ),
    Commune.SAN_ESTEBAN: Geography(
        region=Region.V,
        province=Province.LOS_ANDES,
        commune=Commune.SAN_ESTEBAN,
    ),
    Commune.LIMACHE: Geography(
        region=Region.V,
        province=Province.MARGA_MARGA,
        commune=Commune.LIMACHE,
    ),
    Commune.OLMUE: Geography(
        region=Region.V,
        province=Province.MARGA_MARGA,
        commune=Commune.OLMUE,
    ),
    Commune.QUILPUE: Geography(
        region=Region.V,
        province=Province.MARGA_MARGA,
        commune=Commune.QUILPUE,
    ),
    Commune.VILLA_ALEMANA: Geography(
        region=Region.V,
        province=Province.MARGA_MARGA,
        commune=Commune.VILLA_ALEMANA,
    ),
    Commune.CABILDO: Geography(
        region=Region.V,
        province=Province.PETORCA,
        commune=Commune.CABILDO,
    ),
    Commune.LA_LIGUA: Geography(
        region=Region.V,
        province=Province.PETORCA,
        commune=Commune.LA_LIGUA,
    ),
    Commune.PAPUDO: Geography(
        region=Region.V,
        province=Province.PETORCA,
        commune=Commune.PAPUDO,
    ),
    Commune.PETORCA: Geography(
        region=Region.V,
        province=Province.PETORCA,
        commune=Commune.PETORCA,
    ),
    Commune.ZAPALLAR: Geography(
        region=Region.V,
        province=Province.PETORCA,
        commune=Commune.ZAPALLAR,
    ),
    Commune.HIJUELAS: Geography(
        region=Region.V,
        province=Province.QUILLOTA,
        commune=Commune.HIJUELAS,
    ),
    Commune.LA_CALERA: Geography(
        region=Region.V,
        province=Province.QUILLOTA,
        commune=Commune.LA_CALERA,
    ),
    Commune.LA_CRUZ: Geography(
        region=Region.V,
        province=Province.QUILLOTA,
        commune=Commune.LA_CRUZ,
    ),
    Commune.NOGALES: Geography(
        region=Region.V,
        province=Province.QUILLOTA,
        commune=Commune.NOGALES,
    ),
    Commune.QUILLOTA: Geography(
        region=Region.V,
        province=Province.QUILLOTA,
        commune=Commune.QUILLOTA,
    ),
    Commune.ALGARROBO: Geography(
        region=Region.V,
        province=Province.SAN_ANTONIO,
        commune=Commune.ALGARROBO,
    ),
    Commune.CARTAGENA: Geography(
        region=Region.V,
        province=Province.SAN_ANTONIO,
        commune=Commune.CARTAGENA,
    ),
    Commune.EL_QUISCO: Geography(
        region=Region.V,
        province=Province.SAN_ANTONIO,
        commune=Commune.EL_QUISCO,
    ),
    Commune.EL_TABO: Geography(
        region=Region.V,
        province=Province.SAN_ANTONIO,
        commune=Commune.EL_TABO,
    ),
    Commune.SAN_ANTONIO: Geography(
        region=Region.V,
        province=Province.SAN_ANTONIO,
        commune=Commune.SAN_ANTONIO,
    ),
    Commune.SANTO_DOMINGO: Geography(
        region=Region.V,
        province=Province.SAN_ANTONIO,
        commune=Commune.SANTO_DOMINGO,
    ),
    Commune.SAN_FELIPE: Geography(
        region=Region.V,
        province=Province.SAN_FELIPE_DE_ACONCAGUA,
        commune=Commune.SAN_FELIPE,
    ),
    Commune.CATEMU: Geography(
        region=Region.V,
        province=Province.SAN_FELIPE_DE_ACONCAGUA,
        commune=Commune.CATEMU,
    ),
    Commune.LLAYLLAY: Geography(
        region=Region.V,
        province=Province.SAN_FELIPE_DE_ACONCAGUA,
        commune=Commune.LLAYLLAY,
    ),
    Commune.PANQUEHUE: Geography(
        region=Region.V,
        province=Province.SAN_FELIPE_DE_ACONCAGUA,
        commune=Commune.PANQUEHUE,
    ),
    Commune.PUTAENDO: Geography(
        region=Region.V,
        province=Province.SAN_FELIPE_DE_ACONCAGUA,
        commune=Commune.PUTAENDO,
    ),
    Commune.SANTA_MARIA: Geography(
        region=Region.V,
        province=Province.SAN_FELIPE_DE_ACONCAGUA,
        commune=Commune.SANTA_MARIA,
    ),
    Commune.CASABLANCA: Geography(
        region=Region.V,
        province=Province.VALPARAISO,
        commune=Commune.CASABLANCA,
    ),
    Commune.CONCON: Geography(
        region=Region.V,
        province=Province.VALPARAISO,
        commune=Commune.CONCON,
    ),
    Commune.JUAN_FERNANDEZ: Geography(
        region=Region.V,
        province=Province.VALPARAISO,
        commune=Commune.JUAN_FERNANDEZ,
    ),
    Commune.PUCHUNCAVI: Geography(
        region=Region.V,
        province=Province.VALPARAISO,
        commune=Commune.PUCHUNCAVI,
    ),
    Commune.QUINTERO: Geography(
        region=Region.V,
        province=Province.VALPARAISO,
        commune=Commune.QUINTERO,
    ),
    Commune.VALPARAISO: Geography(
        region=Region.V,
        province=Province.VALPARAISO,
        commune=Commune.VALPARAISO,
    ),
    Commune.VIÑA_DEL_MAR: Geography(
        region=Region.V,
        province=Province.VALPARAISO,
        commune=Commune.VIÑA_DEL_MAR,
    ),
    # VI: Región del Libertador General Bernardo O'Higgins
    Commune.CODEGUA: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.CODEGUA,
    ),
    Commune.COINCO: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.COINCO,
    ),
    Commune.COLTAUCO: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.COLTAUCO,
    ),
    Commune.DOÑIHUE: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.DOÑIHUE,
    ),
    Commune.GRANEROS: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.GRANEROS,
    ),
    Commune.LAS_CABRAS: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.LAS_CABRAS,
    ),
    Commune.MACHALI: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.MACHALI,
    ),
    Commune.MALLOA: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.MALLOA,
    ),
    Commune.OLIVAR: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.OLIVAR,
    ),
    Commune.PEUMO: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.PEUMO,
    ),
    Commune.PICHIDEGUA: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.PICHIDEGUA,
    ),
    Commune.QUINTA_DE_TILCOCO: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.QUINTA_DE_TILCOCO,
    ),
    Commune.RANCAGUA: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.RANCAGUA,
    ),
    Commune.REQUINOA: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.REQUINOA,
    ),
    Commune.RENGO: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.RENGO,
    ),
    Commune.SAN_FRANCISCO_DE_MOSTAZAL: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.SAN_FRANCISCO_DE_MOSTAZAL,
    ),
    Commune.SAN_VICENTE_DE_TAGUA_TAGUA: Geography(
        region=Region.VI,
        province=Province.CACHAPOAL,
        commune=Commune.SAN_VICENTE_DE_TAGUA_TAGUA,
    ),
    Commune.LA_ESTRELLA: Geography(
        region=Region.VI,
        province=Province.CARDENAL_CARO,
        commune=Commune.LA_ESTRELLA,
    ),
    Commune.LITUECHE: Geography(
        region=Region.VI,
        province=Province.CARDENAL_CARO,
        commune=Commune.LITUECHE,
    ),
    Commune.MARCHIGUE: Geography(
        region=Region.VI,
        province=Province.CARDENAL_CARO,
        commune=Commune.MARCHIGUE,
    ),
    Commune.NAVIDAD: Geography(
        region=Region.VI,
        province=Province.CARDENAL_CARO,
        commune=Commune.NAVIDAD,
    ),
    Commune.PAREDONES: Geography(
        region=Region.VI,
        province=Province.CARDENAL_CARO,
        commune=Commune.PAREDONES,
    ),
    Commune.PICHILEMU: Geography(
        region=Region.VI,
        province=Province.CARDENAL_CARO,
        commune=Commune.PICHILEMU,
    ),
    Commune.CHEPICA: Geography(
        region=Region.VI,
        province=Province.COLCHAGUA,
        commune=Commune.CHEPICA,
    ),
    Commune.CHIMBARONGO: Geography(
        region=Region.VI,
        province=Province.COLCHAGUA,
        commune=Commune.CHIMBARONGO,
    ),
    Commune.LOLOL: Geography(
        region=Region.VI,
        province=Province.COLCHAGUA,
        commune=Commune.LOLOL,
    ),
    Commune.NANCAGUA: Geography(
        region=Region.VI,
        province=Province.COLCHAGUA,
        commune=Commune.NANCAGUA,
    ),
    Commune.PALMILLA: Geography(
        region=Region.VI,
        province=Province.COLCHAGUA,
        commune=Commune.PALMILLA,
    ),
    Commune.PERALILLO: Geography(
        region=Region.VI,
        province=Province.COLCHAGUA,
        commune=Commune.PERALILLO,
    ),
    Commune.PLACILLA: Geography(
        region=Region.VI,
        province=Province.COLCHAGUA,
        commune=Commune.PLACILLA,
    ),
    Commune.PUMANQUE: Geography(
        region=Region.VI,
        province=Province.COLCHAGUA,
        commune=Commune.PUMANQUE,
    ),
    Commune.SAN_FERNANDO: Geography(
        region=Region.VI,
        province=Province.COLCHAGUA,
        commune=Commune.SAN_FERNANDO,
    ),
    Commune.SANTA_CRUZ: Geography(
        region=Region.VI,
        province=Province.COLCHAGUA,
        commune=Commune.SANTA_CRUZ,
    ),
    # VII: Región del Maule
    # Province de Cauquenes
    Commune.CAUQUENES: Geography(
        region=Region.VII,
        province=Province.CAUQUENES,
        commune=Commune.CAUQUENES,
    ),
    Commune.CHANCO: Geography(
        region=Region.VII,
        province=Province.CAUQUENES,
        commune=Commune.CHANCO,
    ),
    Commune.PELLUHUE: Geography(
        region=Region.VII,
        province=Province.CAUQUENES,
        commune=Commune.PELLUHUE,
    ),
    # Province de Curico
    Commune.CURICO: Geography(
        region=Region.VII,
        province=Province.CURICO,
        commune=Commune.CURICO,
    ),
    Commune.HUALAÑE: Geography(
        region=Region.VII,
        province=Province.CURICO,
        commune=Commune.HUALAÑE,
    ),
    Commune.LICANTEN: Geography(
        region=Region.VII,
        province=Province.CURICO,
        commune=Commune.LICANTEN,
    ),
    Commune.MOLINA: Geography(
        region=Region.VII,
        province=Province.CURICO,
        commune=Commune.MOLINA,
    ),
    Commune.RAUCO: Geography(
        region=Region.VII,
        province=Province.CURICO,
        commune=Commune.RAUCO,
    ),
    Commune.ROMERAL: Geography(
        region=Region.VII,
        province=Province.CURICO,
        commune=Commune.ROMERAL,
    ),
    Commune.SAGRADA_FAMILIA: Geography(
        region=Region.VII,
        province=Province.CURICO,
        commune=Commune.SAGRADA_FAMILIA,
    ),
    Commune.TENO: Geography(
        region=Region.VII,
        province=Province.CURICO,
        commune=Commune.TENO,
    ),
    Commune.VICHUQUEN: Geography(
        region=Region.VII,
        province=Province.CURICO,
        commune=Commune.VICHUQUEN,
    ),
    # Province de Linares
    Commune.COLBUN: Geography(
        region=Region.VII,
        province=Province.LINARES,
        commune=Commune.COLBUN,
    ),
    Commune.LINARES: Geography(
        region=Region.VII,
        province=Province.LINARES,
        commune=Commune.LINARES,
    ),
    Commune.LONGAVI: Geography(
        region=Region.VII,
        province=Province.LINARES,
        commune=Commune.LONGAVI,
    ),
    Commune.PARRAL: Geography(
        region=Region.VII,
        province=Province.LINARES,
        commune=Commune.PARRAL,
    ),
    Commune.RETIRO: Geography(
        region=Region.VII,
        province=Province.LINARES,
        commune=Commune.RETIRO,
    ),
    Commune.SAN_JAVIER: Geography(
        region=Region.VII,
        province=Province.LINARES,
        commune=Commune.SAN_JAVIER,
    ),
    Commune.VILLA_ALEGRE: Geography(
        region=Region.VII,
        province=Province.LINARES,
        commune=Commune.VILLA_ALEGRE,
    ),
    Commune.YERBAS_BUENAS: Geography(
        region=Region.VII,
        province=Province.LINARES,
        commune=Commune.YERBAS_BUENAS,
    ),
    # Province de Talca
    Commune.CONSTITUCION: Geography(
        region=Region.VII,
        province=Province.TALCA,
        commune=Commune.CONSTITUCION,
    ),
    Commune.CUREPTO: Geography(
        region=Region.VII,
        province=Province.TALCA,
        commune=Commune.CUREPTO,
    ),
    Commune.EMPEDRADO: Geography(
        region=Region.VII,
        province=Province.TALCA,
        commune=Commune.EMPEDRADO,
    ),
    Commune.MAULE: Geography(
        region=Region.VII,
        province=Province.TALCA,
        commune=Commune.MAULE,
    ),
    Commune.PELARCO: Geography(
        region=Region.VII,
        province=Province.TALCA,
        commune=Commune.PELARCO,
    ),
    Commune.PENCAHUE: Geography(
        region=Region.VII,
        province=Province.TALCA,
        commune=Commune.PENCAHUE,
    ),
    Commune.RIO_CLARO: Geography(
        region=Region.VII,
        province=Province.TALCA,
        commune=Commune.RIO_CLARO,
    ),
    Commune.SAN_CLEMENTE: Geography(
        region=Region.VII,
        province=Province.TALCA,
        commune=Commune.SAN_CLEMENTE,
    ),
    Commune.SAN_RAFAEL: Geography(
        region=Region.VII,
        province=Province.TALCA,
        commune=Commune.SAN_RAFAEL,
    ),
    Commune.TALCA: Geography(
        region=Region.VII,
        province=Province.TALCA,
        commune=Commune.TALCA,
    ),
    # XVI: Región de Ñuble
    # Province de Diguillín
    Commune.BULNES: Geography(
        region=Region.XVI,
        province=Province.DIGUILLIN,
        commune=Commune.BULNES,
    ),
    Commune.CHILLAN: Geography(
        region=Region.XVI,
        province=Province.DIGUILLIN,
        commune=Commune.CHILLAN,
    ),
    Commune.CHILLAN_VIEJO: Geography(
        region=Region.XVI,
        province=Province.DIGUILLIN,
        commune=Commune.CHILLAN_VIEJO,
    ),
    Commune.EL_CARMEN: Geography(
        region=Region.XVI,
        province=Province.DIGUILLIN,
        commune=Commune.EL_CARMEN,
    ),
    Commune.PEMUCO: Geography(
        region=Region.XVI,
        province=Province.DIGUILLIN,
        commune=Commune.PEMUCO,
    ),
    Commune.PINTO: Geography(
        region=Region.XVI,
        province=Province.DIGUILLIN,
        commune=Commune.PINTO,
    ),
    Commune.QUILLON: Geography(
        region=Region.XVI,
        province=Province.DIGUILLIN,
        commune=Commune.QUILLON,
    ),
    Commune.SAN_IGNACIO: Geography(
        region=Region.XVI,
        province=Province.DIGUILLIN,
        commune=Commune.SAN_IGNACIO,
    ),
    Commune.YUNGAY: Geography(
        region=Region.XVI,
        province=Province.DIGUILLIN,
        commune=Commune.YUNGAY,
    ),
    # Province de Itata
    Commune.COBQUECURA: Geography(
        region=Region.XVI,
        province=Province.ITATA,
        commune=Commune.COBQUECURA,
    ),
    Commune.COELEMU: Geography(
        region=Region.XVI,
        province=Province.ITATA,
        commune=Commune.COELEMU,
    ),
    Commune.NINHUE: Geography(
        region=Region.XVI,
        province=Province.ITATA,
        commune=Commune.NINHUE,
    ),
    Commune.PORTEZUELO: Geography(
        region=Region.XVI,
        province=Province.ITATA,
        commune=Commune.PORTEZUELO,
    ),
    Commune.QUIRIHUE: Geography(
        region=Region.XVI,
        province=Province.ITATA,
        commune=Commune.QUIRIHUE,
    ),
    Commune.RANQUIL: Geography(
        region=Region.XVI,
        province=Province.ITATA,
        commune=Commune.RANQUIL,
    ),
    Commune.TREHUACO: Geography(
        region=Region.XVI,
        province=Province.ITATA,
        commune=Commune.TREHUACO,
    ),
    # Province de Punilla
    Commune.COIHUECO: Geography(
        region=Region.XVI,
        province=Province.PUNILLA,
        commune=Commune.COIHUECO,
    ),
    Commune.ÑIQUEN: Geography(
        region=Region.XVI,
        province=Province.PUNILLA,
        commune=Commune.ÑIQUEN,
    ),
    Commune.SAN_CARLOS: Geography(
        region=Region.XVI,
        province=Province.PUNILLA,
        commune=Commune.SAN_CARLOS,
    ),
    Commune.SAN_FABIAN: Geography(
        region=Region.XVI,
        province=Province.PUNILLA,
        commune=Commune.SAN_FABIAN,
    ),
    Commune.SAN_NICOLAS: Geography(
        region=Region.XVI,
        province=Province.PUNILLA,
        commune=Commune.SAN_NICOLAS,
    ),
    # VIII: Región del Biobío
    # Province de Arauco
    Commune.ARAUCO: Geography(
        region=Region.VIII,
        province=Province.ARAUCO,
        commune=Commune.ARAUCO,
    ),
    Commune.CAÑETE: Geography(
        region=Region.VIII,
        province=Province.ARAUCO,
        commune=Commune.CAÑETE,
    ),
    Commune.CONTULMO: Geography(
        region=Region.VIII,
        province=Province.ARAUCO,
        commune=Commune.CONTULMO,
    ),
    Commune.CURANILAHUE: Geography(
        region=Region.VIII,
        province=Province.ARAUCO,
        commune=Commune.CURANILAHUE,
    ),
    Commune.LEBU: Geography(
        region=Region.VIII,
        province=Province.ARAUCO,
        commune=Commune.LEBU,
    ),
    Commune.LOS_ALAMOS: Geography(
        region=Region.VIII,
        province=Province.ARAUCO,
        commune=Commune.LOS_ALAMOS,
    ),
    Commune.TIRUA: Geography(
        region=Region.VIII,
        province=Province.ARAUCO,
        commune=Commune.TIRUA,
    ),
    # Province de Biobío
    Commune.ALTO_BIO_BIO: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.ALTO_BIO_BIO,
    ),
    Commune.ANTUCO: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.ANTUCO,
    ),
    Commune.CABRERO: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.CABRERO,
    ),
    Commune.LAJA: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.LAJA,
    ),
    Commune.LOS_ANGELES: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.LOS_ANGELES,
    ),
    Commune.MULCHEN: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.MULCHEN,
    ),
    Commune.NACIMIENTO: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.NACIMIENTO,
    ),
    Commune.NEGRETE: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.NEGRETE,
    ),
    Commune.QUILACO: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.QUILACO,
    ),
    Commune.QUILLECO: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.QUILLECO,
    ),
    Commune.SAN_ROSENDO: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.SAN_ROSENDO,
    ),
    Commune.SANTA_BARBARA: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.SANTA_BARBARA,
    ),
    Commune.TUCAPEL: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.TUCAPEL,
    ),
    Commune.YUMBEL: Geography(
        region=Region.VIII,
        province=Province.BIOBIO,
        commune=Commune.YUMBEL,
    ),
    # Province de Concepción
    Commune.CHIGUAYANTE: Geography(
        region=Region.VIII,
        province=Province.CONCEPCION,
        commune=Commune.CHIGUAYANTE,
    ),
    Commune.CONCEPCION: Geography(
        region=Region.VIII,
        province=Province.CONCEPCION,
        commune=Commune.CONCEPCION,
    ),
    Commune.CORONEL: Geography(
        region=Region.VIII,
        province=Province.CONCEPCION,
        commune=Commune.CORONEL,
    ),
    Commune.FLORIDA: Geography(
        region=Region.VIII,
        province=Province.CONCEPCION,
        commune=Commune.FLORIDA,
    ),
    Commune.HUALPEN: Geography(
        region=Region.VIII,
        province=Province.CONCEPCION,
        commune=Commune.HUALPEN,
    ),
    Commune.HUALQUI: Geography(
        region=Region.VIII,
        province=Province.CONCEPCION,
        commune=Commune.HUALQUI,
    ),
    Commune.LOTA: Geography(
        region=Region.VIII,
        province=Province.CONCEPCION,
        commune=Commune.LOTA,
    ),
    Commune.PENCO: Geography(
        region=Region.VIII,
        province=Province.CONCEPCION,
        commune=Commune.PENCO,
    ),
    Commune.SAN_PEDRO_DE_LA_PAZ: Geography(
        region=Region.VIII,
        province=Province.CONCEPCION,
        commune=Commune.SAN_PEDRO_DE_LA_PAZ,
    ),
    Commune.SANTA_JUANA: Geography(
        region=Region.VIII,
        province=Province.CONCEPCION,
        commune=Commune.SANTA_JUANA,
    ),
    Commune.TALCAHUANO: Geography(
        region=Region.VIII,
        province=Province.CONCEPCION,
        commune=Commune.TALCAHUANO,
    ),
    Commune.TOME: Geography(
        region=Region.VIII,
        province=Province.CONCEPCION,
        commune=Commune.TOME,
    ),
    # IX: Región de la Araucanía
    # Province de Cautín
    Commune.CARAHUE: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.CARAHUE,
    ),
    Commune.CHOL_CHOL: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.CHOL_CHOL,
    ),
    Commune.CUNCO: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.CUNCO,
    ),
    Commune.CURARREHUE: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.CURARREHUE,
    ),
    Commune.FREIRE: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.FREIRE,
    ),
    Commune.GALVARINO: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.GALVARINO,
    ),
    Commune.GORBEA: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.GORBEA,
    ),
    Commune.LAUTARO: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.LAUTARO,
    ),
    Commune.LONCOCHE: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.LONCOCHE,
    ),
    Commune.MELIPEUCO: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.MELIPEUCO,
    ),
    Commune.NUEVA_IMPERIAL: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.NUEVA_IMPERIAL,
    ),
    Commune.PADRE_LAS_CASAS: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.PADRE_LAS_CASAS,
    ),
    Commune.PERQUENCO: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.PERQUENCO,
    ),
    Commune.PITRUFQUEN: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.PITRUFQUEN,
    ),
    Commune.PUCON: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.PUCON,
    ),
    Commune.PUERTO_SAAVEDRA: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.PUERTO_SAAVEDRA,
    ),
    Commune.TEMUCO: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.TEMUCO,
    ),
    Commune.TEODORO_SCHMIDT: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.TEODORO_SCHMIDT,
    ),
    Commune.TOLTEN: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.TOLTEN,
    ),
    Commune.VILCUN: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.VILCUN,
    ),
    Commune.VILLARRICA: Geography(
        region=Region.IX,
        province=Province.CAUTIN,
        commune=Commune.VILLARRICA,
    ),
    # Province de Malleco
    Commune.ANGOL: Geography(
        region=Region.IX,
        province=Province.MALLECO,
        commune=Commune.ANGOL,
    ),
    Commune.COLLIPULLI: Geography(
        region=Region.IX,
        province=Province.MALLECO,
        commune=Commune.COLLIPULLI,
    ),
    Commune.CURACAUTIN: Geography(
        region=Region.IX,
        province=Province.MALLECO,
        commune=Commune.CURACAUTIN,
    ),
    Commune.ERCILLA: Geography(
        region=Region.IX,
        province=Province.MALLECO,
        commune=Commune.ERCILLA,
    ),
    Commune.LONQUIMAY: Geography(
        region=Region.IX,
        province=Province.MALLECO,
        commune=Commune.LONQUIMAY,
    ),
    Commune.LOS_SAUCES: Geography(
        region=Region.IX,
        province=Province.MALLECO,
        commune=Commune.LOS_SAUCES,
    ),
    Commune.LUMACO: Geography(
        region=Region.IX,
        province=Province.MALLECO,
        commune=Commune.LUMACO,
    ),
    Commune.PUREN: Geography(
        region=Region.IX,
        province=Province.MALLECO,
        commune=Commune.PUREN,
    ),
    Commune.RENAICO: Geography(
        region=Region.IX,
        province=Province.MALLECO,
        commune=Commune.RENAICO,
    ),
    Commune.TRAIGUEN: Geography(
        region=Region.IX,
        province=Province.MALLECO,
        commune=Commune.TRAIGUEN,
    ),
    Commune.VICTORIA: Geography(
        region=Region.IX,
        province=Province.MALLECO,
        commune=Commune.VICTORIA,
    ),
    # XIV: Región de Los Ríos
    # Province del Ranco
    Commune.FUTRONO: Geography(
        region=Region.XIV,
        province=Province.RANCO,
        commune=Commune.FUTRONO,
    ),
    Commune.LA_UNION: Geography(
        region=Region.XIV,
        province=Province.RANCO,
        commune=Commune.LA_UNION,
    ),
    Commune.LAGO_RANCO: Geography(
        region=Region.XIV,
        province=Province.RANCO,
        commune=Commune.LAGO_RANCO,
    ),
    Commune.RIO_BUENO: Geography(
        region=Region.XIV,
        province=Province.RANCO,
        commune=Commune.RIO_BUENO,
    ),
    # Province de Valdivia
    Commune.CORRAL: Geography(
        region=Region.XIV,
        province=Province.VALDIVIA,
        commune=Commune.CORRAL,
    ),
    Commune.LANCO: Geography(
        region=Region.XIV,
        province=Province.VALDIVIA,
        commune=Commune.LANCO,
    ),
    Commune.LOS_LAGOS: Geography(
        region=Region.XIV,
        province=Province.VALDIVIA,
        commune=Commune.LOS_LAGOS,
    ),
    Commune.MAFIL: Geography(
        region=Region.XIV,
        province=Province.VALDIVIA,
        commune=Commune.MAFIL,
    ),
    Commune.MARIQUINA: Geography(
        region=Region.XIV,
        province=Province.VALDIVIA,
        commune=Commune.MARIQUINA,
    ),
    Commune.PAILLACO: Geography(
        region=Region.XIV,
        province=Province.VALDIVIA,
        commune=Commune.PAILLACO,
    ),
    Commune.PANGUIPULLI: Geography(
        region=Region.XIV,
        province=Province.VALDIVIA,
        commune=Commune.PANGUIPULLI,
    ),
    Commune.VALDIVIA: Geography(
        region=Region.XIV,
        province=Province.VALDIVIA,
        commune=Commune.VALDIVIA,
    ),
    # X: Región de Los Lagos
    # Province de Chiloé
    Commune.ANCUD: Geography(
        region=Region.X,
        province=Province.CHILOE,
        commune=Commune.ANCUD,
    ),
    Commune.CASTRO: Geography(
        region=Region.X,
        province=Province.CHILOE,
        commune=Commune.CASTRO,
    ),
    Commune.CHONCHI: Geography(
        region=Region.X,
        province=Province.CHILOE,
        commune=Commune.CHONCHI,
    ),
    Commune.CURACO_DE_VELEZ: Geography(
        region=Region.X,
        province=Province.CHILOE,
        commune=Commune.CURACO_DE_VELEZ,
    ),
    Commune.DALCAHUE: Geography(
        region=Region.X,
        province=Province.CHILOE,
        commune=Commune.DALCAHUE,
    ),
    Commune.PUQUELDON: Geography(
        region=Region.X,
        province=Province.CHILOE,
        commune=Commune.PUQUELDON,
    ),
    Commune.QUEILEN: Geography(
        region=Region.X,
        province=Province.CHILOE,
        commune=Commune.QUEILEN,
    ),
    Commune.QUELLON: Geography(
        region=Region.X,
        province=Province.CHILOE,
        commune=Commune.QUELLON,
    ),
    Commune.QUEMCHI: Geography(
        region=Region.X,
        province=Province.CHILOE,
        commune=Commune.QUEMCHI,
    ),
    Commune.QUINCHAO: Geography(
        region=Region.X,
        province=Province.CHILOE,
        commune=Commune.QUINCHAO,
    ),
    # Province de Llanquihue
    Commune.CALBUCO: Geography(
        region=Region.X,
        province=Province.LLANQUIHUE,
        commune=Commune.CALBUCO,
    ),
    Commune.COCHAMO: Geography(
        region=Region.X,
        province=Province.LLANQUIHUE,
        commune=Commune.COCHAMO,
    ),
    Commune.FRESIA: Geography(
        region=Region.X,
        province=Province.LLANQUIHUE,
        commune=Commune.FRESIA,
    ),
    Commune.FRUTILLAR: Geography(
        region=Region.X,
        province=Province.LLANQUIHUE,
        commune=Commune.FRUTILLAR,
    ),
    Commune.LLANQUIHUE: Geography(
        region=Region.X,
        province=Province.LLANQUIHUE,
        commune=Commune.LLANQUIHUE,
    ),
    Commune.LOS_MUERMOS: Geography(
        region=Region.X,
        province=Province.LLANQUIHUE,
        commune=Commune.LOS_MUERMOS,
    ),
    Commune.MAULLIN: Geography(
        region=Region.X,
        province=Province.LLANQUIHUE,
        commune=Commune.MAULLIN,
    ),
    Commune.PUERTO_MONTT: Geography(
        region=Region.X,
        province=Province.LLANQUIHUE,
        commune=Commune.PUERTO_MONTT,
    ),
    Commune.PUERTO_VARAS: Geography(
        region=Region.X,
        province=Province.LLANQUIHUE,
        commune=Commune.PUERTO_VARAS,
    ),
    # Province de Osorno
    Commune.OSORNO: Geography(
        region=Region.X,
        province=Province.OSORNO,
        commune=Commune.OSORNO,
    ),
    Commune.PUERTO_OCTAY: Geography(
        region=Region.X,
        province=Province.OSORNO,
        commune=Commune.PUERTO_OCTAY,
    ),
    Commune.PURRANQUE: Geography(
        region=Region.X,
        province=Province.OSORNO,
        commune=Commune.PURRANQUE,
    ),
    Commune.PUYEHUE: Geography(
        region=Region.X,
        province=Province.OSORNO,
        commune=Commune.PUYEHUE,
    ),
    Commune.RIO_NEGRO: Geography(
        region=Region.X,
        province=Province.OSORNO,
        commune=Commune.RIO_NEGRO,
    ),
    Commune.SAN_PABLO: Geography(
        region=Region.X,
        province=Province.OSORNO,
        commune=Commune.SAN_PABLO,
    ),
    Commune.SAN_JUAN_DE_LA_COSTA: Geography(
        region=Region.X,
        province=Province.OSORNO,
        commune=Commune.SAN_JUAN_DE_LA_COSTA,
    ),
    # Province de Palena
    Commune.CHAITEN: Geography(
        region=Region.X,
        province=Province.PALENA,
        commune=Commune.CHAITEN,
    ),
    Commune.FUTALEUFU: Geography(
        region=Region.X,
        province=Province.PALENA,
        commune=Commune.FUTALEUFU,
    ),
    Commune.HUALAIHUE: Geography(
        region=Region.X,
        province=Province.PALENA,
        commune=Commune.HUALAIHUE,
    ),
    Commune.PALENA: Geography(
        region=Region.X,
        province=Province.PALENA,
        commune=Commune.PALENA,
    ),
    # XI: Región Aysén del General Carlos Ibáñez del Campo
    # Province de Aysén
    Commune.AYSEN: Geography(
        region=Region.XI,
        province=Province.AYSEN,
        commune=Commune.AYSEN,
    ),
    Commune.CISNES: Geography(
        region=Region.XI,
        province=Province.AYSEN,
        commune=Commune.CISNES,
    ),
    Commune.LAS_GUAITECAS: Geography(
        region=Region.XI,
        province=Province.AYSEN,
        commune=Commune.LAS_GUAITECAS,
    ),
    # Province de Capitán Prat
    Commune.COCHRANE: Geography(
        region=Region.XI,
        province=Province.CAPITAN_PRAT,
        commune=Commune.COCHRANE,
    ),
    Commune.O_HIGGINS: Geography(
        region=Region.XI,
        province=Province.CAPITAN_PRAT,
        commune=Commune.O_HIGGINS,
    ),
    Commune.TORTEL: Geography(
        region=Region.XI,
        province=Province.CAPITAN_PRAT,
        commune=Commune.TORTEL,
    ),
    # Province de Coyhaique
    Commune.COYHAIQUE: Geography(
        region=Region.XI,
        province=Province.COYHAIQUE,
        commune=Commune.COYHAIQUE,
    ),
    Commune.LAGO_VERDE: Geography(
        region=Region.XI,
        province=Province.COYHAIQUE,
        commune=Commune.LAGO_VERDE,
    ),
    # Province de General Carrera
    Commune.CHILE_CHICO: Geography(
        region=Region.XI,
        province=Province.GENERAL_CARRERA,
        commune=Commune.CHILE_CHICO,
    ),
    Commune.RIO_IBAÑEZ: Geography(
        region=Region.XI,
        province=Province.GENERAL_CARRERA,
        commune=Commune.RIO_IBAÑEZ,
    ),
    # XII: Región de Magallanes y de la Antártica Chilena
    # Province de Antártica Chilena
    Commune.ANTARTICA: Geography(
        region=Region.XII,
        province=Province.ANTARTICA_CHILENA,
        commune=Commune.ANTARTICA,
    ),
    Commune.CABO_DE_HORNOS: Geography(
        region=Region.XII,
        province=Province.ANTARTICA_CHILENA,
        commune=Commune.CABO_DE_HORNOS,
    ),
    # Province de Magallanes
    Commune.LAGUNA_BLANCA: Geography(
        region=Region.XII,
        province=Province.MAGALLANES,
        commune=Commune.LAGUNA_BLANCA,
    ),
    Commune.PUNTA_ARENAS: Geography(
        region=Region.XII,
        province=Province.MAGALLANES,
        commune=Commune.PUNTA_ARENAS,
    ),
    Commune.RIO_VERDE: Geography(
        region=Region.XII,
        province=Province.MAGALLANES,
        commune=Commune.RIO_VERDE,
    ),
    Commune.SAN_GREGORIO: Geography(
        region=Region.XII,
        province=Province.MAGALLANES,
        commune=Commune.SAN_GREGORIO,
    ),
    # Province de Tierra del Fuego
    Commune.PORVENIR: Geography(
        region=Region.XII,
        province=Province.TIERRA_DEL_FUEGO,
        commune=Commune.PORVENIR,
    ),
    Commune.PRIMAVERA: Geography(
        region=Region.XII,
        province=Province.TIERRA_DEL_FUEGO,
        commune=Commune.PRIMAVERA,
    ),
    Commune.TIMAUKEL: Geography(
        region=Region.XII,
        province=Province.TIERRA_DEL_FUEGO,
        commune=Commune.TIMAUKEL,
    ),
    # Province de Ultima Esperanza
    Commune.PUERTO_NATALES: Geography(
        region=Region.XII,
        province=Province.ULTIMA_ESPERANZA,
        commune=Commune.PUERTO_NATALES,
    ),
    Commune.TORRES_DEL_PAYNE: Geography(
        region=Region.XII,
        province=Province.ULTIMA_ESPERANZA,
        commune=Commune.TORRES_DEL_PAYNE,
    ),
    # RM: Región Metropolitana de Santiago
    # Province de Chacabuco
    Commune.COLINA: Geography(
        region=Region.RM,
        province=Province.CHACABUCO,
        commune=Commune.COLINA,
    ),
    Commune.LAMPA: Geography(
        region=Region.RM,
        province=Province.CHACABUCO,
        commune=Commune.LAMPA,
    ),
    Commune.TIL_TIL: Geography(
        region=Region.RM,
        province=Province.CHACABUCO,
        commune=Commune.TIL_TIL,
    ),
    # Province de Cordillera
    Commune.PIRQUE: Geography(
        region=Region.RM,
        province=Province.CORDILLERA,
        commune=Commune.PIRQUE,
    ),
    Commune.PUENTE_ALTO: Geography(
        region=Region.RM,
        province=Province.CORDILLERA,
        commune=Commune.PUENTE_ALTO,
    ),
    Commune.SAN_JOSE_DE_MAIPO: Geography(
        region=Region.RM,
        province=Province.CORDILLERA,
        commune=Commune.SAN_JOSE_DE_MAIPO,
    ),
    # Province de Maipo
    Commune.BUIN: Geography(
        region=Region.RM,
        province=Province.MAIPO,
        commune=Commune.BUIN,
    ),
    Commune.CALERA_DE_TANGO: Geography(
        region=Region.RM,
        province=Province.MAIPO,
        commune=Commune.CALERA_DE_TANGO,
    ),
    Commune.PAINE: Geography(
        region=Region.RM,
        province=Province.MAIPO,
        commune=Commune.PAINE,
    ),
    Commune.SAN_BERNARDO: Geography(
        region=Region.RM,
        province=Province.MAIPO,
        commune=Commune.SAN_BERNARDO,
    ),
    # Province de Melipilla
    Commune.ALHUE: Geography(
        region=Region.RM,
        province=Province.MELIPILLA,
        commune=Commune.ALHUE,
    ),
    Commune.CURACAVI: Geography(
        region=Region.RM,
        province=Province.MELIPILLA,
        commune=Commune.CURACAVI,
    ),
    Commune.MARIA_PINTO: Geography(
        region=Region.RM,
        province=Province.MELIPILLA,
        commune=Commune.MARIA_PINTO,
    ),
    Commune.MELIPILLA: Geography(
        region=Region.RM,
        province=Province.MELIPILLA,
        commune=Commune.MELIPILLA,
    ),
    Commune.SAN_PEDRO: Geography(
        region=Region.RM,
        province=Province.MELIPILLA,
        commune=Commune.SAN_PEDRO,
    ),
    # Province de Santiago
    Commune.CERRILLOS: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.CERRILLOS,
    ),
    Commune.CERRO_NAVIA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.CERRO_NAVIA,
    ),
    Commune.CONCHALI: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.CONCHALI,
    ),
    Commune.EL_BOSQUE: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.EL_BOSQUE,
    ),
    Commune.ESTACION_CENTRAL: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.ESTACION_CENTRAL,
    ),
    Commune.HUECHURABA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.HUECHURABA,
    ),
    Commune.INDEPENDENCIA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.INDEPENDENCIA,
    ),
    Commune.LA_CISTERNA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.LA_CISTERNA,
    ),
    Commune.LA_GRANJA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.LA_GRANJA,
    ),
    Commune.LA_FLORIDA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.LA_FLORIDA,
    ),
    Commune.LA_PINTANA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.LA_PINTANA,
    ),
    Commune.LA_REINA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.LA_REINA,
    ),
    Commune.LAS_CONDES: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.LAS_CONDES,
    ),
    Commune.LO_BARNECHEA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.LO_BARNECHEA,
    ),
    Commune.LO_ESPEJO: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.LO_ESPEJO,
    ),
    Commune.LO_PRADO: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.LO_PRADO,
    ),
    Commune.MACUL: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.MACUL,
    ),
    Commune.MAIPU: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.MAIPU,
    ),
    Commune.ÑUÑOA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.ÑUÑOA,
    ),
    Commune.PEDRO_AGUIRRE_CERDA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.PEDRO_AGUIRRE_CERDA,
    ),
    Commune.PEÑALOLEN: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.PEÑALOLEN,
    ),
    Commune.PROVIDENCIA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.PROVIDENCIA,
    ),
    Commune.PUDAHUEL: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.PUDAHUEL,
    ),
    Commune.QUILICURA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.QUILICURA,
    ),
    Commune.QUINTA_NORMAL: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.QUINTA_NORMAL,
    ),
    Commune.RECOLETA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.RECOLETA,
    ),
    Commune.RENCA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.RENCA,
    ),
    Commune.SAN_MIGUEL: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.SAN_MIGUEL,
    ),
    Commune.SAN_JOAQUIN: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.SAN_JOAQUIN,
    ),
    Commune.SAN_RAMON: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.SAN_RAMON,
    ),
    Commune.SANTIAGO: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.SANTIAGO,
    ),
    Commune.VITACURA: Geography(
        region=Region.RM,
        province=Province.SANTIAGO,
        commune=Commune.VITACURA,
    ),
    # Province de Talagante
    Commune.EL_MONTE: Geography(
        region=Region.RM,
        province=Province.TALAGANTE,
        commune=Commune.EL_MONTE,
    ),
    Commune.ISLA_DE_MAIPO: Geography(
        region=Region.RM,
        province=Province.TALAGANTE,
        commune=Commune.ISLA_DE_MAIPO,
    ),
    Commune.PADRE_HURTADO: Geography(
        region=Region.RM,
        province=Province.TALAGANTE,
        commune=Commune.PADRE_HURTADO,
    ),
    Commune.PEÑAFLOR: Geography(
        region=Region.RM,
        province=Province.TALAGANTE,
        commune=Commune.PEÑAFLOR,
    ),
    Commune.TALAGANTE: Geography(
        region=Region.RM,
        province=Province.TALAGANTE,
        commune=Commune.TALAGANTE,
    ),
}
