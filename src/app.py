import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc

import pandas as pd
from datetime import datetime

import plotly.graph_objects as go

# Cargar datos
df = pd.read_excel("BASE DATOS RG ALTURAS.xlsx", sheet_name="GENERAL")

# Limpieza de datos
def eliminar_columnas(df):
    df = df.drop(["uni",
                "SELECCIÓN POLIZA",
                "CURSO INTERNO RG ALTURAS",
                "#SEGUIMIENTO CERTIFICADO",
                "CONSTANCIA VOCACIONAL",
                "ID CURSO MINTRAB",
                "PRIMER NOMBRE",
                "SEGUNDO NOMBRE",
                "PRIMER APELLIDO",
                "SEGUNDO APELLIDO",
                "TIPO DE DOCUMENTO",
                "# DOCUMENTO",
                "TELEFONO",
                "ARL",
                "FECHA INSCRIPCION",
                "FECHA FIN CURSO",
                "CLIENTE DE",
                "APROBO",
                "CC",
                "EPS",
                "ARL2",
                "CER MED",
                "CAR EMP",
                "POL",
                "OBSERVACIONES"],
                axis=1
                )
    
    df = df.iloc[0:3888,:]
    #df = df.dropna()
    #df = df.count()

    return df

# Aplicar limpieza a df
df = eliminar_columnas(df)

'''
 Las siguientes tres variables designan un diccionario que reemplazará valores duplicados o repetidos, 
 o valores mal redactados.
'''

limpieza_nivel_educativo = {"BACHILLERATO": "BACHILLER",
                            "TECNICO PROFESIONAL": "TECNICO",
                            "INSTALADOR": "TECNICO",
                            "TECNOLGO": "TECNOLOGO",
                            "TECNOLOGA": "TECNOLOGO",
                            "TECNOGO": "TECNOLOGO",
                            "MAESTRIA": "PROFESIONAL",
                            "POSTGRADO": "PROFESIONAL"
                            }

