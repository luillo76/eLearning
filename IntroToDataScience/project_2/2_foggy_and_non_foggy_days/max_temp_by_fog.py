import pandas as pd
import pandasql

##Index([u'date', u'maxpressurem', u'maxdewptm', u'maxpressurei', u'maxdewpti', u'since1julheatingdegreedaysnormal', u'heatingdegreedaysnormal', u'since1sepcoolingdegreedaysnormal', u'hail', u'since1julsnowfallm', u'since1julheatingdegreedays', u'maxvisi', u'since1sepheatingdegreedaysnormal', u'heatingdegreedays', u'mindewptm', u'since1sepheatingdegreedays', u'maxwspdm', u'since1julsnowfalli', u'since1sepcoolingdegreedays', u'snow', u'meanvism', u'meandewptm', u'snowdepthm', u'meanvisi', u'fog', u'snowdepthi', u'minvism', u'since1jancoolingdegreedays', u'minvisi', u'coolingdegreedaysnormal', u'gdegreedays', u'maxwspdi', u'meanwindspdi', u'meanpressurei', u'monthtodateheatingdegreedaysnormal', u'meanwindspdm', u'meanpressurem', u'tornado', u'mindewpti', u'mintempi', u'meandewpti', u'rain', u'mintempm', u'minhumidity', u'precipsource', u'minwspdi', u'meanwdird', u'meanwdire', u'minwspdm', u'monthtodatesnowfalli', u'monthtodatecoolingdegreedaysnormal', u'monthtodatesnowfallm', u'maxhumidity', u'coolingdegreedays', u'maxtempm', u'minpressurei', u'monthtodatecoolingdegreedays', u'maxtempi', u'minpressurem', u'humidity', u'precipi', u'snowfalli', u'since1jancoolingdegreedaysnormal', u'precipm', u'snowfallm', u'thunder', u'monthtodateheatingdegreedays', u'meantempi', u'maxvism', u'meantempm'], dtype='object')
##
def max_temp_aggregate_by_fog(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data.  The SQL query should return two columns and
    two rows - whether it was foggy or not (0 or 1) and the max
    maxtempi for that fog value (i.e., the maximum max temperature
    for both foggy and non-foggy days).  The dataframe will be 
    titled 'weather_data'. You'll need to provide the SQL query.
    
    You might also find that interpreting numbers as integers or floats may not
    work initially.  In order to get around this issue, it may be useful to cast
    these numbers as integers.  This can be done by writing cast(column as integer).
    So for example, if we wanted to cast the maxtempi column as an integer, we would actually
    write something like where cast(maxtempi as integer) = 76, as opposed to simply 
    where maxtempi = 76.
    
    You can see the weather data that we are passing in below:
    https://www.dropbox.com/s/7sf0yqc9ykpq3w8/weather_underground.csv
    '''
    weather_data = pd.read_csv(filename)

    q = "select fog, max(cast (maxtempi as integer)) from weather_data group by fog;"

    #Execute your SQL command against the pandas frame
    rainy_days = pandasql.sqldf(q.lower(), locals())
    return rainy_days


if __name__ == "__main__":
    input_filename = "weather_underground.csv"
    output_filename = "output.csv"
    student_df = max_temp_aggregate_by_fog(input_filename)
    student_df.to_csv(output_filename)
