import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from black_scholes import BlackScholes

def show_page(S, K, T, sigma, r, spot_min, spot_max, vol_min, vol_max):
    st.title("Long (Bullish) Spread Trades Strategies")
    st.markdown("""A long butterfly spread strategy can be constructed with both calls and puts. The nature of the spread trade is neutral with hedges for large volatility spikes.""")
    st.markdown("""**Construction with calls**: long 1 call option at a lower strike price (K1), short 2 calls at a middle strike price (K2), and long 1 call option at a higher strike price (K3)""")
    st.markdown("""**Construction with calls**: long 1 call option at a lower strike price (K1), short 2 calls at a middle strike price (K2), and long 1 call option at a higher strike price (K3)""")
    st.markdown("""**Strategy**: Profit off low volatility, creating a profit band in between K1 and K3, where K2 is maximum profit. Movements outside of the band are hedged. For the trade to work, distances should be symmetric between K1, K2, and K3""")
    st.markdown("""**Outcome**: Hedges large volatility spikes, makes the most when price is stable (at K2).""")
    st.markdown("""**When to use**: Expecting low volatility, but don't want to risk drastic spikes in an uncertain environment.""")

    st.write("""### Enter Additional Parameters for Butterfly Trades (Default is a 5% spread)""")
    col1, col2 = st.columns(2)
    with col1:
        spread_pct_call = st.number_input("Call Spread %", value=5.0, key="spread_pct_call")
        K1_call = st.number_input("Lower Strike Price (K1)", value=K * (1 - spread_pct_call / 100), key="op_K1_call")
        K3_call = st.number_input("Higher Strike Price (K3)", value=K * (1 + spread_pct_call / 100), key="op_K3_call")
        K2_call = st.number_input("Middle Strike Price (K2) i.e. Ideal Expected Underlying Price", value=(K1_call + K3_call) / 2, key="op_K2_call")
        dummy_purchase_price = 0  # Temporarily use 0 for the purchase price
        bs_call1 = BlackScholes(S, K1_call, T, r, sigma, dummy_purchase_price)
        bs_call2 = BlackScholes(S, K2_call, T, r, sigma, dummy_purchase_price)
        bs_call3 = BlackScholes(S, K3_call, T, r, sigma, dummy_purchase_price)
        call_price1 = bs_call1.call_option_price()
        call_price2 = bs_call2.call_option_price()
        call_price3 = bs_call3.call_option_price()
        purchase_price_call1 = st.number_input("Lower Strike Call Price", value=call_price1, key="op_purchase_price_call1")
        purchase_price_call2 = st.number_input("Middle Strike Call Price", value=call_price2, key="op_purchase_price_call2")
        purchase_price_call3 = st.number_input("Higher Strike Call Price", value=call_price3, key="op_purchase_price_call3")
        net_premium_call = purchase_price_call1 + 2 * purchase_price_call2 + purchase_price_call3

    with col2:
        spread_pct_put = st.number_input("Put Spread %", value=5.0, key="spread_pct_put")
        K1_put = st.number_input("Lower Strike Price (K1)", value=K * (1 - spread_pct_put / 100), key="op_K1_put")
        K3_put = st.number_input("Higher Strike Price (K3)", value=K * (1 + spread_pct_put / 100), key="op_K3_put")
        K2_put = st.number_input("Middle Strike Price (K2) i.e. Ideal Expected Underlying Price", value=(K1_put + K3_put) / 2, key="op_K2_put")
        dummy_purchase_price = 0  # Temporarily use 0 for the purchase price
        bs_put1 = BlackScholes(S, K1_put, T, r, sigma, dummy_purchase_price)
        bs_put2 = BlackScholes(S, K2_put, T, r, sigma, dummy_purchase_price)
        bs_put3 = BlackScholes(S, K3_put, T, r, sigma, dummy_purchase_price)
        put_price1 = bs_put1.put_option_price()
        put_price2 = bs_put2.put_option_price()
        put_price3 = bs_put3.put_option_price()
        purchase_price_put1 = st.number_input("Lower Strike Put Price", value=put_price1, key="op_purchase_price_put1")
        purchase_price_put2 = st.number_input("Middle Strike Put Price", value=put_price2, key="op_purchase_price_put2")
        purchase_price_put3 = st.number_input("Higher Strike Put Price", value=put_price3, key="op_purchase_price_put3")
        net_premium_put = purchase_price_put1 + 2 * purchase_price_put2 + purchase_price_put3

    st.markdown("""**Disclaimer**: Deep out of the money losses are smaller because the cost of construction will be much cheaper for wider spread construction. Entering a position at current values will lead to max losses as shown in profit tables""")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Long Butterfly Call Spread Heatmap")
        heatmap_fig_call, profit_fig_call = call_butterfly_spread(S, K1_call, K2_call, K3_call, T, sigma, r, purchase_price_call1, purchase_price_call2, purchase_price_call3, spot_min, spot_max, vol_min, vol_max)
        st.pyplot(heatmap_fig_call)
    with col2:
        st.markdown("### Long Butterfly Put Spread Heatmap")
        heatmap_fig_put, profit_fig_put = put_butterfly_spread(S, K1_put, K2_put, K3_put, T, sigma, r, purchase_price_put1, purchase_price_put2, purchase_price_put3, spot_min, spot_max, vol_min, vol_max)
        st.pyplot(heatmap_fig_put)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Long Butterfly Call Spread Profit")
        st.pyplot(profit_fig_call)
        st.write(f"Net Premium for Call Butterfly Spread: {net_premium_call:.2f}")
    with col4:
        st.markdown("### Long Butterfly Put Spread Profit")
        st.pyplot(profit_fig_put)
        st.write(f"Net Premium for Put Butterfly Spread: {net_premium_put:.2f}")

    bs_model_call1 = BlackScholes(S, K1_call, T, r, sigma, purchase_price_call1)
    bs_model_call2 = BlackScholes(S, K2_call, T, r, sigma, purchase_price_call2)
    bs_model_call3 = BlackScholes(S, K3_call, T, r, sigma, purchase_price_call3)
    bs_model_put1 = BlackScholes(S, K1_put, T, r, sigma, purchase_price_put1)
    bs_model_put2 = BlackScholes(S, K2_put, T, r, sigma, purchase_price_put2)
    bs_model_put3 = BlackScholes(S, K3_put, T, r, sigma, purchase_price_put3)

    col5, col6 = st.columns(2)
    with col5:
        st.write("### Combined Greeks for Bear Call Spread")
        display_greeks(bs_model_call1, bs_model_call2, bs_model_call3, "call")
    with col6:
        st.write("### Combined Greeks for Bear Put Spread")
        display_greeks(bs_model_put1, bs_model_put2, bs_model_put3, "put")


