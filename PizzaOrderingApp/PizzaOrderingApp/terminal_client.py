import requests

def place_order():
    customer_name = input("Enter your name: ")
    pizza_type = input("Enter pizza type ('Margherita', 'Pepperoni', 'BBQ Chicken', 'Veggie', 'Cheese'.): ")
    quantity = input("Enter quantity: ")

    response = requests.post('http://127.0.0.1:8000/pizza/order/', data={
        'customer_name': customer_name,
        'pizza_type': pizza_type,
        'quantity': quantity
    })

    if response.status_code in (200, 201):     # Handle both success codes
        print("Order response:", response.json())
    else:
        try:
            print("Failed to place order:", response.json())
        except requests.exceptions.JSONDecodeError:
            print(f"Error: Server returned non-JSON response (Status {response.status_code}): {response.text}")

if __name__ == "__main__":
    while True:
        place_order()