import pandas as pd

def read_calender(file_name):
    """Reads TimeEdit csv file"""
    df = pd.read_csv(file_name, header = 2, sep = ',')
    return df

def clean_calender(dataframe,program):
    """Remove some unused columns""" #Currently hardcoded
    dataframe = dataframe.drop(['Grupp','URL','Mitt namn','Kurs/program '], axis = 1)
    for row in dataframe['Text']:
        if program not in row:
            dataframe = dataframe[dataframe.Text != row]
    dataframe.fillna('', inplace=True)
    return dataframe

def new_calender(clean_frame): 
    """Creates a new dataframe based on the google format (Subject, Startdate, Starttime, Enddate, Endtime)"""
    sub_list = []
    for sub in clean_frame['Kurs']:
        sub_list.append(sub)

    str_date = []
    for start_date in clean_frame['Startdatum']:
        date = date_converter(start_date)
        str_date.append(date)

    str_time = []
    for start_time in clean_frame['Starttid']:
        time = time_converter(start_time)
        str_time.append(time)
    
    end_date_list = []
    for end_date in clean_frame['Slutdatum']:
        end_d = date_converter(end_date)
        end_date_list.append(end_d)

    end_time_list = []
    for end_time in clean_frame['Sluttid']:
        end_t = time_converter(end_time)
        end_time_list.append(end_t)
    
    description_list = summery(clean_frame)

    data_dict = {'Subject': sub_list,'Start Date': str_date,'Start Time': str_time,'End Date': end_date_list,'End Time': end_time_list, 'Description': description_list}
    calender = pd.DataFrame(data_dict)
    return calender

def time_converter(time):
    """Takes 24-h clock and change it to 12-h clock and adds AM/PM. (ex. 16:00 = 04:00 PM)"""
    numbers = time.split(':')
    number = int(numbers[0])
    end = numbers[1]
    if number < 12 or number == 12:
        result = time + ' AM'
    else:
        value = str(number - 12)
        result = '0'+ value + ':' + end + ' PM'
    return result

def date_converter(date):
    """Changes the date to google-format. (ex. Year-month-date to month/date/year)"""
    datum = date.split('-')
    temp = datum[0]
    datum[0] = datum[1]
    datum[1] = datum[2]
    datum[2] = temp
    result = '/'.join(datum)
    return result

def summery(clean_frame):
    """Adds some of the different columns together with valueble information"""
    moment_list= []
    for moment in clean_frame['Moment']:
        moment_list.append(moment)
    
    person_list = []
    for person in clean_frame['Person']:
        person_list.append(person)
    
    lokal_list = []
    for lokal in clean_frame['Lokal']:
        lokal_list.append(lokal)

    text_list = []
    for text in clean_frame['Text']:
        text_list.append(text)
    
    summery_list = []
    length_of_rows = len(clean_frame)
    for value in range(0,length_of_rows):
        summery_list.append(f'Moment: {moment_list[value]}\nAnsvarig: {person_list[value]}\nSal: {lokal_list[value]}\nInformation: {text_list[value]}')

    return summery_list

def main():
    """Mainprogram, Hardcoded for BTH-Program-codes."""
    program = {1:'DVAMI20h',2: 'MTACI20h', 3:'IEACI20h', 4:'MTGHM20h',5:'MTACI20h',6:'DVADS20h',7:'PAASP20h',8:'DVGHI20h',9:'PAAMJ20h'}
    length = len(program)
    loop = True
    print('-----------------------')
    print('Vad heter din csv fil?')
    print('-----------------------')
    print('Exempel: Bth-schema.csv')
    print('OBS! Case sensitive och avsluta med .csv!')
    file_name = input('Svar: ') # TimeEdit.csv filename.
    print()
    print('-----------------------')
   
    while loop == True:
            for number, info in program.items():
                print(f'{number}. {info}')
            print('-----------------------')
            try: 
                choice = int(input(f'Vilket program tillhör du (1-{length}): '))
            except Exception as error:
                print(f'Error: {error}. Välj mellan siffran 1 och {length} till ditt program')
            else:
                code = program[choice]

            try:
                dataframe = read_calender(file_name)
            except Exception as err:
                print('===========================================')
                print(f'Error: {err}. \nMöjliga fel:\n1. Felstavat csv-filen.\n2. Csv-filen ligger fel.\nTips! Lägg csv-filen i samma mapp som python-scriptet.')
                print('===========================================')
                loop = False
            else:
                clean_frame = clean_calender(dataframe,code)
                calender = new_calender(clean_frame)
                calender.to_csv(f'{code}-kalender.csv', sep=',') # Writes new csv file to import to google.
                print(f'Skapar fil {code}-kalender.csv')
            loop = False
    return

if __name__ == '__main__':
    main()