def call_butterfly_spread(S, K1, K2, K3, T, sigma, r, purchase_price_call1, purchase_price_call2, purchase_price_call3, spot_min, spot_max, vol_min, vol_max):
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

    def plot_heatmap(K1, K2, K3, purchase_price_call1, purchase_price_call2, purchase_price_call3):
        profits = np.zeros((len(vol_range), len(spot_range)))
        for i, vol in enumerate(vol_range):
            for j, spot in enumerate(spot_range):
                c_bs_long_k1 = BlackScholes(spot, K1, T, r, vol, purchase_price_call1)
                c_bs_short_k2 = BlackScholes(spot, K2, T, r, vol, purchase_price_call2)
                c_bs_long_k3 = BlackScholes(spot, K3, T, r, vol, purchase_price_call3)
                long_K1_call_price = c_bs_long_k1.call_option_price()
                short_K2_call_price = c_bs_short_k2.call_option_price()
                long_K3_call_price = c_bs_long_k3.call_option_price()
                long_K1_call_profit = np.maximum(spot - K1, 0) - long_K1_call_price
                short_K2_call_profit = short_K2_call_price - np.maximum(spot - K2, 0)
                long_K3_call_profit = np.maximum(spot - K3, 0) - long_K3_call_price
                profit = long_K1_call_profit + (2 * short_K2_call_profit) + long_K3_call_profit
                profits[i, j] = profit

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(profits[::-1], xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range[::-1], 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax, center=0)
        ax.set_title('Butterfly Spread Profits')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')
        return fig

    def plot_payoff_chart():
        spot_prices = np.linspace(spot_min, spot_max, 100)
        long_k1_call_profits = []
        short_k2_call_profits = []
        long_k3_call_profits = []
        total_profits = []

        for spot in spot_prices:
            long_k1_call_profit = np.maximum(spot - K1, 0) - purchase_price_call1
            short_k2_call_profit = purchase_price_call2 - np.maximum(spot - K2, 0)
            long_k3_call_profit = np.maximum(spot - K3, 0) - purchase_price_call3
            total_profit = long_k1_call_profit + (2 * short_k2_call_profit) + long_k3_call_profit
            
            long_k1_call_profits.append(long_k1_call_profit)
            short_k2_call_profits.append(short_k2_call_profit)
            long_k3_call_profits.append(long_k3_call_profit)
            total_profits.append(total_profit)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(spot_prices, total_profits, label='Butterfly Spread Profit', color='green')
        ax.plot(spot_prices, long_k1_call_profits, 'b--', label='Long K1 Call Profit')
        ax.plot(spot_prices, short_k2_call_profits, 'r--', label='Short K2 Calls Profit')
        ax.plot(spot_prices, long_k3_call_profits, 'g--', label='Long K3 Call Profit')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(K1, color='blue', linestyle='--', linewidth=0.5, label='Lower Strike Price (K1)')
        ax.axvline(K2, color='red', linestyle='--', linewidth=0.5, label='Middle Strike Price (K2)')
        ax.axvline(K3, color='green', linestyle='--', linewidth=0.5, label='Higher Strike Price (K3)')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Profit')
        ax.set_title('Call Butterfly Spread Profit')
        ax.legend()
        return fig

    return plot_heatmap(K1, K2, K3, purchase_price_call1, purchase_price_call2, purchase_price_call3), plot_payoff_chart()

