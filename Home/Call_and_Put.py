import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from black_scholes import BlackScholes

def show_page(S, K, T, sigma, r, purchase_price_call, purchase_price_put, spot_min, spot_max, vol_min, vol_max):

    st.title("Option Profit Heatmaps")
    st.markdown("""See how varying spot price and volatility affect your option position""")
    st.markdown("""Disclaimer: Profit is calculated using live pricing and time to expiry. Expiring out of the money results in a loss equal to the premium paid""")

    bs_model = BlackScholes(S, K, T, r, sigma, 0)

    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

    def plot_heatmap(bs_model, spot_range, vol_range, K, purchase_price, option_type="call"):
        profit = np.zeros((len(vol_range), len(spot_range)))

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
                profit[i, j] = bs_temp.calculate_payoff(spot, option_type)

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(profit[::-1], xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range[::-1], 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax, center=0)
        ax.set_title(f'{option_type.capitalize()} Option Profit')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')

        return fig
    
    def display_greeks(bs_model, option_type):
        st.markdown("### Option Greeks")
        greeks = {
            "Delta": bs_model.delta(option_type),
            "Gamma": bs_model.gamma(),
            "Vega": bs_model.vega(),
            "Rho": bs_model.rho(option_type),
            "Theta": bs_model.theta(option_type)
        }
        for greek, value in greeks.items():
            st.write(f"**{greek}:** {value:.4f}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Call Option Profit Heatmap")
        heatmap_fig_call = plot_heatmap(bs_model, spot_range, vol_range, K, purchase_price_call, "call")
        st.pyplot(heatmap_fig_call)
        display_greeks(bs_model, "call")

    with col2:
        st.markdown("### Put Option Profit Heatmap")
        heatmap_fig_put = plot_heatmap(bs_model, spot_range, vol_range, K, purchase_price_put, "put")
        st.pyplot(heatmap_fig_put)
        display_greeks(bs_model, "put")
