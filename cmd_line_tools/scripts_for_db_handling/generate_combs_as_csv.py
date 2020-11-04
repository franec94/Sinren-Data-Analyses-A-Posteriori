from utils.libs import *

from sklearn.model_selection import ParameterGrid
from lenses import lens


def save_data_to_db(grid_comb, args, table_name = 'table_todo_list_runs'):

    attr_names = list(map(operator.itemgetter(0), grid_comb[0].items()))
    sql_statement = get_sql_statement_insert_table(table_name, attr_names)
    print(sql_statement)

    data = list(map(lambda item: list(item.values()), grid_comb))

    logger.info('Insert combinations into db.')
    inserted_list, skipped_list = insert_data_by_sql_statement(data[:], args.db_resource, table_name, attr_names)
    if args.show_results_via_table:
        # headers = BenfordResult._fields
        if len(skipped_list) != 0:
            tabular_data = skipped_list[:5] # list(map(lambda item: item.values(), res))[:5]
            headers = list(map(operator.itemgetter(0), grid_comb[0].items()))

            if args.save_df_as_csv:
                logger.info('Save skipped rows into csv file.')
                columns = list(map(operator.itemgetter(0), grid_comb[0].items()))
                skipped_list_df = pd.DataFrame(data = skipped_list, columns = columns)
                skipped_list_filename = os.path.join(args.output_location, 'skipped_rows_table.csv')
                skipped_list_df.to_csv(skipped_list_filename)
                pass

            data = dict(tabular_data=tabular_data, headers=headers, tablefmt='fancy_grid')
            print(tabulate.tabulate(**data))
        else:
            
            logger.info('Skipped-Rows Table is Empty!')
            print('Skipped-Rows Table is Empty!')
        pass
    if args.show_results_via_table:
        # headers = BenfordResult._fields
        if len(inserted_list) != 0:
            tabular_data = inserted_list[:5] # list(map(lambda item: item.values(), res))[:5]
            headers = list(map(operator.itemgetter(0), grid_comb[0].items()))

            data = dict(tabular_data=tabular_data, headers=headers, tablefmt='fancy_grid')
            print(tabulate.tabulate(**data))
            if args.save_df_as_csv:
                logger.info('Save insert rows into csv file.')
                columns = list(map(operator.itemgetter(0), grid_comb[0].items()))
                inserted_list_df = pd.DataFrame(data = inserted_list, columns = columns)
                inserted_list_filename = os.path.join(args.output_location, 'inserted_rows_table.csv')
                inserted_list_df.to_csv(inserted_list_filename)
                pass
        else:
            logger.info('Insert-Rows Table is Empty!')
            print('Insert-Rows Table is Empty!')
        pass
    return


def main(args, conf_data):
    logger = ROOT_LOGGER

    logger.info('runnig main...')

    grid_comb = list(ParameterGrid(dict(map(lambda item: (item[0], item[1]['vals']), conf_data.items()))))

    columns = list(map(operator.itemgetter(0), grid_comb[0].items()))
    grid_comb_df = pd.DataFrame(data = grid_comb, columns = columns)
    if args.save_df_as_csv:
        logger.info('Save combinations as csv file.')
        grid_combs_filename = os.path.join(args.output_location, 'grid_combs_table.csv')
        grid_comb_df.to_csv(grid_combs_filename)

        pass

    
    data = lens.summarise(grid_comb_df)
    exp = lens.explore(data)
    exp.describe()
    sys.exit(0)

    if args.show_results_via_table:
        # headers = BenfordResult._fields
        tabular_data = list(map(lambda item: item.values(), grid_comb))[:5]
        headers = list(map(operator.itemgetter(0), grid_comb[0].items()))
        # pprint(conf_data.items())
        data = dict(tabular_data=tabular_data, headers=headers, tablefmt='fancy_grid')
        print(tabulate.tabulate(**data))
        pass
    # pprint(data[0])

    if args.save_data_to_db:
        save_data_to_db(grid_comb = grid_comb, args = args)
        pass
    pass


if __name__ == "__main__":
    parser = get_argparser_for_generating_data()
    args = parser.parse_args()

    args, conf_data, logger = preprocess_cmd_line_args_for_jpeg_compression(args)
    ROOT_LOGGER = logger
    
    pprint(args)
    # pprint(conf_data)

    main(args, conf_data)
    pass