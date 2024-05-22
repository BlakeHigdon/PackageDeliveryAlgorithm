from time import sleep
from Packages import Package
from hashmap import HashMap
from queue import Queue
from datetime import datetime
import sys
import datetime
import copy


class DeliveryTruck:
    # default constructor
    # space and time complexity of O(1)
    def __init__(self, id):
        self.MPH = 18
        self.id = id
        self.packages = HashMap()
        self.delivery_addresses = set()
        self.route = Queue()
        self.num_packages = 0

    # will return the truck ID and remaining package count
    # space and time complexity of O(1)
    def __str__(self):
        return f"DeliveryTruck{self.id} has {self.num_packages} packages to deliver still."

    # space and time complexity of O(1)
    # adds 1 to num_packages and adds a target delivery address
    def add_package(self, package):
        if package is None or package.address_name is None:
            raise ValueError("Package or its address is invalid")

        self.packages.add(package.id, package)
        self.num_packages += 1
        self.delivery_addresses.add(package.address_name)

    # space and time complexity of O(1)
    # returns the trucks packages
    def get_packages(self):
        return self.packages

    # space and time complexity of O(1)
    # removes a package from the delivery truck
    def delete_package(self, package):
        self.packages.dlt(package)
        self.num_packages -= 1
        self.delivery_addresses.remove(package.address_name)

    # Algorithm used: Nearest Neighbor
    # Space complexity: O(1)
    # Time complexity O(N^2)
    # Starts at the hub and visits the closest delivery address each time.
    # When the truck is empty it will return to the hub.
    def nearest_neighbor(self, address_list):
        # Copying remaining_addresses as a set
        remaining_addresses = self.delivery_addresses.copy()
        curr_address = None  # Initialize current address
        distance_traveled = 0

        while len(remaining_addresses) > 0:
            # Get the first address from remaining_addresses
            if curr_address is None:
                curr_address = list(remaining_addresses)[0]  # Start with the first item in the set

            # Get the item corresponding to the current address
            item = address_list.get(curr_address)
            if item is None:
                raise ValueError(f"Invalid address in adjacency matrix: {curr_address}")

            # Retrieve 'edges' safely
            edges = getattr(item, 'edges', None)
            if edges is None:
                raise TypeError(f"No edges found for address: {curr_address}")  # Handle invalid edges

            closest_neighbor = sys.maxsize
            for edge in edges:
                if edge.end_node in remaining_addresses:
                    if float(edge.weight) < closest_neighbor:
                        closest_neighbor = float(edge.weight)
                        curr_address = edge.end_node
                        next_address = [edge.end_node, edge.weight]

            # Discard the current address after processing
            remaining_addresses.discard(curr_address)
            self.route.put(next_address)  # Add to the delivery route

        return distance_traveled  # Return the total distance traveled

    # the 2 below functions both have a space and time complexity of O(n)
    # packages_on_trucks will return all packages on all trucks at any time
    # out_for_delivery will take in an address name and return  all packages going to that address
    def packages_on_trucks(self):
        all_packages = list()
        for i in range(1, 41):
            package = self.packages.get(str(i))
            if package is not None:
                all_packages.append(package.id)
        return all_packages

    def out_for_delivery(self, delivery_address_name):
        curr_packages = list()
        for i in range(1, 41):
            package = self.packages.get(str(i))
            if package is not None:
                if package.address_name == delivery_address_name:
                    curr_packages.append(package.id)
        return curr_packages

    # the below function will handle delivery of packages

    def delivery(self, departure_time, pkg_handler, packages_statuses, package_nine_update):
        return_time = None
        distance = 0
        update_nine = False

        # ADDS 'DELIVERED' TO DICTIONARY IF NOT ALREADY IN THERE
        if "DELIVERED" not in packages_statuses:
            packages_statuses["DELIVERED"] = set()

        # STORES PACKAGE DELIVERY TIME
        if "DELIVERED_TIME" not in packages_statuses:
            packages_statuses["DELIVERED_TIME"] = dict()

        # STORE TIME PACKAGES BEGIN TRANSIT
        if "DEPARTURE_TIME" not in packages_statuses:
            packages_statuses["DEPARTURE_TIME"] = dict()

        # STORE TIME PACKAGES LEAVE THE HUB
        if "LEFT_HUB" not in packages_statuses:
            packages_statuses["LEFT_HUB"] = dict()

        for i in range(1, 41):
            dummy_package = self.packages.get(str(i))
            if dummy_package is not None:
                packages_statuses["LEFT_HUB"][int(dummy_package.get_id())] = departure_time.strftime("%H:%M:%S")

        # used when packages are loaded onto the truck and 'move' for the first time
        begin_transit = departure_time.strftime("%H:%M:%S")
        while self.route.qsize() > 0:
            next_stop = self.route.get()
            curr_packages = self.out_for_delivery(next_stop[0])
            distance += float(next_stop[1])
            hours_driven = distance / self.MPH
            current_time = departure_time + datetime.timedelta(hours=hours_driven)

            # create an object to help us check if package 9 can realize its mistake or not
            ten_twenty = datetime.datetime(2024, 5, 7, 10, 20, 0, 0)

            # display progress to terminal
            if next_stop[0] == "Western Governors University":
                print(current_time.strftime("%H:%M:%S") + " Delivery Truck" + self.id +
                      " is en route to " + next_stop[0] + "\n")
            else:
                print(current_time.strftime("%H:%M:%S") + ' Delivery Truck' + self.id +
                      " delivering to " + next_stop[0] + "|")
            sleep(0.02)

            if current_time >= ten_twenty and not package_nine_update and self.id == "1_trip2" and not update_nine:
                print("\n")
                print(f"Current delivery address for package 9 is incorrect. To fix enter 'update'")
                print("\n")
                response = input("Response: ")
                if response != "update":
                    print(f"Nice Try Mr/Ms Evaluator!")
                    print("\n")
                    print(f"Current delivery address for package 9 is incorrect. To fix enter 'update'")
                    response = input("Response: ")
                if response == "update":
                    corrected_information = ((Package("9", "Third District Juvenile Court",
                                                                "410 S State St", "EOD",
                                                                "Salt Lake City", "84111", "2", "IN TRANSIT")))
                    pkg_handler.packages_hash.add(corrected_information.id, corrected_information)
                    update_nine = True
                    print("\n")
            # record data after the update to 9
            packages_on_trucks = self.packages_on_trucks()
            time = current_time.strftime("%H:%M:%S")
            if packages_statuses is None:
                packages_statuses = dict()
            for packages in curr_packages:


                if time not in packages_statuses:
                    packages_statuses[time] = dict()
                dummy_package = self.packages.get(packages)

                # update status of packages that get delivered and record time
                dummy_package.set_status("DELIVERED")
                packages_statuses["DELIVERED_TIME"][int(dummy_package.get_id())] = time
                packages_statuses["DEPARTURE_TIME"][int(dummy_package.get_id())] = begin_transit

                # update package status
                self.packages.add(packages, dummy_package)

                pkg_key = str(dummy_package.get_id())
                packages_statuses[time][pkg_key] = copy.deepcopy(dummy_package)

                if (str(i) not in curr_packages and dummy_package is not None
                        and dummy_package.get_status() != "DELIVERED"):

                    dummy_package.set_status("IN TRANSIT")

                    packages_statuses[time][dummy_package.get_id()] = copy.deepcopy(dummy_package)

                    packages_statuses["DELIVERED_TIME"][int(dummy_package.get_id())] = time

                elif dummy_package is not None and dummy_package.get_status() == "DELIVERED" or str(
                        dummy_package.get_id() in packages_statuses["DELIVERED"]):
                    packages_statuses[time][dummy_package.get_id] = copy.deepcopy(dummy_package)
                    packages_statuses["DELIVERED"].add(dummy_package.get_id())

                elif dummy_package is not None and dummy_package.get_status() != "DELIVERED" and dummy_package.get_status() != "IN TRANSIT":
                    print(dummy_package.get_id() + " is not in transit or delivered. Ensure it left the hub.")

            for i in range(1, 41):
                dummy_package = pkg_handler.packages_hash.get(str(i))

                if i in packages_statuses["DELIVERED"]:
                    packages_statuses[time][dummy_package.get_id()] = copy.deepcopy(dummy_package)
            begin_transit = time

        return_time = departure_time + datetime.timedelta(hours=hours_driven)

        return [return_time, hours_driven, distance, package_nine_update]
