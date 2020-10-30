import argparse

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
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

    pprint(conf_data)

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
    return merged_df

if __name__ == '__main__':
    # app.run_server(debug=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("--path_conf", type=str, dest='path_conf_file')
    args = parser.parse_args()

    merged_df = dash_get_data_merged(path_conf_file=args.path_conf_file)
    x = 'bpp'; hue='compression'
    y_list = "psnr,ssim,CR".split(",")
    figs_list = []
    for y in y_list:
        # print(f'Processing: {y}')
        fig = px.scatter(merged_df, x=f"{x}", y=f"{y}", color=f"{hue}",title=f'{y.upper()} vs. {x.upper()} | gropude by {hue.upper()} in merged-df')
        figs_list.append(fig)
        pass

    figs_list = list(map(lambda fig: dcc.Graph(figure=fig), figs_list))
    app = dash.Dash()
    """
    app.layout = html.Div([
        dcc.Graph(figure=fig),
        dcc.Graph(figure=fig),
        dcc.Graph(figure=fig),
    ])
    """
    app.layout = html.Div(figs_list)
    app.run_server(debug=True, use_reloader=False, host='localhost') 
    pass
