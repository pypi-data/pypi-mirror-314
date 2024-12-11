

sec_per_day                     = 60*60*24


def transform(values, source: str, variable: str):

    """
    Process an array linearly
    with scalar multiplicator and addend
    given by variable parameter dictionary
    """

    from my_.resources.sources import query_unit_transform
    
    ux_method                   = query_unit_transform(source, variable, 'methods')

    if ux_method == 'linear':

        from my_.math.mapping import linear

        m                       = query_unit_transform(source, variable, 'm')
        b                       = query_unit_transform(source, variable, 'b')

        values_uxb              = linear(values, m, b)

    return values_uxb


def transform_df(df, source: str, variables: list):
    
    from my_.resources.sources import query_unit_transform

    df_out                      = df.copy()
    
    for i_col, col in enumerate(df.columns):

        variable                = variables[i_col]

        ux_method               = query_unit_transform(source, variable, 'methods')

        if ux_method == 'linear':

            from my_.math.mapping import linear

            m                       = query_unit_transform(source, variable, 'm')
            b                       = query_unit_transform(source, variable, 'b')

            df_out[col]              = linear(df[col].astype('float'), m, b)

    return df_out