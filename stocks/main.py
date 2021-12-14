import pandas


def clean_currency(x):
    """ If the value is a string, then remove currency symbol and delimiters
    otherwise, the value is numeric and can be converted
    """
    if isinstance(x, str):
        return x.replace('$', '').replace(',', '')
    return x


transactions_df = pandas.read_csv('Savings - Stock transactions.csv')

for c in ['Shares', 'Share price', 'Buy Price', 'Buy Commission', 'Cost Basis']:
    transactions_df[c] = transactions_df[c].apply(clean_currency).astype('float')


def calculate_losses(stock, share_price):
    individual_transactions = transactions_df[transactions_df['Fund / Stock'] == stock]

    overpriced_stocks = individual_transactions[individual_transactions['Share price'] > share_price]
    current_value_of_overpriced_stocks = overpriced_stocks['Shares'] * share_price
    losses = (overpriced_stocks['Cost Basis'] - current_value_of_overpriced_stocks).sum()

    underpriced_stocks = individual_transactions[individual_transactions['Share price'] <= share_price]
    current_value_of_underpriced_stocks = underpriced_stocks['Shares'] * share_price
    gains = (current_value_of_underpriced_stocks - underpriced_stocks['Cost Basis']).sum()
    total_returns = (individual_transactions['Shares'] * share_price).sum()

    print(f'total value of overpriced shares: {current_value_of_overpriced_stocks.sum()}')
    print(f'number of shares priced greater than {share_price}: {overpriced_stocks["Shares"].sum()}')
    print(f'total number of shares: {individual_transactions["Shares"].sum()}')
    print(f'losses: {losses}')
    print(f'gains: {gains}')
    print(f'total returns: {total_returns}')


calculate_losses('VTSAX', 108.26)
