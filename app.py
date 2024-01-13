from flask import Flask, request, jsonify, redirect, url_for,session
from flask_cors import CORS
from bokeh.plotting import figure,curdoc
from bokeh.embed import json_item
from bokeh.transform import cumsum
import json
import pandas as pd
from math import pi
from bokeh.palettes import Category20c
from bokeh.models import WMTSTileSource, ColumnDataSource, HoverTool,RangeTool, LayoutDOM,BasicTicker, ColorBar,LinearColorMapper, PrintfTickFormatter, CustomJS
import numpy as np
import requests
import time
from numpy import cumprod, linspace, random
from bokeh.plotting import figure, show
from bokeh.sampledata.stocks import AAPL
from bokeh.layouts import layout,column
from bokeh.core.properties import Instance, String
from bokeh.util.compiler import TypeScript
from bokeh.palettes import Sunset8
from bokeh.sampledata.stocks import MSFT
from bokeh.io import output_file
from bokeh.models.widgets import DataTable, TableColumn
# from scipy.stats.kde import gaussian_kde
from scipy.stats import gaussian_kde
from bokeh.sampledata.unemployment1948 import data
from bokeh.transform import transform
from flask import Flask, request, jsonify
from flask_cors import CORS
from bokeh.plotting import figure
from bokeh.embed import json_item
from bokeh.transform import linear_cmap
from bokeh.models.tickers import BasicTicker
from bokeh.models.formatters import PrintfTickFormatter
from bokeh.transform import LinearColorMapper
from bokeh.palettes import Viridis256
from bokeh.transform import transform
import os
from bokeh.layouts import row
from bokeh.models import (ColumnDataSource, DataCube, GroupingInfo,
                          StringFormatter, SumAggregator, TableColumn)
from bokeh.models import Arrow, VeeHead, HTMLTemplateFormatter
from icecream import ic 
from bokeh.models import Button

app = Flask(__name__)
CORS(app) 
# ic.disable() 
ic.enable()
global p
app.secret_key = 'your_secret_key'
@app.route('/generate_chart', methods=['GET','POST'])

def generate_chart():
    valid_chart_types = [2,3,4,5,6,7,8,9,10,11,12,13]  

    try:
        if request.method == 'POST':
            data = request.get_json()
            chart_type = data.get('chartType')
            ic(chart_type)
            if chart_type in valid_chart_types:
                if chart_type == 13:
                   
                    table_data = fetch_table_data() 
                    add_tabledata = add_data()   
                    # merged_data = merge_datasets(table_data, add_tabledata)
                    ic(add_tabledata)
                    selected_color = update_table_lettercolor()
                    chart_data = generate_bokeh_chart(chart_type,table_data)
                    # print( chart_data,selected_color,"chart_data")
                    ic(chart_data,selected_color)
                    return jsonify({'chartData': chart_data}), 200
                else:
                    chart_data = generate_bokeh_chart(chart_type)
                    return jsonify({'chartData': chart_data}), 200
            else:
                ic.configureOutput(prefix="Invalid chart type: ") 
                ic(chart_type)
                return jsonify({'error': 'Invalid chart type.'}), 400
        else:
            return jsonify({'error': 'Method not allowed.'}), 405
    except Exception as e:
        return jsonify({'error': str(e)}), 500
def fetch_table_data():
    try:
        response = requests.get("http://restapi.adequateshop.com/api/Tourist?page=2")
        response.raise_for_status()
        table_data = response.json()
        # for key, value in table_data.items():
        #     print(f"Key: {key}, Value: {value}")
        swapped_data_list = [{value: key for key, value in item.items()} for item in table_data["data"]]
        for swapped_data in swapped_data_list:
            for key, value in swapped_data.items():
            #    print(f"Keyswap: {key}, Valueswap: {value}")
            #   ic.configureOutput(prefix="Keyswap Valueswap")
              ic(key, value)
        return table_data
    except Exception as e:
        print("Error fetching table data:", str(e))
        return None
