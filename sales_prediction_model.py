import pandas as pd
import numpy as np
import datetime as dt
# import date
import pickle


# input = [3, '2018-02-01']


def input_processing(input):
    print(input)
    dc = {"date" : input[1], "item": input[0], 'sales': 0}

    df = pd.DataFrame(dc, index=[0])

    df["date"] = pd.to_datetime(df["date"])
    df["year_month"] = df["date"].dt.to_period('M')
    df["year_month"] = df["year_month"].astype(str)

    df = df.groupby(["year_month", "item"]).agg({"sales":"sum"})

    # print(df)
    df = df.reset_index()
    df.groupby("item").agg({"sales":"sum"}).sort_values \
    (by="sales", ascending=False).head()
    df.groupby("item").agg({"sales":"sum"}).sort_values \
    (by="sales").head()

    print((df["year_month"]))
    
    # print((df["year_month"][0]))
    # print(df["month"])
    df["month"] = str(df["year_month"][0])[5:]

    df["year"] = int(str(df["year_month"][0])[:4])

    # print(df)

    # print(df)
    # final_df = create_date_features(final_df)
    #We will add lag features for sales variable (3 months, 6 months, 12 months)
    def lag_features(dataframe, lags):
        for lag in lags:
            dataframe['sales_lag_' + str(lag)] = dataframe.groupby(["item"])['sales'].transform(
                lambda x: x.shift(lag))
        return dataframe
    df = lag_features(df, [3, 6, 12])
    #We will add rolling mean features for sales variable (3 months, 6 months, 12 months, 15 months)
    def roll_mean_features(dataframe, windows):
        for window in windows:
            dataframe['sales_roll_mean_' + str(window)] = dataframe.groupby([ "item"])['sales']. \
                                                            transform(
                lambda x: x.shift(1).rolling(window=window, min_periods=2, win_type="triang").mean())
        return dataframe
    df = roll_mean_features(df, [3, 6, 12, 15])

    #Finally, we will add exponentially weighted mean features (3 months, 6 months, 12 months, 15 months)
    def ewm_features(dataframe, alphas, lags):
        for alpha in alphas:
            for lag in lags:
                dataframe['sales_ewm_alpha_' + str(alpha).replace(".", "") + "_lag_" + str(lag)] = \
                    dataframe.groupby([ "item"])['sales'].transform(lambda x: x.shift(lag).ewm(alpha=alpha).mean())
        return dataframe

    alphas = [0.95, 0.9, 0.8, 0.7, 0.5]
    lags = [3, 6, 9, 12, 15]
    df = ewm_features(df, alphas, lags)

    df = pd.get_dummies(df, columns=[ 'item', 'month']) #One-hot encoding
    df['sales'] = np.log1p(df["sales"].values) 

    train_lgbm = df.loc[df["year"].astype(int)<2017]
    val_lgbm = df.loc[df["year"].astype(int)==2017]

    cols = [col for col in df.columns if col not in ["id", "sales", "year_month", "year"]]
    # print(len(cols))

    cols = ['sales_lag_3',
    'sales_lag_6',
    'sales_lag_12',
    'sales_roll_mean_3',
    'sales_roll_mean_6',
    'sales_roll_mean_12',
    'sales_roll_mean_15',
    'sales_ewm_alpha_095_lag_3',
    'sales_ewm_alpha_095_lag_6',
    'sales_ewm_alpha_095_lag_9',
    'sales_ewm_alpha_095_lag_12',
    'sales_ewm_alpha_095_lag_15',
    'sales_ewm_alpha_09_lag_3',
    'sales_ewm_alpha_09_lag_6',
    'sales_ewm_alpha_09_lag_9',
    'sales_ewm_alpha_09_lag_12',
    'sales_ewm_alpha_09_lag_15',
    'sales_ewm_alpha_08_lag_3',
    'sales_ewm_alpha_08_lag_6',
    'sales_ewm_alpha_08_lag_9',
    'sales_ewm_alpha_08_lag_12',
    'sales_ewm_alpha_08_lag_15',
    'sales_ewm_alpha_07_lag_3',
    'sales_ewm_alpha_07_lag_6',
    'sales_ewm_alpha_07_lag_9',
    'sales_ewm_alpha_07_lag_12',
    'sales_ewm_alpha_07_lag_15',
    'sales_ewm_alpha_05_lag_3',
    'sales_ewm_alpha_05_lag_6',
    'sales_ewm_alpha_05_lag_9',
    'sales_ewm_alpha_05_lag_12',
    'sales_ewm_alpha_05_lag_15',
    'item_1',
    'item_2',
    'item_3',
    'item_4',
    'item_5',
    'item_6',
    'item_7',
    'item_8',
    'item_9',
    'item_10',
    'item_11',
    'item_12',
    'item_13',
    'item_14',
    'item_15',
    'item_16',
    'item_17',
    'item_18',
    'item_19',
    'item_20',
    'item_21',
    'item_22',
    'item_23',
    'item_24',
    'item_25',
    'item_26',
    'item_27',
    'item_28',
    'item_29',
    'item_30',
    'item_31',
    'item_32',
    'item_33',
    'item_34',
    'item_35',
    'item_36',
    'item_37',
    'item_38',
    'item_39',
    'item_40',
    'item_41',
    'item_42',
    'item_43',
    'item_44',
    'item_45',
    'item_46',
    'item_47',
    'item_48',
    'item_49',
    'item_50',
    'month_01',
    'month_02',
    'month_03',
    'month_04',
    'month_05',
    'month_06',
    'month_07',
    'month_08',
    'month_09',
    'month_10',
    'month_11',
    'month_12']


    # print(len(cols))
    count = 34
    for i in cols:
        if i not in df.columns:
            df.insert(count, i, [0], True)
            count+=1


    X_val = df[cols]
    Y_val = df["sales"]
    model_path = 'Model/model_pkl.pkl'
    model_load = pickle.load(open(model_path, 'rb'))
    # print(X_val)
    y_pred_val = (model_load.predict(X_val))
    
    result = round(y_pred_val[0], 4)
    return result

# def define_model():

#     model_path = 'model_pkl.pkl'
#     model_load = pickle.load(open(model_path, 'rb'))
#     return model_load

# print(X_val)
# X_val=X_val.drop(['date'], axis=1)
