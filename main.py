from menu import load_menu, find_item, display_menu
from system import Customer, Payment, RestaurantSystem
from ordering import Order, Invoice, OrderManager


if __name__ == "__main__":

    print("\n__Welcome to the Restaurant Ordering System!__")

    menu_items = load_menu("menu.txt")

    # user
    name = input("Enter your name: ")
    phone = input("Enter your phone number (optional): ") or "N/A"

    # system
    system = RestaurantSystem(menu_items)

    # customer
    customer: Customer = system.create_customer(name, phone)

    # menu
    display_menu(menu_items)

    # order
    order = Order()
    customer.create_order(order)

    # manager
    manager = OrderManager()
    manager.create_order(order)

    try:
        num_items = int(input("How many items would you like to add?: "))
    except ValueError:
        num_items = 1

    for i in range(num_items):
        choice = input("Enter item name (you can type part of it): ")
        item = find_item(menu_items, choice)

        if item:
            try:
                quantity = int(input("Enter quantity: "))
            except ValueError:
                quantity = 1

            for _ in range(quantity):
                order.add_item(item)
        else:
            print("Item not found")

    # show order
    print("\nYour order:")
    order.show_order()

    # invoice
    invoice = Invoice(order)
    invoice.print_invoice()

    # show all orders
    print("\nAll orders in system:")
    manager.list_orders()

    # payment
    method = input("Enter payment method (cash/card/online): ").lower()
    while method not in Payment.accepted_methods:
        method = input("Invalid. Enter again: ").lower()

    payment = Payment(invoice.total_amount, method)
    payment.process_payment()
    payment.generate_receipt()