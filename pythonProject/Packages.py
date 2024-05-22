import csv


class Package:
    def __init__(self, id, address_name, delivery_address, deadline, delivery_city, delivery_zip, weight, status):
        if not id or not address_name:
            raise ValueError("Package ID or address is invalid")

        self.id = id
        self.address_name = address_name
        self.delivery_address = delivery_address
        self.deadline = deadline
        self.delivery_city = delivery_city
        self.delivery_zip = delivery_zip
        self.weight = weight
        self.status = status

    def __str__(self):

        return (f"{self.id}, {self.status}, {self.address_name}, {self.delivery_address}, {self.deadline}, "
                f"{self.delivery_city}, {self.delivery_zip}, {self.weight}")

    # update package info
    def update(self, new_delivery_address, new_address_name, new_city, new_zip, new_status):
        self.delivery_address = new_delivery_address
        self.address_name = new_address_name
        self.delivery_city = new_city
        self.delivery_zip = new_zip
        self.status = new_status

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def get_id(self):
        return self.id