limpieza_empresas = {"INDEPENDIENTE": "PARTICULAR",
                    "JARAMILLO MORA": "JARAMILLO MORA CONSTRUCTORA SA",
                    "BRILLASEO": "BRILLASEO SAS",
                    "BRILLASEO AS": "BRILLASEO SAS",
                    "SERVIVALLE":"DISTRIBUIDORA SERVIVALLE SAS",
                    "EMCALI": "EMCALI EICE ESP",
                    "EMPRESAS MUNICIPALES DE CALI E.I.C.E. E.S.P.": "EMCALI EICE ESP",
                    "BECERRA GUERRERO S A S" : "BECERRA GUERRERO SAS",
                    "A Y G PROYECTOS Y MONTAJES" : "A Y G PROYECTOS Y MONTAJES SAS",
                    "DCYT": "DCYT INGENIERIA S.A.S",
                    "DCYT INGENIERIA SAS": "DCYT INGENIERIA S.A.S",
                    "PYP CONTRUCCIONES": "CONSTRUCCIONES PYP",
                    "P Y P CONSTRUCCIONES": "CONSTRUCCIONES PYP",
                    "MAKA INGENIERIA": "MAKA INGENIERIA SAS",
                    "MAKA": "MAKA INGENIERIA SAS",
                    "GESILVI": "GESILVI SAS",
                    "GOODYEAR": "GOODYEAR DE COLOMBIA SA",
                    "INCODE":"INCODE SAS",
                    "INCODE INGENIERIA CONSTRUCCION Y DISEÑO ELECTRICO S.A.S": "INCODE SAS",
                    'INCODE INGENIERIA CONSTRUCCION Y\\nDISEÑO ELECTRICO S.A.S': "INCODE SAS",
                    "CONSTRUCCIONES SAUL VIVEROS": "CONSTRUCCIONES SAUL VIVEROS SAS",
                    "SAUL VIVEROS": "CONSTRUCCIONES SAUL VIVEROS SAS",
                    "CONINGENIERIA":"CONINGENIERIA SAS",
                    "TRANSPORTES Y MANTENIMIENTO B Y B SAS.": "TRANSPORTES Y MANTYENIMIENTO B & B SAS",
                    "HIDROCONSTRUCCIONES": "HIDROCONSTRUCCIONES JV SAS",
                    "CUBIERTAS Y MACHIMBRES MANCILLA": "MACHIMBRES Y CUBIERTAS MANCILLA SAS",
                    "MACHIMBRES Y CUBIERTAS MANCILLA": "MACHIMBRES Y CUBIERTAS MANCILLA SAS",
                    "CUBIERTAS": "ALFA CUBIERTAS SAS",
                    "ALFA CUBIERTAS":"ALFA CUBIERTAS SAS",
                    "MONTAJES ELECTRICOS INDUSTRIALES DEL VALLE SAS": "MONTAJES ELECTRICOS INDUSTRIALES DEL VALLE S.A.S.",
                    "SAP AUTOMATIZACION": "SOLUCIONES AUTOMATICAS PROGRAMABLES SAP SAS",
                    "SAP": "SOLUCIONES AUTOMATICAS PROGRAMABLES SAP SAS",
                    "CONINGENIERIA": "CONINGENIERIA SAS",
                    "COINGENIERIA": "CONINGENIERIA SAS",
                    "ARIS GRUESO": "ARIS GRUESO CONSTRUCCIONES SAS",
                    "BLANCO Y NEGRO": "BLANCO Y NEGRO MASIVO SA",
                    "BLANCO Y NEGRO MASIVO": "BLANCO Y NEGRO MASIVO SA",
                    "RAN SERVICIOS": "RAN SERVICIOS INTEGRALES SAS",
                    "PCL": "PRODUCTOS DE CAUCHO Y LONA SAS",
                    "GESILVI":"GESILVI SAS",
                    "STORAGE GESILVI":"GESILVI SAS",
                    "JJ OS CONSTRUCCIONES":"JJ OS CONSTRUCCIONES SAS",
                    "SERVICONSTRUCCIONES": "SERVICONSTRUCCIONES HD SAS",
                    "JAM INGENIERIA": "JAM INGENIERIA Y SERVICIOS SAS",
                    "DISEÑO Y CONSTRUCCION CALI": "DISEÑO Y CONSTRUCCION CALI LTDA",
                    "JG MONTAJES":"JG INGENIERIA Y SERVICIO SAS",
                    "JG INGENIERIA": "JG INGENIERIA Y SERVICIO SAS",
                    "MARC": "MARC SAS",
                    "MANAGEMENT AND RISK CONTROL SAS": "MARC SAS",
                    "SUMA PROYECTOS": "SUMA PROYECTOS DE INGENIERIA",
                    "SUMAPROYECTOS": "SUMA PROYECTOS DE INGENIERIA",
                    "ROCAFORTE": "ROCAFORTE CONSTRUCCIONES S.A.S",
                    "REFRISERVICIOS": "REFRISERVICIOS SAS",
                    "ACABAL": "ACABAL SAS",
                    "JFR INGENIERIA": "JFR INGENIERIA CIVIL S.A.S",
                    "GEMCON": "GEMCON SAS",
                    "ACABAL JAJ SAS": "ACABADOS JAJ",
                    "RRM INGENIERIA": "RRM INGENIERIA Y CONSTRUCCION S A S",
                    "CONSTRUCCIONES Y ACABADOS  AA SAS": "CONSTRUCCIONES Y ACABADOS AA",
                    "CONSTRUCCIONES AA": "CONSTRUCCIONES Y ACABADOS AA",
                    "DISTRIACABADOS": "DISTRIACABADOS CIA Y LTDA",
                    "MACHIMBRES Y CUBIERTAS MANCILLA": "MACHIMBRES Y CUBIERTAS MANCILLA SAS",
                    "OSCAR GOMEZ Y CIA": "OSCAR GOMEZ Y CIA SAS",
                    "VENFIL INGENIERA SAS": "VENFIL INGENIERIA",
                    "HES INGENIERA": "HES INGENIERA SAS",
                    "VENFIL": "VENFIL INGENIERIA",
                    "FORMAS E INGENIERIA": "FORMAS E INGENIERIA SAS",
                    "FORMAS E INGENIERA SAS": "FORMAS E INGENIERIA SAS",
                    "LATINA INGENIERA SAS": "LATINA INGENIERIA",
                    "IMPORTACIONES TROPI": "IMPORTACIONES Y ASESORIAS TROPI SAS",
                    "IMPORTADORA TROPI": "IMPORTACIONES Y ASESORIAS TROPI SAS",
                    "ASESORIAS E IMPORTACIONES TROPI": "IMPORTACIONES Y ASESORIAS TROPI SAS",
                    "H Y C SOLUCIONES INTEGRALES": "H Y C SOLUCIONES INTEGRALES SAS",
                    "A Y G PROYECTOS Y MONTAJES": "A Y G PROYECTOS Y MONTAJES SAS",
                    "HIDROCONSTRUCCIONES": "HIDROCONSTRUCCIONES JV SAS",
                    "FIBER FUSION": "FIBER FUSIONES SAS",
                    "KEPPLER": "ACABADOS KEPPLER",
                    "ACABADOS KEPLEER SAS": "ACABADOS KEPPLER",
                    "ALTIVA": "ALTIVA INGENIERIA SAS",
                    "ALTIVA SAS": "ALTIVA INGENIERIA SAS",
                    "ALTIVA INGENIERIA": "ALTIVA INGENIERIA SAS",
                    "ALTIVA INGENIERIA EN TRANSPORTE VERTICAL S.A.S": "ALTIVA INGENIERIA SAS",
                    "SERVINDUSTRIALESDEL PACIFICIO SAS.": "SERVINDUSTRIALES DEL PACIFICO SAS",
                    "INSELCOM": "INSELCOM SAS",
                    "HNOVA INGENIERIA": "HNOVA INGENIERIA SAS",
                    "H NOVA INGENIERIA": "HNOVA INGENIERIA SAS",
                    "REFRIGERACION AVL": "AVL REFRIGERACION SAS",
                    "AVL REFRIGERACION": "AVL REFRIGERACION SAS",
                    "SISTEMAS AUTOMATICOS DE CONTROL": "SISTEMAS AUTOMATICOS DE CONTROL SAS",
                    "FUTURAL ALUMINIOS": "LEHNER FUTURAL Y ALUMINIOS SAS",
                    "HERNANDO OROZCO": "HERNANDO OROZCO Y CIA SAS",
                    "AMBIENTAR": "AMBIENTAR DE COLOMBIA SAS",
                    "AMBIENTAR INGENIERIA": "AMBIENTAR DE COLOMBIA SAS",
                    "APLIARQUI": "APLIARQUI SAS",
                    "PERFORACIONES Y REDES P&P SAS.": "PERFORACIONES Y REDES P&P SAS",
                    "CONSTRUCCIONES Y REDES P Y P": "PERFORACIONES Y REDES P&P SAS",
                    "CONSTRUCCIONES Y REDES": "PERFORACIONES Y REDES P&P SAS",
                    "PUBLI AP": "PUBLI AP SAS",
                    "MAKRO SOLUCIONES INDUSTRIALES LTDA.": "MAKRO SOLUCIONES INDUSTRIALES LTDA",
                    "VIDAL COBO ALEXANDER": "ACABADOS VIDAL SAS",
                    "TANK CARE": "TANK CARE SAS",
                    "REFRIPOLAR": "GRUPO REFRIPOLAR SAS",
                    "CONSTRUCTORA AIA": "CONSTRUCTORA AIA SAS",
                    "AIA": "CONSTRUCTORA AIA SAS",
                    "EDIFICAR CONSTRUCONSULTORES S.A.S": "EDIFICAR CONSTRUCONSULTORES SAS",
                    "ADVANCE ELECTRIC": "ADVANCE ELECTRIC INGENIERIA SAS",
                    "JH INVERSIONES": "JH INVERSIONES SAS",
                    "MULTISERV INDUSTRIALES": "MULTISERV INDUSTRIALES SAS",
                    "MULTISERV INDUSTRIALES S.A.S.": "MULTISERV INDUSTRIALES SAS",
                    "SERVICIOS Y SUMINISTROS DEL VALLE": "SERVICIOS Y SUMINISTROS DEL VALLE SAS",
                    "INGESA SAS": "INGESAS SAS",
                    "LUMEN": "LUMEN GRAPHICS SAS",
                    "LUMEN ": "LUMEN GRAPHICS SAS",
                    "LUMEN SAS": "LUMEN GRAPHICS SAS",
                    "DISEÑO Y CONSTRUCCION ": "DISEÑO Y CONSTRUCCION",
                    "DISEÑO Y CONSTRUCCION DE OBRAS": "DISEÑO Y CONSTRUCCION DE OBRAS SAS",
                    "AG CONSTRUCCIONES": "AG CONSTRUCCIONES SAS",
                    "CONSTRUCCIONES Y ACABADOS M.V.C S.A.S.": "CONSTRUCCIONES Y ACABADOS MVC SAS",
                    "ALMATEC LOGISTICA INTELIGENTE SAS": "ALMATEC SAS",
                    "MGA MONTAJES Y MANTENIMIENTO ELECTRICO INDUSTRIAL SAS": "MGA MONTAJE Y MANTENIMIENTO ELECTRICO INDUSTRIAL SAS",
                    "MGA": "MGA MONTAJE Y MANTENIMIENTO ELECTRICO INDUSTRIAL SAS",
                    "TRANSPORTES Y MANTYENIMIENTO B & B SAS.": "TRANSPORTES Y MANTENIMIENTO B Y B SAS",
                    "POTENCIA ELECTRICA": "POTENCIA ELECTRICA M&M SAS",
                    "MONTAJES ELECTRICOS INDUSTRIALES DEL VALLE S.A.S.": "MONTAJES ELECTRICOS INDUSTRIALES DEL VALLE SAS",
                    "INGEAS": "INGEAS SAS",
                    "TRANSPORTE YCARGA LA SULTANA S.A.S": "TRANSPORTE Y CARGA LA SULTANA SAS.",
                    "TRANSPORTE Y CARGA LA SULTANA SAS.": "TRANSPORTE Y CARGA LA SULTANA SAS",
                    "CENTRO AIRE ACONDICIONADO": "CENTRO DE SERVICIO DE AIRE ACONDICIONADO",
                    "CONSTRUCCIONES LIVIANAS": "CONSTRUCCIONES LIVIANAS ZUÑIGA SAS",
                    "SERVICIOS Y MONTAJES INDUSTRIALES ASTAIZA S.A.S.": "SERVICIOS Y MONTAJES INDUSTRIALES ASTAIZA SAS",
                    "GYG ASOCIADOS INGENIEROS CIVILIES S.A.S": "G Y G ASOCIADOS INGENIERIOS CIVILES SAS",
                    "EDGAR GONZALEZ CIA LTDA": "EDGAR GONZALEZ Y CIA LTDA",
                    "ESPECIALIDADES ELECTROMECANICAS EU": "ESPECIALIDADES ELECTROMECANICAS",
                    "MG ESTANTERIA": "MG ESTANTERIAS SAS",
                    "MG ESTANTERIA SAS": "MG ESTANTERIAS SAS",
                    "C Y F INGENIERIA": "CYF INGENIERIA Y TELECOMUNICACIONES SAS",
                    "SERVICIOS Y CONTRUCCIONES ALARCON SAS": "SERVICIOS Y CONSTRUCCIONES ALARCON SAS",
                    "UNION TEMPORAL M&C2021": "UNION TEMPORAL MYC 2021",
                    "RG ALTURAS": "RG ALTURAS SALUD Y SEGURIDAD EN EL TRABAJO SAS",
                    "REFRIGERACION CRG": "REFRIGERACION CRG SAS",
                    "JGB SAS": "JGB SA",
                    "MARIA DAISY VIAFARA": "MARIA DAYSI VIAFARA",
                    "ARTIARE SAS": "ARTIAIRE",
                    "JRINCON INGENIERIA": "J RINCON INGENIERIA",
                    "CONSMACOL ": "CONSMACOL",
                    'INGENIERIA Y \\nSUPERVISION TECNICA S.A.S': "INGENIERIA Y SUPERVISION TECNICA S.A.S",
                    "TRAZAMOS INGENIERIA": "TRAZAMOS INGENIERIA SAS",
                    "INGENIERIA DE INVERSIONES MPF": "INGENIERIA E INVERSIONES MPF SAS",
                    "DISPAPELES SAS": "DISPAPELES",
                    'EVENTOS Y LOGISTICA\\nCARVAJAL MEJIA SAS': "EVENTOS Y LOGISTICA CARVAJAL MEJIA SAS",
                    'GESTION\\nTECNOLOGIA Y DESARROLLO EMPRESARIAL SAS': "GESTION TECNOLOGIA Y DESARROLLO EMPRESARIAL SAS",
                    "MULTIPROYECTOS JERC": "MULTIPROYECTOS JERC SAS",
                    "SELDA SOLUCIONES SAS": "SELDA SAS",
                    "BANNER PRINT PUBLICIDAD": "BANNER PRINT PUBLICIDAD SAS",
                    "GR PUBLICIDAD": "GR PUBLICIDAD LTDA",
                    "FORMAS CREATIVAS": "FORMAS CREATIVAS PUBLICIDAD SAS",
                    "FORMAS CREATIVAS ": "FORMAS CREATIVAS PUBLICIDAD SAS",
                    "AMAYA": "MIGUEL AMAYA SAS",
                    "MERV": "MERV SAS",
                    "TOPOGRAFIA Y CONSTRUCCION D.C": "TOPOGRAFIA Y CONSTRUCCION DC",
                    "PROFESOR EDUARDO": "EDUARDO PROFESOR",
                    "CONCRETOS Y REDES": "CONCRETO Y REDES RYM SAS",
                    "BRICO": "BRICO INGENIERIA",
                    "TECCOI": "TECCOI SAS",
                    "VENTURELLO SAS": "VENTURELLO DISTRIBUCIONES SAS",
                    'SOLUTIONS\\nTECHNOLOGY GLOBAL SAS': "SOLUTIONS TECHNOLOGY GLOBAL SAS",
                    'PROGRESAR AL\\nFUTURO S.A.S.': "PROGRESAR AL FUTURO S.A.S.",
                    'GLOBAL\\nCONSTRUCTION COMPANY S.A.S.': "GLOBAL CONSTRUCTION COMPANY S.A.S.",
                    "ESRUCTURAS Y MAMPOSTERIA CASTRO": "ESTRUCTURAS Y MAMPOSTERIA CASTRO",
                    "ESTRUCTURA Y MAMPOSTERIA": "ESTRUCTURAS Y MAMPOSTERIA CASTRO",
                    "RESET ": "RESET- REDES SEGURIDAD Y TECNOLOGIA",
                    'ELECTRICOS LIAM\\nDAVID SAS': "ELECTRICOS LIAM DAVID SAS",
                    "RED A GAS": "RED A GAS Y CALEFACCION SAS",
                    "ELETRINTEC SAS": "ELECTRINTEC SAS",
                    "BUFALO CERRAMIENTOS Y COSNTRUCCIONES": "BUFALO CERRAMIENTOS Y CONSTRUCCIONES",
                    "ACABADOS FERNANDO PENA BERMUDEZ E HIJO S": "ACABADOS FERNANDO PENA BERMUDEZ E HIJOS",
                    "SERVI CONSTRUCCIONES": "SERVICONSTRUCCIONES HD SAS",
                    "CONVICICON SAS": "CONVICCION SAS",
                    "STG SAS": "SOLUTIONS TECHNOLOGY GLOBAL SAS",
                    "SOLITEMP S.A..": "SOLITEMP S.A.",
                    "RICARD": "RICARD RESPUESTAS"
                    }

