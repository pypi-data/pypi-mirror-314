def remove_null_value(dataset, categorial_or_timestamp_columns=None, numerical_columns=None):

    if(dataset.isnull().sum().sum()>0):
        if (categorial_or_timestamp_columns != None):
            for column in categorial_or_timestamp_columns:
                dataset.dropna(subset=[column], inplace=True)
        if (numerical_columns != None):
            for column in numerical_columns:
                dataset[column].fillna(dataset[column].mean(), inplace=True)
    return dataset