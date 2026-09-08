# CLASS: Order
from menu import MenuItem

class Order:
    """
    Represents a customer's order.

    Attributes:
        order_id (int): Unique order identifier
        items (list): List of MenuItem objects
        __total_price (float): Total price of the order (private)
    """

    order_counter = 1  # class variable for unique order IDs

    def __init__(self):
        # Assign unique ID
        self.order_id = Order.order_counter
        Order.order_counter += 1

        self.items = []
        self.__total_price = 0

    # Property for encapsulated total price
    @property
    def total_price(self):
        """Returns total price of the order."""
        return self.__total_price

    def add_item(self, item: MenuItem):
        """Adds an item to the order and updates total price."""
        self.items.append(item)
        self.__total_price += item.price

    def remove_item(self, item: MenuItem):
        """Removes an item from the order if it exists."""
        if item in self.items:
            self.items.remove(item)
            self.__total_price -= item.price

    def show_order(self):
        """Displays all items in the order with quantities."""
        done = []
        result = ''
        for item in self.items:
            if item not in done:
                count = self.items.count(item)
                print(f"\n{count}x {item.name}: €{count * item.price:.2f}")
                done.append(item)

    # Operator overloading: combine two orders
    def __add__(self, other):
        """Combines two orders into one."""
        for item in other.items:
            self.add_item(item)
        return self

    # Operator overloading: compare orders
    def __gt__(self, other):
        """Checks if this order is more expensive than another."""
        return self.total_price > other.total_price

    def __eq__(self, other):
        """Checks if two orders have equal total price."""
        return self.total_price == other.total_price

    def __str__(self):
        """Returns the items in the order"""
        result = f"Order {self.order_id}: "
        for item in self.items:
            result += f"\n-{item}"
        return result

# CLASS: OrderManager
class OrderManager:
    """
    Manages all orders in the system.

    Attributes:
        orders (list): List of all orders
    """

    def __init__(self):
        self.orders = []

    @classmethod
    def default_manager(cls):
        """Creates a default OrderManager instance."""
        return cls()

    def create_order(self, order: Order):
        """Adds a new order to the system."""
        self.orders.append(order)

    def delete_order(self, order):
        """Removes an order from the system."""
        try:
            self.orders.remove(order)
        except ValueError:
            print("Order not found")

    def find_order(self, order_id: int):
        """Finds an order by its ID."""
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    def list_orders(self):
        """Displays all orders."""
        for order in self.orders:
            print(f"Order {order.order_id}:")
            order.show_order()

    def __str__(self):
        result ='Orders: '
        for order in self.orders:
            result += f"\n{order}"
        return result

# CLASS: Invoice
class Invoice:
    """
    Represents an invoice for a specific order.

    Attributes:
        invoice_id (str): Unique invoice identifier
        order (Order): Associated order
        subtotal (float): Total before discount and tax
        discounted (float): Price after discount
        tax (float): Calculated tax
        __total_amount (float): Final total amount (private)
    """

    invoice_counter = 1  # class variable for unique invoice IDs

    def __init__(self, order: Order):
        # Generate unique invoice ID
        self.invoice_id = f"I{Invoice.invoice_counter:03}"
        Invoice.invoice_counter += 1

        self.order = order
        self.__subtotal = 0
        self.discounted = 0
        self._tax = 0
        self.__total_amount = 0

    @property
    def total_amount(self):
        """Returns final total amount."""
        return self.__total_amount

    @property
    def subtotal(self):
        """Returns subtotal"""
        return self.__subtotal

    @subtotal.setter
    def subtotal(self):
        return self.order.total_price

    @staticmethod
    def calculate_tax(subtotal: float):
        """Calculates tax (9%)."""
        return 0.09 * subtotal

    @staticmethod
    def apply_discount(total: float) -> float:
        """
        Applies discount:
        - 10% discount if total >= 20
        """
        if total >= 20:
            discount = total * 0.10
            print(f"10% discount: -€{discount:.2f}")
            return total - discount
        else:
            print("No discount applied")
            return total

    def generate_invoice(self):
        """Calculates all invoice values."""
        self.__subtotal = self.order.total_price
        self.discounted = self.apply_discount(self.__subtotal)
        self._tax = self.calculate_tax(self.discounted)
        self.__total_amount = self.discounted + self._tax

    def print_invoice(self):
        """Prints the full invoice."""
        self.generate_invoice()

        print("\nInvoice")
        print(f"ID: {self.invoice_id}")

        self.order.show_order()

        print(f"Subtotal: €{self.__subtotal:.2f}")
        print(f"Tax: €{self._tax:.2f}")
        print(f"Total: €{self.__total_amount:.2f}")

    def __str__(self):
        return f"Total amount order {self.order.order_id}: €{self.__total_amount: .2f}"

