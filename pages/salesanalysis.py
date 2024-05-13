import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__, path = "/salesanalysis", title = "Category Analysis")
superstore = pd.read_csv("data/Superstore.csv", encoding = "latin1")
superstore["Order Date"]=pd.to_datetime(superstore["Order Date"], format="%m/%d/%Y")


categorysales = superstore.groupby('Category')['Sales'].sum()

segmentsales = superstore.groupby('Segment')['Sales'].sum()
segment_sales_distribution = px.pie(names = segmentsales.index, 
                                      values = categorysales.values,
                                      hole = 0.8,
                                      color_discrete_sequence = px.colors.qualitative.Dark24_r)

segment_sales_distribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                           legend_font_color = 'white', title = dict(font = dict(color = 'white')))

totalsales = '${:,}'.format(round(segmentsales.sum(), 2))
segment_sales_distribution.add_annotation(text = "Total Sales by Segment", showarrow = False,
                                            font_size = 11.5, font_color = 'White',
                                            y = 0.55)
segment_sales_distribution.add_annotation(text = totalsales, showarrow = False,
                                            font_size = 10, font_color = 'White', y = 0.45)



categoryprofit = superstore.groupby('Category')['Profit'].sum()
categoryprofitdistribution = px.pie(names = categoryprofit.index, 
                                      values = categoryprofit.values,
                                      hole = 0.8,
                                      color_discrete_sequence = px.colors.qualitative.Dark24_r)

categoryprofitdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                           legend_font_color = 'white')

totalprofit = '${:,}'.format(round(categoryprofit.sum(), 2))
categoryprofitdistribution.add_annotation(text = "Total Profit by Category", showarrow = False,
                                            font_size = 11.5, font_color = 'White',
                                            y = 0.55)
categoryprofitdistribution.add_annotation(text = totalprofit, showarrow = False,
                                            font_size = 10, font_color = 'White', y = 0.45)



categoryprofit = superstore.groupby('Category')['Profit'].sum()
categoryprofitdistribution = px.pie(names = categoryprofit.index, 
                                      values = categoryprofit.values,
                                      hole = 0.8,
                                      color_discrete_sequence = px.colors.qualitative.Dark24_r)

categoryprofitdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                           legend_font_color = 'white')

totalprofit = '${:,}'.format(round(categoryprofit.sum(), 2))
categoryprofitdistribution.add_annotation(text = "Total Profit by Category", showarrow = False,
                                            font_size = 11.5, font_color = 'White',
                                            y = 0.55)
categoryprofitdistribution.add_annotation(text = totalprofit, showarrow = False,
                                            font_size = 10, font_color = 'White', y = 0.45)



categorysalesprofitdiscount = superstore.groupby('Category').agg(
                      {"Sales" : 'sum', 'Profit' : 'sum', 'Discount' : 'sum'}  
                    ).reset_index()

categorysalesprofitdiscountdistribution = px.scatter(categorysalesprofitdiscount, x = 'Profit', y = 'Sales', color = 'Category',
                                             size = "Discount" , title = "Category Profit for Sales Vs Returns")

categorysalesprofitdiscountdistribution.update_layout(plot_bgcolor = 'rgba(0,0,0,0)', paper_bgcolor = 'rgba(0,0,0,0)',
                                              xaxis = dict(title = "Total Profit", color = 'white'),
                                              yaxis = dict(title = "Total Sales", color = 'white'),
                                              title = dict(font  = dict(color = 'white')),
                                              legend_font_color = 'white'
                                              )

categorysalesprofitdiscountdistribution.update_xaxes(showgrid = False)
categorysalesprofitdiscountdistribution.update_yaxes(showgrid = False)






categorysubcategorysales = superstore.groupby(['Category', 'Sub-Category'])['Sales'].sum().reset_index()

categorysubcategorysalesdistribution = px.sunburst(categorysubcategorysales, path = ['Category', 'Sub-Category'], values = 'Sales')

categorysubcategorysalesdistribution.update_layout(paper_bgcolor = 'rgba(0,0,0,0)')

categorysubcategorysalesdistribution.update_traces(marker = dict(colors = px.colors.qualitative.Dark24))



categorysegmentsales = superstore.groupby(['Segment', 'Category', 'Sub-Category'])['Sales'].sum().reset_index()

categorysegmentsalesdistribution = px.sunburst(categorysegmentsales, path = ['Segment', 'Category', 'Sub-Category'], values = 'Sales', color_discrete_sequence=px.colors.qualitative.Dark24_r)

categorysegmentsalesdistribution.update_layout(title = "Categories and Sub-Categories Sales by Segment",
                                              title_font = dict(color = 'White'),
                                              paper_bgcolor = 'rgba(0,0,0,0)')

categorysegmentsalesdistribution.update_traces(marker = dict(colors = px.colors.qualitative.Dark24_r))


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




salesquantity = superstore.groupby(['Segment']).agg(
                      {"Sales" : 'sum', 'Quantity' : 'sum'}  
                    ).reset_index()

