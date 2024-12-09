def remove_null_value(dataset, categorial_or_timestamp_columns=None):
    if dataset.isnull().sum().sum() > 0:
        if categorial_or_timestamp_columns is not None:
            for column in categorial_or_timestamp_columns:
                dataset.dropna(subset=[column], inplace=True)

        numerical_columns = [col for col in dataset.select_dtypes(include=['number']).columns 
                             if col not in categorial_or_timestamp_columns]

        for column in numerical_columns:
            dataset[column].fillna(dataset[column].mean(), inplace=True)
    
    return dataset
