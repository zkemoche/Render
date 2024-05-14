import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dash_table import FormatTemplate
import dash_ag_grid as dag

dash.register_page(__name__, path="/salesanalysis", title='Sales Profit Analysis', name='Sales Profit Analysis')

superstore = pd.read_csv('data/Superstore.csv', encoding='latin1')

superstore['Order Date'] = pd.to_datetime(superstore['Order Date'], format = "%m/%d/%Y")


# Profit by Segment

categoryprofit = superstore.groupby('Category')['Profit'].sum()
categoryprofitdistribution = px.pie(names = categoryprofit.index, 
                                      values = categoryprofit.values,
                                      hole = 0.7,
                                      color_discrete_sequence = px.colors.qualitative.Dark24_r)

categoryprofitdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                           legend_font_color = 'white')

totalprofit = '${:,}'.format(round(categoryprofit.sum(), 2))
categoryprofitdistribution.add_annotation(text = "Total Profit by Category", showarrow = False,
                                            font_size = 14, font_color = 'White',
                                            y = 0.55)
categoryprofitdistribution.add_annotation(text = totalprofit, showarrow = False,
                                            font_size = 14, font_color = 'White', y = 0.45)


# Category and Sub-Category Sales by Segment

categorysegmentsales = superstore.groupby(['Segment', 'Category', 'Sub-Category'])['Sales'].sum().reset_index()

categorysegmentsalesdistribution = px.sunburst(categorysegmentsales, path = ['Segment', 'Category', 'Sub-Category'], values = 'Sales', color_discrete_sequence=px.colors.qualitative.Dark24_r)

categorysegmentsalesdistribution.update_layout(paper_bgcolor = 'rgba(0,0,0,0)')

categorysegmentsalesdistribution.update_traces(marker = dict(colors = px.colors.qualitative.Dark24_r))


# Top n customer sales over years

totalsalesbycustomer = superstore.groupby(['Customer Name', 'Order Date'])['Sales'].sum().reset_index()

totalsalesbycustomer = totalsalesbycustomer.groupby('Customer Name')['Sales'].sum().reset_index()

top5customersbysales = totalsalesbycustomer.nlargest(5, 'Sales')['Customer Name']

filteredtop5 = superstore[superstore['Customer Name'].isin(top5customersbysales)]

totalsalesovertimetop5 = filteredtop5.groupby(['Customer Name', filteredtop5['Order Date'].dt.year])['Sales'].sum().reset_index()
totalsalesovertimetop5['Order Date'] = pd.to_datetime(totalsalesovertimetop5['Order Date'], format = "%Y")

totalsalesovertimetop5distribution = px.area(totalsalesovertimetop5, x = 'Order Date', y = "Sales", color = "Customer Name", title = "Customer Sales Over Years")

totalsalesovertimetop5distribution.update_layout(plot_bgcolor = 'rgba(0,0,0,0)', paper_bgcolor = "rgba(0,0,0,0)",
                                                  legend_font_color = 'white', title_font = dict(color = "white"),
                                                  xaxis = dict(title = "Order Date", color = "white"),
                                                  yaxis = dict(title = "Total Sales", color = "white"),
                                                  )

totalsalesovertimetop5distribution.update_xaxes(showgrid = False)
totalsalesovertimetop5distribution.update_yaxes(showgrid = False)


# Top 5 customer profit over years

totalprofitbycustomer = superstore.groupby(['Customer Name', 'Order Date'])['Profit'].sum().reset_index()

totalprofitbycustomer = totalprofitbycustomer.groupby('Customer Name')['Profit'].sum().reset_index()

top5customersbyprofit = totalprofitbycustomer.nlargest(5, 'Profit')['Customer Name']

filteredtop5 = superstore[superstore['Customer Name'].isin(top5customersbyprofit)]

totalprofitovertimetop5 = filteredtop5.groupby(['Customer Name', filteredtop5['Order Date'].dt.year])['Profit'].sum().reset_index()
totalprofitovertimetop5['Order Date'] = pd.to_datetime(totalprofitovertimetop5['Order Date'], format = "%Y")

totalprofitovertimetop5distribution = px.area(totalprofitovertimetop5, x = 'Order Date', y = "Profit", color = "Customer Name", title = "Customer Profit Over Years")