salesquantitydist1 = px.bar(salesquantity, x="Segment", y="Sales", title='Sales by Segment', text_auto='', color_discrete_sequence=px.colors.qualitative.Dark24_r)

salesquantitydist1.update_layout(title=dict(font=dict(color='white')), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                       xaxis=dict(title=dict(font=dict(color='white')), tickfont=dict(color='white')),
                       yaxis=dict(showticklabels=False), yaxis_title='', xaxis_title = '')

salesquantitydist1.update_yaxes(showgrid=False, gridcolor='rgba(255, 255, 255, 0.2)', zeroline=True, zerolinecolor='rgba(0, 0, 0, 0)')

salesquantitydist1.update_traces(marker_line_width=0, textfont_size=12, textfont_color='white', textangle=0, texttemplate='%{y:,}', textposition="outside", cliponaxis=False)


#sales quantity grouped bar

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


categorysalesprofit = superstore.groupby('Category').agg(
                      {"Sales" : 'sum', 'Profit' : 'sum', 'Quantity' : 'sum'}  
                    ).reset_index()

categorysalesprofitdistribution = px.scatter(categorysalesprofit, x = 'Profit', y = 'Sales', color = 'Category',
                                             size = "Quantity" , title = "Category Quantity for Sales Vs Returns")

categorysalesprofitdistribution.update_layout(plot_bgcolor = 'rgba(0,0,0,0)', paper_bgcolor = 'rgba(0,0,0,0)',
                                              xaxis = dict(title = "Total Profit", color = 'white'),
                                              yaxis = dict(title = "Total Sales", color = 'white'),
                                              title = dict(font  = dict(color = 'white')),
                                              legend_font_color = 'white'
                                              )

categorysalesprofitdistribution.update_xaxes(showgrid = False)
categorysalesprofitdistribution.update_yaxes(showgrid = False)



layout = html.Div(
    children = [
        dbc.Row(
            children=[
               dbc.Col(
                  dcc.Dropdown(
                    superstore['City'].unique(),
                    "Los Angeles",
                    id="City_dropdown",
                    style={'background': 'black', 'color': 'Yellow', 'font-size': 20}
                  )
               ),
               dbc.Col(
                  dcc.RadioItems(
                     superstore['Region'].unique(),
                     id = "region_radio_items"
                  )
               )
               
                
            ]
        ),
        dbc.Row(
            children = [
                dbc.Col(
                    children = dcc.Graph(id="sales_category_distribution", responsive=True)
                ),
                dbc.Col(
                    children = dcc.Graph(figure = segment_sales_distribution, responsive=True)
                ),
                dbc.Col(
                    children = dcc.Graph(figure=categoryprofitdistribution, responsive = True)
                ),
            ]
        ),
      dbc.Row(
         children = [    
            dbc.Col(
               dcc.Graph(figure=totalsalesovertimetop5distribution, responsive = True)
            ),
            dbc.Col(
               dcc.Graph(figure=totalprofitovertimetop5distribution, responsive = True)
            ),    
         ]
      ),
      dbc.Row(
         children = [
        dbc.Col(
               dcc.Graph(figure=categorysubcategorysalesdistribution, responsive = True)
            ),
            dbc.Col(
               dcc.Graph(figure=categorysegmentsalesdistribution, responsive = True)
            ),
            dbc.Col(
               dcc.Graph(figure=salesquantitydist1, responsive = True)
            ),   
         ]
      ),
      dbc.Row(
          children=[
        dbc.Col(
               dcc.Graph(figure=salesquantitydist, responsive = True)
            ),
            dbc.Col(
               dcc.Graph(figure=categorysalesprofitdiscountdistribution, responsive = True)
            ),      
          ]
      ),
      dbc.Row(
          children=[
        dbc.Col(
               dcc.Graph(figure=categorysalesprofitdistribution, responsive = True)
            ),
                  
          ]
      )
    ]
)

@callback(
   Output("sales_category_distribution", "figure"),
   Input("City_dropdown", 'value'),
   Input("region_radio_items", 'value')
)

def update_sales_category_distribution(city_value,region_value):
   city_filter_superstore=superstore[superstore['City']==city_value | superstore['Region']==region_value]

   categorysales = city_filter_superstore.groupby('Category')['Sales'].sum()
   categorysalesdistribution = px.pie(names = categorysales.index, 
                                       values = categorysales.values,
                                       hole = 0.8,
                                       color_discrete_sequence = px.colors.qualitative.Dark24_r)

   categorysalesdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                             legend_font_color = 'white', title = dict(font = dict(color = 'white', size=14)))

   totalsales = '${:,}'.format(round(categorysales.sum(), 2))
   categorysalesdistribution.add_annotation(text = "Total Sales by Category", showarrow = False,
                                             font_size = 11.5, font_color = 'White',
                                             y = 0.55)
   categorysalesdistribution.add_annotation(text = totalsales, showarrow = False,
                                             font_size = 10, font_color = 'White', y = 0.45)
   return categorysalesdistribution