def merge_datasets(table_data, added_data):
    return {**table_data, **added_data}
def generate_bokeh_chart(chart_type,table_data=None,time=None):
    p = figure(title="Bokeh Chart", x_axis_label="X-axis", y_axis_label="Y-axis",resizable= True,)
    x = {
    'United States': 157,
    'United Kingdom': 93,
    'Japan': 89,
    'China': 63,
    'Germany': 44,
    'India': 42,
    'Italy': 40,
    'Australia': 35,
    'Brazil': 32,
    'France': 31,
    'Taiwan': 31,
    'Spain': 29,}

    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(x)]
    if chart_type == 2: 
        p = figure(title="Line Chart",toolbar_location=None, tools="")
        p.line([1, 2, 3, 4, 5], [10, 20, 30, 40, 60], line_width=2)
        # show(p)
    elif chart_type == 3:
        p = figure(title="Wedge Chart",toolbar_location=None, tools="")
        p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='country', source=data)
    elif chart_type == 4:
        p = figure(title="Vertical Bar Chart",toolbar_location=None, tools="")
        p.vbar(x=[1, 2, 3, 4, 5], top=[10, 20, 30, 40, 50], width=0.5)
    elif chart_type == 5:
        def generate_random_weather_data():
            cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru"]
            temperature = np.random.randint(25, 35, len(cities))
            humidity = np.random.randint(50, 80, len(cities))
            weather_data = pd.DataFrame({"City": cities, "Temperature (C)": temperature, "Humidity (%)": humidity})
            return weather_data
        weather_data=generate_random_weather_data()
        city_coordinates = {
            "Delhi": (28.6139, 77.2090),
            "Mumbai": (19.0760, 72.8777),
            "Chennai": (13.0827, 80.2707),
            "Kolkata": (22.5726, 88.3639),
            "Bengaluru": (12.9716, 77.5946),
        }
        def web_mercator(lat, lon):
            k = 6378137
            x = lon * (k * np.pi / 180.0)
            y = np.log(np.tan((90 + lat) * np.pi / 360)) * k
            return x, y
        weather_data["x"], weather_data["y"] = zip(*[web_mercator(lat, lon) for lat, lon in city_coordinates.values()])

        # Create the India map plot
        # x_range, y_range = ((-13884029, -7453304), (2698291, 6455972))
        x_range, y_range = ((7753304, 9753304), (9004291, 13055972))
        p = figure(
            title="Maps",
            # width=1200, height=600,
            # tools="pan,wheel_zoom,reset",
            toolbar_location=None, tools="",
             x_range=x_range, 
             y_range=y_range, 
             x_axis_label="mercator",
              y_axis_label="mercator")

        # Add the base map
        url = "http://a.basemaps.cartocdn.com/rastertiles/voyager/{Z}/{X}/{Y}.png"
        attribution = "Tiles by Carto, under CC By 3.0 Data by OSM under ODBL"
        p.add_tile(WMTSTileSource(url=url, attribution=attribution))
        source = ColumnDataSource(weather_data)
        p.circle(x="x", y="y", size=15, fill_color="firebrick", source=source,legend_field="City")
        # Show the legend for weather conditions
        p.legend.title = "City"
        p.legend.location = "top_left"

        # Add tooltips to display weather data on hover
        hover = HoverTool(tooltips=[("City", "@City"), ("Temperature (C)", "@{Temperature (C)}"), ("Humidity (%)", "@{Humidity (%)}")])
        p.add_tools(hover)
    elif chart_type == 6:
 
        p = figure(title="Surface Plot",toolbar_location=None, tools="")
        CODE = """
        import {LayoutDOM, LayoutDOMView} from "models/layouts/layout_dom"
        import {ColumnDataSource} from "models/sources/column_data_source"
        import * as p from "core/properties"

        declare namespace vis {
        class Graph3d {
            constructor(el: HTMLElement | DocumentFragment, data: object, OPTIONS: object)
            setData(data: vis.DataSet): void
        }

        class DataSet {
            add(data: unknown): void
        }
        }

        const OPTIONS = {
        # width: '650px',
        # height: '600px',
        style: 'surface',
        showPerspective: true,
        showGrid: true,
        keepAspectRatio: true,
        verticalRatio: 1.0,
        cameraPosition: {
            horizontal: -0.35,
            vertical: 0.22,
            distance: 1.8,
        },
        }

        export class Surface3dView extends LayoutDOMView {
        declare model: Surface3d

        private _graph: vis.Graph3d

        initialize(): void {
            super.initialize()

            const url = "https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.js"
            const script = document.createElement("script")
            script.onload = () => this._init()
            script.async = false
            script.src = url
            document.head.appendChild(script)
        }

        private _init(): void {

            this._graph = new vis.Graph3d(this.shadow_el, this.get_data(), OPTIONS)

            this.connect(this.model.data_source.change, () => {
            this._graph.setData(this.get_data())
            })
        }

        get_data(): vis.DataSet {
            const data = new vis.DataSet()
            const source = this.model.data_source
            for (let i = 0; i < source.get_length()!; i++) {
            data.add({
                x: source.data[this.model.x][i],
                y: source.data[this.model.y][i],
                z: source.data[this.model.z][i],
            })
            }
            return data
        }

        get child_models(): LayoutDOM[] {
            return []
        }
        }

        export namespace Surface3d {
        export type Attrs = p.AttrsOf<Props>

        export type Props = LayoutDOM.Props & {
            x: p.Property<string>
            y: p.Property<string>
            z: p.Property<string>
            data_source: p.Property<ColumnDataSource>
        }
        }

        export interface Surface3d extends Surface3d.Attrs {}

        export class Surface3d extends LayoutDOM {
        declare properties: Surface3d.Props
        declare __view_type__: Surface3dView

        constructor(attrs?: Partial<Surface3d.Attrs>) {
            super(attrs)
        }

        static __name__ = "Surface3d"

        static {
            
            this.prototype.default_view = Surface3dView


            this.define<Surface3d.Props>(({String, Ref}) => ({
            x:[ String ],
            y:[ String ],
            z:[ String ],
            data_source:[Ref(ColumnDataSource)],
            }))
        }
        }
        """

        class Surface3d(LayoutDOM):

            __implementation__ = TypeScript(CODE)

            data_source = Instance(ColumnDataSource)

            x = String()
            y = String()
            z = String()


        x = np.arange(0, 300, 10)
        y = np.arange(0, 300, 10)

        xx, yy = np.meshgrid(x, y)
        xx = xx.ravel()
        yy = yy.ravel()

        value = np.sin(xx / 50) * np.cos(yy / 50) * 50 + 50

        source = ColumnDataSource(data=dict(x=xx, y=yy, z=value))

        p = Surface3d(x="x", y="y", z="z", 
                            data_source=source, 
                            # width=680, 
                            # height=600
                            )
     
    elif chart_type == 7:
        x, y = np.meshgrid(np.linspace(0, 3, 40), np.linspace(0, 2, 30))
        z = 1.3*np.exp(-2.5*((x-1.3)**2 + (y-0.8)**2)) - 1.2*np.exp(-2*((x-1.8)**2 + (y-1.3)**2))

        p = figure(
        #     width=550, 
        # height=300,
        toolbar_location=None, tools="",
         x_range=(0, 3), y_range=(0, 2))

        levels = np.linspace(-1, 1, 9)
        contour_renderer = p.contour(x, y, z, levels, fill_color=Sunset8, line_color="black")

        colorbar = contour_renderer.construct_color_bar()
        p.add_layout(colorbar, "below")
    elif chart_type == 8:
        df = pd.DataFrame(MSFT)[60:120]
        df["date"] = pd.to_datetime(df["date"])
        # print(df.columns)
        ic(df.columns)

        inc = df.close > df.open
        dec = df.open > df.close
        w = 16*60*60*1000 # milliseconds

        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
        hover = HoverTool(tooltips=[
            ("Date", "@date{%F}"),
            ("Open", "@open"),
            ("Close", "@close"),
            ("High", "@high"),
            ("Low", "@low")
        ], formatters={'@date': 'datetime'}, mode='vline')


        p = figure(x_axis_type="datetime",
        #  tools=TOOLS,
          toolbar_location=None, tools="",
        # width=1000, height=400,
                title="MSFT Candlestick", background_fill_color="#efefef")
        p.xaxis.major_label_orientation = 0.8 # radians
        p.add_tools(hover)
        p.segment(df.date, df.high, df.date, df.low, color="black")

        p.vbar(df.date[dec], w, df.open[dec], df.close[dec], color="#eb3c40")
        p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="white",
            line_color="#49a3a3", line_width=2)
    elif chart_type == 9:
        def violin(data=None,
            steps=100,
            range_extension=0.5,
            pdf_min_cutoff=0.001,
            title=None,
            y_axis_label=None,
            y_axis_max=None,
            y_axis_min=None,
            fill_color='#1F77B4'):
        
            """Function to plot a violin plot."""

            # Calculate maximum, minimum
            _min = data.min()
            _max = data.max()
            
            # Don't build the chart if the minimum and maximum are the same.
            if _max == _min:
                _str = ("""violin plot function error. """
                        """Maxmimum and minimum values of the input data series """
                        """are the same.""")
                raise ValueError(_str)

            # Train the KDE
            pdf = gaussian_kde(data)
            
            # Extend the range of the data by range_extension - doing this to prevent
            # the pdf from truncation when plotted using the y value range
            _e_range = (1 + range_extension)*(_max - _min)        
            _e_min = (_min + _max - _e_range)/2

            # Build the y values
            y = [_e_min + (step*_e_range)/steps for step in range(steps+1)]  
            # Calculate the pdf at each of the y values
            x = pdf.evaluate(y) 

            # Now remove any values past the minimum and maximum that are too small 
            # to plot
            _too_small = max(x)*pdf_min_cutoff
            df = pd.DataFrame({'x': x, 'y': y})
            df = df[((df['y'] <= _max) & (df['y'] >= _min)) |
                    ((df['y'] > _max) & (df['x'] > _too_small)) | 
                    ((df['y'] < _min) & (df['x'] > _too_small))]
            
            p = figure(title=title,
                        y_axis_label=y_axis_label,toolbar_location=None, tools="")
            
            p.harea(y=df['y'],
                        x1=df['x'],
                        x2=-df['x'],
                        fill_color=fill_color)
            
            p.xaxis.visible = False
            p.xgrid.grid_line_color = None
            
            if y_axis_max is not None and df['y'].max() > y_axis_max:
                p.y_range.end = y_axis_max
                
            if y_axis_min is not None and df['y'].min() < y_axis_min:
                p.y_range.start = y_axis_min
            
            return p
        
        # Get the directory where the script is located
        script_directory = os.path.dirname(os.path.abspath(__file__))

            # Construct the absolute path to the CSV file
        csv_path = os.path.join(script_directory, 'gapminder_full.csv')

            # Read the CSV file
        dataframe = pd.read_csv(csv_path, encoding="ISO-8859-1")
        # dataframe = pd.read_csv("gapminder_full.csv", 
        #                         # error_bad_lines=False, 
        #                         encoding="ISO-8859-1")

        p = violin(data=dataframe['life_exp'],
                    title="Violin example",
                    y_axis_label="Age at death")
    elif chart_type == 10:
        num_points = 300

        now = time.time()
        dt = 24*3600  # days in seconds
        dates = linspace(now, now + num_points*dt, num_points) * 1000  # times in ms
        acme = cumprod(random.lognormal(0.0, 0.04, size=num_points))
        choam = cumprod(random.lognormal(0.0, 0.04, size=num_points))

        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

        r = figure(x_axis_type="datetime", 
        # tools=TOOLS
         toolbar_location=None, tools="")

        r.line(dates, acme, color='#1F78B4', legend_label='ACME')  
        r.line(dates, choam, color='#FB9A99', legend_label='CHOAM') 

        r.title = "Stock Returns"
        r.grid.grid_line_alpha = 0.3

        c = figure(tools=TOOLS)

        c.circle(acme, choam, color='#A6CEE3', legend_label='close') 

        c.title = "ACME / CHOAM Correlations"
        c.grid.grid_line_alpha = 0.3
        p=layout([[r, c]])
    elif chart_type == 11:
       
        dates = np.array(AAPL['date'], dtype=np.datetime64)
        source = ColumnDataSource(data=dict(date=dates, close=AAPL['adj_close']))

        t = figure(
            # height=300, width=800,
             tools="xpan", toolbar_location=None,
                x_axis_type="datetime", x_axis_location="above",
                background_fill_color="#efefef", x_range=(dates[1500], dates[2500]))

        line = t.line('date', 'close', source=source)
        t.yaxis.axis_label = 'Price'

        select = figure(title="Drag the middle and edges of the selection box to change the range above",
                        # height=130, width=800, 
                        y_range=t.y_range,
                        x_axis_type="datetime", y_axis_type=None,
                        tools="", toolbar_location=None, background_fill_color="#efefef")

        range_tool = RangeTool(x_range=t.x_range)
        range_tool.overlay.fill_color = "navy"
        range_tool.overlay.fill_alpha = 0.2

        select.line('date', 'close', source=source)
        select.ygrid.grid_line_color = None
        select.add_tools(range_tool)
        p=column(t, select)
    elif chart_type == 12:
      # Create example data
        data = {
            'Category': ['A', 'B', 'C', 'D'],
            'Jan': [10, 20, 30, 40],
            'Feb': [15, 25, 35, 45],
            'Mar': [5, 15, 25, 35],
            'Apr': [25, 35, 45, 55],
        }
        df = pd.DataFrame(data)
        values = df.iloc[:, 1:].values
        # source = ColumnDataSource(df.melt(id_vars='Category', var_name='Month', value_name='Value'))

        
        # mapper = LinearColorMapper(palette=Viridis256, low=df.iloc[:, 1:].min().min(), high=df.iloc[:, 1:].max().max())
        mapper = LinearColorMapper(palette=Viridis256, low=np.min(values), high=np.max(values))
        # Create the figure
        p = figure(title="Heatmap Example", x_range=list(df['Category']), y_range=list(reversed(df.columns[1:])), toolbar_location=None, tools="")

        # Add the heatmap rectangles
        # p.rect(x="Category", y="index", width=1, height=1, source=source, line_color=None, fill_color=transform('value', mapper))
        p.image(image=[values], x=0, y=0, dw=len(df['Category']), dh=len(df.columns[1:]), color_mapper=mapper)
        # Add color bar
        color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
        p.add_layout(color_bar, 'right')

       
        p.xaxis.axis_label = "Category"
        p.yaxis.axis_label = "Month"
    elif chart_type == 13:
       
        # def get_html_formatter(apply_column_value):
        #     ic(apply_column_value)
        #     print(apply_column_value,"*&^$#!@#!@@@@@~#@%&")
        #     template = """
        #             <div style="background:<%= 
        #                 (function colorfromint(){
        #                     if(apply_column_value == condition_column_value){
        #                         return('#f14e08')}
        #                     else if (condition_column_value == 'Negative')
        #                         {return('#8a9f42')}
        #                     else if (condition_column_value == 'Invalid')
        #                         {return('#8f6b31')}
        #                     }()) %>; 
        #                 color: red"> 
        #             <%= value %>
        #             </div>
        #         """.replace('result_col',apply_column_value)
                
        #     return HTMLTemplateFormatter(template=template)
        data_key = 'data'                       # Replace this with the actual key in your dictionary
        df = pd.DataFrame(table_data.get(data_key, [])) 
            
            # if is_transposed:
            # # Transpose the DataFrame
            #     print("fghfghfghfghfghfghfhf")
            #     df = df.transpose()
            #     print(df)
        transposed_df = df.transpose()
            # print(transposed_df,"tdt")
        ic(transposed_df)
        source = ColumnDataSource(df)
        # tourist_names = df['tourist_name'].tolist()
        #     # print("Tourist Names:", tourist_names)
        # ic(tourist_names)

            # source = ColumnDataSource( transposed_df )
            # stats = df.describe().reset_index()
            # source_stats = ColumnDataSource(stats)
            # for key, value in df.items():
            #     print(f"Key: {key}, Value: {value}")
            # columns[1].formatters = [{"bold": True}]
        # columns = [TableColumn(field=col, title=col,formatter=get_html_formatter()) for col in df.columns]
        columns = [TableColumn(field=col, title=col, formatter=HTMLTemplateFormatter(template='<div><u><%= value %></u></div>')) for col in df.columns]

        # columns = [TableColumn(field=col, title=col,formatter=HTMLTemplateFormatter(template='<u><%= value %></u>')) for col in df.columns]
            # name = [entry['tourist_name'] for entry in data_key]
            # print("name>>>>",name)
        p = DataTable(source=source, columns=columns,editable=True,fit_columns=True,selectable=True,index_position=None,sortable=True)
       
        # button = Button(label="Click Me!")

        # # Create a CustomJS callback for the Button
        # js_callback = CustomJS(code="""
        #     console.log("Button clicked!");
        #     alert("Button clicked!");
        # """)

        # # Attach the callback to the Button
        # button.js_on_click(js_callback)
        # p = column(p1, button)
        # def update_bg_color(attr, old, new):
        #        ic(new)
        #        if new == 'save_clicked':
                    
        #             p.styles({'background': [(0, '#FFD700')]})
        # # Attach the callback to the DataTable's name property
        # p.on_change('name', update_bg_color)
        custom_js_callback = CustomJS(args=dict(source=source), code="""
        alert("DataTable button clicked!");
    console.log("Save button clicked! Implement your logic here.");
    var data = source.data;
    console.log(data);
""")
        p.js_on_event('button_click', custom_js_callback)
        # add_data(source)
