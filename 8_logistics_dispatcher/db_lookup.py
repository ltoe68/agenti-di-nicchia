import pandas as pd

def lookup_shipment(order_id):
    """
    Searches for an order_id in the shipments.csv file.
    Returns a dictionary with status details or None if not found.
    """
    try:
        df = pd.read_csv("shipments.csv")
        # Ensure order_id is string for comparison
        df['order_id'] = df['order_id'].astype(str)
        order_id = str(order_id).strip()
        
        result = df[df['order_id'] == order_id]
        
        if not result.empty:
            return result.iloc[0].to_dict()
        else:
            return None
    except Exception as e:
        return {"error": str(e)}
