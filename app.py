# DASH: Seminario de progrmación
## SECOP II - Contratos Electrónicos - ACTIVOS

from sodapy import Socrata
import pandas as pd
import numpy as np
from app import dcc, dash, html, Input, Output
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Base de datos de SECOP II  Contratos Electrónicos - ACTIVOS.
 
client = Socrata("www.datos.gov.co", None,timeout=200000)

query="""
SELECT nombre_entidad as Entidad,
            departamento as Departamento,
            nit_entidad as NIT,
            valor_del_contrato as Valor,
            objeto_del_contrato as Objeto,
            tipo_de_contrato as Tipo,
            ciudad as Municipio,
            fecha_de_firma as Fecha
"""

results = client.get("jbjy-vk9h", query=query)


DF_contratos=pd.DataFrame(results)
DF_contratos.dtypes

DF_contratos['Valor']=DF_contratos['Valor'].astype(float)

# Creación del dash que permite la visualización de la distribución de contratos públicos 
#  en Colombia según el departamento.

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H4("Análisis de Contratos Públicos"),
        html.P("Departamento:"),
        dcc.Dropdown(
            id="departamento",
            options=[{"label": dep, "value": dep} for dep in DF_contratos["Departamento"].unique()],
            value=DF_contratos["Departamento"].iloc[0],
        ),
        dcc.Graph(id="dist-contratos-municipio"),
    ]
)

@app.callback(
    Output("dist-contratos-municipio", "figure"),
    Input("departamento", "value"),
)
def display_dist_contratos_municipio(departamento):
    df = DF_contratos[DF_contratos["Departamento"] == departamento]
    fig = px.bar(df, x="Municipio", title=f"Distribución de Contratos en {departamento}",
    )
    fig.update_xaxes(title_text="Municipio")
    fig.update_yaxes(title_text="Cantidad de Contratos")
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
