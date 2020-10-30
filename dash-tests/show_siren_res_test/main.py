import argparse

import dash
import dash_auth
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly

from utils.libs import *

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


def dash_get_data_merged(path_conf_file):
    # -- Read conf.txt.
    conf_file_path = f'{path_conf_file}'
    conf_data = read_conf_file(conf_file_path)

    # -- Load Siren Data into Dataframe.
    constraints = get_constraints_for_query_db()

    records_list, result_dict_df, query_str, chained_constraints = fetch_data_by_constraints(
        conf_data, constraints, fetch_data_downloaded = True)

    data = list(map(operator.itemgetter(1), result_dict_df.items()))
    siren_df = pd.concat(data)

    # -- Load Image for JPEG computing.
    im = load_target_image(image_file_path = None)
    crop_size = conf_data['cropped_image']['crop_size']
    if isinstance(crop_size, str):
        crop_size = eval(crop_size)
    elif isinstance(crop_size, int):
        crop_size = (crop_size, crop_size)
        pass
    if conf_data['cropped_image']['flag'] is True:
        im_cropped = get_cropped_by_center_image(im, target = crop_size)
    else:
        im_cropped = im
        pass

    qualities_arr = np.arange(20, 95+1, dtype = np.int)
    cropped_file_size_bits = None
    with BytesIO() as f:
        im_cropped.save(f, format='PNG')
        cropped_file_size_bits = f.getbuffer().nbytes * 8
        pass
    result_tuples, failure_qualities = \
        calculate_several_jpeg_compression(im_cropped, cropped_file_size_bits, qualities_arr)
    data = list(map(operator.methodcaller('_asdict'), result_tuples))
    jpeg_df = pd.DataFrame(data = data)

    # -- Merge
    vars_dict = dict(
        image=im_cropped,                                                                  # Target Image , either cropped or not.
        siren_columns_for_merge="psnr,ssim,CR,bpp,file_size_bits,compression".split(","),  # Here, list siren_df columns for merge purpose.
        jpeg_columns_for_merge="psnr,ssim,CR,bpp,file_size_bits,compression".split(","),   # Here, list jpeg_df columns for merge purpose.
        columns_names_merge="psnr,ssim,CR,bpp,file_size_bits,compression".split(","),      # Here, list new columns name after merge.
    )
    merged_df, siren_df, jpeg_df = prepare_and_merge_target_dfs(
       siren_df, jpeg_df,
        **vars_dict
    )
    return merged_df, siren_df, jpeg_df 

def get_app_to_run(figs_list):
    app = dash.Dash('Siren+Jpeg Results', external_stylesheets=[dbc.themes.DARKLY])
    value_theme = None
    value_old = 'plotly_dark'

    if SHOW_RESULTS_BY_TABS:
        tab_list = []; card_list = None
        tab_names = iter(['scatter-mereged (PSNR,SSIM, CR)', 'box-mereged (PSNR,SSIM, CR)', 'kde-mereged (PSNR,SSIM, CR)', 'mse-siren (SCATTER,BOX,KDE)', 'summary']) # , 'graphics options'])
        for ii, a_fig in enumerate(figs_list):
            if ii % 3 == 0:
                if card_list != None:
                    tab_list.append(dbc.Tab(dbc.Card(card_list, body=True), label=f'{next(tab_names)}'))
                    pass
                card_list = []
                pass
            card_list.append(a_fig)
            pass

        tab_list.append(dbc.Tab(dbc.Card(card_list, body=True), label=f'{next(tab_names)}'))
        tab_list.append(dbc.Tab(dbc.Card(figs_list, body=True), label=f'{next(tab_names)}'))
    
        """
        opts = ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
        opts_list = list(map(lambda item: dict(label=item, value=item), opts))
        tab_list.append(dbc.Tab(dbc.Card(
            [
                html.Div([
                dcc.Dropdown(
                    id='demo-dropdown',
                        options=opts_list,
            value='plotly_dark'
        )]),
        html.Div(id='dd-output-container')
            ]
            , body=True), label=f'{next(tab_names)}'))
        app.layout = dbc.Tabs(children=tab_list, id="tabs-with-classes")
    
    
        @app.callback(
            dash.dependencies.Output('dd-output-container', 'children'),
            [dash.dependencies.Input('demo-dropdown', 'value')])
        def update_output(value):
            value_theme = value
            return 'You have selected "{}"'.format(value)
        """
        app.layout = dbc.Tabs(tab_list, id="tabs-with-classes")
    else:
        app.layout = html.Div(figs_list)
        pass
    return app