totalprofitovertimetop5distribution.update_layout(plot_bgcolor = 'rgba(0,0,0,0)', paper_bgcolor = "rgba(0,0,0,0)",
                                                  legend_font_color = 'white', title_font = dict(color = "white"),
                                                  xaxis = dict(title = "Order Date", color = "white"),
                                                  yaxis = dict(title = "Total Profit", color = "white"),
                                                  )

totalprofitovertimetop5distribution.update_xaxes(showgrid = False)
totalprofitovertimetop5distribution.update_yaxes(showgrid = False)


# Sales and Quantity by Segment

salesquantity = superstore.groupby(['Segment']).agg(
                      {"Sales" : 'sum', 'Quantity' : 'sum'}  
                    ).reset_index()

salesquantitydist = px.bar(salesquantity, x="Segment", y="Sales", title='Quantity and Sales by Segment', text_auto='', color_discrete_sequence=px.colors.qualitative.Dark24_r)

salesquantitydist.update_layout(title=dict(font=dict(color='white')), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                       xaxis=dict(title=dict(font=dict(color='white')), tickfont=dict(color='white')),
                       yaxis=dict(showticklabels=False), yaxis_title='', xaxis_title = '')

salesquantitydist.update_yaxes(showgrid=False, gridcolor='rgba(255, 255, 255, 0.2)', zeroline=True, zerolinecolor='rgba(0, 0, 0, 0)')

salesquantitydist.update_traces(marker_line_width=0, textfont_size=12, textfont_color='white', textangle=0, texttemplate='%{y:,}', textposition="outside", cliponaxis=False)

segmentsales = px.line(salesquantity, x= 'Segment', y='Quantity')

salesquantitydist.update_traces(marker_line_width=0, textfont_size=12, textfont_color='white', textangle=0, texttemplate='%{y:,}', textposition="outside", cliponaxis=False)

salesquantitydist.add_trace(segmentsales.data[0])


# Products Table AG Grid
products_table_ag_grid = dag.AgGrid(
   rowData = superstore.to_dict('records'),
   id = "products-table",
   columnDefs=[
      {"field":"Product ID", 'filter': True},
      {"field":"Customer Name", 'headerName':'Customer', 'filter': True},
      {"field":"Segment", 'filter': True},
      {"field":"City", 'filter': True},
      {"field":"Category", 'filter': True},
      {"field":"Profit", 'filter': True},
      
   ],
   className="ag-theme-alpine-dark",
            columnSize="sizeToFit",
            dashGridOptions={'pagination':True},
)


# Layout
layout = html.Div(
   children=[
      dbc.Row(
         children = [
            dbc.Col(
                  dcc.Dropdown(
                     superstore['City'].unique(),
                     id = "city_dropdown",
                     placeholder = "Choose a City",
                     style = {
                        'background-color' : 'black',
                        'border-radius' : '2px'
                     },
                  )
            ),
            dbc.Col(
                  dcc.RadioItems(
                     superstore['Region'].unique(),
                     id = "region_radio_items",
                     inline=True,
                     className="d-flex justify-content-evenly text-light"
                  )
            )
         ]
      ),
      dbc.Row(
         children = [
            html.H1('Sales', className='text-light'),
            html.Hr(),
            dbc.Col(
               dbc.Row(
                  children = [
                     dbc.Col(
                        dcc.Graph(id = "sales_category_distribution", responsive = True)
                     ),
                     dbc.Col(
                        dcc.Graph(id = "sales_category_subcategory_distribution", responsive = True)
                     )
                  ]
               )
            ),
            dbc.Col(
               dbc.Row(
                  children = [
                     html.H6('By Segment', className = 'text-light'),
                     dbc.Col(
                        dcc.Graph(id = "total_sales_by_segment", responsive = True)
                     ),
                     dbc.Col(
                        dcc.Graph(figure=categorysegmentsalesdistribution)
                     )
                  ]
               ),
               className="border border-warning"
            ),
         ]
      ),
      dbc.Row(
         children = [
            dbc.Col(
               dcc.Graph(figure=totalsalesovertimetop5distribution, responsive = True)
            ),
            dbc.Col(
                  dcc.Graph(figure = totalprofitovertimetop5distribution, responsive = True)
            ),
         ]
      ),
      dbc.Row(
         children = [
            dbc.Col(
               dcc.Graph(figure=salesquantitydist, responsive = True)
            )
         ]
      ),
      dbc.Row(
         products_table_ag_grid
      )
   ],
)

@callback(
   Output("sales_category_distribution", "figure"),
   Input('city_dropdown', 'value'),
   Input('region_radio_items', 'value'),
)

