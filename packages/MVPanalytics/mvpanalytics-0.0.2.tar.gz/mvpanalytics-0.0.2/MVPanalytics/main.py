def keitaro_parser(api_key, host, firstdate='', lastdate='', interval = '30_days_ago', timezone = 'Europe/Moscow', filters = [], grouping = ['stream', 'offer_group'], metrics = ['sub_id_12','clicks', 'campaign_unique_clicks', 'sale_revenue', 'epc_confirmed', 'approve', 'sales']):
    
    """
    Функция позволяет парсить данные с кейтаро по запросу. Порядок действий следующий, надо формировать отчёт в кейтаро, затем забирать необходимые данные как указано в гайде: https://docs.keitaro.io/ru/development/admin-api.html
    
    api_key: (str) - апи-ключ для доступа в кейтаро
    
    host: (str) - url ля доступа к кейтаро
    
    firstdate: (str) - дата, с которой необходимо начать отчёт формта YYYY-MM-DD, либо пустота, если interval не равен custom_date_range
    
    lastade: (str) - дата, на которой необходимо закончить отчёт формта YYYY-MM-DD, либо пустота, если interval не равен custom_date_range
    
    interval: (str) - за какой период взяты данные (берётся из кейтаро)
    
    timezone: (str) - Параметр который не надо менять
    
    filters: list(dictionary()) - список из словарей, копировать строго из кейтаро
    
    grouping: list() - параметр, по которому осуществляется группировка (брать строго из кейтаро)
    
    metrics: list() - метрики, выбираемые в настройках кейтаро 
    
    """
    
    import requests
    import json
    import pandas as pd
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import scipy.stats as sts
    api_url = f'{host}admin_api/v1/'
    if interval != 'custom_date_range':
        params =  {
            'range': {
            'interval': interval,
            },
            'timezone': timezone,
            'filters': []+filters,
            'grouping': grouping,
            'metrics': metrics
            }

    else:
        params = {
            'range': {
                'from': firstdate,
                'interval': interval,
                'timezone': timezone,
                'to': lastdate
            },
            'filters': []+filters,
            'grouping': grouping,
            'metrics': metrics
            }
        
    headers = {'Api-Key': api_key}

    response = requests.post(
        url=f'{api_url}report/build',
        headers=headers,
        json=params
    )

    parsed_response = json.loads(response.text)

    df_per_days = pd.DataFrame(parsed_response['rows'])
    if 'day' in grouping:
        df_per_days['day'] = pd.to_datetime(df_per_days['day'])
    elif 'datetime' in grouping:
        df_per_days['datetime'] = pd.to_datetime(pd.to_datetime(df_per_days['datetime']).dt.date)
    elif 'day_hour' in grouping:
        df_per_days['day_hour'] = pd.to_datetime(pd.to_datetime(df_per_days['day_hour'], format = "%Y%m%d%H"))
    if 'sub_id' in df_per_days.columns:
        df_per_days = df_per_days.drop('sub_id', axis = 1)
    return(df_per_days)                