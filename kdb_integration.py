from pyq import q

def save_parameters_to_kdb(S, K, T, sigma, r, purchase_price_call, purchase_price_put, num_contracts_call, num_contracts_put):
    # Connect to kdb+ (assuming it's running on localhost and default port 5000)
    qconn = q.q

    # Table structure
    qconn('parameters:([] S:(); K:(); T:(); sigma:(); r:(); purchase_price_call:(); purchase_price_put:(); num_contracts_call:(); num_contracts_put:())')
    
    # Insert parameters
    qconn(f'insert[`parameters](`${S}; `${K}; `${T}; `${sigma}; `${r}; `${purchase_price_call}; `${purchase_price_put}; `${num_contracts_call}; `${num_contracts_put})')