def update_sales_category_distribution(city_value, region_value):
   if city_value or region_value:
      city_filter_superstore = superstore[(superstore['City'] == city_value) | (superstore['Region'] == region_value)]
      
      # Sales by Category
      categorysales = city_filter_superstore.groupby('Category')['Sales'].sum()
   else:
      # Sales by Category
      categorysales = superstore.groupby('Category')['Sales'].sum()

   categorysalesdistribution = px.pie(names = categorysales.index, 
                                       values = categorysales.values,
                                       hole = 0.7,
                                       color_discrete_sequence = px.colors.qualitative.Dark24_r)

   categorysalesdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                          legend_font_color = 'white', title = dict(font = dict(color = 'white')))

   totalsales = '${:,}'.format(round(categorysales.sum(), 2))
   categorysalesdistribution.add_annotation(text = "Total Sales by Category", showarrow = False,
                                             font_size = 14, font_color = 'White',
                                             y = 0.55)
   categorysalesdistribution.add_annotation(text = totalsales, showarrow = False,
                                             font_size = 14, font_color = 'White', y = 0.45)
   
   return categorysalesdistribution

@callback(
   Output('sales_category_subcategory_distribution', 'figure'),
   Input('city_dropdown', 'value'),
)
def update_sales_category_subcategory_distribution(city_value):
   if city_value:
      city_filter_superstore = superstore[(superstore['City'] == city_value)]

      # Sales by Category and Sub-Category
      
      categorysubcategorysales = city_filter_superstore.groupby(['Category', 'Sub-Category'])['Sales'].sum().reset_index()

      categorysubcategorysalesdistribution = px.sunburst(categorysubcategorysales, path = ['Category', 'Sub-Category'], values = 'Sales')

      categorysubcategorysalesdistribution.update_layout(paper_bgcolor = 'rgba(0,0,0,0)')

      categorysubcategorysalesdistribution.update_traces(marker = dict(colors = px.colors.qualitative.Dark24))
   else:
      # Sales by Category and Sub-Category
      
      categorysubcategorysales = superstore.groupby(['Category', 'Sub-Category'])['Sales'].sum().reset_index()

      categorysubcategorysalesdistribution = px.sunburst(categorysubcategorysales, path = ['Category', 'Sub-Category'], values = 'Sales')

      categorysubcategorysalesdistribution.update_layout(paper_bgcolor = 'rgba(0,0,0,0)')

      categorysubcategorysalesdistribution.update_traces(marker = dict(colors = px.colors.qualitative.Dark24))

   return categorysubcategorysalesdistribution

@callback(
   Output('total_sales_by_segment', 'figure'),
   Input('sales_category_distribution', 'clickData'),
)
def update_total_sales_by_segment(click_value):
   if click_value:
      city_filter_superstore = superstore[superstore['Category'] == click_value['points'][0]['label']]

      # Sales by Segment
      segmentsales = city_filter_superstore.groupby('Segment')['Sales'].sum()
      segmentsalesdistribution = px.pie(names = segmentsales.index, 
                                          values = segmentsales.values,
                                          hole = 0.7,
                                          color_discrete_sequence = px.colors.qualitative.Dark24_r)

      segmentsalesdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                                legend_font_color = 'white', title = dict(font = dict(color = 'white')))

      totalsales = '${:,}'.format(round(segmentsales.sum(), 2))
      segmentsalesdistribution.add_annotation(text = "Total Sales by Segment", showarrow = False, font_color = 'White',
                                                y = 0.55)
      segmentsalesdistribution.add_annotation(text = totalsales, showarrow = False, font_color = 'White', y = 0.45)
   else:
      segmentsales = superstore.groupby('Segment')['Sales'].sum()
      segmentsalesdistribution = px.pie(names = segmentsales.index, 
                                          values = segmentsales.values,
                                          hole = 0.7,
                                          color_discrete_sequence = px.colors.qualitative.Dark24_r)

      segmentsalesdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                                legend_font_color = 'white', title = dict(font = dict(color = 'white')))

      totalsales = '${:,}'.format(round(segmentsales.sum(), 2))
      segmentsalesdistribution.add_annotation(text = "Total Sales by Segment", showarrow = False, font_color = 'White',
                                                y = 0.55)
      segmentsalesdistribution.add_annotation(text = totalsales, showarrow = False, font_color = 'White', y = 0.45)
   
   return segmentsalesdistribution