import numpy as np
from scipy.stats import norm

class BlackScholes:
    def __init__(self, S, K, T, r, sigma, purchase_price):
        self.S = S  # Current stock price
        self.K = K  # Strike price
        self.T = T  # Time to maturity
        self.r = r  # Risk-free interest rate
        self.sigma = sigma  # Volatility
        self.purchase_price = purchase_price

    def d1(self):
        return (np.log(self.S / self.K) +
                (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.T)

    def call_option_price(self):
        return (self.S * norm.cdf(self.d1()) -
                self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2()))

    def put_option_price(self):
        return (self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2()) -
                self.S * norm.cdf(-self.d1()))

    def calculate_prices(self):
        call_price = self.call_option_price()
        put_price = self.put_option_price()
        return call_price, put_price

    def calculate_payoff(self, spot_price, option_type):
        self.S = spot_price
        call_price = self.call_option_price()
        put_price = self.put_option_price()
        
        if option_type == "call":
            return np.maximum(call_price - self.purchase_price, -self.purchase_price)
        elif option_type == "put":
            return np.maximum(put_price - self.purchase_price, -self.purchase_price)
        


        
         # Greek calculations
    def delta(self, option_type):
        if option_type == "call":
            return norm.cdf(self.d1())
        elif option_type == "put":
            return norm.cdf(self.d1()) - 1

    def gamma(self):
        return norm.pdf(self.d1()) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self):
        return (self.S * norm.pdf(self.d1()) * np.sqrt(self.T) * 0.01)

    def rho(self, option_type):
        if option_type == "call":
            return (self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2()) * 0.01)
        elif option_type == "put":
            return (-self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2()) * 0.01)

    def theta(self, option_type):
        term1 = (-self.S * norm.pdf(self.d1()) * self.sigma) / (2 * np.sqrt(self.T))
        if option_type == "call":
            term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2())
            return (term1 - term2) * 0.01
        elif option_type == "put":
            term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2())
            return (term1 + term2) * 0.01
    
        # Hedges
    def delta_hedge(self, option_type):
        return f"To delta hedge, you need to trade {self.delta(option_type)} units of the underlying asset."

    def gamma_hedge(self):
        return f"To gamma hedge, you need to trade {self.gamma()} units of the underlying asset."

    def vega_hedge(self):
        return f"To vega hedge, you need to trade {self.vega()} units of the underlying asset."

    def rho_hedge(self, option_type):
        return f"To rho hedge, you need to trade {self.rho(option_type)} units of the underlying asset."

    def theta_hedge(self, option_type):
        return f"To theta hedge, you need to trade {self.theta(option_type)} units of the underlying asset."