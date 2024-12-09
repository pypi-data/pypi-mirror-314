# -*- coding: utf-8 -*-


__author__ = 'aeiwz'

import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px
import dash


class plot_NMR_spec:
    def __init__(self, spectra, ppm, label):
        
        self.spectra = spectra
        self.ppm = ppm
        self.label = label


    def median_spectra_group(self, color_map=None, 
                    title='<b>Median Spectra of <sup>1</sup>H NMR data</b>', title_font_size=28, 
                    legend_name='<b>Group</b>', legend_font_size=20, 
                    axis_font_size=20, 
                    fig_height = 800, fig_width = 2000,
                    line_width = 1.5, legend_order=None
                    ):

        '''
        Plot median spectra of NMR data
        Parameters:
        - spectra: NMR data in pandas DataFrame format with group labels as index and chemical shift values as columns 
        - ppm: chemical shift values
        - label: group labels
        - color_map: color map for each group
        - title: title of the plot
        - title_font_size: font size of the title
        - legend_name: name of the legend
        - legend_font_size: font size of the legend

        Returns:
        - fig: plotly figure object
        '''

        from plotly import graph_objs as go
        from plotly import express as px

        spectra = pd.DataFrame(self.spectra)
        spectra.columns = self.ppm
        ppm = self.ppm
        label = self.label

        

        df_mean = spectra.groupby(label).median()

        #check if color_map is provided
        if color_map is None:
            color_map = dict(zip(df_mean.index, px.colors.qualitative.Plotly))
        else:
            if len(color_map) != len(df_mean.index):
                raise ValueError('Color map must have the same length as group labels')
            else:
                color_map = color_map

        

        #plot spectra
        fig = go.Figure()
        for i in df_mean.index:
            fig.add_trace(go.Scatter(x=ppm, y=df_mean.loc[i,:], mode='lines', name=i, line=dict(color=color_map[i], width=line_width)))

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
        #fig.update_layout(title='Median Spectra', xaxis_title='δ <sup>1</sup>H', yaxis_title='Intensity')

        #set y-axis tick format to scientific notation with 4 decimal places
        fig.update_layout(yaxis=dict(tickformat=".2e"))

        return fig


    def single_spectra(self, color_map=None, 
                    title='<b>Spectra of <sup>1</sup>H NMR data</b>', title_font_size=28, 
                    legend_name='<b>Group</b>', legend_font_size=20, 
                    axis_font_size=20, 
                    fig_height = 800, fig_width = 2000,
                    line_width = 1.5, legend_order=None
                    ):

        '''
        Plot median spectra of NMR data
        Parameters:
        - spectra: NMR data in pandas DataFrame format with group labels as index and chemical shift values as columns
        - ppm: chemical shift values
        - label: group labels
        - color_map: color map for each group
        - title: title of the plot
        - title_font_size: font size of the title
        - legend_name: name of the legend
        - legend_font_size: font size of the legend

        Returns:
        - fig: plotly figure object
        '''

        from plotly import graph_objs as go
        from plotly import express as px

        spectra = self.spectra
        ppm = self.ppm
        label = self.label
        

        df_spectra = pd.DataFrame(spectra)
        df_spectra.columns = ppm

        #check if color_map is provided
        if color_map is None:
            color_map = dict(zip(df_spectra.index, px.colors.qualitative.Plotly))
        else:
            if len(color_map) != len(df_spectra.index):
                raise ValueError('Color map must have the same length as group labels')
            else:
                color_map = color_map

        

        #plot spectra
        fig = go.Figure()
        for i in df_spectra.index:
            fig.add_trace(go.Scatter(x=ppm, y=df_spectra.loc[i,:], mode='lines', name=i, line=dict(width=line_width)))

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
        #fig.update_layout(title='Median Spectra', xaxis_title='δ <sup>1</sup>H', yaxis_title='Intensity')

        #set y-axis tick format to scientific notation with 4 decimal places
        fig.update_layout(yaxis=dict(tickformat=".2e"))

        return fig




