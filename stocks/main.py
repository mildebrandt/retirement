import pandas


def clean_currency(x):
    """ If the value is a string, then remove currency symbol and delimiters
    otherwise, the value is numeric and can be converted
    """
    if isinstance(x, str):
        if x in ['—', 'Free']:
            return 0.0
        return x.replace('$', '').replace(',', '').replace('−', '-')
    return x


transactions_df = pandas.read_csv('Savings - Vanguard.csv')
transactions_df['NAME'] = transactions_df['NAME'].apply(lambda x: x.split()[0])

for c in ['QUANTITY', 'PRICE', 'AMOUNT', 'COMMISSIONS & FEES']:
    transactions_df[c] = abs(transactions_df[c].apply(clean_currency).astype('float'))


def calculate_losses(stock, share_price):
    # Look only at buy and reinvestment transactions.
    # individual_transactions = transactions_df.loc[
    #     (transactions_df['NAME'].str.startswith(stock) & )]
    buy_transactions = reinvestment_transactions = transactions_df[
        transactions_df['NAME'].str.startswith(stock)]

    buy_transactions = buy_transactions[buy_transactions['TRANSACTION TYPE'].str.startswith('Buy')]
    reinvestment_transactions = reinvestment_transactions[
        reinvestment_transactions['TRANSACTION TYPE'].str.startswith('Reinvestment')]

    purchase_transactions = pandas.concat([buy_transactions, reinvestment_transactions])

    purchase_transactions['CURRENT VALUE'] = purchase_transactions['QUANTITY'] * share_price
    purchase_transactions['GAIN / LOSS'] = (purchase_transactions['CURRENT VALUE'] -
                                            purchase_transactions['AMOUNT'])

    overpriced_stocks = purchase_transactions[purchase_transactions['PRICE'] > share_price]
    print(overpriced_stocks[['TRADE DATE', 'NAME', 'QUANTITY', 'PRICE',
                             'AMOUNT', 'CURRENT VALUE', 'GAIN / LOSS']])
    current_value_of_overpriced_stocks = overpriced_stocks['QUANTITY'] * share_price
    losses = (overpriced_stocks['AMOUNT'] - current_value_of_overpriced_stocks).sum()

    underpriced_stocks = purchase_transactions[purchase_transactions['PRICE'] <= share_price]
    current_value_of_underpriced_stocks = underpriced_stocks['QUANTITY'] * share_price
    gains = (current_value_of_underpriced_stocks - underpriced_stocks['AMOUNT']).sum()
    total_value = (purchase_transactions['QUANTITY'] * share_price).sum()

    print()
    print(f'total value of overpriced shares: ${current_value_of_overpriced_stocks.sum():.2f}')
    print(f'number of shares priced greater than ${share_price}: '
          f'{overpriced_stocks["QUANTITY"].sum():.2f}')
    print(f'total number of shares: {purchase_transactions["QUANTITY"].sum():.2f}')
    print(f'losses: ${losses:.2f}')
    print(f'gains: ${gains:.2f}')
    print(f'total value: ${total_value:.2f}')


calculate_losses('VTSAX', 88.79)
calculate_losses('VBTLX', 9.36)
