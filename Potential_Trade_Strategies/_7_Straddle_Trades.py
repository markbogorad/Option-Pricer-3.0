import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from black_scholes import BlackScholes

def show_page(S, K, T, sigma, r, spot_min, spot_max, vol_min, vol_max):
    st.title("Straddle Trade Strategies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Long Straddle")
        st.markdown("""A long straddle strategy involves buying both a call and a put option with the same strike price and expiration date.""")
        st.markdown("""**Construction**: long 1 call option and long 1 put option with the same strike price (K) and expiration date.""")
        st.markdown("""**Strategy**: Establish a position that profits from large volatility.""")
        st.markdown("""**Outcome**: Profits if the underlying asset moves significantly from the strike price.""")
        st.markdown("""**When to use**: Expecting high volatility but unsure of the direction.""")

        dummy_purchase_price = 0  # Temporarily use 0 for the purchase price
        bs_call_long = BlackScholes(S, K, T, r, sigma, dummy_purchase_price)
        bs_put_long = BlackScholes(S, K, T, r, sigma, dummy_purchase_price)
        call_price_long = bs_call_long.call_option_price()
        put_price_long = bs_put_long.put_option_price()
        purchase_price_call_long = st.number_input("Call Option Price (Long Straddle)", value=call_price_long, key="long_straddle_purchase_price_call")
        purchase_price_put_long = st.number_input("Put Option Price (Long Straddle)", value=put_price_long, key="long_straddle_purchase_price_put")

        st.markdown("### Long Straddle Heatmap")
        heatmap_fig_long_straddle, profit_fig_long_straddle = straddle_spread(S, K, T, sigma, r, purchase_price_call_long, purchase_price_put_long, spot_min, spot_max, vol_min, vol_max, strategy='long')
        st.pyplot(heatmap_fig_long_straddle, use_container_width=True)

        st.markdown("### Long Straddle Profit")
        st.pyplot(profit_fig_long_straddle, use_container_width=True)

        net_premium_long_straddle = purchase_price_call_long + purchase_price_put_long
        st.write(f"Net Premium for Long Straddle: {net_premium_long_straddle:.2f}")

        bs_model_call_long = BlackScholes(S, K, T, r, sigma, purchase_price_call_long)
        bs_model_put_long = BlackScholes(S, K, T, r, sigma, purchase_price_put_long)

        st.write("### Combined Greeks for Long Straddle")
        display_greeks(bs_model_call_long, bs_model_put_long, "straddle")

    with col2:
        st.header("Short Straddle")
        st.markdown("""A short straddle strategy involves selling both a call and a put option with the same strike price and expiration date.""")
        st.markdown("""**Construction**: short 1 call option and short 1 put option with the same strike price (K) and expiration date.""")
        st.markdown("""**Strategy**: Establish a position that profits from minimal price movements.""")
        st.markdown("""**Outcome**: Profits if the underlying asset does not deviate much from the strike price.""")
        st.markdown("""**When to use**: Expecting low volatility and stability in the price movement.""")

        dummy_purchase_price = 0  # Temporarily use 0 for the purchase price
        bs_call_short = BlackScholes(S, K, T, r, sigma, dummy_purchase_price)
        bs_put_short = BlackScholes(S, K, T, r, sigma, dummy_purchase_price)
        call_price_short = bs_call_short.call_option_price()
        put_price_short = bs_put_short.put_option_price()
        purchase_price_call_short = st.number_input("Call Option Price (Short Straddle)", value=call_price_short, key="short_straddle_purchase_price_call")
        purchase_price_put_short = st.number_input("Put Option Price (Short Straddle)", value=put_price_short, key="short_straddle_purchase_price_put")

        st.markdown("### Short Straddle Heatmap")
        heatmap_fig_short_straddle, profit_fig_short_straddle = straddle_spread(S, K, T, sigma, r, purchase_price_call_short, purchase_price_put_short, spot_min, spot_max, vol_min, vol_max, strategy='short')
        st.pyplot(heatmap_fig_short_straddle, use_container_width=True)

        st.markdown("### Short Straddle Profit")
        st.pyplot(profit_fig_short_straddle, use_container_width=True)

        net_premium_short_straddle = purchase_price_call_short + purchase_price_put_short
        st.write(f"Net Premium for Short Straddle: {net_premium_short_straddle:.2f}")

        bs_model_call_short = BlackScholes(S, K, T, r, sigma, purchase_price_call_short)
        bs_model_put_short = BlackScholes(S, K, T, r, sigma, purchase_price_put_short)

        st.write("### Combined Greeks for Short Straddle")
        display_greeks(bs_model_call_short, bs_model_put_short, "straddle")