def put_butterfly_spread(S, K1, K2, K3, T, sigma, r, purchase_price_put1, purchase_price_put2, purchase_price_put3, spot_min, spot_max, vol_min, vol_max):
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

    def plot_heatmap(K1, K2, K3, purchase_price_put1, purchase_price_put2, purchase_price_put3):
        profits = np.zeros((len(vol_range), len(spot_range)))
        for i, vol in enumerate(vol_range):
            for j, spot in enumerate(spot_range):
                p_bs_long_k1 = BlackScholes(spot, K1, T, r, vol, purchase_price_put1)
                p_bs_short_k2 = BlackScholes(spot, K2, T, r, vol, purchase_price_put2)
                p_bs_long_k3 = BlackScholes(spot, K3, T, r, vol, purchase_price_put3)
                long_k1_put_price = p_bs_long_k1.put_option_price()
                short_k2_put_price = p_bs_short_k2.put_option_price()
                long_k3_put_price = p_bs_long_k3.put_option_price()
                long_k1_put_profit = np.maximum(K1 - spot, 0) - long_k1_put_price
                short_k2_put_profit = short_k2_put_price - np.maximum(K2 - spot, 0)     
                long_k3_put_profit = np.maximum(K3 - spot, 0) - long_k3_put_price
                profit = long_k1_put_profit + (2 * short_k2_put_profit) + long_k3_put_profit
                profits[i, j] = profit

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(profits[::-1], xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range[::-1], 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax, center=0)
        ax.set_title('Butterfly Spread Profits')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')
        return fig

    def plot_payoff_chart():
        spot_prices = np.linspace(spot_min, spot_max, 100)
        long_k1_put_profits = []
        short_k2_put_profits = []
        long_k3_put_profits = []
        total_profits = []

        for spot in spot_prices:
            long_k1_put_profit = np.maximum(K1 - spot, 0) - purchase_price_put1
            short_k2_put_profit = purchase_price_put2 - np.maximum(K2 - spot, 0)        
            long_k3_put_profit = np.maximum(K3 - spot, 0) - purchase_price_put3

            total_profit = long_k1_put_profit + (2 * short_k2_put_profit) + long_k3_put_profit
            
            long_k1_put_profits.append(long_k1_put_profit)
            short_k2_put_profits.append(short_k2_put_profit)
            long_k3_put_profits.append(long_k3_put_profit)
            total_profits.append(total_profit)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(spot_prices, total_profits, label='Butterfly Spread Profit', color='green')
        ax.plot(spot_prices, long_k1_put_profits, 'b--', label='Long K1 Put Profit')
        ax.plot(spot_prices, short_k2_put_profits, 'r--', label='Short K2 Put Profit')
        ax.plot(spot_prices, long_k3_put_profits, 'g--', label='Long K3 Put Profit')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(K1, color='blue', linestyle='--', linewidth=0.5, label='Lower Strike Price (K1)')
        ax.axvline(K2, color='red', linestyle='--', linewidth=0.5, label='Middle Strike Price (K2)')
        ax.axvline(K3, color='green', linestyle='--', linewidth=0.5, label='Higher Strike Price (K3)')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Profit')
        ax.set_title('Put Butterfly Spread Profit')
        ax.legend()
        return fig

    return plot_heatmap(K1, K2, K3, purchase_price_put1, purchase_price_put2, purchase_price_put3), plot_payoff_chart()



def display_greeks(bs_model1, bs_model2, bs_model3, option_type):
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
    greeks3 = {
        "Delta": bs_model3.delta(option_type),
        "Gamma": bs_model3.gamma(),
        "Vega": bs_model3.vega(),
        "Rho": bs_model3.rho(option_type),
        "Theta": bs_model3.theta(option_type)
    }
    combined_greeks = {k: greeks1[k] + 2 * greeks2[k] + greeks3[k] for k in greeks1.keys()}
    
    for greek, value in combined_greeks.items():
        st.markdown(f"**{greek}:** {value:.4f}")