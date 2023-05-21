MONTHS = ['Siječanj', 'Veljača', 'Ožujak', 'Travanj','Svibanj','Lipanj', 'Srpanj', 'Kolovoz', 'Rujan', 'Listopad', 'Studeni', 'Prosinac']
WORK_FLAGS = ['Redovni rad', 'Putni nalog', 'Bolovanje', 'Slobodan dan', 'Godišnji odmor', 'Rad od kuće']
MONTH_VALUE = {
    'Siječanj': 1,
    'Veljača': 2,
    'Ožujak': 3,
    'Travanj': 4,
    'Svibanj': 5,
    'Lipanj': 6,
    'Srpanj':7,
    'Kolovoz': 8,
    'Rujan': 9,
    'Listopad': 10,
    'Studeni': 11,
    'Prosinac': 12
}

def graph_data_dict(workerErvs, year):
    graph_data = {}

    pie_chart = {
        'Redovni rad': 0,
        'Putni nalog': 0,
        'Bolovanje': 0,
        'Slobodan dan': 0,
        'Godišnji odmor': 0,
        'Rad od kuće': 0,
        'labels': WORK_FLAGS, 
        'data': []
    }

    bar_chart = {
        'data': [],
        'labels': MONTHS
    }
    
    active_years = []
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
                pie_chart[erv.flag] += 1
        bar_chart['data'].append(month_ervs)

    for label in pie_chart['labels']:
        pie_chart['data'].append(pie_chart[label])

    graph_data['bar_chart'] = bar_chart
    graph_data['pie_chart'] = pie_chart
    return graph_data

def specific_pie_chart(workerErvs, year, month):
    pie_chart = {
        'Redovni rad': 0,
        'Putni nalog': 0,
        'Bolovanje': 0,
        'Slobodan dan': 0,
        'Godišnji odmor': 0,
        'Rad od kuće': 0,
        'labels': WORK_FLAGS, 
        'data': [],
        'months': MONTHS
    }

    for erv in workerErvs:
        if month == 'Ukupno':
            if erv.current_date.year == int(year):
                pie_chart[erv.flag] +=1
        else:
            if erv.current_date.year == int(year) and erv.current_date.month == MONTH_VALUE[month]:
                pie_chart[erv.flag] +=1

    for label in pie_chart['labels']:
        pie_chart['data'].append(pie_chart[label])

    return pie_chart