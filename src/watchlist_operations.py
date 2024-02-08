import os
import pandas as pd

import constants as c


def watchlist(folder, index):
    query = {}
    files_list = [file for file in os.listdir(
        f'{folder}\\') if file.endswith(".csv")]

    report = pd.read_csv(os.path.join(folder, files_list[-1]))
    df = pd.read_csv(os.path.join(folder, files_list[0]))

    for symbol in report["SYMBOL"]:
        if symbol in df["SYMBOL"].tolist():
            report_index = report.index.get_loc(
                report[report['SYMBOL'] == symbol].index[0])
            df_index = df.index.get_loc(df[df['SYMBOL'] == symbol].index[0])
            old_close = df.at[df_index, 'CLOSE']
            current_close = report.at[report_index, 'CLOSE']
            roc = ((current_close - old_close) / old_close) * 100
            query[symbol] = roc

    report = report.query('SERIES == "EQ"')  # Adjust as needed
    df = df.query('SERIES == "EQ"')  # Adjust as needed

    report.insert(len(report.columns), 'ROC',
                  value=report['SYMBOL'].map(query))
    report = report.sort_values(by='ROC', ascending=False)

    # Read existing Excel file
    existing_data = pd.read_excel(c.RESULTS_FILE, sheet_name=None)

    # Specify sheet names
    sheet_names = ['3 MONTHS', '1 MONTH', '5 DAYS']

    # Update the existing sheets or create new ones
    with pd.ExcelWriter(c.RESULTS_FILE, engine='xlsxwriter') as writer:
        for sheet_name in sheet_names:
            # If the sheet already exists, overwrite the new data
            if sheet_name in existing_data:
                report.head(50).to_excel(
                    writer, sheet_name=sheet_name, index=False)
            else:
                # If the sheet doesn't exist, create a new one
                report.head(50).to_excel(
                    writer, sheet_name=sheet_name, index=False)




def closingFilter(folder):
    del_columns = ['TOTTRDVAL', 'TIMESTAMP', 'TOTALTRADES',
                   'ISIN', 'Unnamed: 13', 'ROC', 'LAST']
    folder = os.path.join(folder, "DATA/1 MONTH")
    files_list = [file for file in os.listdir(
        f'{folder}\\') if file.endswith(".csv")]
    currentFile = pd.read_csv(os.path.join(folder, files_list[-2]))
    cmp = dict(zip(currentFile['SYMBOL'], currentFile['CLOSE']))
    f1 = pd.read_csv(os.path.join(folder, files_list[-3]))
    d1 = dict(zip(f1['SYMBOL'], f1['CLOSE']))
    f2 = pd.read_csv(os.path.join(folder, files_list[-4]))
    d2 = dict(zip(f2['SYMBOL'], f2['CLOSE']))
    f3 = pd.read_csv(os.path.join(folder, files_list[-5]))
    d3 = dict(zip(f3['SYMBOL'], f3['CLOSE']))


    one_month = pd.read_excel(c.RESULTS_FILE, sheet_name='1 MONTH')
    three_months = pd.read_excel(c.RESULTS_FILE, sheet_name='3 MONTHS')
    five_days = pd.read_excel(c.RESULTS_FILE,sheet_name='5 DAYS')

    one_month['CMP'] = one_month['SYMBOL'].map(cmp)
    three_months['CMP'] = three_months['SYMBOL'].map(cmp)
    five_days['CMP'] = five_days['SYMBOL'].map(cmp)

    one_month['D1'] = one_month['SYMBOL'].map(d1)
    three_months['D1'] = three_months['SYMBOL'].map(d1)
    five_days['D1'] = five_days['SYMBOL'].map(d1)

    one_month['D2'] = one_month['SYMBOL'].map(d2)
    three_months['D2'] = three_months['SYMBOL'].map(d2)
    five_days['D2'] = five_days['SYMBOL'].map(d2)

    one_month['D3'] = one_month['SYMBOL'].map(d3)
    three_months['D3'] = three_months['SYMBOL'].map(d3)
    five_days['D3'] = five_days['SYMBOL'].map(d3)

    condition = '((CLOSE < 1.01*CMP) & (CLOSE>.99*CMP)) & ((CMP < 1.01*D1) & (CMP>.99*D1)) & ((D1 < 1.01*D2) & (D1>.99*D2)) & ((D2 < 1.01*D3) & (D2>.99*D3))'
    for col in del_columns:
        one_month.pop(col)
        three_months.pop(col)
        five_days.pop(col)

    five_days.query(condition).to_excel(c.FIVE_DAYS_FILE, index=False)
    one_month.query(condition).to_excel(c.ONE_MONTH_FILE, index=False)
    three_months.query(condition).to_excel(c.THREE_MONTHS_FILE, index=False)

