import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap
from black_scholes import BlackScholes

# Define a custom colormap with more contrast
colors = ["#FFFFFF", "#800080"]  # Light blue to purple
cmap = LinearSegmentedColormap.from_list("custom_cmap", colors, N=256)

def generate_heatmap_data(bs_model, greek_method, spot_min, spot_max, vol_min, vol_max, option_type, num_contracts):
    spot_range = np.linspace(spot_min, spot_max, 10)  
    vol_range = np.linspace(vol_min, vol_max, 10)   
    heatmap_data = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_model.S = spot
            bs_model.sigma = vol
            if greek_method in ['gamma', 'vega']:
                greek_value = getattr(bs_model, greek_method)() * num_contracts
            else:
                greek_value = getattr(bs_model, greek_method)(option_type) * num_contracts
            heatmap_data[i, j] = greek_value

    return heatmap_data, spot_range, vol_range

def plot_heatmap(heatmap_data, spot_range, vol_range, greek_name, option_type):
    fig, ax = plt.subplots(figsize=(12, 10))  # Increased figure size
    sns.heatmap(np.abs(heatmap_data[::-1]), xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range[::-1], 2), annot=heatmap_data[::-1], fmt=".2f", cmap=cmap, ax=ax, center=0)
    ax.set_title(f'Heatmap of {greek_name} for {option_type.capitalize()} Options')
    ax.set_xlabel('Spot Price')
    ax.set_ylabel('Volatility')
    plt.xticks(rotation=45, ha='right')  
    plt.yticks(rotation=0)  
    st.pyplot(fig)

