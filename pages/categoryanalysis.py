import dash
from dash import html, dcc, dash_table, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dash_table import FormatTemplate

dash.register_page(__name__, path="/productanalysis", title='Product Analysis', name='Product Analysis')

superstore = pd.read_csv('data/Superstore.csv', encoding='latin1')

# Country Distribution

countryquantity = superstore.groupby('Country')['Quantity'].sum().reset_index()

countryquantitydistribution = px.scatter_geo(countryquantity, locations = countryquantity['Country'],
                                            locationmode = "country names",
                                            size = countryquantity.groupby("Country")['Quantity'].sum().values,
                                            color = countryquantity.groupby("Country")['Quantity'].sum().values,
                                            projection = "natural earth", color_continuous_scale = "magma_r")

countryquantitydistribution.update_layout(paper_bgcolor = "rgba(0,0,0,0)",
                                          geo = dict(
                                            bgcolor = "rgba(0,0,0,0)",
                                            landcolor = 'slategrey', showcountries = True,
                                            showcoastlines = True
                                          ))

countryquantitydistribution.update_geos(showframe = True)

countryquantitydistribution.update_coloraxes(colorbar_title = "Quantity Sold", colorbar_title_font_color = 'White', colorbar_tickfont = dict(color = 'white'))


# Product Trend

superstore['Order Date'] = pd.to_datetime(superstore['Order Date'], format = "%m/%d/%Y")

monthlycategorytrend = superstore.groupby(['Category', pd.Grouper(key = "Order Date", freq = 'ME')])['Quantity'].sum().reset_index()

monthlycategorytrenddistribution = px.line(monthlycategorytrend, x = "Order Date", y = "Quantity", color = 'Category',
                                           title = 'Monthly Trend of Goods Sold', line_shape = "spline")

monthlycategorytrenddistribution.update_layout(yaxis = dict(showticklabels = False), 
                                       xaxis = dict(tickfont = dict(color = 'white'), categoryorder = "total descending"),
                                       yaxis_title = "", xaxis_title = "",
                                       paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
                                       title = dict(font = dict(color = 'white')),
                                       legend_title_font_color = 'White', legend_font_color = 'White')

monthlycategorytrenddistribution.update_yaxes(showgrid = False, gridcolor = 'rgba(0,0,0,0)', zeroline = False, zerolinecolor = "rgba(0, 0, 0, 0)")
monthlycategorytrenddistribution.update_xaxes(showgrid = False, gridcolor = 'rgba(0,0,0,0)', zeroline = False, zerolinecolor = "rgba(0, 0, 0, 0)")

# Products Table

products_table = dash_table.DataTable(
   data = superstore.to_dict('records'), 
   id = "tweets-table",
   columns=[
      {"name": "Product ID", "id": "Product ID", 'type': 'text', 'presentation' : 'input'},
      {"name": "Category", "id": "Category"},
      {"name": "Sub-Category", "id": "Sub-Category"},
      {"name": "Product Name", "id": "Product Name"},
      {"name": "Profit", "id": "Profit", "type": 'numeric', "format" :FormatTemplate.money(2)}
   ],
   page_size = 10,
   style_data={
      'whiteSpace': 'normal',
      'backgroundColor': 'transparent',
      'color': 'white',
      'margin': '10px 0',
      'height': 80
   },
   filter_action="native",
   filter_options={
      "placeholder_text" : "Search for a value"
   },
   style_filter={"backgroundColor" : "transparent", "color" : "#cba052", 'textAlign': 'left'},
   sort_action="native",
   style_header={
      'backgroundColor': 'transparent', "color" : "#cba052"
   },
   style_cell_conditional=[
      {'if': {'column_id': 'Product ID'}, 'textAlign' : "center", 'width': '15%'},
      {'if': {'column_id': 'Category'}, 'textAlign' : "center", 'width': '10%'},
      {'if': {'column_id': 'Sub-Category'}, 'textAlign' : "center", 'width': '15%'},
      {'if': {'column_id': 'Product Name'}, 'textAlign' : "right", 'width': '50%'},
      {'if': {'column_id': 'Profit'}, 'textAlign' : "right", 'width': '10%'},
   ],
   style_cell={'textAlign': 'left', 'backgroundColor': 'transparent', 'font-family': 'Arial'},
   style_as_list_view=True,
   css=[{'selector': '::placeholder', 'rule': 'color: #cba052;'}]  
)

# Layout
layout = html.Div(
   children=[
      dbc.Row(
         dcc.Dropdown(superstore['Segment'].unique(), id = "segment_dropdown", placeholder = "Select a Segment")
      ),
      dbc.Row(
         children = [
            dbc.Col(
               dcc.Graph(id="category_quantity_distribution", responsive = True)
            ),
            dbc.Col(
               dcc.Graph(id ="category_subcategory_distribution", responsive = True)
            ),
            dbc.Col(
               dcc.Graph(id="city_quantity_percentage_distribution", responsive = True)
            ),
         ]
      ),
      dbc.Row(
         children = [
            dbc.Col(
               dcc.Graph(figure=countryquantitydistribution, responsive = False)
            ),
            dbc.Col(
               dcc.Graph(id="city_quantity_distribution", responsive = False)
            ),
         ]
      ),
      dbc.Row(
         dcc.Graph(figure=monthlycategorytrenddistribution, responsive = True)
      ),
      dbc.Row(
         products_table
      )
   ],
)