# La función siguiente se encarga de la limpieza de las columnas

def limpieza_columnas(df):
    # Limpieza de la columna de "NIVEL EDUCATIVO"
    df.loc[:3887, "NIVEL EDUCATIVO"] = df.loc[:3887, "NIVEL EDUCATIVO"].replace(limpieza_nivel_educativo)
    
    # Reemplazando valor "TRABAJADOR AUTORIZADO" con "AUTORIZADO" en la columna "CURSO"
    df["CURSO"].replace("TRABAJADOR AUTORIZADO", "AUTORIZADO", inplace=False)
    
    # Aplicando limpieza de la columna de "EMPRESA"
    df.loc[:3887, "EMPRESA"] = df.loc[:3887, "EMPRESA"].replace(limpieza_empresas)
    
    #--------------------------------------------------------------------
    
    # Estableciendo formato datetime a "FECHA INICIO CURSO"
    df["FECHA INICIO CURSO"] = pd.to_datetime(df["FECHA INICIO CURSO"], format="%m/%d/%Y", errors="coerce")
    
    # Creando una columna "AÑO" en df a partir de la extracción del formato %Y en 'FECHA INICIO CURSO'
    df['AÑO'] = df['FECHA INICIO CURSO'].dt.year
    
    # Elimina filas con valores nulos en "AÑO"
    df = df.dropna(subset=['AÑO'])
    
    # Cogemos los datos de todas las filas de la columna "AÑO", los redondeamos y los transformamos a un dato de tipo "int"
    df.loc[:, 'AÑO'] = df['AÑO'].round().astype(int)
    
    
    df["FECHA  NACIMIENTO"] = pd.to_datetime(df["FECHA  NACIMIENTO"], format='%m/%d/%Y', errors='coerce')
    
    df_fechas_validas = df[df["FECHA  NACIMIENTO"].notnull()]
    
    fecha_actual = datetime.now()
    
    df_fechas_validas.loc[:, "DIFERENCIA DE DIAS"] = (fecha_actual - df_fechas_validas["FECHA  NACIMIENTO"]).dt.days
    
    df_fechas_validas.loc[:, "EDAD"] = df_fechas_validas["DIFERENCIA DE DIAS"] / 365
    
    # Ahora, "EDAD" contendrá la edad de cada persona en años en el dataframe 
    df["EDAD"] = df_fechas_validas["EDAD"]
    
    return df

df = limpieza_columnas(df)

# ----------------------------------------------------------------------------------------------------------------------------------------

# Crear la aplicación de Dash

'''

'''
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MORPH])

# Definir la función para crear el gráfico de competencia
def grafico_competencia(df):
    
    competencia_cantidad = df["CER TSA"].value_counts().nlargest(5)
    competencia_sort = competencia_cantidad.sort_values(ascending=False)
    
    colores = [
    "#5A5E5A",
    "#726B72",
    "#8A788D",
    "#A28598",
    "#BA92A3",
    "#CCAAAE",
    "#D6BEB7",
    "#E3C9C2",
    "#F0D6C7",
    "#F7E3D2"
    ]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=competencia_sort.index, y=competencia_sort.values, marker_color=colores))
    fig.update_layout(
        title="Los 5 centros de entrenamiento de donde más vienen los trabajadores",
        xaxis_title="Cantidad de personas",
        yaxis_title="Centros de entrenamiento",
        
    )

    return fig

# Definir la función para crear el gráfico de los cursos
def grafico_cursos(df, instructor):
    
    # Si instructor es None, devolver el gráfico completo (sin filtrar)
    if instructor is None:
        df_cursos = df
    else:
        df_cursos = df[df['INSTRUCTOR'] == instructor]
    
    colores = [
    "#5A4177",
    "#724E82",
    "#8A5B8D",
    "#A26898",
    "#BA75A3",
    "#CC82AE",
    "#D78FB7",
    "#E49CC2",
    "#F1A9C7",
    "#F7B6D2"
]
    fig = go.Figure()
    fig.add_trace(go.Bar(x = df_cursos["CURSO"].unique(),
                         y = df_cursos["CURSO"].value_counts(),
                         marker_color = colores))
    
    fig.update_layout(
        title = "Número de personas en los diferentes tipos de cursos",
        xaxis_title = "Curso",
        yaxis_title = "Cantidad de personas",
        xaxis_tickmode = "array",
        xaxis_tickvals = df_cursos["CURSO"][:3531]
    
    )

    return fig

# Definir la función para crear el gráfico del país de nacimiento
def grafico_pais_nacimiento(df):
    colores = ["#31293F", "#554D74", "#796EA8"]
    contenido = df["PAIS  NACIMIENTO"].value_counts()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=contenido.index,
                         y=contenido,
                         marker_color = colores))
    
    fig.update_layout(
        title="Países de origen de las personas que asisten al curso",
        xaxis_title="Paises",
        yaxis_title="Cantidad de personas"
    )

    return fig

# Definir la función para crear el gráfico de los instructores
def grafico_instructor(df, curso):
    
    # Si curso es None, devolver el gráfico completo (sin filtrar)
    if curso is None:
        df_instructor = df
    else:
        df_instructor = df[df['CURSO'] == curso]
    
    colores = [
    "#75827A",
    "#828F87",
    "#9C9C92",
    "#A9A9A7",
    "#B6B6D2"
    ]
    
    instructor_cantidad = df_instructor["INSTRUCTOR"].value_counts().nlargest(5)
    instructor_sort = instructor_cantidad.sort_values(ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=instructor_sort,
                         y=instructor_sort.index,
                         orientation="h",
                         marker_color=colores))
    
    fig.update_layout(
    title="Los 5 instructores que más cursos dictan en la empresa RG ALTURAS",
    xaxis_title="Cantidad de personas a las que les dictó clase",
    yaxis_title="Instructor"
    )
    
    return fig

# Definir la función para crear el gráfico del nivel educativo
def grafico_nivel_edu(df, rango_edad):
    
    # Si rango_edad es None, devolver el gráfico completo (sin filtrar)
    if rango_edad is None:
        df_nivel_edu = df
    else:
        min_edad, max_edad = map(int, rango_edad.strip("").split("-"))
        df_nivel_edu = df[(df['EDAD'] >= min_edad) & (df['EDAD'] < max_edad)]
    
    contenido = df_nivel_edu["NIVEL EDUCATIVO"].value_counts()
    
    colores = [
    "#ff0000",
    "#ff7f00",
    "#ffff00",
    "#ff9900",
    "#ffcc00",
    "#ffc000",
    "#ffffcc",
    "#ffeeee",
    "#ffeeff",
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x = contenido.index, y = contenido, marker_color = colores))
    fig.update_layout(
    title = "Número de personas en los diferentes niveles educativos",
    yaxis_title = "Cantidad de personas",
    xaxis_title = "Nivel Educativo"
    )
    
    return fig

# Definir la función para crear el gráfico sobre las empresas
def grafico_analisis_emp(df, rango_edad=None, genero=None):
    
    # Crear una copia de df para no alterar el DataFrame original
    df_analisis_emp = df.copy()
    
    # Si rango_edad no es None, filtrar df_copy por rango de edad
    if rango_edad is not None:
        min_edad, max_edad = map(int, rango_edad.split("-"))
        df_analisis_emp = df_analisis_emp[(df_analisis_emp['EDAD'] >= min_edad) & (df_analisis_emp['EDAD'] < max_edad)]
    
    # Si genero no es None, filtrar df_copy por genero
    if genero is not None:
        df_analisis_emp = df_analisis_emp[df_analisis_emp['GENERO'] == genero]
    
    emp = df_analisis_emp["EMPRESA"].value_counts().nlargest(10)
    emp_sort = emp.sort_values(ascending=True)
    
    colores = [
    "#726A72",
    "#8A778D",
    "#A28498",
    "#BA91A3",
    "#CCA8AE",
    "#D6B5B7",
    "#E3C2C2",
    "#F0CFC7",
    "#F7D9D2"
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=emp_sort,
                         y=emp_sort.index,
                         orientation="h",
                         marker_color= colores))
    fig.update_layout(
    title = "Las 10 empresas de donde vienen más trabajadores a realizar el curso de alturas",
    xaxis_title = "Empresas",
    yaxis_title = "Cantidad de personas"
    )
    
    return fig