def show_page():
    # Retrieve input parameters from the sidebar
    S = st.session_state.op_S
    K = st.session_state.op_K
    T = st.session_state.op_T
    sigma = st.session_state.op_sigma
    r = st.session_state.op_r
    purchase_price_call = st.session_state.op_purchase_price_call
    purchase_price_put = st.session_state.op_purchase_price_put

    # Initialize the Black-Scholes models for call and put options
    bs_model_call = BlackScholes(S, K, T, r, sigma, purchase_price_call)
    bs_model_put = BlackScholes(S, K, T, r, sigma, purchase_price_put)

    col1, col2 = st.columns(2)
    
    with col1:
        num_contracts_call = st.number_input("Number of Call Contracts", value=1, min_value=1, step=1)
    with col2:
        num_contracts_put = st.number_input("Number of Put Contracts", value=1, min_value=1, step=1)

    # Aggregate calculations for calls
    delta_call = bs_model_call.delta("call") * num_contracts_call
    gamma_call = bs_model_call.gamma() * num_contracts_call
    vega_call = bs_model_call.vega() * num_contracts_call
    rho_call = bs_model_call.rho("call") * num_contracts_call
    theta_call = bs_model_call.theta("call") * num_contracts_call

    # Aggregate calculations for puts
    delta_put = bs_model_put.delta("put") * num_contracts_put
    gamma_put = bs_model_put.gamma() * num_contracts_put
    vega_put = bs_model_put.vega() * num_contracts_put
    rho_put = bs_model_put.rho("put") * num_contracts_put
    theta_put = bs_model_put.theta("put") * num_contracts_put

    # Combined aggregate Greeks
    total_delta = delta_call + delta_put
    total_gamma = gamma_call + gamma_put
    total_vega = vega_call + vega_put
    total_rho = rho_call + rho_put
    total_theta = theta_call + theta_put

    # Calculate the opposing positions required to hedge each Greek
    hedge_delta_underlying = -total_delta / bs_model_call.delta("call") if bs_model_call.delta("call") != 0 else float('inf')
    hedge_delta_option = -total_delta / bs_model_put.delta("put") if bs_model_put.delta("put") != 0 else float('inf')
    
    hedge_gamma_underlying = -total_gamma / bs_model_call.gamma() if bs_model_call.gamma() != 0 else float('inf')
    hedge_gamma_option = -total_gamma / bs_model_put.gamma() if bs_model_put.gamma() != 0 else float('inf')
    
    hedge_vega_underlying = -total_vega / bs_model_call.vega() if bs_model_call.vega() != 0 else float('inf')
    hedge_vega_option = -total_vega / bs_model_put.vega() if bs_model_put.vega() != 0 else float('inf')
    
    hedge_rho_underlying = -total_rho / bs_model_call.rho("call") if bs_model_call.rho("call") != 0 else float('inf')
    hedge_rho_option = -total_rho / bs_model_put.rho("put") if bs_model_put.rho("put") != 0 else float('inf')
    
    hedge_theta_underlying = -total_theta / bs_model_call.theta("call") if bs_model_call.theta("call") != 0 else float('inf')
    hedge_theta_option = -total_theta / bs_model_put.theta("put") if bs_model_put.theta("put") != 0 else float('inf')

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Aggregate Greeks: Call")
        st.markdown(f"**Delta:** {delta_call:.4f}")
        st.markdown(f"**Gamma:** {gamma_call:.4f}")
        st.markdown(f"**Vega:** {vega_call:.4f}")
        st.markdown(f"**Rho:** {rho_call:.4f}")
        st.markdown(f"**Theta:** {theta_call:.4f}")

        st.subheader("Call Optimal Hedge")
        st.markdown(f"**Delta Hedge:** {hedge_delta_underlying:.4f} units of the underlying asset or {hedge_delta_option:.4f} put options")
        st.markdown(f"**Gamma Hedge:** {hedge_gamma_underlying:.4f} units of the underlying asset or {hedge_gamma_option:.4f} put options")
        st.markdown(f"**Vega Hedge:** {hedge_vega_underlying:.4f} units of the underlying asset or {hedge_vega_option:.4f} put options")
        st.markdown(f"**Rho Hedge:** {hedge_rho_underlying:.4f} units of the underlying asset or {hedge_rho_option:.4f} put options")
        st.markdown(f"**Theta Hedge:** {hedge_theta_underlying:.4f} units of the underlying asset or {hedge_theta_option:.4f} put options")
        
    with col2:
        st.subheader("Aggregate Greeks: Put")
        st.markdown(f"**Delta:** {delta_put:.4f}")
        st.markdown(f"**Gamma:** {gamma_put:.4f}")
        st.markdown(f"**Vega:** {vega_put:.4f}")
        st.markdown(f"**Rho:** {rho_put:.4f}")
        st.markdown(f"**Theta:** {theta_put:.4f}")
    
        st.subheader("Put Optimal Hedge")
        st.markdown(f"**Delta Hedge:** {hedge_delta_underlying:.4f} units of the underlying asset or {hedge_delta_option:.4f} call options")
        st.markdown(f"**Gamma Hedge:** {hedge_gamma_underlying:.4f} units of the underlying asset or {hedge_gamma_option:.4f} call options")
        st.markdown(f"**Vega Hedge:** {hedge_vega_underlying:.4f} units of the underlying asset or {hedge_vega_option:.4f} call options")
        st.markdown(f"**Rho Hedge:** {hedge_rho_underlying:.4f} units of the underlying asset or {hedge_rho_option:.4f} call options")
        st.markdown(f"**Theta Hedge:** {hedge_theta_underlying:.4f} units of the underlying asset or {hedge_theta_option:.4f} call options")

    # Heatmaps for Greeks
    st.header("Heatmaps for Greeks")

    spot_min = st.session_state.hp_spot_min
    spot_max = st.session_state.hp_spot_max
    vol_min = st.session_state.hp_vol_min
    vol_max = st.session_state.hp_vol_max

    greek_method = st.selectbox("Select Greek to Display", ["Delta", "Gamma", "Vega", "Rho", "Theta"])
    greek_name = greek_method.capitalize()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Heatmap for {greek_name} (Call Options)")
        heatmap_data, spot_range, vol_range = generate_heatmap_data(bs_model_call, greek_method.lower(), spot_min, spot_max, vol_min, vol_max, "call", num_contracts_call)
        plot_heatmap(heatmap_data, spot_range, vol_range, greek_name, "call")

    with col2:
        st.subheader(f"Heatmap for {greek_name} (Put Options)")
        heatmap_data, spot_range, vol_range = generate_heatmap_data(bs_model_put, greek_method.lower(), spot_min, spot_max, vol_min, vol_max, "put", num_contracts_put)
        plot_heatmap(heatmap_data, spot_range, vol_range, greek_name, "put")
