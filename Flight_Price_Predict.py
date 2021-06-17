import pandas as pd
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import sys

remove_col = ['Route', 'Additional_Info']
training_dataset = 'datasets_140442_330428_Data_Train.xlsx'
testing_dataset = 'datasets_140442_330428_Test_set.xlsx'
model_filename = 'finalized_model.pkl'


def date_of_journey_extract(flight_df):
    # Date_of_Journey column does have month and day information which will be kept in two separate columns.

    flight_df['Journey_Month'] = pd.to_datetime(flight_df['Date_of_Journey'], dayfirst=True).dt.month
    flight_df['Journey_Date'] = pd.to_datetime(flight_df['Date_of_Journey'], dayfirst=True).dt.day

    # Now we can drop this column.
    remove_col.append('Date_of_Journey')
    return flight_df


def dep_time_extract(flight_df):
    # we will split this record in hour and minute column
    flight_df['Dep_Hour'] = pd.to_datetime(flight_df['Dep_Time']).dt.hour
    flight_df['Dep_Minute'] = pd.to_datetime(flight_df['Dep_Time']).dt.minute

    # let's drop this column
    remove_col.append('Dep_Time')
    return flight_df


def arrival_time_extract(flight_df):
    # we will extract hour and minute info from this column and will drop this at the end
    flight_df['Arrival_Hour'] = pd.to_datetime(flight_df['Arrival_Time']).dt.hour
    flight_df['Arrival_Minute'] = pd.to_datetime(flight_df['Arrival_Time']).dt.minute

    remove_col.append('Arrival_Time')
    return flight_df


def duration_extract(flight_df):
    # print(duration_list[0])
    flight_df['Duration'] = flight_df['Duration'].apply(lambda x: '0h ' + x if 'h' not in x and 'm' in x else x + ' 0m' if 'm' not in x and 'h' in x else x)
    flight_df['Duration_Hour'] = flight_df['Duration'].apply(lambda x: int(x.strip().split()[0].replace('h', '')))
    flight_df['Duration_Minute'] = flight_df['Duration'].apply(lambda x: int(x.strip().split()[1].replace('m', '')))
    remove_col.append('Duration')
    return flight_df


def total_stop_manipulation(flight_df):
    # we will replace 'non-stop' as '0 stops' and then remove ' stops' word
    flight_df['Total_Stops'] = flight_df['Total_Stops'].replace('non-stop', '0 stops')
    print('Total stop : ', flight_df['Total_Stops'].unique())
    flight_df['Total_Stops'] = flight_df['Total_Stops'].apply(lambda x: x.split()[0])
    flight_df['Total_Stops'] = pd.to_numeric(flight_df['Total_Stops'])
    # convert this column into integer
    # print(flight_df['Total_Stops'])
    return flight_df


def feature_remove(df, labels):
    df.drop(labels=labels, axis=1, inplace=True)
    return df


def missing_value_handle(train_df):
    # Flight departure time is 09:45 06th May,2019 and arrival time is 09:25 07th May,2019... We don't have any info of Route and Total_Stops.
    # As per knowledge, flight is having 1 stop. But not sure. Hence am removing this row.
    train_df.dropna(axis=0, how='any', inplace=True)
    # let's check flight price after removing null value
    train_df.isnull().sum()
    return train_df


def feature_engineering_pipeline(df):
    df = missing_value_handle(df)
    df = date_of_journey_extract(df)
    df = dep_time_extract(df)
    df = arrival_time_extract(df)
    df = duration_extract(df)
    df = total_stop_manipulation(df)
    return df


# Categorical Data Handling
def oneHotEncoding(df, column):
    temp = pd.get_dummies(data=df[[column]], prefix=column, prefix_sep='_', drop_first=False)
    df = pd.concat([df, temp], axis=1)
    remove_col.append(column)
    return df


def categoricalDataHandling(data):
    data = oneHotEncoding(data, 'Source')
    print('Source unique : ', data['Source'].unique())
    data['Destination'] = data['Destination'].replace('New Delhi','Delhi')
    data = oneHotEncoding(data, 'Destination')
    print('Destination : ', data['Destination'].unique())
    data = oneHotEncoding(data, 'Airline')
    print('Airline : ', data['Airline'].unique())
    data = feature_remove(data, list(set(remove_col)))
    return data