# Definir la función para crear el gráfico del área de trabajo de los inscritos en el curso
def grafico_area_tra(df, rango_edad=None, genero=None, nivel_educativo=None):
    
    # Filtrar el DataFrame en función de los valores seleccionados
    df_area_tra = df.copy()
    
    if rango_edad:
        min_edad, max_edad = map(int, rango_edad.split("-"))
        df_area_tra = df_area_tra[(df_area_tra['EDAD'] >= min_edad) & (df_area_tra['EDAD'] < max_edad)]
    if genero:
        df_area_tra = df_area_tra[df_area_tra['GENERO'] == genero]
    if nivel_educativo:
        df_area_tra = df_area_tra[df_area_tra['NIVEL EDUCATIVO'] == nivel_educativo]

    # Crear el gráfico
    area = df_area_tra["AREA DE TRABAJO"].value_counts().nlargest(10)
    valores = area.index
    frecuencias = area.values
    
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=valores,
                         values=frecuencias))
    fig.update_layout(title = "Las 10 áreas de trabajo donde más trabajan las personas que asisten al curso")
    
    return fig

# Definir la función para crear el gráfico de los cargos que ejercen los estudiantes
def grafico_cargos(df, rango_edad=None, genero=None, nivel_educativo=None):
    
    # Filtrar el DataFrame en función de los valores seleccionados
    df_cargos = df.copy()
    if rango_edad:
        min_edad, max_edad = map(int, rango_edad.split("-"))
        df_cargos = df_cargos[(df_cargos['EDAD'] >= min_edad) & (df_cargos['EDAD'] < max_edad)]
    if genero:
        df_cargos = df_cargos[df_cargos['GENERO'] == genero]
    if nivel_educativo:
        df_cargos = df_cargos[df_cargos['NIVEL EDUCATIVO'] == nivel_educativo]

    # Crear el gráfico
    cargo = df_cargos["CARGO ACTUAL"].value_counts().nlargest(10).sort_values(ascending=False)
    valores = cargo.index
    frecuencias = cargo.values
    
    colores = [
    "#52C41A",
    "#72D924",
    "#93E429",
    "#B4ED2E",
    "#D5F033",
    "#F5F338",
    "#F8E63C",
    "#F1D940",
    "#E4D244",
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=valores,
                         y=frecuencias,
                         marker_color = colores))
    fig.update_layout(
    title="Los 10 cargos de trabajo donde más se encuentran las personas que asisten al curso",
    xaxis_title="Cantidad de personas",
    yaxis_title="Cargo"
    )
    
    return fig


# Definir la función para crear el gráfico del género de los estudiantes
def grafico_genero(df, rango_edad=None, nivel_educativo=None):
    
    # Filtrar el DataFrame en función de los valores seleccionados
    df_genero = df.copy()
    
    if rango_edad:
        min_edad, max_edad = map(int, rango_edad.split("-"))
        df_genero = df_genero[(df_genero['EDAD'] >= min_edad) & (df_genero['EDAD'] < max_edad)]
    if nivel_educativo:
        df_genero = df_genero[df_genero['NIVEL EDUCATIVO'] == nivel_educativo]

    # Crear el gráfico
    cantidad = df_genero["GENERO"].value_counts()
    genero = df_genero["GENERO"].unique()
    
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=genero, values=cantidad))
    fig.update_layout(title="Gráfica sobre la asistencia a los cursos según su género")
    
    return fig
    
# Definir la función para crear el gráfico de la edad de los estudiantes
def grafico_edad(df, genero=None, nivel_educativo=None):
    
    # Filtrar el DataFrame en función de los valores seleccionados
    df_edad = df.copy()
    
    if genero:
        df_edad = df_edad[df_edad['GENERO'] == genero]
    if nivel_educativo:
        df_edad = df_edad[df_edad['NIVEL EDUCATIVO'] == nivel_educativo]

    # Crear el gráfico
    frecuencias = go.histogram.XBins(size=10)
    colores = ["#E7939A",
    "#F5A59C",
    "#F8B7A0",
    "#F9C9A4",
    "#FABBA8",
    "#E7CCBE",
    "#F5D6C2",
    "#F8E8D6",
    "#F9F9DE"
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df_edad["EDAD"], xbins=frecuencias, marker_color=colores))
    fig.update_layout(
        title="Gráfico de la edad de las personas que asisten al curso de alturas",
        xaxis_title="Edad",
        yaxis_title="Cantidad de personas"
    )
    
    return fig


def grafico_estado_asistencia(df, rango_edad=None, genero=None, empresa=None):
    # Filtrar el DataFrame en función de los valores seleccionados
    df_asistencia = df.copy()
    if rango_edad:
        min_edad, max_edad = map(int, rango_edad.split("-"))
        df_asistencia = df_asistencia[(df_asistencia['EDAD'] >= min_edad) & (df_asistencia['EDAD'] < max_edad)]
    if genero:
        df_asistencia = df_asistencia[df_asistencia['GENERO'] == genero]
    if empresa:
        df_asistencia = df_asistencia[df_asistencia['EMPRESA'] == empresa]

    # Crear el gráfico
    years_of_interest = [2021, 2022, 2023]
    asistencia = df_asistencia["AÑO"].value_counts()
    min_year = int(asistencia.index.min())
    max_year = int(asistencia.index.max())

    fig = go.Figure()


    
    if empresa == "BLANCO Y NEGRO MASIVO SA":   
        # Línea de asistencia
        fig.add_trace(
            go.Scatter(
                x=years_of_interest,
                y=asistencia[years_of_interest].fillna(0),
                line=dict(color="#0004FF"),
                name="Asistencia"
            )
        )

        # Puntos de interés
        fig.add_trace(
            go.Scatter(
                x=years_of_interest,
                y=[asistencia.get(year, 0) for year in years_of_interest],
                mode="markers",
                marker=dict(
                    color="#0004FF",
                    size=20,
                    symbol="circle"
                ),
                name="Punto de interés anual"
            )
        )     
       
        fig.update_layout(
                title="Cantidad de asistencia en los diferentes años a RG ALTURAS",
                xaxis_title="Año",
                yaxis_title="Cantidad de asistencia",
                xaxis_range=[round(min_year, 0), round(max_year, 0)],
                showlegend=True,
                images=[dict(
                    source="assets/mio_image.jpg",
                    xref="paper", yref="paper",
                    x=0, y=1,
                    sizex=1, sizey=1,
                    sizing="stretch",
                    opacity=0.6,
                    layer="below")]
            )
        
    else:
        # Línea de asistencia
        fig.add_trace(
            go.Scatter(
                x=years_of_interest,
                y=asistencia[years_of_interest].fillna(0),
                line=dict(color="#2b9172"),
                name="Asistencia"
            )
        )

        # Puntos de interés
        fig.add_trace(
            go.Scatter(
                x=years_of_interest,
                y=[asistencia.get(year, 0) for year in years_of_interest],
                mode="markers",
                marker=dict(
                    color="#2b9175",
                    size=20,
                    symbol="circle"
                ),
                name="Punto de interés anual"
            )
        )
        
        fig.update_layout(
            title="Cantidad de asistencia en los diferentes años a RG ALTURAS",
            xaxis_title="Año",
            yaxis_title="Cantidad de asistencia",
            xaxis_range=[round(min_year, 0), round(max_year, 0)],
            showlegend=True,   
            images=[dict(
                    source="assets/Imagen de WhatsApp 2023-10-03 a las 16.41.37_119eb856.jpg",
                    xref="paper", yref="paper",
                    x=0, y=1,
                    sizex=1, sizey=1,
                    sizing="stretch",
                    opacity=0.4,
                    layer="below")]
            )
                
    return fig

# ---------------------------------------------------------------------------------------------------

# Estilo para el título
titulo_style = {
    'text-align': 'center',
    'margin': '15px', 
}

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

dropdown_items_nivel_educativo_area_tra = [dbc.DropdownMenuItem("Selecciona un nivel educativo",
                                                                id='dropdown-educativo-area-tra-None')] + \
                 [dbc.DropdownMenuItem(i,
                                       id=f'dropdown-educativo-area-tra-{i}') for i in df['NIVEL EDUCATIVO'].unique()]
                 