class group_plot:

    '''
    Plot box plot and violin plot of a dataset
    Parameters:
    - dataset: pandas data frame or series
    - label: list of group labels
    '''


    def __init__(self, dataset, label):

        self.dataset = dataset
        self.label = label

        #Dataset must be a data frame or series
        if not isinstance(dataset, (pd.DataFrame, pd.Series)):
            raise ValueError('Dataset must be a pandas data frame or series')
        #Label must be a list
        if len(label) != len(dataset):
            raise ValueError('Label must be a list of the same length as the dataset')
        
        

    def box_plot(self, color_dict=None, 
                    show_value = True,  font_size=24, 
                    title_font_size=24, fig_height= 800, 
                    fig_width=500, y_label='Absolute concentration (mM)',
                    legend_name='Class', legend_font_size=18, legend_orientation='h',
                    legend_x=0.5, legend_y=-0.08, yanchor = 'top', xanchor = 'center'):

        '''
        Plot box plot of a dataset
        Parameters:
        - dataset: pandas data frame or series
        - label: list of group labels
        - color_dict: color dictionary for each group
        - show_value: show data points
        - font_size: font size of the axis
        - title_font_size: font size of the title
        - fig_height: height of the figure
        - fig_width: width of the figure
        - y_label: y-axis label
        - legend_name: name of the legend
        - legend_font_size: font size of the legend
        - legend_orientation: orientation of the legend
        - legend_x: x position of the legend
        - legend_y: y position of the legend
        - yanchor: y anchor of the legend
        - xanchor: x anchor of the legend

        Returns:
        - fig: plotly figure object
        '''

        dataset = self.dataset
        label = self.label
    
        import plotly.express as px
        import pandas as pd
        

        df = pd.DataFrame(dataset)
        df['Class'] = label
        column = df.columns[0]
        
        
        #--------- color dictionary -----------#
        if color_dict is not None:
            if not isinstance(color_dict, dict):
                raise ValueError('color_dict must be a dictionary')
            else:
                color_dict = color_dict
        else:
            color_dict = dict(zip(df['Class'].unique(), px.colors.qualitative.Plotly))
        #--------------------------------------#
        
        legend_name = legend_name
        fig_height = fig_height
        fig_width = fig_width
        
        if show_value == True:
            points = 'all'
        else:
            points = None
        
        
        fig = px.box(df, y=column, 
                            color=df['Class'],
                            color_discrete_map=color_dict,
                            width=fig_width, height=fig_height,
                            labels={'Class': legend_name},
                            points=points,
                            hover_data=['Class', df.index])
        
        #add title and set to center with size 24 and bold
        fig.update_layout(title={'text': '<b>{}</b>'.format(column), 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}, font=dict(size=title_font_size))
        #add y label 'Absolute concentration (mM)' and set to bold
        fig.update_yaxes(title_text=f'{y_label}</b>', title_font=dict(size=font_size))
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_layout(legend=dict(
            orientation=legend_orientation,
            itemwidth=50,
            yanchor=yanchor,
            y=legend_y,
            xanchor=xanchor,
            x=legend_x,
            font=dict(
                size=legend_font_size,
                color="black"
            ) 
        ))
        #background color
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        self.fig = fig
        return fig



    def violin_plot(self, color_dict=None, show_value = True, show_box=True, font_size=24, 
                    title_font_size=24, fig_height= 800, fig_width=500, y_label='Absolute concentration (mM)',
                    legend_name='Class', legend_font_size=18, legend_orientation='h', legend_x=0.5, legend_y=-0.08,
                    yanchor = 'top', xanchor = 'center'):
        
        '''
        Plot violin plot of a dataset
        Parameters:
        - dataset: pandas data frame or series
        - label: list of group labels
        - color_dict: color dictionary for each group
        - show_value: show data points
        - font_size: font size of the axis
        - title_font_size: font size of the title
        - fig_height: height of the figure
        - fig_width: width of the figure
        - y_label: y-axis label
        - legend_name: name of the legend
        - legend_font_size: font size of the legend
        - legend_orientation: orientation of the legend
        - legend_x: x position of the legend
        - legend_y: y position of the legend
        - yanchor: y anchor of the legend
        - xanchor: x anchor of the legend

        Returns:
        - fig: plotly figure object
        '''


        dataset = self.dataset
        label = self.label
        
        import plotly.express as px
        import pandas as pd
        
        #Dataset must be a data frame or series
        if not isinstance(dataset, (pd.DataFrame, pd.Series)):
            raise ValueError('Dataset must be a pandas data frame or series')
        #Label must be a list
        if len(label) != len(dataset):
            raise ValueError('Label must be a list of the same length as the dataset')
        
        
        df = pd.DataFrame(dataset)
        df['Class'] = label
        column = df.columns[0]
        
        
        #--------- color dictionary -----------#
        if color_dict is not None:
            if not isinstance(color_dict, dict):
                raise ValueError('color_dict must be a dictionary')
            else:
                color_dict = color_dict
        else:
            color_dict = dict(zip(df['Class'].unique(), px.colors.qualitative.Plotly))
        #--------------------------------------#
        
        legend_name = legend_name
        fig_height = fig_height
        fig_width = fig_width
        
        if show_value == True:
            points = 'all'
        else:
            points = None
        
        
        fig = px.violin(df, y=column, 
                            color=df['Class'],
                            color_discrete_map=color_dict,
                            width=fig_width, height=fig_height,
                            labels={'Class': legend_name},
                            points=points,
                            hover_data=['Class', df.index],
                            box=show_box)
        
        #add title and set to center with size 24 and bold
        fig.update_layout(title={'text': '<b>{}</b>'.format(column), 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}, font=dict(size=title_font_size))
        #add y label 'Absolute concentration (mM)' and set to bold
        fig.update_yaxes(title_text=f'{y_label}</b>', title_font=dict(size=font_size))
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_layout(legend=dict(
            orientation=legend_orientation,
            itemwidth=50,
            yanchor=yanchor,
            y=legend_y,
            xanchor=xanchor,
            x=legend_x,
            font=dict(
                size=legend_font_size,
                color="black"
            ) 
        ))
        #background color
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        self.fig = fig
        
        return fig





