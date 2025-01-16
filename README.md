
---

# **Option Pricing Series**

## **Interactive Streamlit Application for Option Payoffs and Strategies**

**Try it live**: [Option Pricing Series Interactive App](https://optionstrategist.streamlit.app)

**Author**: Mark Bogorad  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.12.0-green)
![KDB+](https://img.shields.io/badge/KDB+-Integration-yellow)
![Finance](https://img.shields.io/badge/Finance-Options-red)

---

## **Summary**

The **Option Pricing Series** is a dynamic Streamlit application designed to visualize option payoffs and explore trading strategies. It integrates **Black-Scholes pricing models**, visual heatmaps, and optimal hedging calculations with a real-time input storage mechanism powered by **KDB+**.

The app provides traders and financial engineers with tools to analyze how varying spot prices and volatilities affect option payoffs, helping users make informed decisions.

---

## **Features**

- **Heatmaps**: Visualize how option profits vary with spot prices and volatilities.
- **Trade Strategies**: Explore predefined strategies like covered calls, protective puts, and strangles.
- **Greeks Calculation**: Compute Delta, Gamma, Vega, Rho, and Theta for hedging decisions.
- **KDB+ Integration**: Store and retrieve user inputs for enhanced data tracking.
- **Interactive UI**: Real-time adjustments to parameters via Streamlit sliders and inputs.

---

## **Relevance**

Option pricing and risk management are critical in financial engineering. Traditional static calculations are enhanced here with:
- Real-time interactivity for exploring multiple scenarios.
- Integration with KDB+ for efficient data storage and retrieval.
- A focus on visual and intuitive analysis, ideal for both novice and professional users.

---

## **Methodology**

### **Core Functionality**
- **Black-Scholes Model**: Computes call and put prices, profits, and option Greeks.
- **Heatmap Visualization**: Plots profit for various spot prices and volatilities.
- **Optimal Hedges**: Calculates hedge ratios for risk management.

### **Tools and Libraries**
- **Streamlit**: Builds the user interface.
- **KDB+**: Stores user inputs.
- **Pandas, NumPy, SciPy**: Enables data manipulation and statistical calculations.
- **Matplotlib, Seaborn**: For visualizations.

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/markbogorad/option-pricing-series.git
   cd option-pricing-series
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run main.py
   ```

4. (Optional) Start the KDB+ server for input storage:
   ```bash
   q -p 5001
   ```

---

## **Usage**

1. **Set Parameters**: Input current asset price, strike price, volatility, etc., in the sidebar.
2. **Visualize Payoffs**: Navigate between tabs to explore heatmaps, strategies, and hedges.
3. **Analyze Results**: View and download stored inputs or utilize KDB+ for advanced data tracking.

---

## **Example**

### **Call and Put Option Profit Heatmaps**
Heatmaps display profits for call and put options based on:
- Spot Price (X-axis)
- Volatility (Y-axis)

### **Optimal Hedges**
Greeks such as Delta and Vega are calculated to provide actionable hedging insights:
- Example Delta Hedge:  
  > "To delta hedge, trade 0.34 units of the underlying asset."

---

## **License**

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

---
