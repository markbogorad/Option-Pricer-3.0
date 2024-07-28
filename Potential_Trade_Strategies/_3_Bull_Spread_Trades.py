import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from black_scholes import BlackScholes

def show_page(S, K, T, sigma, r, spot_min, spot_max, vol_min, vol_max):
    st.title("Bullish Spread Trades Strategies")
    st.markdown("""A bull spread strategy can be constructed with both calls and puts. The nature of the spread trade is slightly bullish with hedges for large volatility spikes""")
    st.markdown("""**Construction with calls**: long call option at a lower strike price (K1) + short call option at a higher strike price (K2)""")
    st.markdown("""**Construction with puts**: long put option at a higher strike price (K2) + short a put option at a lower strike price (K1)""")
    st.markdown("""**Strategy**: Establish a slightly bullish position (achieved from net premium) by purchasing equally sized, offsetting contracts - hedging for drastic changes""")
    st.markdown("""**Outcome**: Limits both potential profit and potential loss.""")
    st.markdown("""**When to use**: Moderately bullish outlook on the stock, expecting the stock price to rise but not significantly beyond the higher strike price.""")

    st.write("""### Enter Additional Parameters for Spread Trades (Default is a 5% spread)""")
    col1, col2 = st.columns(2)
    with col1:
        spread_pct_call = st.number_input("Call Spread %", value=5.0, key="spread_pct_call")
        K1_call = st.number_input("Lower Strike Price (K1_call)", value=K * (1 - spread_pct_call / 100), key="op_K1_call")
        K2_call = st.number_input("Higher Strike Price (K2_call)", value=K * (1 + spread_pct_call / 100), key="op_K2_call")
        dummy_purchase_price = 0  # Temporarily use 0 for the purchase price
        bs_call1 = BlackScholes(S, K1_call, T, r, sigma, dummy_purchase_price)
        bs_call2 = BlackScholes(S, K2_call, T, r, sigma, dummy_purchase_price)
        call_price1 = bs_call1.call_option_price()
        call_price2 = bs_call2.call_option_price()
        purchase_price_call1 = st.number_input("Lower Strike Call Price", value=call_price1, key="op_purchase_price_call1")
        purchase_price_call2 = st.number_input("Higher Strike Call Price", value=call_price2, key="op_purchase_price_call2")

    with col2:
        spread_pct_put = st.number_input("Put Spread %", value=5.0, key="spread_pct_put")
        K1_put = st.number_input("Lower Strike Price (K1_put)", value=K * (1 - spread_pct_put / 100), key="op_K1_put")
        K2_put = st.number_input("Higher Strike Price (K2_put)", value=K * (1 + spread_pct_put / 100), key="op_K2_put")
        dummy_purchase_price = 0  # Temporarily use 0 for the purchase price
        bs_put1 = BlackScholes(S, K2_put, T, r, sigma, dummy_purchase_price)
        bs_put2 = BlackScholes(S, K1_put, T, r, sigma, dummy_purchase_price)
        put_price1 = bs_put1.put_option_price()
        put_price2 = bs_put2.put_option_price()
        purchase_price_put1 = st.number_input("Lower Strike Put Price", value=put_price2, key="op_purchase_price_put1")
        purchase_price_put2 = st.number_input("Higher Strike Put Price", value=put_price1, key="op_purchase_price_put2")
    
    st.markdown("""**Disclaimer**: Deep out of the money losses are smaller because the cost of construction will be much cheaper for wider spread construction. Entering a position at current values will lead to max losses as shown in profit tables""")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Bull Call Spread Heatmap")
        heatmap_fig_call, profit_fig_call = bull_call_spread(S, K1_call, K2_call, T, sigma, r, purchase_price_call1, purchase_price_call2, spot_min, spot_max, vol_min, vol_max)
        st.pyplot(heatmap_fig_call)
    with col2:
        st.markdown("### Bull Put Spread Heatmap")
        heatmap_fig_put, payoff_fig_put = bull_put_spread(S, K1_put, K2_put, T, sigma, r, purchase_price_put1, purchase_price_put2, spot_min, spot_max, vol_min, vol_max)
        st.pyplot(heatmap_fig_put)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Bull Call Spread Profit")
        st.pyplot(profit_fig_call)
    with col4:
        st.markdown("### Bull Put Spread Profit")
        st.pyplot(payoff_fig_put)

    bs_model_call1 = BlackScholes(S, K1_call, T, r, sigma, purchase_price_call1)
    bs_model_call2 = BlackScholes(S, K2_call, T, r, sigma, purchase_price_call2)
    bs_model_put1 = BlackScholes(S, K1_put, T, r, sigma, purchase_price_put1)
    bs_model_put2 = BlackScholes(S, K2_put, T, r, sigma, purchase_price_put2)

    col5, col6 = st.columns(2)
    with col5:
        st.write("### Combined Greeks for Bear Call Spread")
        display_greeks(bs_model_call1, bs_model_call2, "call")
    with col6:
        st.write("### Combined Greeks for Bear Put Spread")
        display_greeks(bs_model_put1, bs_model_put2, "put")