class unipair:

    '''
    This function takes in a dataframe and a column name and returns the index of the dataframe and the names of the pairs
    of the unique values in the column.
    Parameters
    ----------
    meta: pandas dataframe
        The dataframe to be used.
    column_name: str
    Unipair(meta, column_name).indexing()
    '''


    def __init__(self, dataset, column_name):
        

        meta = dataset
        self.meta = meta
        self.column_name = column_name
        

        """
        This function takes in a dataframe and a column name and returns the index of the dataframe and the names of the pairs
        of the unique values in the column.
        Parameters
        ----------
        meta: pandas dataframe
            The dataframe to be used.
        column_name: str
        Unipair(meta, column_name).indexing()
        
        """
        import pandas as pd
        import numpy as np
        def warnings():
            import warnings
            warnings.filterwarnings("ignore")
        #check unique values in the column
        if meta[column_name].nunique() < 3:
            # Raise warnings.warn(Group in the column is less than 3")
            warnings("Group in the column is less than 3")
            #raise Warning("Group in the column is less than 3")
            pass

        else:
            pass
        #check meta is a dataframe
        if not isinstance(meta, pd.DataFrame):
            raise ValueError("meta should be a pandas dataframe")
        #check column_name is a string
        if not isinstance(column_name, str):
            raise ValueError("column_name should be a string")
        

        df = meta
        y = df[column_name].unique()
        pairs = []
        for i in range(len(y)):
            for j in range(i+1, len(y)):
                pairs.append([y[i], y[j]])
        
        index_ = []
        for i in range(len(pairs)):
            inside_index = []
            for j in range(2):
                inside_index.append(list((df.loc[df[column_name] == pairs[i][j]]).index))
            index_list = [inside_index[0] + inside_index[1]]
            index_.append(index_list[0])
        pairs
        index_
        names = []
        for i in range(len(pairs)):
            
            names.append(str(pairs[i][0]) + "_vs_" + str(pairs[i][1]))
            #check names if contain / replace with _ 
            names[i] = names[i].replace('/', '_')
            
        del df
        del y
        
        self.index_ = index_
        self.names = names
        
        
        

    def get_index(self):

        '''
        Get the index of the dataframe
        Returns
        -------
        index_: list
            The index of the dataframe
        '''

        index_ = self.index_
        return index_
    
    def get_name(self):

        '''
        Get the names of the pairs
        Returns
        -------
        names: list
            The names of the pairs
        '''

        names = self.names
        return names
    
    def get_meta(self):

        '''
        Get the dataframe
        Returns
        -------
        meta: pandas dataframe
            The dataframe
        '''

        meta = self.meta
        column_name = self.column_name
        return meta[column_name]
    
    def get_column_name(self):

        '''
        Get the column name
        Returns
        -------
        column_name: str
            The column name
        '''

        column_name = self.column_name
        return column_name
    
    def get_dataset(self):

        '''
        Get the dataset
        Returns
        -------
        dataset: pandas dataframe
            The dataset
        '''
        
        df = self.meta
        index_ = self.index_
        list_of_df = []
        for i in range(len(index_)):
            list_of_df.append(df.loc[index_[i]])
        
        #Create object attribute
        self.list_of_df = list_of_df
        return list_of_df
        
