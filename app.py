# .venv/Scripts/activate
import dash
from dash import Dash,html,dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title = "Superstore Analysis", use_pages = True)

sidebar = html.Div(
    children = [
        html.Div(
            children = dcc.Link(f"{page['name']}", href = page["relative_path"])
        ) for page in dash.page_registry.values()
    ],
)

app.layout = html.Div(
    children = [
        dbc.Row(
            children = [
                dbc.Col(
                    children = sidebar,
                    width = 1
                    
                ),
                dbc.Col(
                    children = [
                        dash.page_container
                    ]
                )
            ]
        )
    ],
    className = "bg-black"
)

if __name__ == '__main__':
    app.run(debug = True, use_reloader = True)