dropdown_nivel_educativo_area_tra = dbc.DropdownMenu(
    label="Selecciona un nivel educativo",
    children=dropdown_items_nivel_educativo_area_tra,
    id='dropdown-educativo-area-tra',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------

dropdown_items_nivel_educativo_cargos = [dbc.DropdownMenuItem("Selecciona un nivel educativo",
                                                              id='dropdown-educativo-cargos-None')] + \
                 [dbc.DropdownMenuItem(i,
                                       id=f'dropdown-educativo-cargos-{i}') for i in df['NIVEL EDUCATIVO'].unique()]
                 
dropdown_nivel_educativo_cargos = dbc.DropdownMenu(
    label="Selecciona un nivel educativo",
    children=dropdown_items_nivel_educativo_cargos,
    id='dropdown-educativo-cargos',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------

dropdown_items_nivel_educativo_genero = [dbc.DropdownMenuItem("Selecciona un nivel educativo",
                                                              id='dropdown-educativo-genero-None')] + \
                 [dbc.DropdownMenuItem(i,
                                       id=f'dropdown-educativo-genero-{i}') for i in df['NIVEL EDUCATIVO'].unique()]
                 
dropdown_nivel_educativo_genero = dbc.DropdownMenu(
    label="Selecciona un nivel educativo",
    children=dropdown_items_nivel_educativo_genero,
    id='dropdown-educativo-genero',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------

dropdown_items_nivel_educativo_edad = [dbc.DropdownMenuItem("Selecciona un nivel educativo",
                                                            id='dropdown-educativo-edad-None')] + \
                 [dbc.DropdownMenuItem(i,
                                       id=f'dropdown-educativo-edad-{i}') for i in df['NIVEL EDUCATIVO'].unique()]
                 
dropdown_nivel_educativo_edad = dbc.DropdownMenu(
    label="Selecciona un nivel educativo",
    children=dropdown_items_nivel_educativo_edad,
    id='dropdown-educativo-edad',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Crear los elementos del menú desplegable
dropdown_items_cursos = [dbc.DropdownMenuItem("Selecciona un instructor",
                                              id='dropdown-cursos-Todos')] + \
                        [dbc.DropdownMenuItem(i,
                                              id=f'dropdown-cursos-{i}') for i in df['INSTRUCTOR'].unique()]

# Crear el menú desplegable
dropdown_cursos = dbc.DropdownMenu(
    label="Selecciona un instructor",
    children=dropdown_items_cursos,
    id='dropdown-cursos',
    style={'margin-bottom': '20px'}
)

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Crear los elementos del menú desplegable
dropdown_items_instructores = [dbc.DropdownMenuItem("Selecciona un curso",
                                                    id='dropdown-instructores-Todos')] + \
                              [dbc.DropdownMenuItem(i,
                                                    id=f'dropdown-instructores-{i}') for i in df['CURSO'].unique()]

# Crear el menú desplegable
dropdown_instructores = dbc.DropdownMenu(
    label="Selecciona un curso",
    children=dropdown_items_instructores,
    id='dropdown-instructores',
    style={'margin-bottom': '20px'}
)

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Crear los elementos del menú desplegable para "EDAD"
dropdown_items_edad_nivel_edu = [dbc.DropdownMenuItem("Selecciona un rango de edad",
                                                      id='dropdown-edad-nivel-edu-None')] + \
                      [dbc.DropdownMenuItem(i,
                                            id=f'dropdown-edad-nivel-edu-{i}') for i in ["10-20", "20-30", "30-40", "40-50", "50-60", "60-70"]]

# Crear el menú desplegable para "EDAD"
dropdown_edad_nivel_edu = dbc.DropdownMenu(
    label="Selecciona un rango de edad",
    children=dropdown_items_edad_nivel_edu,
    id='dropdown-edad-nivel-edu',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------

dropdown_items_edad_analisis_emp =  [dbc.DropdownMenuItem("Selecciona un rango de edad",
                                                          id='dropdown-edad-analisis-emp-None')] + \
                                    [dbc.DropdownMenuItem(i,
                                                          id=f'dropdown-edad-analisis-emp-{i}') for i in ["10-20", "20-30", "30-40", "40-50", "50-60", "60-70"]]

dropdown_edad_analisis_emp = dbc.DropdownMenu(
    label="Selecciona un rango de edad",
    children=dropdown_items_edad_analisis_emp,
    id='dropdown-edad-analisis-emp',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------

dropdown_items_edad_area_tra =  [dbc.DropdownMenuItem("Selecciona un rango de edad",
                                                      id='dropdown-edad-area-tra-None')] + \
                                    [dbc.DropdownMenuItem(i,
                                                          id=f'dropdown-edad-area-tra-{i}') for i in ["10-20", "20-30", "30-40", "40-50", "50-60", "60-70"]]

dropdown_edad_area_tra = dbc.DropdownMenu(
    label="Selecciona un rango de edad",
    children=dropdown_items_edad_area_tra,
    id='dropdown-edad-area-tra',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------

dropdown_items_edad_cargos =  [dbc.DropdownMenuItem("Selecciona un rango de edad",
                                                    id='dropdown-edad-cargos-None')] + \
                                    [dbc.DropdownMenuItem(i,
                                                          id=f'dropdown-edad-cargos-{i}') for i in ["10-20", "20-30", "30-40", "40-50", "50-60", "60-70"]]

dropdown_edad_cargos = dbc.DropdownMenu(
    label="Selecciona un rango de edad",
    children=dropdown_items_edad_cargos,
    id='dropdown-edad-cargos',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------

dropdown_items_edad_genero =  [dbc.DropdownMenuItem("Selecciona un rango de edad",
                                                    id='dropdown-edad-genero-None')] + \
                                    [dbc.DropdownMenuItem(i,
                                                          id=f'dropdown-edad-genero-{i}') for i in ["10-20", "20-30", "30-40", "40-50", "50-60", "60-70"]]

dropdown_edad_genero = dbc.DropdownMenu(
    label="Selecciona un rango de edad",
    children=dropdown_items_edad_genero,
    id='dropdown-edad-genero',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------

dropdown_items_edad_asistencia =  [dbc.DropdownMenuItem("Selecciona un rango de edad",
                                                        id='dropdown-edad-asistencia-None')] + \
                                    [dbc.DropdownMenuItem(i,
                                                          id=f'dropdown-edad-asistencia-{i}') for i in ["10-20", "20-30", "30-40", "40-50", "50-60", "60-70"]]

dropdown_edad_asistencia = dbc.DropdownMenu(
    label="Selecciona un rango de edad",
    children=dropdown_items_edad_asistencia,
    id='dropdown-edad-asistencia',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Crear los elementos del menú desplegable para "GENERO"
dropdown_items_genero = [dbc.DropdownMenuItem("Selecciona un género",
                                              id='dropdown-genero-None')] + \
                        [dbc.DropdownMenuItem(i,
                                              id=f'dropdown-genero-{i}') for i in df["GENERO"].unique()]

# Crear el menú desplegable para "GENERO"
dropdown_genero = dbc.DropdownMenu(
    label="Selecciona un género",
    children=dropdown_items_genero,
    id='dropdown-genero',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------

dropdown_items_genero_area_tra = [dbc.DropdownMenuItem("Selecciona un género",
                                                       id='dropdown-genero-area-tra-None')] + \
                        [dbc.DropdownMenuItem(i,
                                              id=f'dropdown-genero-area-tra-{i}') for i in df["GENERO"].unique()]

dropdown_genero_area_tra = dbc.DropdownMenu(
    label="Selecciona un género",
    children=dropdown_items_genero_area_tra,
    id='dropdown-genero-area-tra',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------

dropdown_items_genero_cargos = [dbc.DropdownMenuItem("Selecciona un género", id='dropdown-genero-cargos-None')] + \
                        [dbc.DropdownMenuItem(i, id=f'dropdown-genero-cargos-{i}') for i in df["GENERO"].unique()]

dropdown_genero_cargos = dbc.DropdownMenu(
    label="Selecciona un género",
    children=dropdown_items_genero_cargos,
    id='dropdown-genero-cargos',
    className="mr-3 p-0",
    group=True
)

#---------------------------------------------------------------------------------------------------

dropdown_items_genero_edad = [dbc.DropdownMenuItem("Selecciona un género", id='dropdown-genero-edad-None')] + \
                        [dbc.DropdownMenuItem(i, id=f'dropdown-genero-edad-{i}') for i in df["GENERO"].unique()]

dropdown_genero_edad = dbc.DropdownMenu(
    label="Selecciona un género",
    children=dropdown_items_genero_edad,
    id='dropdown-genero-edad',
    className="mr-3 p-0",
    group=True
)

#---------------------------------------------------------------------------------------------------

dropdown_items_genero_asistencia = [dbc.DropdownMenuItem("Selecciona un género",
                                                         id='dropdown-genero-asistencia-None')] + \
                        [dbc.DropdownMenuItem(i,
                                              id=f'dropdown-genero-asistencia-{i}') for i in df["GENERO"].unique()]

dropdown_genero_asistencia = dbc.DropdownMenu(
    label="Selecciona un género",
    children=dropdown_items_genero_asistencia,
    id='dropdown-genero-asistencia',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

'''
A tener en cuenta:

El "\" simplemente indica que dos líneas de código deben
tratarse como una sola instrucción por el intérprete de Python.

'''


empresas_por_frecuencia = df["EMPRESA"].value_counts().index

dropdown_items_empresa = [dbc.DropdownMenuItem("Selecciona una empresa",
                                               id='dropdown-empresa-None')] + \
                         [dbc.DropdownMenuItem(i,
                                               id=f'dropdown-empresa-{i.replace(".", "-")}') for i in empresas_por_frecuencia]

dropdown_empresa = dbc.DropdownMenu(
    label="Selecciona una empresa",
    children=dropdown_items_empresa,
    id='dropdown-empresa',
    className="mr-3 p-0",
    group=True
)

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------



# Definir el diseño del dashboard
app.layout = dbc.Container([
    
    html.H1("Dashboard - RG Alturas", style = titulo_style, ),
    
    #-----------------------------------------------------------------
    
    dcc.Store(id='store-edad', storage_type='memory'),
    dcc.Store(id='store-genero', storage_type='memory'),
    
    dcc.Store(id='store-edad-area-tra', storage_type='memory'),
    dcc.Store(id='store-genero-area-tra', storage_type='memory'),
    dcc.Store(id='store-educativo-area-tra', storage_type='memory'),
    
    dcc.Store(id='store-edad-cargos', storage_type='memory'),
    dcc.Store(id='store-genero-cargos', storage_type='memory'),
    dcc.Store(id='store-educativo-cargos', storage_type='memory'),
    
    dcc.Store(id='store-edad-genero', storage_type='memory'),
    dcc.Store(id='store-educativo-genero', storage_type='memory'),
    
    dcc.Store(id='store-genero-edad', storage_type='memory'),
    dcc.Store(id='store-educativo-edad', storage_type='memory'),
    
    dcc.Store(id='store-edad-asistencia', storage_type='memory'),
    dcc.Store(id='store-genero-asistencia', storage_type='memory'),
    dcc.Store(id='store-empresa', storage_type='memory'),
    
    #-----------------------------------------------------------------
    
    dbc.ButtonGroup([
        dbc.Button(
            "Centros de entrenamiento",
            id="collapse-button-competencia",
            className="mr-3",
            color="primary",
            n_clicks=0,
        ),
        
        dbc.Button(
            "N° de personas en cursos",
            id="collapse-button-cursos",
            className="mr-3",
            color="primary",
            n_clicks=0,
        ),
        
        dbc.Button(
            "País de origen",
            id="collapse-button-pais",
            className="mr-3",
            color="primary",
            n_clicks=0,
        ),
        
        dbc.Button(
            "Instructores",
            id="collapse-button-instructores",
            className="mr-3",
            color="primary",
            n_clicks=0,
        ),
        
        dbc.Button(
            "Nivel educativo",
            id="collapse-button-nivel-educativo",
            className="mr-3",
            color="primary",
            n_clicks=0,
        ),
        
        dbc.Button(
            "Empresas",
            id="collapse-button-empresas",
            className="mr-3",
            color="primary",
            n_clicks=0,
        ),
        
        dbc.Button(
            "Área de trabajo",
            id="collapse-button-area",
            className="mr-3",
            color="primary",
            n_clicks=0,
        ),
        
        dbc.Button(
            "Cargos que desempeñan",
            id="collapse-button-cargos",
            className="mr-3",
            color="primary",
            n_clicks=0,
        ),

        dbc.Button(
            "Distribución por género",
            id="collapse-button-genero",
            className="mr-3",
            color="primary",
            n_clicks=0,
        ),

        dbc.Button(
            "Distribución por edad",
            id="collapse-button-edad",
            className="mr-3",
            color="primary",
            n_clicks=0,
        ),

        dbc.Button(
            "Estado de asistencia",
            id="collapse-button-asistencia",
            className="mr-3",
            color="primary",
            n_clicks=0,
    )       
    ], size="md"),
    
    
    html.Div(style={'marginTop': 20, 'marginBottom': 20}),
    
    
    # Inicializar el gráfico con el valor inicial
    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            dcc.Graph(
                id = 'grafico-competencia',
                figure = grafico_competencia(df)
            )
        ])),
        id="collapse-competencia",
        is_open=False,
    ),
    
    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            
            dropdown_cursos,
            
            dcc.Graph(
            id = 'grafico-cursos',
            figure = grafico_cursos(df, None)
            )
        ])),
        id="collapse-cursos",
        is_open=False,
    ),
    
    dbc.Collapse(
        dbc.Card(dbc.CardBody(
            dcc.Graph(
            id = 'grafico-pais-nacimiento',
            figure = grafico_pais_nacimiento(df)
        ))),
        id="collapse-pais",
        is_open=False,
    ),
    
    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            
            dropdown_instructores,
            
            dcc.Graph(
            id = 'grafico-instructores',
            figure = grafico_instructor(df, None)
        )]
                              )),
        id="collapse-instructores",
        is_open=False,
    ),
    
    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            
            dropdown_edad_nivel_edu,
                       
            dcc.Graph(
            id = 'grafico-nivel-educativo',
            figure = grafico_nivel_edu(df, None),
            className = "mt-3"
            
        )])),
        
        id="collapse-nivel-educativo",
        is_open=False,
    ),
    
    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            
            dbc.ButtonGroup([dropdown_edad_analisis_emp,
                             dropdown_genero],
                            size="md", className="mb-3"),
            
            dcc.Graph(
                id = 'grafico-analisis-empresas',
                figure = grafico_analisis_emp(df)
            )
        ])),
        id="collapse-empresas",
        is_open=False,
    ),
    
        dbc.Collapse(
            dbc.Card(dbc.CardBody([
                
                dbc.ButtonGroup([dropdown_edad_area_tra,
                                 dropdown_genero_area_tra,
                                 dropdown_nivel_educativo_area_tra],
                                size="md", className="mb-3"),
                
                dcc.Graph(
                    id = 'grafico-area-trabajo',
                    figure = grafico_area_tra(df)
                )
            ])),
            id="collapse-area",
            is_open=False,
        ),
    
        dbc.Collapse(
            dbc.Card(dbc.CardBody([
                
                dbc.ButtonGroup([dropdown_edad_cargos,
                                 dropdown_genero_cargos,
                                 dropdown_nivel_educativo_cargos],
                                size="md", className="mb-3"),
                
                dcc.Graph(
                    id = 'grafico-cargos',
                    figure = grafico_cargos(df)
                )
            ])),
            id="collapse-cargos",
            is_open=False,
        ),

    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            
            dbc.ButtonGroup([dropdown_edad_genero,
                             dropdown_nivel_educativo_genero],
                            size="md", className="mb-3"),
            
            dcc.Graph(
                id = 'grafico-genero',
                figure = grafico_genero(df)
            )
        ])),
        id="collapse-genero",
        is_open=False,
    ),
    
    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            
            dbc.ButtonGroup([dropdown_genero_edad,
                             dropdown_nivel_educativo_edad],
                            size="md", className="mb-3"),
            
            dcc.Graph(
                id = 'grafico-edad',
                figure = grafico_edad(df)
            )
        ])),
        id="collapse-edad",
        is_open=False,
    ),

    
    dbc.Collapse(
    dbc.Card(dbc.CardBody([
        dbc.ButtonGroup([dropdown_edad_asistencia,
                         dropdown_genero_asistencia,
                         dropdown_empresa],
                        size="md", className="mb-3"),
        dcc.Graph(
            id = 'grafico-estado-asistencia',
            figure = grafico_estado_asistencia(df)
        )
    ])),
    id="collapse-asistencia",
    is_open=False,
    ),   
])

