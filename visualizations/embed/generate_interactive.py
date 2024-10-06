import numpy as np
import pandas as pd
import geopandas as gpd
from datetime import date
import re

from branca.colormap import LinearColormap 
from jinja2 import Template

from bokeh.layouts import column, row
from bokeh.models import CustomJS, Span, Slider,  ColumnDataSource, DateSlider, LinearAxis
from bokeh.models.ranges import Range1d
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import Div

import folium
from folium.elements import JSCSSMixin
from folium.features import GeoJson
from folium.map import Layer



class TimeSliderChoropleth(JSCSSMixin, Layer):
    """
    Create a choropleth with a timeslider for timestamped data.

    Visualize timestamped data, allowing users to view the choropleth at
    different timestamps using a slider.

    Parameters
    ----------
    data: str
        geojson string
    styledict: dict
        A dictionary where the keys are the geojson feature ids and the values are
        dicts of `{time: style_options_dict}`
    highlight: bool, default False
        Whether to show a visual effect on mouse hover and click.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls.
    overlay : bool, default False
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening.
    init_timestamp: int, default 0
        Initial time-stamp index on the slider. Must be in the range
        `[-L, L-1]`, where `L` is the maximum number of time stamps in
        `styledict`. For example, use `-1` to initialize the slider to the
        latest timestamp.
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
        {
            let timestamps = {{ this.timestamps|tojson }};
            let styledict = {{ this.styledict|tojson }};
            let current_timestamp = timestamps[{{ this.init_timestamp }}];

            let slider_body = d3.select("body").insert("div", "div.folium-map")
                .attr("id", "slider_{{ this.get_name() }}");
            $("#slider_{{ this.get_name() }}").hide();
            // insert time slider
            slider_body.append("input")
                .attr("type", "range")
                .attr('width', 1440)
                .attr('height', 30)
                .attr("min", 0)
                .attr("max", timestamps.length - 1)
                .attr("value", {{ this.init_timestamp }})
                .attr("step", "1")
                .style('align', 'left');
            // insert time slider label
            slider_body.append("output")
                .attr("width", "100")
                .style('font-size', '15px')
                .style('text-align', 'right')
                .style('font-weight', '500%')
                .style('margin', '5px');


            let datestring = new Date(parseInt(current_timestamp)*1000).toDateString();
            d3.select("#slider_{{ this.get_name() }} > output").text("Date: " + datestring);

            let fill_map = function(){
                for (var feature_id in styledict){
                    let style = styledict[feature_id]//[current_timestamp];
                    var fillColor = 'white';
                    var opacity = 0;
                    if (current_timestamp in style){
                        fillColor = style[current_timestamp]['color'];
                        opacity = style[current_timestamp]['opacity'];
                        d3.selectAll('#{{ this.get_name() }}-feature-'+feature_id
                        ).attr('fill', fillColor)
                        .style('fill-opacity', opacity);
                    }
                }
            }

            d3.select("#slider_{{ this.get_name() }} > input").on("input", function() {
                current_timestamp = timestamps[this.value];
                var datestring = new Date(parseInt(current_timestamp)*1000).toDateString();
                d3.select("#slider_{{ this.get_name() }} > output").text("Date: " + datestring);
                fill_map();
            });

            let onEachFeature;
            {% if this.highlight %}
                 onEachFeature = function(feature, layer) {
                    layer.on({
                        mouseout: function(e) {
                        if (current_timestamp in styledict[e.target.feature.id]){
                            var opacity = styledict[e.target.feature.id][current_timestamp]['opacity'];
                            d3.selectAll('#{{ this.get_name() }}-feature-'+e.target.feature.id).style('fill-opacity', opacity);
                        }
                    },
                        mouseover: function(e) {
                        if (current_timestamp in styledict[e.target.feature.id]){
                            d3.selectAll('#{{ this.get_name() }}-feature-'+e.target.feature.id).style('fill-opacity', 1);
                        }
                    },
                        click: function(e) {
                            {{this._parent.get_name()}}.fitBounds(e.target.getBounds());
                    }
                    });
                };
            {% endif %}

            var {{ this.get_name() }} = L.geoJson(
                {{ this.data|tojson }},
                {onEachFeature: onEachFeature}
            );

            {{ this.get_name() }}.setStyle(function(feature) {
                if (feature.properties.style !== undefined){
                    return feature.properties.style;
                }
                else{
                    return "";
                }
            });

            let onOverlayAdd = function(e) {
                {{ this.get_name() }}.eachLayer(function (layer) {
                    layer._path.id = '{{ this.get_name() }}-feature-' + layer.feature.id;
                });

                $("#slider_{{ this.get_name() }}").show();

                d3.selectAll('path')
                .attr('stroke', '{{ this.stroke_color }}')
                .attr('stroke-width', {{ this.stroke_width }})
                .attr('stroke-dasharray', '5,5')
                .attr('stroke-opacity', {{ this.stroke_opacity }})
                .attr('fill-opacity', 0);

                fill_map();
            }
            {{ this.get_name() }}.on('add', onOverlayAdd);
            {{ this.get_name() }}.on('remove', function() {
                $("#slider_{{ this.get_name() }}").hide();
            })

            {%- if this.show %}
            {{ this.get_name() }}.addTo({{ this._parent.get_name() }});
            $("#slider_{{ this.get_name() }}").show();
            {%- endif %}
        }
        {% endmacro %}
        """
    )

    default_js = [("d3v4", "https://d3js.org/d3.v4.min.js")]

    def __init__(
        self,
        data,
        styledict,
        highlight: bool = False,
        name=None,
        overlay=True,
        control=True,
        show=True,
        init_timestamp=0,
        stroke_opacity=1,
        stroke_width=0.8,
        stroke_color="#FFFFFF",
    ):
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self.data = GeoJson.process_data(GeoJson({}), data)
        self.highlight = highlight

        self.stroke_opacity = stroke_opacity
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color

        if not isinstance(styledict, dict):
            raise ValueError(
                f"styledict must be a dictionary, got {styledict!r}"
            )  # noqa
        for val in styledict.values():
            if not isinstance(val, dict):
                raise ValueError(
                    f"Each item in styledict must be a dictionary, got {val!r}"
                )  # noqa

        # Make set of timestamps.
        timestamps_set = set()
        for feature in styledict.values():
            timestamps_set.update(set(feature.keys()))
        try:
            timestamps = sorted(timestamps_set, key=int)
        except (TypeError, ValueError):
            timestamps = sorted(timestamps_set)

        self.timestamps = timestamps
        self.styledict = styledict
        assert (
            -len(timestamps) <= init_timestamp < len(timestamps)
        ), f"init_timestamp must be in the range [-{len(timestamps)}, {len(timestamps)}) but got {init_timestamp}"
        if init_timestamp < 0:
            init_timestamp = len(timestamps) + init_timestamp
        self.init_timestamp = init_timestamp

