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
