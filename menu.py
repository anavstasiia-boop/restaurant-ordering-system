# BASE CLASS: MenuItem
class MenuItem:
    """
    Represents a general item on the restaurant menu.

    Attributes:
        name (str): Name of the item (public)
        _category (str): Category of the item (protected)
        __price (float): Price of the item (private, encapsulated)
    """

    def __init__(self, name, category, price):
        self.name = name                  # public attribute
        self._category = category         # protected attribute (used in subclasses)
        self.__price = price              # private attribute (encapsulation)

    # Property decorator to safely access price
    @property
    def price(self):
        """Returns the price of the menu item."""
        return self.__price

    # Setter to control modification of price
    @price.setter
    def price(self, value):
        """Sets the price only if it is positive."""
        if value > 0:
            self.__price = value
        else:
            print("Price must be positive")

    # Applies discount using encapsulated price
    def apply_discount(self, percent):
        """Applies a percentage discount to the item price."""
        self.__price *= (1 - percent / 100)

    def display_item(self):
        """Displays item details."""
        print(f"{self.name} ({self._category}) - €{self.__price:.2f}")

    # String representation of object
    def __str__(self):
        """Returns readable string representation of MenuItem."""
        return f"{self.name} - {self._category} - €{self.__price:.2f}"



# SUBCLASS: Food
class Food(MenuItem):
    """
    Represents a food item in the menu.

    Inherits from MenuItem.

    Attributes:
        calories (int): Number of calories in the food item
    """

    def __init__(self, name, category, price, calories):
        super().__init__(name, category, price)
        self.calories = calories

    def is_vegetarian(self):
        """Checks if the food item is vegetarian."""
        return self._category.lower() == "vegetarian"

    # Method overriding (Polymorphism)
    def display_item(self):
        """Displays food-specific details."""
        print(f"Food: {self.name} | {self.calories} kcal | €{self.price:.2f}")

    def __str__(self):
        """Returns readable string representation of Food."""
        return f"Food: {self.name}, Calories: {self.calories}, Price: €{self.price:.2f}"

# SUBCLASS: Drink
class Drink(MenuItem):
    """
    Represents a drink item in the menu.

    Inherits from MenuItem.

    Attributes:
        size (str): Size of the drink (e.g., Small, Medium, Large)
    """

    def __init__(self, name, category, price, size):
        super().__init__(name, category, price)
        self.size = size

    def change_size(self, new_size):
        """Changes the size of the drink."""
        self.size = new_size

    # Method overriding
    def display_item(self):
        """Displays drink-specific details."""
        print(f"Drink: {self.name} ({self.size}) - €{self.price:.2f}")

    def __str__(self):
        """Returns readable string representation of Drink."""
        return f"Drink: {self.name}, Size: {self.size}, Price: €{self.price:.2f}"



# MENU FUNCTIONS
def load_menu(filename):
    """
    Loads menu items from a file.

    File format:
    Food,name,category,price,calories
    Drink,name,category,price,size

    Returns:
        list: List of MenuItem objects
    """
    items = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split(",")

            if parts[0] == "Food":
                item = Food(parts[1], parts[2], float(parts[3]), int(parts[4]))
            elif parts[0] == "Drink":
                item = Drink(parts[1], parts[2], float(parts[3]), parts[4])
            else:
                continue

            items.append(item)

    return items


def find_item(menu_items, name):
    """
    Finds an item in the menu by (partial) name.

    If multiple matches are found, user selects one.

    Returns:
        MenuItem or None
    """
    name = name.strip().lower()

    matches = [item for item in menu_items if name in item.name.lower()]

    if len(matches) == 1:
        return matches[0]

    elif len(matches) > 1:
        print("Multiple matches found:")
        for i, item in enumerate(matches):
            print(f"{i}: {item.name}")

        try:
            choice = int(input("Choose item number: "))
            return matches[choice]
        except:
            print("Invalid choice")
            return None

    else:
        return None


def display_menu(menu_items):
    """
    Displays the full restaurant menu grouped by category.
    """
    print("\n" + "=" * 40)
    print("              MENU")
    print("=" * 40)

    print("\nFOOD (Vegetarian):")
    print("-" * 40)
    for item in menu_items:
        if isinstance(item, Food) and item.is_vegetarian():
            print(f"{item.name:<20} {item.calories:>4} kcal   €{item.price:>6.2f}")

    print("\nFOOD (Non-Vegetarian):")
    print("-" * 40)
    for item in menu_items:
        if isinstance(item, Food) and not item.is_vegetarian():
            print(f"{item.name:<20} {item.calories:>4} kcal   €{item.price:>6.2f}")

    print("\nDRINKS:")
    print("-" * 40)
    for item in menu_items:
        if isinstance(item, Drink):
            print(f"{item.name:<20} {item.size:<8}   €{item.price:>6.2f}")

    print("=" * 40)