#         js_callback = CustomJS(args=dict(source=source),code="""
#                     console.log("JavaScript callback is working!");
#                 var p = cb_obj ;
#                 var source = p.source;

#                 // Define the style changes
#                 var new_styles = {
#                 'background': '{textformatbgcolor || 'lightblue'}',
#                         'color': '{textformatlettercolor || 'green'}',
#                         'font-weight': '{textFormatbold ? 'bold' : 'normal'}',
#                         'font-style': '{textformatItalic ? 'italic' : 'normal'}',
#                         'text-decoration': '{textformatunderline ? 'underline' }',

# };
#                 // Update the styles of the DataTable
#                 p.styles = new_styles;
#             """)
#         # p.js_on_change('change', js_callback)
#         # p.js_on_event('button_click',js_callback)
#         p.js_on_event('button_click', CustomJS(code="console.log('Button Clicked!');"))
        # p.styles = {
        #         # 'background-color': 'lightblue',
        #         # 'color': 'green',
                
        #         'band_fill_color':'red',
        #         'font-weight': 'bold' if textFormatbold else 'normal',
        #         'font-style': 'italic' if textformatItalic else 'normal',
        #         'text-decoration': 'underline' if textformatunderline else 'none',
        #         'color': textformatlettercolor if textformatlettercolor else 'green',
        #         'background-color': textformatbgcolor if textformatbgcolor else 'lightblue'
        #     }
            
    chart_json = json_item(p, "my_chart")
    return json.dumps(chart_json) 
