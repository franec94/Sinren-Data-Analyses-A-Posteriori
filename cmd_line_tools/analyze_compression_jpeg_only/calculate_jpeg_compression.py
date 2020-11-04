from utils.libs import *


def main(args):

    # data = [jcr._asdict().values()]

    logger = ROOT_LOGGER

    
    logger.info('Calculate compressions by quality:')
    print('Calculate compressions by quality:')
    data_tuples = calculate_compressions_by_quality(args)
    data = list(map(operator.methodcaller('values'), map(operator.methodcaller('_asdict'), data_tuples)))

    # jcr = data_tuples[0]
    # headers = list(jcr._asdict().keys())
    if args.show_results_via_table:
        headers = JpegCompressionResult._fields
        data = dict(tabular_data=data, headers=headers)
        print(tabulate.tabulate(**data))
        pass

    data = list(map(operator.methodcaller('_asdict'), data_tuples))
    res_df = pd.DataFrame(data = data)

    res_filename = os.path.join(args.output_location, 'res.csv')
    res_df.to_csv(f'{res_filename}')

    if args.db_resource != None:
        logger.info('Insert data into db:')
        print('Insert data into db:')
        sql_statement = get_sql_statement_insert_jpeg_compressions_table()
        insert_data_by_sql_statement(
            data = data_tuples,
            db_resource = args.db_resource,
            sql_statement = sql_statement)

    logger.info('Calculate occurences for benford law:')
    print('Calculate occurences for benford law:')
    cnt_gt, cnt_compressed_tmp, data_tuples = calculate_occurences_for_benford_law(args)

    data = list(map(operator.methodcaller('_asdict'), data_tuples))
    res_df = pd.DataFrame(data = data)


    data = list(map(operator.methodcaller('_asdict'), data_tuples))
    result_df = pd.DataFrame(data = data).drop(["counter_gt", "counter_compressed"], axis = 1)

    counter_arr = res_df["counter_gt"].values
    res_df_tmp = get_benfords_from_cntrs(counter_arr)
    columns = list(map(lambda xx: f"gt_{xx}", res_df_tmp.columns))
    result_df[columns] = res_df_tmp

    counter_arr = res_df["counter_compressed"].values
    res_df_tmp = get_benfords_from_cntrs(counter_arr)
    columns = list(map(lambda xx: f"cmprssd_{xx}", res_df_tmp.columns))
    result_df[columns] = res_df_tmp

    if args.show_results_via_table:
        # headers = BenfordResult._fields
        headers = result_df.columns
        data = dict(tabular_data=result_df.values, headers=headers)
        print(tabulate.tabulate(**data))
        pass
    res_filename = os.path.join(args.output_location, 'res_benford.csv')
    result_df.to_csv(res_filename)
    pass

if __name__ == "__main__":
    parser = get_argparser_for_jpeg_compression()
    args = parser.parse_args()

    args, ROOT_LOGGER = preprocess_cmd_line_args_for_jpeg_compression(args)
    # pprint(args)
    main(args)
    pass