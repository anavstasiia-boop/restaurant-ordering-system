# CLASS: RestaurantSystem
class RestaurantSystem:
    """
    Represents the overall restaurant system.

    Attributes:
        menu (list): List of MenuItem objects
        customers (list): List of registered customers
    """

    def __init__(self, menu: list):
        self.menu = menu
        self.customers = []

    def create_customer(self, name: str, phone: str) -> 'Customer':
        """
        Creates a new customer and adds them to the system.

        Returns:
            Customer: Newly created customer object
        """
        customer = Customer(name, phone)
        self.customers.append(customer)
        return customer

# CLASS: Customer
class Customer:
    """
    Represents a customer in the restaurant system.

    Attributes:
        _customer_name (str): Customer name (protected)
        __phone_number (str): Phone number (private)
        __orders (list): List of customer orders (private)
    """

    def __init__(self, customer_name: str, phone_number: str) -> None:
        self._customer_name = customer_name
        self.__phone_number = phone_number
        self.__orders = []

    def __str__(self):
        """Returns readable customer information."""
        return f"Customer: {self._customer_name}, Orders: {len(self.__orders)}"

    # Property for customer name (encapsulation)
    @property
    def customer_name(self):
        """Gets the customer's name."""
        return self._customer_name

    @customer_name.setter
    def customer_name(self, name: str):
        """Sets the customer's name with validation."""
        if len(name) < 1:
            raise ValueError("Name cannot be empty")
        self._customer_name = name

    # Read-only property for phone number
    @property
    def phone_number(self):
        """Gets the customer's phone number."""
        return self.__phone_number

    def create_order(self, order):
        """
        Adds an order to the customer if it doesn't already exist.
        """
        if order not in self.__orders:
            self.__orders.append(order)
            print(f"Order {order.order_id} added for {self._customer_name}.")

    def view_orders(self):
        """Displays all orders of the customer."""
        if not self.__orders:
            print("No orders yet.")
        else:
            for order in self.__orders:
                print(order)

    def cancel_order(self, order_id):
        """
        Cancels an order by its ID.
        """
        original_count = len(self.__orders)

        self.__orders = [o for o in self.__orders if o.order_id != order_id]

        if len(self.__orders) < original_count:
            print(f"Order {order_id} cancelled.")
        else:
            print(f"Order {order_id} not found.")

# CLASS: Payment
class Payment:
    """
    Represents a payment in the system.

    Attributes:
        accepted_methods (list): Available payment methods (class variable)
        payment_counter (int): Counter for generating unique payment IDs
        __payment_id (str): Unique payment identifier (private)
        __amount (float): Payment amount (private)
        __method (str): Payment method (private)
    """

    accepted_methods = ['cash', 'card', 'online']
    payment_counter = 1

    def __init__(self, amount: float, method: str):
        # Generate unique payment ID
        self.__payment_id = f"P{Payment.payment_counter:03}"
        Payment.payment_counter += 1

        self.amount = amount
        self.__method = method

    # Read-only payment ID
    @property
    def payment_id(self):
        """Returns payment ID."""
        return self.__payment_id

    # Read-only payment method
    @property
    def method(self):
        """Returns payment method."""
        return self.__method

    # Property for amount (with validation)
    @property
    def amount(self):
        """Returns payment amount."""
        return self.__amount

    @amount.setter
    def amount(self, value: float):
        """Sets payment amount with validation."""
        if value < 0:
            raise ValueError("Amount cannot be negative")
        self.__amount = value

    @staticmethod
    def validate_payment(amount: float):
        """
        Validates payment amount.

        Returns:
            bool: True if valid, False otherwise
        """
        return amount > 0

    def process_payment(self):
        """Processes the payment if valid."""
        if Payment.validate_payment(self.__amount):
            print(f"Payment {self.__payment_id}: €{self.__amount:.2f} via {self.__method} processed.")
        else:
            print("Invalid payment amount.")

    def generate_receipt(self):
        """Prints a payment receipt."""
        print("\n- Receipt -")
        print(f"ID: {self.__payment_id}")
        print(f"Amount: €{self.__amount:.2f}")
        print(f"Method: {self.__method}")

    def __str__(self):
        """Returns readable string representation of Payment."""
        return f"Payment [{self.__payment_id}] €{self.__amount:.2f}, {self.__method}"

    def __gt__(self, other):
        return self.amount > other.amount

    def __eq__(self, other):
        return self.amount == other.amount