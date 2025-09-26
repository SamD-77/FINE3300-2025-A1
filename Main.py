class MortgagePayment():
    def __init__(self, quoted_rate, amortization_period):
        self.quoted_rate = quoted_rate
        self.amortization_period = amortization_period

    def pva_factor(self, periodic_rate, num_payments):
        """
        Function to calculate the Present Value of Annuity Factor
        """
        pva = (1 - (1 + periodic_rate)**-num_payments) / periodic_rate
        return pva

    def payments(self, principal):
        """
        Takes the principal amount and returns a tuple of all the periodic payment options
        """   
        # Dict with number of payments in year for each payment option
        pmt_frequencies = {
            "monthly": 12,
            "semi-monthly": 24,
            "bi-weekly": 26,
            "weekly": 52
        }

        # Convert semi annual quoted rate to effective annual rate (EAR)
        ear = (1 + self.quoted_rate / 2)**2 - 1

        payment_amounts = [] # list holding calculated payment option amounts
    
        # Loop through payment frequencies dict for each option
        for freq in pmt_frequencies.values():
            periodic_rate = (1 + ear) ** (1 / freq) - 1 # calculate rate for the period with EAR and yearly payment frequency 
            num_pmts = freq * self.amortization_period # calculate number of payments across the amortization period
            payment_amount = principal / self.pva_factor(periodic_rate, num_pmts) # calculate the payment amount
            payment_amounts.append(payment_amount) # add to list of payment amounts

        # Add accelerated payment options to list
        monthly_pmt = payment_amounts[0] # monthly payment amount is first index
        rapid_bi_pmt = monthly_pmt / 2 # calculate accelerated bi-weekly payment amount from monthly amount
        rapid_weekly_pmt = monthly_pmt / 4 # calculate accelerated weekly payment amount from monthly amount
        payment_amounts.append(rapid_bi_pmt)
        payment_amounts.append(rapid_weekly_pmt)

        # Return all payment options as tuple
        return tuple(payment_amounts)
    

class ExchangeRates():
    def __init__(self, file_path):
        """
        Initialize with path to the exchange rate file and reads the most recent USD/CAD exchange rate
        """

        rates_file = open(file_path) # open file
        rates = rates_file.read() # read file

        # Format to 2D list of lists
        rates = rates.split("\n") # split into rows
        rates = [rate.split(",") for rate in rates] # split into columns

        # Set exchange rate
        # Use last row for most recent rate (-2 because last row is empty)
        # Find column by getting index for USD/CAD rate from the top row of headers
        self.exchange_rate = float(rates[-2][rates[0].index("USD/CAD")])

        rates_file.close() # close file


    def convert(self, amount, base_currency, target_currency):
        """
        Takes the amount and two currencies and coverts from one currency to another using the exchange rates read from the exchange rate file
        """
        if base_currency == target_currency: # convert to same currency
            return amount
        
        elif base_currency == "USD" and target_currency == "CAD": # USD to CAD
            return amount * self.exchange_rate
        
        elif base_currency == "CAD" and target_currency == "USD": # CAD to USD
            return amount / self.exchange_rate



# ------------------ Part 1: Mortgage Payments ------------------
# Prompt user to collect relevant data and convert data type from str
principal_amount = float(input("Enter the principal ($): "))
interest_rate = float(input("Enter the quoted interest rate % (e.g 4.85): ")) / 100 # convert from percentage to decimal
amortization_period = int(input("Enter the amortization period in years: "))

# Instantiate object of MortgagePayment
mortgage = MortgagePayment(interest_rate, amortization_period)

# Format and display output
payment_amounts = mortgage.payments(principal_amount) # tuple of payment options amounts

labels = ["Monthly", "Semi-monthly", "Bi-weekly", "Weekly", "Rapid Bi-weekly", "Rapid Weekly"]

print("-" * 25) # line break

# Loop through labels list and payment amounts tuple
for i in range(len(payment_amounts)):
    print(f"{labels[i]} Payment: ${payment_amounts[i]:.2f}") # print each label and corresponding value rounded 2 decimals



# ------------------ Part 2: Exchange Rates ------------------
# Prompt user to input relevant data
print("\n" * 2) # new lines
amount = float(input("Enter the amount to convert ($): "))
from_currency = input("Enter the base currency: ").upper() # input as uppercase
to_currency = input("Enter the currency you are converting to: ").upper()

# Instantiate exchange rates object with file path
exchange_rate = ExchangeRates("BankOfCanadaExchangeRates.csv") 

# Output results
print("-" * 25) # line break
print(f"${amount:.2f} {from_currency} = ${exchange_rate.convert(amount, from_currency, to_currency):.2f} {to_currency}")