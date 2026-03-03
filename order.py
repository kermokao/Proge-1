"""Order."""


class OrderItem:
    """Order Item requested by a customer."""

    def __init__(self, customer: str, name: str, quantity: int, one_item_volume: int):
        """aaa."""
        self.customer = customer
        self.name = name
        self.quantity = quantity
        self.one_item_volume = one_item_volume

    @property
    def total_volume(self) -> int:
        """Calculate and return total volume of all order items together."""
        return self.quantity * self.one_item_volume


class Order:
    """Combination of order items of one customer."""

    def __init__(self, order_items: list):
        """."""
        self.order_items = order_items
        self.destination = None

    @property
    def total_quantity(self) -> int:
        """Calculate and return the sum of quantities of all items in the order."""
        return sum(item.quantity for item in self.order_items)

    @property
    def total_volume(self) -> int:
        """Calculate and return the total volume of all items in the order."""
        return sum(item.total_volume for item in self.order_items)


class Container:
    """Container to transport orders."""

    def __init__(self, volume: int, orders=None):
        """."""
        self.volume = volume
        self.orders = orders if orders is not None else []

    @property
    def volume_left(self) -> int:
        """Return remaining volume left in the container."""
        used_volume = sum(order.total_volume for order in self.orders)
        return self.volume - used_volume


class OrderAggregator:
    """Algorithm of aggregating orders."""

    def __init__(self):
        """Tühi list."""
        self.order_items = []

    def add_item(self, item: OrderItem):
        """Lisab asju listi."""
        self.order_items.append(item)

    def aggregate_order(self, customer: str, max_items_quantity: int, max_volume: int):
        """Vaatab kuhu listi asju lisada."""
        items = []
        total_quantity = 0
        total_volume = 0
        remaining_items = []

        for item in self.order_items:
            if item.customer == customer:
                if total_quantity + item.quantity <= max_items_quantity and \
                   total_volume + item.total_volume <= max_volume:
                    items.append(item)
                    total_quantity += item.quantity
                    total_volume += item.total_volume
                else:
                    remaining_items.append(item)
            else:
                remaining_items.append(item)

        self.order_items = remaining_items
        return Order(items)


class ContainerAggregator:
    """Algorithm to prepare containers."""

    def __init__(self, container_volume: int):
        """."""
        self.container_volume = container_volume
        self.not_used_orders = []

    def prepare_containers(self, orders: tuple) -> dict:
        """."""
        containers_destination = {}

        for order in orders:
            if order.total_volume > self.container_volume:
                self.not_used_orders.append(order)
                continue

            dest = order.destination
            if dest not in containers_destination:
                containers_destination[dest] = []

            placed = False
            for container in containers_destination[dest]:
                if container.volume_left >= order.total_volume:
                    container.orders.append(order)
                    placed = True
                    break

            if not placed:
                new_container = Container(self.container_volume)
                new_container.orders.append(order)
                containers_destination[dest].append(new_container)

        return containers_destination


if __name__ == '__main__':
    print("Order items")

    order_item1 = OrderItem("Apple", "iPhone 11", 100, 10)
    order_item2 = OrderItem("Samsung", "Samsung Galaxy Note 10", 80, 10)
    order_item3 = OrderItem("Mööbel 24", "Laud", 300, 200)
    order_item4 = OrderItem("Apple", "iPhone 11 Pro", 200, 10)
    order_item5 = OrderItem("Mööbel 24", "Diivan", 20, 200)
    order_item6 = OrderItem("Mööbel 24", "Midagi väga suurt", 20, 400)

    print(order_item3.total_volume)  # 60000

    print("Order Aggregator")
    oa = OrderAggregator()
    oa.add_item(order_item1)
    oa.add_item(order_item2)
    oa.add_item(order_item3)
    oa.add_item(order_item4)
    oa.add_item(order_item5)
    oa.add_item(order_item6)
    print(f'Added {len(oa.order_items)}(6 is correct) order items')

    order1 = oa.aggregate_order("Apple", 350, 3000)
    order1.destination = "Tallinn"
    print(f'order1 has {len(order1.order_items)}(2 is correct) order items')

    order2 = oa.aggregate_order("Mööbel 24", 325, 64100)
    order2.destination = "Tallinn"
    print(f'order2 has {len(order2.order_items)}(2 is correct) order items')

    print(f'after orders creation, aggregator has only {len(oa.order_items)}(2 is correct) order items left.')

    print("Container Aggregator")
    ca = ContainerAggregator(70000)
    too_big_order = Order([OrderItem("Apple", "Apple Car", 10000, 300)])
    too_big_order.destination = "Somewhere"
    containers = ca.prepare_containers((order1, order2, too_big_order))
    print(f'prepare_containers produced containers to {len(containers)}(1 is correct) different destination(s)')

    try:
        containers_to_tallinn = containers['Tallinn']
        print(f'volume of the container to tallinn is {containers_to_tallinn[0].volume}(70000 is correct) cm^3')
        print(f'container to tallinn has {len(containers_to_tallinn[0].orders)}(2 is correct) orders')
    except KeyError:
        print('Container to Tallinn not found!')

    print(f'{len(ca.not_used_orders)}(1 is correct) cannot be added to containers')
