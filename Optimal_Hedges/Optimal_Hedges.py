import streamlit as st
from black_scholes import BlackScholes

def show_page():
    st.title("Option Hedging Strategies")

    # Retrieve input parameters from the sidebar
    S = st.session_state.op_S
    K = st.session_state.op_K
    T = st.session_state.op_T
    sigma = st.session_state.op_sigma
    r = st.session_state.op_r
    purchase_price_call = st.session_state.op_purchase_price_call
    purchase_price_put = st.session_state.op_purchase_price_put

    # Input Section for number of contracts
    st.header("Number of Contracts")
    num_contracts_call = st.number_input("Number of Call Contracts", value=1, min_value=1, step=1)
    num_contracts_put = st.number_input("Number of Put Contracts", value=1, min_value=1, step=1)

    # Initialize the Black-Scholes models for call and put options
    bs_model_call = BlackScholes(S, K, T, r, sigma, purchase_price_call)
    bs_model_put = BlackScholes(S, K, T, r, sigma, purchase_price_put)

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
    hedge_delta = -total_delta / bs_model_call.delta("call") if bs_model_call.delta("call") != 0 else float('inf')
    hedge_gamma = -total_gamma / bs_model_call.gamma() if bs_model_call.gamma() != 0 else float('inf')
    hedge_vega = -total_vega / bs_model_call.vega() if bs_model_call.vega() != 0 else float('inf')
    hedge_rho = -total_rho / bs_model_call.rho("call") if bs_model_call.rho("call") != 0 else float('inf')
    hedge_theta = -total_theta / bs_model_call.theta("call") if bs_model_call.theta("call") != 0 else float('inf')

    # Output Section in Two Columns
    st.header("Hedging Strategies")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Aggregate Call Option Strategies")
        st.markdown(f"**Delta:** {delta_call:.4f}")
        st.markdown(f"**Gamma:** {gamma_call:.4f}")
        st.markdown(f"**Vega:** {vega_call:.4f}")
        st.markdown(f"**Rho:** {rho_call:.4f}")
        st.markdown(f"**Theta:** {theta_call:.4f}")

    with col2:
        st.subheader("Aggregate Put Option Strategies")
        st.markdown(f"**Delta:** {delta_put:.4f}")
        st.markdown(f"**Gamma:** {gamma_put:.4f}")
        st.markdown(f"**Vega:** {vega_put:.4f}")
        st.markdown(f"**Rho:** {rho_put:.4f}")
        st.markdown(f"**Theta:** {theta_put:.4f}")

    st.header("Opposing Positions Required to Hedge Each Greek")

    st.markdown(f"**Delta Hedge:** {hedge_delta:.4f} units of the underlying asset")
    st.markdown(f"**Gamma Hedge:** {hedge_gamma:.4f} units of the underlying asset")
    st.markdown(f"**Vega Hedge:** {hedge_vega:.4f} units of the underlying asset")
    st.markdown(f"**Rho Hedge:** {hedge_rho:.4f} units of the underlying asset")
    st.markdown(f"**Theta Hedge:** {hedge_theta:.4f} units of the underlying asset")
