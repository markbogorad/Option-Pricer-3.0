import sys
import os

# Add the directory containing the module to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importing libraries
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

# Importing pages
from black_scholes import BlackScholes
from Home.Call_and_Put import show_page as Call_and_Put

# Trade Strategies
from Potential_Trade_Strategies._1_Covered_Call import show_page as Covered_Call
from Potential_Trade_Strategies._2_Protective_Put import show_page as Protective_Put
from Potential_Trade_Strategies._3_Bull_Spread_Trades import show_page as Bull_Spread_Trades
from Potential_Trade_Strategies._4_Bear_Spread_Trades import show_page as Bear_Spread_Trades
from Potential_Trade_Strategies._5_Long_Butterfly_Trades import show_page as Long_Butterfly_Trades
from Potential_Trade_Strategies._6_Short_Butterfly_Trades import show_page as Short_Butterfly_Trades
from Potential_Trade_Strategies._7_Straddle_Trades import show_page as Straddle_Trades
from Potential_Trade_Strategies._8_Strangle_Trades import show_page as Strangle_Trades

# Hedges
from Optimal_Hedges.Optimal_Hedges import show_page as Optimal_Hedges

# Page configuration
st.set_page_config(
    page_title="Option Pricing Series",
    layout="wide",
    initial_sidebar_state="expanded"
)

def setup_sidebar():
    with st.sidebar:
        st.header("Option Parameters")
        S = st.number_input("Current Asset Price", value=60.0, key="op_S")
        K = st.number_input("Strike Price", value=65.0, key="op_K")
        T = st.number_input("Time to Maturity (Years)", value=0.25, key="op_T")
        sigma = st.number_input("Volatility (σ)", value=0.30, key="op_sigma")
        r = st.number_input("Risk-Free Interest Rate", value=0.08, key="op_r")
        
        # Automatically calculate the purchase prices for call and put
        bs_model = BlackScholes(S, K, T, r, sigma, 0)
        call_price, put_price = bs_model.calculate_prices()
        purchase_price_call = st.number_input("Call Purchase Price (Default is option price)", value=call_price, key="op_purchase_price_call")
        purchase_price_put = st.number_input("Put Purchase Price (Default is option price)", value=put_price, key="op_purchase_price_put")
        
        st.markdown("**Disclaimer:** Changing the purchase prices may cause arbitrage.")

        st.header("Heatmap Parameters")
        spot_min = st.number_input('Min Spot Price', min_value=0.01, value=S*0.8, step=0.01, key="hp_spot_min")
        spot_max = st.number_input('Max Spot Price', min_value=0.01, value=S*1.35, step=0.01, key="hp_spot_max")
        vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=sigma*0.5, step=0.01, key="hp_vol_min")
        vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=sigma*1.5, step=0.01, key="hp_vol_max")
    
    return S, K, T, sigma, r, purchase_price_call, purchase_price_put, spot_min, spot_max, vol_min, vol_max

# Top header navigation using tabs
st.title("Option Pricer 3.0")
tabs = st.tabs(["Call and Put", "Trade Strategies", "Optimal Hedges"])

S, K, T, sigma, r, purchase_price_call, purchase_price_put, spot_min, spot_max, vol_min, vol_max = setup_sidebar()

with tabs[0]:
    Call_and_Put(S, K, T, sigma, r, purchase_price_call, purchase_price_put, spot_min, spot_max, vol_min, vol_max)

with tabs[1]:
    st.header("Trade Strategies")
    trade_strategy = st.selectbox("Choose a trade strategy", ["Covered Call", "Protective Put", "Bull Spread Trades", "Bear Spread Trades", "Long Butterfly Trades", "Short Butterfly Trades", "Straddle Trades", "Strangle Trades"], key="trade_strategy_select")

    if trade_strategy == "Covered Call":
        Covered_Call(S, K, T, sigma, r, purchase_price_call, spot_min, spot_max, vol_min, vol_max)
    elif trade_strategy == "Protective Put":
        Protective_Put(S, K, T, sigma, r, purchase_price_put, spot_min, spot_max, vol_min, vol_max)
    elif trade_strategy == "Bull Spread Trades":
        Bull_Spread_Trades(S, K, T, sigma, r, spot_min, spot_max, vol_min, vol_max)
    elif trade_strategy == "Bear Spread Trades":
        Bear_Spread_Trades(S, K, T, sigma, r, spot_min, spot_max, vol_min, vol_max)
    elif trade_strategy == "Long Butterfly Trades":
        Long_Butterfly_Trades(S, K, T, sigma, r, spot_min, spot_max, vol_min, vol_max)
    elif trade_strategy == "Short Butterfly Trades":
        Short_Butterfly_Trades(S, K, T, sigma, r, spot_min, spot_max, vol_min, vol_max)
    elif trade_strategy == "Straddle Trades":
        Straddle_Trades(S, K, T, sigma, r, spot_min, spot_max, vol_min, vol_max)
    elif trade_strategy == "Strangle Trades":
        Strangle_Trades(S, K, T, sigma, r, spot_min, spot_max, vol_min, vol_max)

with tabs[2]:
    st.header("Optimal Hedges")
    Optimal_Hedges()