def bull_call_spread(S, K1_call, K2_call, T, sigma, r, purchase_price_call1, purchase_price_call2, spot_min, spot_max, vol_min, vol_max):
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

    def plot_heatmap(K1_call, K2_call, purchase_price_call1, purchase_price_call2):
        profits = np.zeros((len(vol_range), len(spot_range)))
        for i, vol in enumerate(vol_range):
            for j, spot in enumerate(spot_range):
                bs_long = BlackScholes(spot, K1_call, T, r, vol, purchase_price_call1)
                bs_short = BlackScholes(spot, K2_call, T, r, vol, purchase_price_call2)
                long_call_price = bs_long.call_option_price()
                short_call_price = bs_short.call_option_price()
                long_call_profit = np.maximum(spot - K1_call, 0) - long_call_price
                short_call_profit = short_call_price - np.maximum(spot - K2_call, 0)
                profit = long_call_profit + short_call_profit
                profits[i, j] = profit

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(profits[::-1], xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range[::-1], 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax, center=0)
        ax.set_title('Bull Call Spread Profits')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')
        return fig

    def plot_payoff_chart():
        spot_prices = np.linspace(spot_min, spot_max, 100)
        long_call_profits = []
        short_call_profits = []
        total_profits = []

        for spot in spot_prices:
            long_call_profit = np.maximum(spot - K1_call, 0) - purchase_price_call1
            short_call_profit = purchase_price_call2 - np.maximum(spot - K2_call, 0)
            total_profit = long_call_profit + short_call_profit
            
            long_call_profits.append(long_call_profit)
            short_call_profits.append(short_call_profit)
            total_profits.append(total_profit)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(spot_prices, total_profits, label='Bull Call Spread Profit', color='green')
        ax.plot(spot_prices, long_call_profits, 'b--', label='Long Call Profit')
        ax.plot(spot_prices, short_call_profits, 'r--', label='Short Call Profit')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(K1_call, color='blue', linestyle='--', linewidth=0.5, label='Lower Strike Price (K1_call)')
        ax.axvline(K2_call, color='red', linestyle='--', linewidth=0.5, label='Higher Strike Price (K2_call)')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Profit')
        ax.set_title('Bull Call Spread Profit')
        ax.legend()
        return fig

    return plot_heatmap(K1_call, K2_call, purchase_price_call1, purchase_price_call2), plot_payoff_chart()

def bull_put_spread(S, K1_put, K2_put, T, sigma, r, purchase_price_put1, purchase_price_put2, spot_min, spot_max, vol_min, vol_max):
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

    def plot_heatmap(K1_put, K2_put, purchase_price_put1, purchase_price_put2):
        profits = np.zeros((len(vol_range), len(spot_range)))
        for i, vol in enumerate(vol_range):
            for j, spot in enumerate(spot_range):
                bs_long = BlackScholes(spot, K1_put, T, r, vol, purchase_price_put1)
                bs_short = BlackScholes(spot, K2_put, T, r, vol, purchase_price_put2)
                long_put_price = bs_long.put_option_price()
                short_put_price = bs_short.put_option_price()
                long_put_profit = np.maximum(K1_put - spot, 0) - long_put_price
                short_put_profit = short_put_price - np.maximum(K2_put - spot, 0)
                profit = long_put_profit + short_put_profit
                profits[i, j] = profit

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(profits[::-1], xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range[::-1], 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax, center=0)
        ax.set_title('Bull Put Spread Profits')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')
        return fig

    def plot_payoff_chart():
        spot_prices = np.linspace(spot_min, spot_max, 100)
        long_put_profits = []
        short_put_profits = []
        total_profits = []

        for spot in spot_prices:
            long_put_profit = np.maximum(K1_put - spot, 0) - purchase_price_put1
            short_put_profit = purchase_price_put2 - np.maximum(K2_put - spot, 0)
            total_profit = long_put_profit + short_put_profit
            
            long_put_profits.append(long_put_profit)
            short_put_profits.append(short_put_profit)
            total_profits.append(total_profit)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(spot_prices, total_profits, label='Bull Put Spread Profit', color='green')
        ax.plot(spot_prices, long_put_profits, 'b--', label='Long Put Profit')
        ax.plot(spot_prices, short_put_profits, 'r--', label='Short Put Profit')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(K1_put, color='blue', linestyle='--', linewidth=0.5, label='Lower Strike Price (K1_put)')
        ax.axvline(K2_put, color='red', linestyle='--', linewidth=0.5, label='Higher Strike Price (K2_put)')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Profit')
        ax.set_title('Bull Put Spread Profit')
        ax.legend()
        return fig

    return plot_heatmap(K1_put, K2_put, purchase_price_put1, purchase_price_put2), plot_payoff_chart()

def calculate_combined_greeks(bs_model1, bs_model2, option_type):
    greeks1 = {
        "Delta": bs_model1.delta(option_type),
        "Gamma": bs_model1.gamma(),
        "Vega": bs_model1.vega(),
        "Rho": bs_model1.rho(option_type),
        "Theta": bs_model1.theta(option_type)
    }
    
    greeks2 = {
        "Delta": bs_model2.delta(option_type),
        "Gamma": bs_model2.gamma(),
        "Vega": bs_model2.vega(),
        "Rho": bs_model2.rho(option_type),
        "Theta": bs_model2.theta(option_type)
    }
    combined_greeks = {k: greeks1[k] + greeks2[k] for k in greeks1.keys()}
    return combined_greeks

def display_greeks(bs_model1, bs_model2, option_type):
    greeks1 = {
        "Delta": bs_model1.delta(option_type),
        "Gamma": bs_model1.gamma(),
        "Vega": bs_model1.vega(),
        "Rho": bs_model1.rho(option_type),
        "Theta": bs_model1.theta(option_type)
    }
    greeks2 = {
        "Delta": bs_model2.delta(option_type),
        "Gamma": bs_model2.gamma(),
        "Vega": bs_model2.vega(),
        "Rho": bs_model2.rho(option_type),
        "Theta": bs_model2.theta(option_type)
    }
    combined_greeks = {k: greeks1[k] + greeks2[k] for k in greeks1.keys()}
    
    for greek, value in combined_greeks.items():
        st.markdown(f"**{greek}:** {value:.4f}")