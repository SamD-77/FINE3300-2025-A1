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
    

test = MortgagePayment(0.055, 25)
print(test.payments(100000))