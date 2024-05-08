import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path = "/salesanalysis", title = "Category Analysis")

superstore = pd.read_csv("data/Superstore.csv", encoding = "latin1")

#categorysalesdistribution

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


#segmentsalesdistribution

segmentsales = superstore.groupby('Segment')['Sales'].sum()
segmentsalesdistribution = px.pie(names = segmentsales.index, 
                                      values = categorysales.values,
                                      hole = 0.7,
                                      color_discrete_sequence = px.colors.qualitative.Dark24_r)

segmentsalesdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                           legend_font_color = 'white', title = dict(font = dict(color = 'white')))

totalsales = '${:,}'.format(round(segmentsales.sum(), 2))
segmentsalesdistribution.add_annotation(text = "Total Sales by Segment", showarrow = False,
                                            font_size = 14, font_color = 'White',
                                            y = 0.55)
segmentsalesdistribution.add_annotation(text = totalsales, showarrow = False,
                                            font_size = 14, font_color = 'White', y = 0.45)


#categoryprofitdistribution

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


#categorysalesprofitdistribution

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


#categorysalesprofitdiscountdistribution

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
categorysalesprofitdistribution.update_yaxes(showgrid = False)


#totalprofitovertimetop5distribution




#totalsalesovertimetop5distribution




#categorysubcategorysalesdistribution

categorysubcategorysales = superstore.groupby(['Category', 'Sub-Category'])['Sales'].sum().reset_index()

categorysubcategorysalesdistribution = px.sunburst(categorysubcategorysales, path = ['Category', 'Sub-Category'], values = 'Sales')

categorysubcategorysalesdistribution.update_layout(paper_bgcolor = 'rgba(0,0,0,0)')

categorysubcategorysalesdistribution.update_traces(marker = dict(colors = px.colors.qualitative.Dark24))


#categorysegmentsalesdistribution

categorysegmentsales = superstore.groupby(['Segment', 'Category', 'Sub-Category'])['Sales'].sum().reset_index()

categorysegmentsalesdistribution = px.sunburst(categorysegmentsales, path = ['Segment', 'Category', 'Sub-Category'], values = 'Sales', color_discrete_sequence=px.colors.qualitative.Dark24_r)

categorysegmentsalesdistribution.update_layout(title = "Categories and Sub-Categories Sales by Segment",
                                              title_font = dict(color = 'White'),
                                              paper_bgcolor = 'rgba(0,0,0,0)')

categorysegmentsalesdistribution.update_traces(marker = dict(colors = px.colors.qualitative.Dark24_r))


#salesquantitydist

salesquantity = superstore.groupby(['Segment']).agg(
                      {"Sales" : 'sum', 'Quantity' : 'sum'}  
                    ).reset_index()

salesquantitydist = px.bar(salesquantity, x="Segment", y="Sales", title='Sales by Segment', text_auto='', color_discrete_sequence=px.colors.qualitative.Dark24_r)

salesquantitydist.update_layout(title=dict(font=dict(color='white')), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                       xaxis=dict(title=dict(font=dict(color='white')), tickfont=dict(color='white')),
                       yaxis=dict(showticklabels=False), yaxis_title='', xaxis_title = '')

salesquantitydist.update_yaxes(showgrid=False, gridcolor='rgba(255, 255, 255, 0.2)', zeroline=True, zerolinecolor='rgba(0, 0, 0, 0)')

salesquantitydist.update_traces(marker_line_width=0, textfont_size=12, textfont_color='white', textangle=0, texttemplate='%{y:,}', textposition="outside", cliponaxis=False)


#salesquantitydist

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



layout = html.Div(
    children = [
        dbc.Row(
            children = [
                dbc.Col(
                    children = dcc.Graph(figure = categorysalesdistribution, responsive = True)
                ),
                dbc.Col(
                    children = dcc.Graph(figure = segmentsalesdistribution, responsive = True)
                ),
                dbc.Col(
                    children = dcc.Graph(figure=categoryprofitdistribution, responsive = True)
                )
            ]
        ),
      dbc.Row(
         children = [
            dbc.Col(
               dcc.Graph(figure=categorysalesprofitdistribution, responsive = True)
            ),
            dbc.Col(
               dcc.Graph(figure=categorysalesprofitdiscountdistribution, responsive = True)
            )
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
         ]
      ),
      dbc.Row(
         children = [
            dbc.Col(
               dcc.Graph(figure=salesquantitydist, responsive = True)
            )
         ]
      )
    ]
)