def straddle_spread(S, K, T, sigma, r, purchase_price_call, purchase_price_put, spot_min, spot_max, vol_min, vol_max, strategy='long'):
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

    def plot_heatmap(K, purchase_price_call, purchase_price_put, strategy):
        profits = np.zeros((len(vol_range), len(spot_range)))
        for i, vol in enumerate(vol_range):
            for j, spot in enumerate(spot_range):
                bs_call = BlackScholes(spot, K, T, r, vol, purchase_price_call)
                bs_put = BlackScholes(spot, K, T, r, vol, purchase_price_put)
                call_price = bs_call.call_option_price()
                put_price = bs_put.put_option_price()
                if strategy == 'long':
                    call_profit = np.maximum(spot - K, 0) - call_price
                    put_profit = np.maximum(K - spot, 0) - put_price
                elif strategy == 'short':
                    call_profit = call_price - np.maximum(spot - K, 0)
                    put_profit = put_price - np.maximum(K - spot, 0)
                profit = call_profit + put_profit
                profits[i, j] = profit

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(profits[::-1], xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range[::-1], 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax, center=0)
        ax.set_title(f'{strategy.capitalize()} Straddle Profits')
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
                call_profit = np.maximum(spot - K, 0) - purchase_price_call
                put_profit = np.maximum(K - spot, 0) - purchase_price_put
            elif strategy == 'short':
                call_profit = purchase_price_call - np.maximum(spot - K, 0)
                put_profit = purchase_price_put - np.maximum(K - spot, 0)
            total_profit = call_profit + put_profit
            
            call_profits.append(call_profit)
            put_profits.append(put_profit)
            total_profits.append(total_profit)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(spot_prices, total_profits, label=f'{strategy.capitalize()} Straddle Profit', color='green')
        ax.plot(spot_prices, call_profits, 'b--', label='Call Profit')
        ax.plot(spot_prices, put_profits, 'r--', label='Put Profit')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(K, color='blue', linestyle='--', linewidth=0.5, label='Strike Price (K)')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Profit')
        ax.set_title(f'{strategy.capitalize()} Straddle Profit')
        ax.legend()
        return fig

    return plot_heatmap(K, purchase_price_call, purchase_price_put, strategy), plot_payoff_chart()

def display_greeks(bs_model_call, bs_model_put, strategy):
    call_greeks = {
        "Delta": bs_model_call.delta("call"),
        "Gamma": bs_model_call.gamma(),
        "Vega": bs_model_call.vega(),
        "Rho": bs_model_call.rho("call"),
        "Theta": bs_model_call.theta("call")
    }
    put_greeks = {
        "Delta": bs_model_put.delta("put"),
        "Gamma": bs_model_put.gamma(),
        "Vega": bs_model_put.vega(),
        "Rho": bs_model_put.rho("put"),
        "Theta": bs_model_put.theta("put")
    }
    combined_greeks = {k: call_greeks[k] + put_greeks[k] for k in call_greeks.keys()}
    for greek, value in combined_greeks.items():
        st.markdown(f"**{greek}:** {value:.4f}")
