import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from black_scholes import BlackScholes

def show_page(S, K, T, sigma, r, purchase_price_call, spot_min, spot_max, vol_min, vol_max):
    st.title("Covered Call Strategy")
    st.markdown("""A covered call strategy involves holding a long position in a stock and selling a call option on the same stock.""")
    st.markdown("""**Strategy**: Match the value of your long position with an equivalent short call position""")
    st.markdown("""**Outcome**: Downside risk hedged via premia income from writing the call. This comes at the exchange of a profit ceiling equal to the strike price (K), where all gains on the underlying will be offset by losses on writing the call""")
    st.markdown("""**When to use**: Neutral to bullish outlook""")

    bs_model = BlackScholes(S, K, T, r, sigma, purchase_price_call)

    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

    def plot_heatmap(bs_model, spot_range, vol_range, K, purchase_price):
        profits = np.zeros((len(vol_range), len(spot_range)))

        for i, vol in enumerate(vol_range):
            for j, spot in enumerate(spot_range):
                bs_temp = BlackScholes(
                    S=spot,
                    K=K,
                    T=bs_model.T,
                    r=bs_model.r,
                    sigma=vol,
                    purchase_price=purchase_price
                )
                call_price = bs_temp.call_option_price()
                short_call_profit = call_price - np.maximum(spot - K,0) # Premium recieved - maximum between 0 and S-K
                stock_profit = spot - S  # Profit from holding the stock
                covered_call_profit = stock_profit + short_call_profit  # Net payoff for covered call
                profits[i, j] = covered_call_profit

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(profits[::-1], xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range[::-1], 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax, center=0)
        ax.set_title('Covered Call Profit')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')

        return fig

    def display_greeks(bs_model):
        greeks = {
            "Delta": bs_model.delta("call") - 1,
            "Gamma": bs_model.gamma(),
            "Vega": bs_model.vega(),
            "Rho": bs_model.rho("call"),
            "Theta": bs_model.theta("call")
        }
        for greek, value in greeks.items():
            st.write(f"**{greek}:** {value:.4f}")

    def plot_profit_graph(S, K, purchase_price_call):
        spot_prices = np.linspace(spot_min, spot_max, 100)
        call_profit = [-np.maximum(spot - K, 0) + purchase_price_call for spot in spot_prices]
        stock_profit = spot_prices - S
        covered_call_profit = stock_profit + np.array(call_profit)

        fig, ax = plt.subplots()
        ax.plot(spot_prices, covered_call_profit, label='Covered Call Profit')
        ax.plot(spot_prices, stock_profit, label='Stock Profit', linestyle='--')
        ax.plot(spot_prices, call_profit, label='Short Call Profit', linestyle='--')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(K, color='black', linewidth=0.5, linestyle='--', label='Strike Price')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Profit')
        ax.set_title('Covered Call Profit')
        ax.legend()

        return fig

    st.subheader("Covered Call Profit Heatmap and Profit Graph")
    col1, col2 = st.columns(2)
    with col1:
        heatmap_fig = plot_heatmap(bs_model, spot_range, vol_range, K, purchase_price_call)
        st.pyplot(heatmap_fig)
    with col2:
        profit_fig = plot_profit_graph(S, K, purchase_price_call)
        st.pyplot(profit_fig)

    st.subheader("Covered Call Greeks")
    display_greeks(bs_model)

