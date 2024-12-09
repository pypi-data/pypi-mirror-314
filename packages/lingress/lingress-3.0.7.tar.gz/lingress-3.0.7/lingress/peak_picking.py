# -*- coding: utf-8 -*-

__auther__ = 'aeiwz'


#Peak picking all spectra and plot using scipy and pyplot

from scipy.signal import find_peaks
import matplotlib.pyplot as plt


def peak_picking(spectra, ppm, threshold=0.05, min_dist=100):
    
        peaks = []
        for i in range(spectra.shape[0]):
            y = spectra.iloc[i,:]
            peaks_, _ = find_peaks(y, height=threshold, distance=min_dist)
            peaks.append(peaks_)
    
        return peaks

peaks = peak_picking(spectra, ppm, threshold=0.05, min_dist=1000)


def plot_peaks(spectra, ppm, peaks, color_map=None, title='Peak picking', title_font_size=28, legend_name='<b>Group</b>', legend_font_size=20, axis_font_size=20, fig_height = 800, fig_width = 2000, line_width = 1.5, legend_order=None):
    
        from plotly import graph_objs as go
        from plotly import express as px
    

    
        #plot spectra
        fig = go.Figure()
        for i in range(spectra.shape[0]):
            fig.add_trace(go.Scatter(x=ppm, y=spectra.iloc[i,:], mode='lines', name=spectra.index[i], line=dict(width=line_width)))
            fig.add_trace(go.Scatter(x=ppm[peaks[i]], y=spectra.iloc[i,peaks[i]], mode='markers', marker=dict(size=5), showlegend=False))

        fig.update_layout(
            autosize=False,
            width=fig_width,
            height=fig_height,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            )
        )

        fig.update_xaxes(showline=True, showgrid=False, linewidth=1, linecolor='rgb(82, 82, 82)', mirror=True)
        fig.update_yaxes(showline=True, showgrid=False, linewidth=1, linecolor='rgb(82, 82, 82)', mirror=True)

        #Set font size of label
        fig.update_layout(font=go.layout.Font(size=axis_font_size))
        #Add title
        fig.update_layout(title={'text': title, 'xanchor': 'center', 'yanchor': 'top'}, 
                        title_x=0.5, 
                        xaxis_title="<b>δ<sup>1</sup>H</b>", yaxis_title="<b>Intensity</b>",
                        title_font_size=title_font_size,
                        title_yanchor="top",
                        title_xanchor="center")

        #Add legend

        fig.update_layout(legend=dict( title=legend_name, font=dict(size=legend_font_size)))
        #Invert x-axis
        fig.update_xaxes(autorange="reversed")

        #Alpha background
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        fig.update_layout(title='Medien Spectra', xaxis_title='δ <sup>1</sup>H', yaxis_title='Intensity')

        #set y-axis tick format to scientific notation with 4 decimal places
        fig.update_layout(yaxis=dict(tickformat=".2e"))

        return fig

plot_peaks(spectra, ppm, peaks, color_map=color_dict_)