if __name__ == '__main__':
    gdf = gpd.read_file('./data/RoutingKeys_WGS84_region.geojson').set_index('RoutingKey')

    input_df = pd.read_csv('./data/housing_prices/preprocessed/mean-housing-prices.csv')
    input_df['VALUE'] = np.log1p(input_df.VALUE.fillna(0).to_numpy().reshape(-1, 1))

    n_sample = 175
    datetime_index = pd.date_range(start='2010-01', end='2024-07', freq="MS")
    dt_index_epochs = datetime_index.astype("int64") // 10 ** 9
    dt_index = dt_index_epochs.astype("U10")
    n_periods = len(datetime_index)

    styledata = {}

    for routing_code in gdf.index:
        df = pd.DataFrame(
            {
                "color": input_df[(input_df['Routing Key'] == routing_code) & (input_df['Dwelling Status'] == 'All Dwelling Statuses') & (input_df['Type of Buyer'] == 'All Buyer Types')].VALUE.to_numpy(),
                "opacity": input_df[(input_df['Routing Key'] == routing_code) & (input_df['Dwelling Status'] == 'All Dwelling Statuses') & (input_df['Type of Buyer'] == 'All Buyer Types')].VALUE.to_numpy()
            },
            index=dt_index,
        )
        styledata[routing_code] = df

    max_color, min_color, max_opacity, min_opacity = 0, 0, 0, 0

    for country, data in styledata.items():
        try:
            max_color = max(max_color, data["color"].max())
            min_color = min(max_color, data["color"].min())
            max_opacity = max(max_color, data["opacity"].max())
            max_opacity = min(max_color, data["opacity"].max())
        except ValueError:
            continue

    cmap = LinearColormap(colors = ('#FFFFFF', '#FF7F0E')).scale(min_color, max_color)

    def norm(x):
        return (x - x.min()) / (x.max() - x.min())

    for country, data in styledata.items():
        try:
            data["color"] = data["color"].apply(cmap)
            data["opacity"] = norm(data["opacity"])
        except ValueError:
            continue

    styledict = {
        str(country): data.to_dict(orient="index") for country, data in styledata.items()
    }

    m = folium.Map(
        width=500,height=500,
        location=(53.5, -8),
        max_bounds=True,
        min_zoom=7,
        zoom_start = 7,
        min_lat=51,
        max_lat=56,
        min_lon=-11,
        max_lon=-5.5,
    )

    loc = 'Average Housing Prices in Ireland'
    title_html = '''
                <h3 align="left" style="font-size:16px"><b>{}</b></h3>
                '''.format(loc)   

    m.get_root().html.add_child(folium.Element(title_html))

    TimeSliderChoropleth(
        gdf.to_json(),
        styledict=styledict,
    ).add_to(m)

    colormap = cmap.to_step(data=np.linspace(500, 3745)/1e3, n = 100,  method = "log")
    colormap.caption = 'Units: EUR (millions)'
    colormap.add_to(m)


    gdf = gpd.read_file('./data/RoutingKeys_WGS84_region.geojson').set_index('RoutingKey')

    input_df = pd.read_csv('./data/completed_new_dwellings/preprocessed/freq-new-dwellings.csv')
    input_df['VALUE'] = input_df.VALUE.fillna(0).to_numpy().reshape(-1, 1)

    n_sample = 50
    datetime_index = pd.date_range(start='2012-03', end='2024-06', freq="3MS")
    dt_index_epochs = datetime_index.astype("int64") // 10 ** 9
    dt_index = dt_index_epochs.astype("U10")
    n_periods = len(datetime_index)

    styledata = {}

    for routing_code in gdf.index:
        df = pd.DataFrame(
            {
                "color": input_df[(input_df['Routing Key'] == routing_code)].VALUE.to_numpy(),
                "opacity": input_df[(input_df['Routing Key'] == routing_code)].VALUE.to_numpy()
            },
            index=dt_index,
        )
        styledata[routing_code] = df

    max_color, min_color, max_opacity, min_opacity = 0, 0, 0, 0

    for country, data in styledata.items():
        try:
            max_color = max(max_color, data["color"].max())
            min_color = min(max_color, data["color"].min())
            max_opacity = max(max_color, data["opacity"].max())
            max_opacity = min(max_color, data["opacity"].max())
        except ValueError:
            continue

    cmap = LinearColormap(colors = ('#FFFFFF', '#008000')).scale(min_color, max_color)

    def norm(x):
        return (x - x.min()) / (x.max() - x.min())

    for country, data in styledata.items():
        try:
            data["color"] = data["color"].apply(cmap)
            data["opacity"] = norm(data["opacity"])
        except ValueError:
            continue

    styledict = {
        str(country): data.to_dict(orient="index") for country, data in styledata.items()
    }

    m2 = folium.Map(
        width=500,height=500,
        location=(53.5, -8),
        max_bounds=True,
        min_zoom=7,
        zoom_start = 7,
        min_lat=51,
        max_lat=56,
        min_lon=-11,
        max_lon=-5.5,
    )

    loc = 'Number of New Dwellings Completed'
    title_html = '''
                <h3 align="left" style="font-size:16px"><b>{}</b></h3>
                '''.format(loc)   
    
    m2.get_root().html.add_child(folium.Element(title_html))

    TimeSliderChoropleth(
        gdf.to_json(),
        styledict=styledict,
    ).add_to(m2)

    colormap = cmap.to_step(data=np.linspace(0, 200), n = 100,  method = "linear")
    colormap.caption = 'Frequency'
    colormap.add_to(m2)


    housing_prices = pd.read_csv('./data/housing_prices/preprocessed/mean-housing-prices.csv')
    housing_prices = housing_prices[(housing_prices.City.isnull()) & (housing_prices['Dwelling Status'] == 'All Dwelling Statuses') & (housing_prices['Type of Buyer'] == 'All Buyer Types')]
    dates = pd.date_range(start='1/1/2010', end='7/1/2024', freq='MS')   
    values = housing_prices.VALUE.tolist()
    source = ColumnDataSource(data=dict(date=dates, value=values))

    new_dwellings = pd.read_csv('./data/completed_new_dwellings/preprocessed/freq-new-dwellings.csv')
    new_dwellings = new_dwellings[(new_dwellings.City.isnull())]
    dates2 = pd.date_range(start='3/1/2012', end='6/1/2024', freq='3MS')   
    values2 = new_dwellings.VALUE.tolist()
    source2 = ColumnDataSource(data=dict(date=dates2, value=values2))


    p = figure(width=1000, height=500, x_axis_type='datetime',
            x_axis_label="Year",
            y_axis_label="Average Price of House in Ireland",
            extra_y_ranges = {"twiny": Range1d(start=0, end=15000)},
            styles = {'top': '600px'})
    p.left[0].formatter.use_scientific = False
    p.line('date', 'value', source=source, line_width=2, legend_label='Average House Price', color = '#FF7F0E')

    p.add_layout(LinearAxis(y_range_name="twiny", axis_label='Number of Completed New Dwellings'), 'right')
    p.line('date', 'value', source=source2, line_width=2, y_range_name="twiny", legend_label='Number of Completed New Dwellings', color = '#008000')


    vline = Span(location=0, dimension='height', line_color='black', line_dash='dashed', line_width=0.5)
    p.renderers.extend([vline])

    sv = DateSlider(width = 760, start=min(dates), end=max(dates), value=min(dates), step=1, margin=10, format = '%b %Y', styles = {'top': '575px', 'left': '100px'})
    sv.js_link('value', vline, 'location')

    sv.js_on_change(
        'value',
        CustomJS(code="""       
            console.log(this.value)
        """))
    p.legend.location = "bottom_right"

    housing_crisis_map = Div(
        text=re.sub("Make this Notebook Trusted to load map: File -> Trust Notebook", "", re.sub(
            r"width\:100\%\;height\:100\%\;left\:0\;top\:0\;border\:none \!important\;", 
            "width:500px;height:850px;left:0;top:0;border:none !important;", m._repr_html_())),
        width=500,
        height=850,
        sizing_mode='scale_width' 
    )

    new_dwellings_map = Div(
        text=re.sub("Make this Notebook Trusted to load map: File -> Trust Notebook", "", re.sub(
            r"width\:100\%\;height\:100\%\;left\:0\;top\:0\;border\:none \!important\;", 
            "width:500px;height:850px;left:500px;top:0;border:none !important;", m2._repr_html_())),
        width=500,
        height=850,
        sizing_mode='scale_width' 
    )
    layout = column(row(housing_crisis_map, new_dwellings_map), sv, p)

    output_file("./visualizations/embed/interactive_visualization.html")
    save(layout)