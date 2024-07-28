import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from black_scholes import BlackScholes

def show_page(S, K, T, sigma, r, spot_min, spot_max, vol_min, vol_max):
    st.title("Strangle Trade Strategies")

    st.write("""### Enter Additional Parameters for Strangle Trades (Default is a 5% spread)""")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Long Strangle")
        st.markdown("""A long strangle strategy involves buying a call and a put option with different strike prices but the same expiration date.""")
        st.markdown("""**Construction**: long 1 out-of-the-money call option and long 1 out-of-the-money put option with the same expiration date.""")
        st.markdown("""**Strategy**: Establish a position that profits from volatility in either direction.""")
        st.markdown("""**Outcome**: Profits if the underlying asset moves significantly above the call strike price or below the put strike price.""")
        st.markdown("""**When to use**: Expecting significant volatility but unsure of the direction, with a lower cost compared to a straddle.""")

        spread_pct_call = st.number_input("Call Spread %", value=5.0, key="spread_pct_call")
        K1_call = st.number_input("Lower Strike Price (K1)", value=K * (1 - spread_pct_call / 100), key="op_K1_call")
        K2_call = st.number_input("Higher Strike Price (K2)", value=K * (1 + spread_pct_call / 100), key="op_K2_call")
        dummy_purchase_price = 0  # Temporarily use 0 for the purchase price
        bs_call1 = BlackScholes(S, K1_call, T, r, sigma, dummy_purchase_price)
        bs_call2 = BlackScholes(S, K2_call, T, r, sigma, dummy_purchase_price)
        call_price1 = bs_call1.call_option_price()
        call_price2 = bs_call2.call_option_price()
        purchase_price_call1 = st.number_input("Lower Strike Call Price", value=call_price1, key="op_purchase_price_call1")
        purchase_price_call2 = st.number_input("Higher Strike Call Price", value=call_price2, key="op_purchase_price_call2")
        net_premium_call = purchase_price_call1 + purchase_price_call2

    with col2:
        st.header("Short Strangle")
        st.markdown("""A short strangle strategy involves selling a call and a put option with different strike prices but the same expiration date.""")
        st.markdown("""**Construction**: short 1 out-of-the-money call option and short 1 out-of-the-money put option with the same expiration date.""")
        st.markdown("""**Strategy**: Establish a position that profits from low volatility, where the underlying asset price stays between the strike prices.""")
        st.markdown("""**Outcome**: Profits if the underlying asset remains within the range defined by the call and put strike prices, resulting in both options expiring worthless.""")
        st.markdown("""**When to use**: Expecting low volatility and stability in the underlying asset price.""")

        spread_pct_put = st.number_input("Put Spread %", value=5.0, key="spread_pct_put")
        K1_put = st.number_input("Lower Strike Price (K1)", value=K * (1 - spread_pct_put / 100), key="op_K1_put")
        K2_put = st.number_input("Higher Strike Price (K2)", value=K * (1 + spread_pct_put / 100), key="op_K2_put")
        dummy_purchase_price = 0  # Temporarily use 0 for the purchase price
        bs_put1 = BlackScholes(S, K1_put, T, r, sigma, dummy_purchase_price)
        bs_put2 = BlackScholes(S, K2_put, T, r, sigma, dummy_purchase_price)
        put_price1 = bs_put1.put_option_price()
        put_price2 = bs_put2.put_option_price()
        purchase_price_put1 = st.number_input("Lower Strike Put Price", value=put_price1, key="op_purchase_price_put1")
        purchase_price_put2 = st.number_input("Higher Strike Put Price", value=put_price2, key="op_purchase_price_put2")
        net_premium_put = purchase_price_put1 + purchase_price_put2

    st.markdown("""**Disclaimer**: Profits are maximized with significant price movements. However, if the price remains stable, the trader incurs a loss equal to the sum of the premiums paid for the call and put options.""")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Long Strangle Heatmap")
        heatmap_fig_call, profit_fig_call = strangle_spread(S, K1_call, K2_call, T, sigma, r, purchase_price_call1, purchase_price_call2, spot_min, spot_max, vol_min, vol_max, strategy='long')
        st.pyplot(heatmap_fig_call, use_container_width=True)
    with col2:
        st.markdown("### Short Strangle Heatmap")
        heatmap_fig_put, profit_fig_put = strangle_spread(S, K1_put, K2_put, T, sigma, r, purchase_price_put1, purchase_price_put2, spot_min, spot_max, vol_min, vol_max, strategy='short')
        st.pyplot(heatmap_fig_put, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Long Strangle Profit")
        st.pyplot(profit_fig_call, use_container_width=True)
        st.write(f"Net Premium for Long Strangle: {net_premium_call:.2f}")
    with col4:
        st.markdown("### Short Strangle Profit")
        st.pyplot(profit_fig_put, use_container_width=True)
        st.write(f"Net Premium for Short Strangle: {net_premium_put:.2f}")

    bs_model_call1 = BlackScholes(S, K1_call, T, r, sigma, purchase_price_call1)
    bs_model_call2 = BlackScholes(S, K2_call, T, r, sigma, purchase_price_call2)
    bs_model_put1 = BlackScholes(S, K1_put, T, r, sigma, purchase_price_put1)
    bs_model_put2 = BlackScholes(S, K2_put, T, r, sigma, purchase_price_put2)

    col5, col6 = st.columns(2)
    with col5:
        st.write("### Combined Greeks for Long Strangle")
        display_greeks(bs_model_call1, bs_model_call2, "call")
    with col6:
        st.write("### Combined Greeks for Short Strangle")
        display_greeks(bs_model_put1, bs_model_put2, "put")

def strangle_spread(S, K1, K2, T, sigma, r, purchase_price_call, purchase_price_put, spot_min, spot_max, vol_min, vol_max, strategy='long'):
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

    def plot_heatmap(K1, K2, purchase_price_call, purchase_price_put, strategy):
        profits = np.zeros((len(vol_range), len(spot_range)))
        for i, vol in enumerate(vol_range):
            for j, spot in enumerate(spot_range):
                bs_call = BlackScholes(spot, K2, T, r, vol, purchase_price_call)
                bs_put = BlackScholes(spot, K1, T, r, vol, purchase_price_put)
                call_price = bs_call.call_option_price()
                put_price = bs_put.put_option_price()
                if strategy == 'long':
                    call_profit = np.maximum(spot - K2, 0) - call_price
                    put_profit = np.maximum(K1 - spot, 0) - put_price
                elif strategy == 'short':
                    call_profit = call_price - np.maximum(spot - K2, 0)
                    put_profit = put_price - np.maximum(K1 - spot, 0)
                profit = call_profit + put_profit
                profits[i, j] = profit

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(profits[::-1], xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range[::-1], 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax, center=0)
        ax.set_title(f'{strategy.capitalize()} Strangle Profits')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')
        return fig

    def plot_payoff_chart():
        spot_prices = np.linspace(spot_min, spot_max, 100)
        call_profits = []
        put_profits = []
        total_profits = []

        for spot in spot_prices:
            if strategy == 'long':
                call_profit = np.maximum(spot - K2, 0) - purchase_price_call
                put_profit = np.maximum(K1 - spot, 0) - purchase_price_put
            elif strategy == 'short':
                call_profit = purchase_price_call - np.maximum(spot - K2, 0)
                put_profit = purchase_price_put - np.maximum(K1 - spot, 0)
            total_profit = call_profit + put_profit
            
            call_profits.append(call_profit)
            put_profits.append(put_profit)
            total_profits.append(total_profit)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(spot_prices, total_profits, label=f'{strategy.capitalize()} Strangle Profit', color='green')
        ax.plot(spot_prices, call_profits, 'b--', label='Call Profit')
        ax.plot(spot_prices, put_profits, 'r--', label='Put Profit')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(K1, color='blue', linestyle='--', linewidth=0.5, label='Lower Strike Price (K1)')
        ax.axvline(K2, color='red', linestyle='--', linewidth=0.5, label='Higher Strike Price (K2)')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Profit')
        ax.set_title(f'{strategy.capitalize()} Strangle Profit')
        ax.legend()
        return fig

    return plot_heatmap(K1, K2, purchase_price_call, purchase_price_put, strategy), plot_payoff_chart()

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
    
    st.markdown("### Combined Greeks")
    for greek, value in combined_greeks.items():
        st.markdown(f"**{greek}:** {value:.4f}")
