from motion_detector import df
import pandas as pd
from bokeh.plotting import figure,show, output_file
from bokeh.models import HoverTool,ColumnDataSource
df['start_string']=df['Start'].dt.strftime("%Y-%m-%d %H:%M:%S")
df['end_string']=df['End'].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)
p = figure(x_axis_type = 'datetime',height=100,width=500,responsive=True,title='Motion Detecor Time Lapse')
p.y_axis.minor_tick_line_color = None
p.ygrid[0].ticker.desired_nu_ticks = 1

hover = HoverTool(tooltips=[("Start","@Start"),("End","@End")])
p.add_tools(hover)
q = p.quad(left='start_string',end='end_string',bottom=0,start=1,color='green',source=cds)
output_file('graph.html')
show(p)