# Model Creation
def metrics_calculation(model, train_x, test_x, train_y, test_y):
    yhat = model.predict(test_x)
    print('Train Score : ', model.score(train_x, train_y))
    print('Test Score :', model.score(test_x, test_y))
    mae = mean_absolute_error(test_y, yhat)
    mse = mean_squared_error(test_y, yhat)
    rmse = np.sqrt(mse)
    r_squared = r2_score(test_y, yhat)
    adjusted_r2 = 1 - (1 - r_squared) * (len(test_y) - 1) / (len(test_y) - test_x.shape[1] - 1)
    print('MAE : ', mae)
    print('MSE : ', mse)
    print('RMSE : ', rmse)
    print('R-Squared : ', r_squared)
    print('Adjusted R^2 : ', adjusted_r2)
    return mae, mse, rmse, r_squared, adjusted_r2


def model_save(model_name):
    pickle.dump(model_name, open(model_filename, 'wb'))


def RF_Model(train_x, train_y):
    # print(train_x.columns.tolist())
    final_model = RandomForestRegressor(bootstrap=True, ccp_alpha=0.0, criterion='mse',
                                        max_depth=25, max_features='auto', max_leaf_nodes=None,
                                        max_samples=None, min_impurity_decrease=0.0,
                                        min_impurity_split=None, min_samples_leaf=1,
                                        min_samples_split=10, min_weight_fraction_leaf=0.0,
                                        n_estimators=600, n_jobs=None, oob_score=False,
                                        random_state=None, verbose=0, warm_start=False)
    final_model.fit(train_x, train_y)
    model_save(final_model)


def training():
    train_df = train_df = pd.read_excel(training_dataset, sheet_name='Sheet1')
    train_df = feature_engineering_pipeline(train_df)
    print('Feature engineering completed...')
    print('No of columns after feature engineering : ', train_df.shape[1])
    train_df = categoricalDataHandling(train_df)
    print('Categorical Data Handling done...')
    print('Total no of columns : ', train_df.shape[1])
    x = train_df.drop('Price', axis=1)
    y = train_df['Price']
    print('train df columns : ', x.columns)
    RF_Model(x, y)
    print('Model created successfully...')


def load_model(model_name):
    loaded_model = pickle.load(open(model_name, 'rb'))
    return loaded_model


def columns_dict_prep():
    column_list = ['Total_Stops', 'Journey_Month', 'Journey_Date', 'Dep_Hour', 'Dep_Minute', 'Arrival_Hour', 'Arrival_Minute', 'Duration_Hour',
                   'Duration_Minute', 'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai', 'Source_Banglore','Destination_Cochin', 'Destination_Delhi',
                   'Destination_Hyderabad', 'Destination_Kolkata', 'Destination_Banglore', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
                   'Airline_Jet Airways', 'Airline_Jet Airways Business', 'Airline_Multiple carriers', 'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
                   'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy', 'Airline_Air Asia']
    column_dict = {col: 0 for col in column_list}
    return column_dict

def predict(airline, date_of_journey, source, destination, dept_time, arrival_time, duration, no_of_stops):
    column_dict = columns_dict_prep()
    print('Column Dict before updating : ', column_dict)

    updated_dict = {'Airline_' + airline: 1, 'Source_' + source: 1, 'Destination_' + destination: 1, 'Journey_Month': date_of_journey.month,
                    'Journey_Date': date_of_journey.day, 'Dep_Hour':dept_time.hour, 'Dep_Minute': dept_time.minute,'Arrival_Hour': arrival_time.hour,
                    'Arrival_Minute': arrival_time.minute, 'Duration_Hour': duration.strip().split()[0].replace('h',''), 'Duration_Minute': duration.strip().split()[1].replace('m','')}
    column_dict.update(updated_dict)
    print('\n\n Updated column dict : \n', column_dict)
    print(len(list(column_dict.keys())))
    test_df = pd.DataFrame(column_dict, index=[0])
    # print('total dict : ', test_df.head())
    model = load_model(model_filename)
    #test_df = feature_engineering_pipeline(test_df)
    #print('Feature engineering completed...')
    print('No of columns after feature engineering : ', test_df.shape[1])
    #test_df = categoricalDataHandling(test_df)
    #print('Categorical Data Handling done...')
    #print('Total no of columns : ', test_df.columns)
    # RF_Model(x, y)
    predict = model.predict(test_df)
    print('Predict : ', predict)
    print('Model is predicted successfully...')
    return predict[0]


if __name__ == "__main__":
    print(sys.executable)
    training()

