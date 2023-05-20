from main.models import ERV


def graph_data_dict(workerErvs, year):
    graph_data = {}
    active_years = []
    graph_data['data']=[]
    graph_data['labels']=['Siječanj', 'Veljača', 'Ožujak', 'Travanja','Svibanj','Lipanj', 'Srpanj', 'Kolovoz', 'Rujan', 'Listopad', 'Studeni', 'Prosinac']
    ervs_for_year = []
    for erv in workerErvs:
        if str(erv.current_date.year) not in active_years:
            active_years.append(str(erv.current_date.year))
        if erv.current_date.year == int(year):
            ervs_for_year.append(erv)
    
    graph_data['years'] = active_years

    for month in range(1,13):
        month_ervs = 0
        for erv in ervs_for_year:
            if erv.current_date.month==month:
                month_ervs += 1
        graph_data['data'].append(month_ervs)
    return graph_data