# ---------------------------------------------------------------

@app.callback(
    Output("collapse-competencia", "is_open"),
    [Input("collapse-button-competencia", "n_clicks")],
    [State("collapse-competencia", "is_open")],
)

def toggle_collapse_competencia(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output('grafico-competencia', 'figure'),
    [Input('grafico-competencia', 'id')]
)

def update_graph_competencia(id):
    return grafico_competencia(df)

#-----------------------------------

@app.callback(
    Output("collapse-cursos", "is_open"),
    [Input("collapse-button-cursos", "n_clicks")],
    [State("collapse-cursos", "is_open")],
)

def toggle_collapse_cursos(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    [Output('grafico-cursos', 'figure'), Output('dropdown-cursos', 'label')],
    [Input(f'dropdown-cursos-{i}', 'n_clicks') for i in ["Todos"] + list(df['INSTRUCTOR'].unique())]
)
def update_graph_cursos(*args):
    # Obtener el contexto del callback para saber qué entrada se activó
    ctx = callback_context

    # Si no se ha hecho clic en ningún DropdownMenuItem, devolver el gráfico actual sin cambios
    if not ctx.triggered:
        return dash.no_update

    # Obtener el ID de la entrada que se activó
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Extraer el instructor del ID de la entrada
    instructor = input_id.split('-')[-1]

    # Si el instructor es "Todos", no aplicar ningún filtro y mantener el label original
    if instructor == "Todos":
        return grafico_cursos(df, None), "Selecciona un instructor"
    else:
        return grafico_cursos(df, instructor), instructor

#-------------------------------------

@app.callback(
    Output("collapse-pais", "is_open"),
    [Input("collapse-button-pais", "n_clicks")],
    [State("collapse-pais", "is_open")],
)

def toggle_collapse_pais(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output('grafico-pais-nacimiento', 'figure'),
    [Input('grafico-pais-nacimiento', 'id')]
)

def update_graph_pais(id):
    return grafico_pais_nacimiento(df)

#-------------------------------------

@app.callback(
    Output("collapse-instructores", "is_open"),
    [Input("collapse-button-instructores", "n_clicks")],
    [State("collapse-instructores", "is_open")],
)
def toggle_collapse_instructores(n, is_open):
    if n:
        return not is_open
    return is_open

# Crear un callback para cada elemento del menú desplegable
@app.callback(
    [Output('grafico-instructores', 'figure'), Output('dropdown-instructores', 'label')],
    [Input(f'dropdown-instructores-{i}', 'n_clicks') for i in ["Todos"] + list(df['CURSO'].unique())]
)
def update_graph_instructores(*args):
    # Obtener el contexto del callback para saber qué entrada se activó
    ctx = callback_context

    # Si no se ha hecho clic en ningún DropdownMenuItem, devolver el gráfico actual sin cambios
    if not ctx.triggered:
        return dash.no_update

    # Obtener el ID de la entrada que se activó
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Extraer el curso del ID de la entrada
    curso = input_id.split('-')[-1]

    # Si el curso es "Todos", no aplicar ningún filtro y mantener el label original
    if curso == "Todos":
        return grafico_instructor(df, None), "Selecciona un curso"
    else:
        return grafico_instructor(df, curso), curso