if __name__ == '__main__':
    # app.run_server(debug=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_conf", type=str, dest='path_conf_file')
    args = parser.parse_args()

    merged_df, siren_df, jpeg_df  = dash_get_data_merged(path_conf_file = args.path_conf_file)
    x = 'bpp'; hue='compression'
    y_list = "psnr,ssim,CR".split(",")
    figs_list = []; templates = ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
    for y in y_list:
        # print(f'Processing: {y}')
        fig = px.scatter(merged_df, template = templates[2], x=f"{x}", y=f"{y}", color=f"{hue}",title=f'{y.upper()} vs. {x.upper()} | gropude by {hue.upper()} in siren+jpeg df')
        figs_list.append(fig)
        pass

    x = 'compression'; y = 'psnr'
    for y in y_list:
        # print(f'Processing: {y}')
        fig = px.box(merged_df, template = templates[2], x =f"{x}",  y=f"{y}")
        fig.update_layout(title_text=f'{y.upper()} | Groupped by {hue} | siren+jpeg dataframes')
        figs_list.append(fig)
        pass
    groups_dict = merged_df.groupby(by = ['compression']).groups
    indices_dict = merged_df.groupby(by = ['compression']).indices
    group_labels = list(map(operator.itemgetter(0), groups_dict.items()))
    indices_arr = list(map(operator.itemgetter(1), indices_dict.items()))

    y = 'psnr'; hue = 'compression'
    for y in y_list:
    # print(f'Processing: {y}')
        hist_data = [merged_df.iloc[indeces][f'{y}'].values for indeces in indices_arr]
        fig = ff.create_distplot(hist_data, group_labels, show_rug=True)
        fig.update_layout(template = templates[2], title_text=f'{y.upper()} | Groupped by {hue} | siren+jpeg dataframes')

        x_min, x_max = merged_df[f'{y}'].values.min(), merged_df[f'{y}'].values.max()
        fig.update_xaxes(range=[x_min, x_max])
        figs_list.append(fig)
        pass

    # Sinre MSE graphics:
    x = 'bpp'; y = "mse"; hue='compression'
    # scatter-siren
    fig = px.scatter(siren_df, x=f"{x}", y=f"{y}", color=f"{hue}")# ,title=f'{y.upper()} vs. {x.upper()} | gropude by {hue.upper()} in siren-df')
    fig.update_layout(template = templates[2], title_text=f'{y.upper()} | Groupped by {hue} | siren-df')
    figs_list.append(fig)

    # box-siren
    fig = px.box(siren_df, template = templates[2], x =f"{hue}",  y=f"{y}")
    fig.update_layout(template = templates[2], title_text=f'{y.upper()} | Groupped by {hue} | siren-df')
    figs_list.append(fig)

    # kde-siren
    groups_dict = siren_df.groupby(by = ['compression']).groups
    indices_dict = siren_df.groupby(by = ['compression']).indices
    group_labels = list(map(operator.itemgetter(0), groups_dict.items()))
    indices_arr = list(map(operator.itemgetter(1), indices_dict.items()))

    hist_data = [siren_df.iloc[indeces][f'{y}'].values for indeces in indices_arr]
    fig = ff.create_distplot(hist_data, group_labels, show_rug=True)
    fig.update_layout(template = templates[2], title_text=f'{y.upper()} | Groupped by {hue} | siren-df')

    x_min, x_max = siren_df[f'{y}'].values.min(), siren_df[f'{y}'].values.max()
    fig.update_xaxes(range=[x_min, x_max])
    figs_list.append(fig)

    figs_list = list(map(lambda fig: dcc.Graph(figure=fig), figs_list))
    # app = dash.Dash()
    """
    app.layout = html.Div([
        dcc.Graph(figure=fig),
        dcc.Graph(figure=fig),
        dcc.Graph(figure=fig),
    ])
    """
    # app.layout = html.Div(figs_list)
    app = get_app_to_run(figs_list)
    app.run_server(debug=True, use_reloader=False, host='localhost') 
    
    pass