@app.route('/add', methods=['POST'])
def add_data():

    
    try:
        data = request.get_json()
        added_tag = data.get('addedtag', {})
        return  jsonify({"added_tag":added_tag}) 

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_tableTextFormat', methods=['POST'])
def update_tableTextFormat():
    try:
        data = request.get_json()
        selected_style = data.get('selectedStyle')
        # print(data,"data")
        ic(data)
        return jsonify({'selectedStyle': selected_style}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_bokeh_data_table(style_message):
    if style_message == 'equalTo':
        print("hello from equal to")
        # chart_json.p.columns[0].formatter.template = '<div style="font-weight: bold;"><%= value %></div>'
    elif style_message == 'italic':
        pass
        # chart_json.p.columns[0].formatter.template = '<div style="font-style: italic;"><%= value %></div>'
    # Add more conditions based on your styling needs


@app.route('/formatconditions',methods=['POST'])
def formatconditions(): 
    try:
        data = request.get_json()
        formatconditions = data.get('formatconditions')
        
        # chart_json = json_item(p, "my_chart")
        # print(formatconditions.values(),formatconditions,"formatconditions")
        condition_column_value = formatconditions['formatconditionsList'].get('conditionColumn')
        apply_column_value = formatconditions['formatconditionsList'].get('ApplyColumn')
        condition_type_value = formatconditions['formatconditionsList'].get('Condition Type')
        alias_name_value = formatconditions['formatconditionsList'].get('aliasName')
        Condition = formatconditions['valueCondition'].get('selectedcondtionFormat')
        update_bokeh_data_table(Condition)
        textFormatbold = formatconditions['conditionalOutput'].get('bold')
        textformatItalic =  formatconditions['conditionalOutput'].get('italic')
        textformatunderline =  formatconditions['conditionalOutput'].get('underline')
        textformatlettercolor =  formatconditions['conditionalOutput'].get('textcolor')
        textformatbgcolor =  formatconditions['conditionalOutput'].get('backgroundcolor')
        tabledatalist = formatconditions.get('tabledata', {})
        roots_data = tabledatalist.get('doc', {}).get('roots', [])
        columns_data = roots_data[0].get('attributes', {}).get('columns', [])
        ic(textFormatbold,textformatbgcolor,textformatlettercolor)
        # print(textFormatbold,"textFormatbold",textformatbgcolor,"textformatbgcolor",textformatlettercolor,"textformatlettercolor")
        # Extract column titles using list comprehension
        column_titles = [column.get('attributes', {}).get('title') for column in columns_data]
        ic(column_titles)
        # print("Column Titles:", column_titles)
        doc = tabledatalist.get("doc", {})

                # Extracting the "roots" section from "doc"
        roots = doc.get("roots", [])
        if roots:
            first_root = roots[0]
            attributes = first_root.get("attributes", {})
            source = attributes.get("source", {})
            source_attributes = source.get("attributes", {})  
            data = source_attributes.get("data", {})
            entries = data.get("entries", [])

                    # Find the entry with the key matching "apply_column_value"
            selected_entry = next((entry[1]["array"] for entry in entries if entry[0] == apply_column_value), [])
            ic(selected_entry)
                    # the values under the specified "applyColumn"
            # print(f"Values for {apply_column_value}:", selected_entry)
            ic(condition_column_value,apply_column_value,Condition)
        # print( condition_column_value,apply_column_value,Condition," >>>>>>>>>>>>>condition_column_value,apply_column_value>>>>>>>>>>>")
        # Check if the values of 'conditionColumn' and 'applyColumn' are the same
        if(condition_type_value == 1):
            # print(Condition,textFormatbold,">>>>>>>selectedCondition func val Condition Type>>>>>>>>>>>>")
            if(Condition == 'equalTo'):
                if(textFormatbold == True):
                    selected_entry["font"] = 'bold'
                    ic(selected_entry['font'])
                    
                elif(textformatItalic == True):
                    pass
                elif (textformatunderline == True):
                    pass
                elif(textformatlettercolor == True):
                    pass
                elif(textformatbgcolor == True):
                    pass
            elif(Condition == 'notEmpty'):
                if(textFormatbold == True):
                #  selected_entry()
                    pass
                elif(textformatItalic == True):
                    pass
                elif (textformatunderline == True):
                    pass
                elif(textformatlettercolor == True):
                    pass
                elif(textformatbgcolor == True):
                    pass
            elif(Condition == 'greaterThan'):
                if(textFormatbold == True):
                #  selected_entry()
                    pass
                elif(textformatItalic == True):
                    pass
                elif (textformatunderline == True):
                    pass
                elif(textformatlettercolor == True):
                    pass
                elif(textformatbgcolor == True):
                    pass
            elif(Condition == 'lessThan'):
                if(textFormatbold == True):
                #  selected_entry()
                    pass
                elif(textformatItalic == True):
                    pass
                elif (textformatunderline == True):
                    pass
                elif(textformatlettercolor == True):
                    pass
                elif(textformatbgcolor == True):
                    pass
        if condition_column_value == apply_column_value:
            print("Values of conditionColumn and applyColumn are the same")
        elif(condition_column_value != 'none'):
            print("Not a empty value")
        # chart_data = generate_bokeh_chart( textFormatbold, textformatItalic,textformatunderline, textformatlettercolor, textformatbgcolor,apply_column_value,condition_column_value,Condition,condition_type_value)
        
        return jsonify({'formatconditions':formatconditions,'chartData':chart_data}),200
    except Exception as e:
        return jsonify({'error': str(e)}),500
 
# @app.route('/valueCondition',methods=['POST'])
# def valueCondition():
#    try:
#         data = request.get_json()
#         selectedCondition = data.get('selectedCondition')
#         # generate_bokeh_chart(selectedfontcolor)
        
#         print(selectedCondition, "selectedCondition1")
#         return jsonify({'selectedCondition': selectedCondition}), 200
#    except Exception as e:
#        print(f"Error in valueCondition: {str(e)}")
#        return jsonify({'error': 'An error occurred'}), 500
@app.route('/swapColumns',methods=['POST'])
def swapColumns():
    try:
        data = request.get_json()
        horizontalColumn = data.get('horizontalColumn')
        verticalColumn = data.get('verticalColumn')
        # print(horizontalColumn,"horizontalColumn",verticalColumn,"verticalColumn")
        ic(horizontalColumn,verticalColumn)
        
        return jsonify({'horizontalColumn':horizontalColumn,'verticalColumn':verticalColumn}),200
    except Exception as e:
        return jsonify({'error': str(e)}),500

@app.route('/update_table_lettercolor', methods=['POST'])   
def update_table_lettercolor():
    try:
        data = request.get_json()
        selectedfontcolor =data.get('selectedColor')
        # generate_bokeh_chart(selectedfontcolor)
        # print(selectedfontcolor,"selectedfontcolor")
        ic(selectedfontcolor)
        return selectedfontcolor
    except Exception as e:
        return jsonify({'error': str(e)}),500

@app.route('/update_table_bgcolor', methods=['POST'])   
def update_table_bgcolor():
    try:
        data = request.get_json()
        selectedbgcolor =data.get('selectedbgColor')
        # generate_bokeh_chart(selectedfontcolor)
        ic(selectedbgcolor)
        # print(selectedbgcolor,"selectedbgcolor")
        return selectedbgcolor,200
    except Exception as e:
        return jsonify({'error': str(e)}),500

if __name__ == '__main__':
    app.run(debug=True)
