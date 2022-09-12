from datetime import datetime, timedelta
import random
MODELS = 200
DOMAINS = 10

list_of_dimensions = ['Completeness', 'Conformity', 'Consistency', 'Integrity', 'Timeliness', 'Uniqueness']
list_of_status = ['Pass', "Fail"]

def base_data():
    today = datetime.today()
    start = today - timedelta(days=30)
    end = today - timedelta(days=1)
    dt = start
    df = []

    while dt <= end:
        for m in range(MODELS):
            domain = m%DOMAINS
            domain_name = "domain_" + str(domain)
            model_name = "model_" + str(m)
            tc_for_model = random.randint(5,15)
            for t in range(tc_for_model):
                dimension = random.choice(list_of_dimensions)
                test_case_no = dimension + "_" + str(t)
                base = {'status': random.choice(list_of_status),
                        'test_case_no': test_case_no,
                        'dimension': dimension,
                        'domain': domain_name,
                        'model': model_name,
                        'execution_time_in_seconds': str(random.randint(5,600)),
                        'run_date_time': dt.strftime('%Y-%m-%d %H:%M:%S')}

                df.append(base)
        dt = dt + timedelta(days=1)

    return df

if __name__ == '__main__':
    data = base_data()
    with open('data.csv', 'w') as fo:
        header = "|".join(data[0].keys())
        fo.write(header)
        fo.write("\n")
        for d in data:
            line = "|".join(d.values())
            fo.write(line)
            fo.write("\n")
