def weightgiver(api_key, host, offer_id, prob_minmax = (0.1, 0.9)):
    
    """
        Функция для раздачи офферам в партнёрке весов (сплитование)
    
        Args:
            api_key: (str) - апи-ключ для доступа в кейтаро
            host: (str) - url для доступа к кейтаро
            offer_id: (str) - id оффера из кейтаро
            prob_minmax: (tuple) - вектор из интервала минимальнго и максимального процента, который может дать модель
    
    """
    
    from scipy.optimize import linprog    
    import numpy as np
    from MVPanalytics.keitaro import keitaro_parser
    spl = keitaro_parser(api_key, host,
        interval='today',
        filters = [{'name': "stream_id", 'operator': "EQUALS", 'expression': offer_id}],
    grouping = ["stream", "offer"],
    metrics = ['epc_confirmed', 'clicks']
    )


    c = np.array(spl['epc_confirmed'].values)*(-1)

    A_eq = np.array([np.ones(len(c))])
    b_eq = np.array([1])

    prob_n = np.array([ prob_minmax for i in range(len(c))])

    res = linprog(c = c, A_eq = A_eq, b_eq = b_eq, bounds = prob_n)

    spl['weights'] = res.x *100
    return(spl)

def off_analyzer(data,target,showcases = False):
    
    """
        Функция, позволяющая выявлять витрины по потоку (или офферу), на которых его: target < EPC, 0 < EPC < target, EPC=0
        
        Args:
            data: (pd.Dataframe) - спаршенные данные с кейтаро, которые должны содержать колонки ['epc_confirmed', 'external_id', 'clicks', 'sale_revenue']
            target: (float) - нижнее удовлетворяющее значеие EPC
            showcases: (bool) - нужна ли подробная таблица, которая выдаёт сами external с epc ниже таргета
            
            Выдача:
                Если showcases = False: Возвращает одну таблицу, которая показывает сколько кликов отливается на витрины с epc по потоку target < EPC, 0 < EPC < target, EPC=0 без уточнения того, какие это витрины
                Если showcases = True: Возвращает 2 таблицs, первая - как из showcases = False, вторая - вместе с external_id
    """
    
    
    
    data['more'] = data['epc_confirmed'].apply(lambda x: f'more than {target} epc' if x >target else( f'less then {target}' if ((x<target)&(x>0))  else 'zero_epc'))
    gr = data[['more', 'epc_confirmed','clicks','sale_revenue']].groupby(by='more').agg({'clicks':['sum','mean','max'], 'sale_revenue':'sum', 'epc_confirmed':['min', 'max']})

    gr['epc_agregated'] = gr[('sale_revenue','sum')]/gr[('clicks', 'sum')]
    if showcases == False:
        return(gr)
    else:
        gr_1 = data[['more', 'external_id','clicks','epc_confirmed']].groupby(by=['more','external_id']).sum().sort_values(by=['more','clicks'], ascending=False)
        return(gr, gr_1)