@callback(
   Output('category_quantity_distribution', 'figure'),
   Output('category_subcategory_distribution', 'figure'),
   Output('city_quantity_percentage_distribution', 'figure'),
   Input('segment_dropdown', 'value')
,)

def multiple_outputs_single_input(segment_value):
   if(segment_value):
      superstore_segment_filter = superstore[superstore['Segment'] == segment_value]
      categoryquantity = superstore_segment_filter.groupby('Category')['Quantity'].sum()
      categorysubcategoryquantity = superstore_segment_filter.groupby(['Category', 'Sub-Category'])['Quantity'].sum().reset_index()
      cityquantitygrouped = superstore_segment_filter.groupby("City")['Quantity'].sum().nlargest(3)
      cityquantitypercentage = superstore_segment_filter['Quantity'].sum()
   else:
      categoryquantity = superstore.groupby('Category')['Quantity'].sum()
      categorysubcategoryquantity = superstore.groupby(['Category', 'Sub-Category'])['Quantity'].sum().reset_index()
      cityquantitygrouped = superstore.groupby("City")['Quantity'].sum().nlargest(3)
      cityquantitypercentage = superstore['Quantity'].sum()
   
   # Total Sold

   categoryquantitydistribution = px.pie(names=categoryquantity.index,
                                       values=categoryquantity.values,
                                       hole=0.7,
                                       color_discrete_sequence=px.colors.qualitative.Dark24_r)

   categoryquantitydistribution.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)",
                                             legend_font_color='white', title=dict(font=dict(color='white')))

   totalquantitysold = '{:,}'.format(categoryquantity.sum())
   categoryquantitydistribution.add_annotation(text="Total Sold", showarrow=False,
                                             font_size=14, font_color='White',
                                             y=0.55)
   categoryquantitydistribution.add_annotation(text=totalquantitysold, showarrow=False,
                                             font_size=14, font_color='White', y=0.45)
   
   # Sub-Category Distribution
   categorysubcategorydistribution = px.sunburst(categorysubcategoryquantity, path=['Category', 'Sub-Category'],
                                                values='Quantity')

   categorysubcategorydistribution.update_layout(paper_bgcolor='rgba(0,0,0,0)')

   categorysubcategorydistribution.update_traces(marker=dict(colors=px.colors.qualitative.Dark24))
   
 # City PercentageDistribution

   cityquantitygroupedsum = cityquantitygrouped.sum()
   percentagedistribution = (cityquantitygrouped / cityquantitypercentage) * 100
   percentagelabels = [f"{city} : {percentage : .2f}%" for city, percentage in
                     zip(cityquantitygrouped.index, percentagedistribution)]

   cityquantitypercentagedistribution = px.pie(names=percentagelabels,
                                             values=cityquantitygrouped.values,
                                             hole=0.7,
                                             color_discrete_sequence=px.colors.qualitative.Dark24_r)

   cityquantitypercentagedistribution.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)",
                                                   legend_font_color='white',
                                                   title=dict(font=dict(color='white')))

   cityquantitypercentagedistribution.add_annotation(text="Top 3 Cities", showarrow=False,
                                                   font_size=13, font_color='White',
                                                   y=0.6)

   cityquantitypercentagedistribution.add_annotation(text="Total Sold", showarrow=False,
                                                   font_size=13, font_color='White',
                                                   y=0.5)

   cityquantitypercentagedistribution.add_annotation(text='{:,}'.format(cityquantitygroupedsum), showarrow=False,
                                                   font_size=13, font_color='White', y=0.4)
   
   return categoryquantitydistribution, categorysubcategorydistribution, cityquantitypercentagedistribution

@callback(
   Output('city_quantity_distribution', 'figure'),
   Input('category_quantity_distribution', 'clickData')
)
def interactive_cross_filtering(clicked_category_value):
   if (clicked_category_value):
      superstore_category_filtered = superstore[superstore['Category'] == clicked_category_value['points'][0]['label']]
      cityquantity = superstore_category_filtered.groupby(['City', 'Sub-Category'])['Quantity'].sum().reset_index()
   else:
      cityquantity = superstore.groupby(['City', 'Sub-Category'])['Quantity'].sum().reset_index()
   
   # City Distribution 

   cityquantitytop5 = cityquantity.groupby('City')['Quantity'].sum().nlargest(3).index
   cityquantitytop5final = cityquantity[cityquantity['City'].isin(cityquantitytop5)]

   cityquantitydistribution = px.bar(cityquantitytop5final, x = "City", y = "Quantity",
                                    color = 'Sub-Category', barmode = 'group',
                                    text = 'Quantity', color_discrete_sequence = px.colors.qualitative.Dark24_r)

   cityquantitydistribution.update_layout(yaxis = dict(showticklabels = False), 
                                          xaxis = dict(tickfont = dict(color = 'white'), categoryorder = "total descending"),
                                          yaxis_title = "", xaxis_title = "",
                                          paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
                                          legend_title_font_color = 'White', legend_font_color = 'White', bargap = 0.1)

   cityquantitydistribution.update_yaxes(showgrid = False, gridcolor = 'rgba(0,0,0,0)', zeroline = False, zerolinecolor = "rgba(0, 0, 0, 0)")

   cityquantitydistribution.update_traces(marker_line_width = 0, textposition = "outside", textfont_color = 'white', textfont_size = 14, cliponaxis = False)

   return cityquantitydistribution