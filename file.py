def run_eda(df):
    '''
    Main function of my_awesome_eda.py module.
    Receives a dataframe as input. 

    Parameters:
    df (pandas.DataFrame): input data

    Returns:
    '''
    stats = get_some_stats(df)
    res_check_data_type = check_data_type(df)
    result_for_num_data = analyze_num_data(df)
    result_for_cat_data = analyze_categorial_data(df)

    with open('result_of_eda.txt', mode='w+') as file:
        file.write(f'Statistics in df\n')
        file.writelines(stats)
        file.write(f'\nData types in df\n')
        file.writelines(res_check_data_type)
        file.write(f'\nResults for numeric data:\n')
        file.writelines(result_for_num_data)
        file.write(f'\nResults for categorial data:\n')
        for col, res in result_for_cat_data.items():
            file.write(f'{col}')
            file.write(res.to_string(index=True))
    return None


def get_some_stats(df):
    '''
    Function
    '''
    stats = []
    df_size = f'Number of rows: {df.shape[0]}\nNumber of columns: {df.shape[1]}\n'
    all_na_in_df = f'Number of NA in df: {df.isna().sum().sum()}\n'
    na_in_rows = f'Number of NA in rows: {df.isna().any(axis=1).sum()}\n'
    na_in_columns = f'Columns with NA: {list(df.columns[df.isna().any()])}\n'
    duplicates = f'Number of duplicate rows: {df.duplicated().sum()}\n'
    stats.extend([df_size, all_na_in_df, na_in_rows, na_in_columns, duplicates])
    return stats
#попробовать ретерн None

def check_data_type(df):
    res_check_data_type = []
    numeric_columns = []
    object_columns = []
    categorial_columns = []
    for col in df.columns:
        if len(pd.unique(df[col])) <= 10:
            categorial_columns.append(col)
        elif df[col].dtype == 'int64' or df[col].dtype == 'float64':
            numeric_columns.append(col)
        else:
            object_columns.append(col)
    num_cols = f'Numeric data in {numeric_columns} columns\n'
    obj_cols = f'Object data in {object_columns} columns\n'
    cat_cols = f'Categorial data in {categorial_columns} columns\n'
    res_check_data_type.extend([num_cols, obj_cols, cat_cols])
    return res_check_data_type


def analyze_num_data(numeric_df):
    result_for_num_data = []
    for col in numeric_df.columns:
        q1 = numeric_df[col].quantile(q=0.25)
        q3 = numeric_df[col].quantile(q=0.75)
        iqr = q3 - q1
        result_for_num_data.append([f'Min value of {col}: {numeric_df[col].min()}\n',
                                    f'Max value of {col}: {numeric_df[col].max()}\n',
                                    f'Mean of {col}: {numeric_df[col].mean()}\n',
                                    f'SD of {col}: {numeric_df[col].std()}\n',
                                    f'Q0.25 of {col}: {q1}\n',
                                    f'Median of {col}: {numeric_df[col].median()}\n',
                                    f'Q0.75 of {col}: {q3}\n'])
        sum_outliers = ((numeric_df[col] < (q1 - 1.5 * iqr)) | (numeric_df[col] > (q3 + 1.5 * iqr))).sum()
        result_for_num_data.append(f'Outliers in {col}: {sum_outliers}\n')
    return result_for_num_data


def analyze_categorial_data(categorial_columns):
    result_for_cat_data = {}
    for col in categorial_columns:
        counts = df[col].value_counts()
        frequency = counts / len(df[col])
        result_for_cat_data[col] = pd.DataFrame(
            {'Counts for each class:': counts,
             'Frequencies:': frequency})
    return result_for_cat_data

run_eda(df)