#-------------------------------------

@app.callback(
    Output("collapse-nivel-educativo", "is_open"),
    [Input("collapse-button-nivel-educativo", "n_clicks")],
    [State("collapse-nivel-educativo", "is_open")],
)
def toggle_collapse_nivel_edu(n, is_open):
    if n:
        return not is_open
    return is_open

# Crear un callback para cada elemento del menú desplegable
@app.callback(
    [Output('grafico-nivel-educativo', 'figure'), Output('dropdown-edad-nivel-edu', 'label')],
    [Input(f'dropdown-edad-nivel-edu-{i}', 'n_clicks') for i in ["None", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70"]]
)
def update_graph_nivel_edu(*args):
    # Obtener el contexto del callback para saber qué entrada se activó
    ctx = dash.callback_context

    # Si no se ha hecho clic en ningún DropdownMenuItem, devolver el gráfico actual sin cambios y el label predeterminado
    if not ctx.triggered:
        return dash.no_update

    # Obtener el ID de la entrada que se activó
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Extraer el rango de edad del ID de la entrada
    rango_edad = input_id.split('-nivel-edu-')[-1]

    # Si rango_edad es 'None', devolver el gráfico sin filtrar y el label predeterminado
    if rango_edad == 'None':
        return grafico_nivel_edu(df, None), "Selecciona un rango de edad"
    else:
       return grafico_nivel_edu(df, rango_edad), rango_edad


#-------------------------------------

@app.callback(
    Output("collapse-empresas", "is_open"),
    [Input("collapse-button-empresas", "n_clicks")],
    [State("collapse-empresas", "is_open")],
)
def toggle_collapse_empresas(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    [Output('grafico-analisis-empresas', 'figure', allow_duplicate=True), 
     Output('store-edad', 'data', allow_duplicate=True), 
     Output('store-genero', 'data', allow_duplicate=True),
     Output('dropdown-edad-analisis-emp', 'label', allow_duplicate=True), 
     Output('dropdown-genero', 'label', allow_duplicate=True)],
    [Input(f'dropdown-edad-analisis-emp-{i}', 'n_clicks') for i in ["None", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70"]] +
    [Input(f'dropdown-genero-{i}', 'n_clicks') for i in ["None"] + list(df["GENERO"].unique())],
    [State('store-edad', 'data'), State('store-genero', 'data')],
    prevent_initial_call=True
)
def update_graph_empresas(*args):
    ctx = callback_context

    if not ctx.triggered:
        return dash.no_update

    input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    rango_edad = args[-2]
    genero = args[-1]

    if 'edad' in input_id:
        rango_edad = input_id.split('-emp-')[-1]
        if rango_edad == 'None':
            rango_edad = None
    elif 'genero' in input_id:
        genero = input_id.split('-genero-')[-1]
        if genero == 'None':
            genero = None

    # Si no se ha seleccionado un rango de edad o un género, se muestran todos los datos
    if rango_edad == "Selecciona un rango de edad":
        rango_edad = None
    if genero == "Selecciona un género":
        genero = None

    label_edad = rango_edad if rango_edad else "Selecciona un rango de edad"
    label_genero = genero if genero else "Selecciona un género"

    return grafico_analisis_emp(df, rango_edad, genero), rango_edad, genero, label_edad, label_genero

#-------------------------------------

@app.callback(
    Output("collapse-area", "is_open"),
    [Input("collapse-button-area", "n_clicks")],
    [State("collapse-area", "is_open")],
)
def toggle_collapse_area(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    [Output('grafico-area-trabajo', 'figure', allow_duplicate=True), 
     Output('store-edad-area-tra', 'data', allow_duplicate=True), 
     Output('store-genero-area-tra', 'data', allow_duplicate=True),
     Output('store-educativo-area-tra', 'data', allow_duplicate=True),
     Output('dropdown-edad-area-tra', 'label', allow_duplicate=True), 
     Output('dropdown-genero-area-tra', 'label', allow_duplicate=True),
     Output('dropdown-educativo-area-tra', 'label', allow_duplicate=True)],
    [Input(f'dropdown-edad-area-tra-{i}', 'n_clicks') for i in ["None", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70"]] +
    [Input(f'dropdown-genero-area-tra-{i}', 'n_clicks') for i in ["None"] + list(df["GENERO"].unique())] +
    [Input(f'dropdown-educativo-area-tra-{i}', 'n_clicks') for i in ["None"] + list(df["NIVEL EDUCATIVO"].unique())],
    [State('store-edad-area-tra', 'data'), State('store-genero-area-tra', 'data'), State('store-educativo-area-tra', 'data')],
    prevent_initial_call=True
)
def update_graph_area_tra(*args):
    ctx = callback_context

    if not ctx.triggered:
        return dash.no_update

    input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    rango_edad = args[-3]
    genero = args[-2]
    nivel_educativo = args[-1]

    if 'edad' in input_id:
        rango_edad = input_id.split('-edad-area-tra-')[-1]
        if rango_edad == 'None':
            rango_edad = None
    elif 'genero' in input_id:
        genero = input_id.split('-genero-area-tra-')[-1]
        if genero == 'None':
            genero = None
    elif 'educativo' in input_id:
        nivel_educativo = input_id.split('-educativo-area-tra-')[-1]
        if nivel_educativo == 'None':
            nivel_educativo = None

    label_edad = rango_edad if rango_edad else "Selecciona un rango de edad"
    label_genero = genero if genero else "Selecciona un género"
    label_educativo = nivel_educativo if nivel_educativo else "Selecciona un nivel educativo"

    return grafico_area_tra(df, rango_edad, genero, nivel_educativo), rango_edad, genero, nivel_educativo, label_edad, label_genero, label_educativo


#-------------------------------------

@app.callback(
    Output("collapse-cargos", "is_open"),
    [Input("collapse-button-cargos", "n_clicks")],
    [State("collapse-cargos", "is_open")],
)
def toggle_collapse_cargos(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    [Output('grafico-cargos', 'figure', allow_duplicate=True), 
     Output('store-edad-cargos', 'data', allow_duplicate=True), 
     Output('store-genero-cargos', 'data', allow_duplicate=True),
     Output('store-educativo-cargos', 'data', allow_duplicate=True),
     Output('dropdown-edad-cargos', 'label', allow_duplicate=True), 
     Output('dropdown-genero-cargos', 'label', allow_duplicate=True),
     Output('dropdown-educativo-cargos', 'label', allow_duplicate=True)],
    [Input(f'dropdown-edad-cargos-{i}', 'n_clicks') for i in ["None", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70"]] +
    [Input(f'dropdown-genero-cargos-{i}', 'n_clicks') for i in ["None"] + list(df["GENERO"].unique())] +
    [Input(f'dropdown-educativo-cargos-{i}', 'n_clicks') for i in ["None"] + list(df["NIVEL EDUCATIVO"].unique())],
    [State('store-edad-cargos', 'data'), State('store-genero-cargos', 'data'), State('store-educativo-cargos', 'data')],
    prevent_initial_call=True
)
def update_graph_cargos(*args):
    ctx = callback_context

    if not ctx.triggered:
        return dash.no_update

    input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    rango_edad = args[-3]
    genero = args[-2]
    nivel_educativo = args[-1]

    if 'edad' in input_id:
        rango_edad = input_id.split('-edad-cargos-')[-1]
        if rango_edad == 'None':
            rango_edad = None
    elif 'genero' in input_id:
        genero = input_id.split('-genero-cargos-')[-1]
        if genero == 'None':
            genero = None
    elif 'educativo' in input_id:
        nivel_educativo = input_id.split('-educativo-cargos-')[-1]
        if nivel_educativo == 'None':
            nivel_educativo = None

    label_edad = rango_edad if rango_edad else "Selecciona un rango de edad"
    label_genero = genero if genero else "Selecciona un género"
    label_educativo = nivel_educativo if nivel_educativo else "Selecciona un nivel educativo"

    return grafico_cargos(df, rango_edad, genero, nivel_educativo), rango_edad, genero, nivel_educativo, label_edad, label_genero, label_educativo

#-------------------------------------

@app.callback(
    Output("collapse-genero", "is_open"),
    [Input("collapse-button-genero", "n_clicks")],
    [State("collapse-genero", "is_open")],
)
def toggle_collapse_genero(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    [Output('grafico-genero', 'figure'), 
     Output('store-edad-genero', 'data'), 
     Output('store-educativo-genero', 'data'),
     Output('dropdown-edad-genero', 'label'), 
     Output('dropdown-educativo-genero', 'label')],
    [Input(f'dropdown-edad-genero-{i}', 'n_clicks') for i in ["None", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70"]] +
    [Input(f'dropdown-educativo-genero-{i}', 'n_clicks') for i in ["None"] + list(df["NIVEL EDUCATIVO"].unique())],
    [State('store-edad-genero', 'data'), State('store-educativo-genero', 'data')],
    prevent_initial_call=True
)
def update_graph_genero(*args):
    ctx = callback_context

    if not ctx.triggered:
        return dash.no_update

    input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    rango_edad = args[-2]
    nivel_educativo = args[-1]

    if 'edad' in input_id:
        rango_edad = input_id.split('-edad-genero-')[-1]
        if rango_edad == 'None':
            rango_edad = None
    elif 'educativo' in input_id:
        nivel_educativo = input_id.split('-educativo-genero-')[-1]
        if nivel_educativo == 'None':
            nivel_educativo = None

    label_edad = rango_edad if rango_edad else "Selecciona un rango de edad"
    label_educativo = nivel_educativo if nivel_educativo else "Selecciona un nivel educativo"

    return grafico_genero(df, rango_edad, nivel_educativo), rango_edad, nivel_educativo, label_edad, label_educativo

#-------------------------------------

@app.callback(
    Output("collapse-edad", "is_open"),
    [Input("collapse-button-edad", "n_clicks")],
    [State("collapse-edad", "is_open")],
)
def toggle_collapse_edad(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    [Output('grafico-edad', 'figure'), 
     Output('store-genero-edad', 'data'), 
     Output('store-educativo-edad', 'data'),
     Output('dropdown-genero-edad', 'label'), 
     Output('dropdown-educativo-edad', 'label')],
    [Input(f'dropdown-genero-edad-{i}', 'n_clicks') for i in ["None"] + list(df["GENERO"].unique())] +
    [Input(f'dropdown-educativo-edad-{i}', 'n_clicks') for i in ["None"] + list(df["NIVEL EDUCATIVO"].unique())],
    [State('store-genero-edad', 'data'), State('store-educativo-edad', 'data')],
    prevent_initial_call=True
)
def update_graph_edad(*args):
    ctx = callback_context

    if not ctx.triggered:
        return dash.no_update, "Selecciona un género", "Selecciona un nivel educativo", "Selecciona un género", "Selecciona un nivel educativo"

    input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    genero = args[-2]
    nivel_educativo = args[-1]

    if 'genero' in input_id:
        genero = input_id.split('-genero-edad-')[-1]
        if genero == 'None':
            genero = None
    elif 'educativo' in input_id:
        nivel_educativo = input_id.split('-educativo-edad-')[-1]
        if nivel_educativo == 'None':
            nivel_educativo = None

    label_genero = genero if genero else "Selecciona un género"
    label_educativo = nivel_educativo if nivel_educativo else "Selecciona un nivel educativo"

    return grafico_edad(df, genero, nivel_educativo), genero, nivel_educativo, label_genero, label_educativo

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# Esta es una de las devoluciones de llamada en Dash.

# En Dash, una devolución de llamada es una función que se ejecuta en respuesta
# a algún tipo de evento o cambio en los datos de entrada. 

# Esta devolución de llamada se activará cuando el número de clics
# en el botón “collapse-button-asistencia” cambie.

# La devolución de llamada actualizará el estado de “is_open” del
# componente “collapse-asistencia”.


@app.callback(
    Output("collapse-asistencia", "is_open"),
    [Input("collapse-button-asistencia", "n_clicks")],
    [State("collapse-asistencia", "is_open")],
)

# Esta es la definición de la función que se ejecutará cuando
# se active la devolución de llamada.

# Toma dos argumentos:
# n, que es el número de clics en el botón,
# e is_open, que es el estado actual de “is_open” del componente “collapse-asistencia”.


def toggle_collapse_asistencia(n, is_open): # <------------------
    if n:
        return not is_open
    return is_open


# Si el botón ha sido presionado (o sea, n no es None),
# entonces la función devuelve el valor opuesto al estado actual de “is_open”.

# Si el botón no ha sido presionado, la función devuelve el estado actual de “is_open”.
# Esto tiene el efecto de alternar el estado de “is_open” cada vez que se presiona el botón.


#-----------------

# Esta devolución de llamada se activará cuando el número de clics
# en cualquiera de los menús desplegables cambie. 

# La devolución de llamada actualizará el gráfico ‘grafico-estado-asistencia’, los componentes de
# almacenamiento ‘store-edad-asistencia’, ‘store-genero-asistencia’, ‘store-empresa’,
# y las etiquetas de los menús desplegables.



@app.callback(
    [Output('grafico-estado-asistencia', 'figure'), 
     Output('store-edad-asistencia', 'data'), 
     Output('store-genero-asistencia', 'data'),
     Output('store-empresa', 'data'),
     Output('dropdown-edad-asistencia', 'label'), 
     Output('dropdown-genero-asistencia', 'label'),
     Output('dropdown-empresa', 'label')],
    [Input(f'dropdown-edad-asistencia-{i}', 'n_clicks') for i in ["None", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70"]] +
    [Input(f'dropdown-genero-asistencia-{i}', 'n_clicks') for i in ["None"] + list(df["GENERO"].unique())] +
    [Input(f'dropdown-empresa-{i}', 'n_clicks') for i in ["None"] + [i.replace(".", "-") for i in empresas_por_frecuencia]],
    [State('store-edad-asistencia', 'data'),
     State('store-genero-asistencia', 'data'),
     State('store-empresa', 'data')],
    prevent_initial_call=True
)

# Esta es la definición de la función que
# se ejecutará cuando se active la devolución de llamada.

# La función update_graph_asistencia se
# ejecuta cuando cambia el número de clics en los menús desplegables.

# Toma un número variable de argumentos, que son los valores actuales de los menús
# desplegables y los componentes de almacenamiento.

# En Python, puedes definir una función que tome un número variable de argumentos utilizando el operador *.
# En este caso, *args es una lista de argumentos que se pasan a la función.
# El número de argumentos puede variar cada vez que se llama a la función.

def update_graph_asistencia(*args): # <-----------------------------
    
    ctx = callback_context  # Esta línea obtiene el contexto de la devolución de llamada actual,
                            # que contiene información sobre qué entrada activó la devolución de llamada.

    if not ctx.triggered:                 # Si no se activó ninguna entrada
        return dash.no_update             # (es decir, esta es la primera vez que se ejecuta la devolución de llamada),
                                          # la función devuelve dash.no_update,
                                          # lo que significa que no se deben actualizar los componentes de salida.
    

    # Estas líneas obtienen el ID de la entrada que
    # activó la devolución de llamada y los valores actuales
    # de los componentes de almacenamiento.
    
    
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]        # Esta línea obtiene el ID de la entrada que
                                                                # activó la devolución de llamada.
                                                                
                                                                # ctx.triggered[0]['prop_id'] devuelve una cadena que
                                                                # contiene el ID de la entrada y la propiedad de la entrada
                                                                # que cambió, separados por un punto.
                                                                # 
                                                                # Por ejemplo, podría ser algo como
                                                                # ‘dropdown-empresa-10-20.n_clicks’.
                                                                # 
                                                                # La función split('.')[0] divide esta cadena en el
                                                                # punto y toma la primera parte, que es el ID de la entrada.
    
    
    # Estas líneas obtienen los valores actuales de los componentes de almacenamiento.
    # args es una lista de argumentos que se pasaron a la función.
    
    # Los argumentos son los valores actuales de los menús desplegables y
    # los componentes de almacenamiento. 
    
    # args[-3], args[-2], y args[-1]
    # obtienen los últimos tres elementos de la lista,
    # que son los valores actuales de los componentes de almacenamiento para
    # el rango de edad, el género y la empresa, respectivamente.
    
    
    rango_edad = args[-3]
    genero = args[-2]
    empresa = args[-1]

    
    # Estas líneas de código están verificando si la cadena ‘edad’ está en input_id,
    # que es el ID de la entrada que activó la devolución de llamada.
    
    # Si ‘edad’ está en input_id, entonces se asume que el menú desplegable de edad
    # fue el que activó la devolución de llamada.

    # La segunda línea divide input_id en la cadena ‘-edad-asistencia-’
    # y toma la última parte, que se asume que es el rango de edad seleccionado.
    
    # Por ejemplo, si input_id es ‘dropdown-edad-asistencia-10-20’,
    # entonces rango_edad será ‘10-20’.

    # La tercera línea verifica si rango_edad es ‘None’,
    # lo que indicaría que se seleccionó la opción “None” en el menú desplegable.
    
    # Si es así, se establece rango_edad en None.
    


    if 'edad' in input_id:
        rango_edad = input_id.split('-edad-asistencia-')[-1]
        if rango_edad == 'None':
            rango_edad = None
    elif 'genero' in input_id:
        genero = input_id.split('-genero-asistencia-')[-1]
        if genero == 'None':
            genero = None
    elif 'empresa' in input_id:
        empresa = input_id.split('-empresa-')[-1].replace("-", ".")
        if empresa == 'None':
            empresa = None
     
    
    # Estas líneas crean las etiquetas para los menús desplegables
    # basándose en los valores actuales de los componentes de almacenamiento.
    
           
    label_edad = rango_edad if rango_edad else "Selecciona un rango de edad"
    label_genero = genero if genero else "Selecciona un género"
    label_empresa = empresa if empresa else "Selecciona una empresa"

    
    # Finalmente, la función devuelve el gráfico actualizado,
    # los valores actualizados de los componentes de almacenamiento
    # y las etiquetas de los menús desplegables.
    

    return grafico_estado_asistencia(df, rango_edad, genero, empresa), rango_edad, genero, empresa, label_edad, label_genero, label_empresa

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

if __name__=='__main__':
    app.run_server(debug=False)