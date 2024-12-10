import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from black_scholes import BlackScholes

def show_page(S, K, T, sigma, r, purchase_price_put, spot_min, spot_max, vol_min, vol_max):

    st.title("Protective Put Strategy")
    st.markdown("""A protective put strategy involves holding a long position in a stock and buying a put option on the same stock.""")
    st.markdown("""**Strategy**: Match the value of your long position with an equivalent position in a long put""")
    st.markdown("""**Outcome**: Provides downside protection, limiting potential losses to the strike price (K) of the put option minus the premium paid, while maintaining unlimited upside potential on the long stock position. A similar position nature to that of a long call""")
    st.markdown("""**When to use**: Bearish or uncertain outlook on the stock, where downside protection is desired while still participating in potential upside gains.""")

    bs_model = BlackScholes(S, K, T, r, sigma, purchase_price_put)

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
                put_price = bs_temp.put_option_price()
                put_profit = np.maximum(put_price - purchase_price, -purchase_price)
                stock_profit = spot - S  # Profit from holding the stock
                protective_put_profit = stock_profit + put_profit  # Net profit for protective put
                profits[i, j] = protective_put_profit

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(profits[::-1], xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range[::-1], 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax, center=0)
        ax.set_title('Protective Put Profit')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')

        return fig

    def display_greeks(bs_model):
        greeks = {
            "Delta": bs_model.delta("put") + 1,  # Long stock adds 1 to delta
            "Gamma": bs_model.gamma(),
            "Vega": bs_model.vega(),
            "Rho": bs_model.rho("put"),
            "Theta": bs_model.theta("put")
        }
        for greek, value in greeks.items():
            st.write(f"**{greek}:** {value:.4f}")

    def plot_profit_graph(S, K, purchase_price_put):
        spot_prices = np.linspace(spot_min, spot_max, 100)
        put_profits = [np.maximum(K - spot, 0) - purchase_price_put for spot in spot_prices]
        stock_profits = spot_prices - S
        protective_put_profits = np.array(stock_profits) + np.array(put_profits)

        fig, ax = plt.subplots()
        ax.plot(spot_prices, protective_put_profits, label='Protective Put Profit')
        ax.plot(spot_prices, stock_profits, label='Stock Profit', linestyle='--')
        ax.plot(spot_prices, put_profits, label='Long Put Profit', linestyle='--')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(K, color='black', linewidth=0.5, linestyle='--', label='Strike Price')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Profit')
        ax.set_title('Protective Put Profit')
        ax.legend()

        return fig

    st.subheader("Protective Put Heatmap and Profit Graph")
    col1, col2 = st.columns(2)
    with col1:
        heatmap_fig = plot_heatmap(bs_model, spot_range, vol_range, K, purchase_price_put)
        st.pyplot(heatmap_fig)
    with col2:
        profit_fig = plot_profit_graph(S, K, purchase_price_put)
        st.pyplot(profit_fig)

    st.subheader("Protective Put Greeks")
    display_greeks(bs_model)
