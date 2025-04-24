import requests

def check_order_status():
    order_id = input("Enter your Order ID: ")
    response = requests.get(f'http://127.0.0.1:8000/order_status/{order_id}/')

    if response.status_code == 200:
        print("Order Status:", response.json()['status'])
    else:
        print("Order not found.")

if __name__ == "__main__":
    check_order_status()
    