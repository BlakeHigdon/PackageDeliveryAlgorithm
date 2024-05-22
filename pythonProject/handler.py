import csv
from Packages import Package
from hashmap import HashMap


# this is going to construct a hashmap of all important package information.

class Handler:
    # the functions below all have time complexity O(1)
    def __init__(self):
        self.TOTAL = 40
        self.packages = {}
        self.packages_hash = HashMap()
        self.build_from_csv()

    def __iter__(self):
        return iter([self.packages for id, package in self.packages.items()])

    def __len__(self):
        return len(self.packages)

    def insert(self, item):
        self.packages[item.id] = item

    # this will take the raw package data and city names and construct the hashmap
    # time complexity O(n).
    def build_from_csv(self):
        convert_csv_to_address_names = HashMap()

        import csv

        with open("WGUPS Distance Table(1).csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

            # Validate each row
            for row in rows:
                if len(row) != 3:
                    raise ValueError("Incorrect number of fields:", row)  # Check for correct format
                # bug fixing
                id, name, address = row
                # print("ID:", id, "Name:", name, "Address:", address)  # Debugging output
            for data in rows:
                convert_csv_to_address_names.add(data[2], data[1])

        with open("WGUPS Package File.csv") as packageFile:
            reader = csv.reader(packageFile)
            package_data = list(reader)

            # print("CSV data loaded. Total rows:", len(package_data))
            # for package in package_data:
            #   print("Package data:", package)  # Inspect each row

            for package in package_data:
                address_name = package[1]  # This is the key used for mapping
                if address_name is None or address_name.strip() == "":
                    raise ValueError("Invalid package address:", address_name)  # Validate key

                mapped_address = convert_csv_to_address_names.get(address_name)  # Get mapped address
                if mapped_address is None:
                    raise ValueError("No mapping for:", address_name)  # If the mapping is incorrect

        for entry in package_data:
            if len(entry) > 1:
                self.insert(Package(id=entry[0], address_name=convert_csv_to_address_names.get(entry[1]),
                                    delivery_address=entry[1], deadline=entry[5],
                                    delivery_city=entry[2], delivery_zip=entry[4], weight=entry[6],
                                    status="AT THE HUB"))
                self.packages_hash.add(entry[0],
                                       Package(id=entry[0], address_name=convert_csv_to_address_names.get(entry[1]),
                                               delivery_address=entry[1], deadline=entry[5],
                                               delivery_city=entry[2], delivery_zip=entry[4], weight=entry[6],
                                               status="AT THE HUB"))

    # Below function looks up an ID and returns the package with it. Time complexity O(1)
    def package_id_lookup(self, id):
        return self.packages_hash.get(id)

    # time complexity of the below functions is O(n) for each.
    # The will lookup the input criteria and output all packages that have a match with the input.

    def package_deadline_lookup(self, deadline):
        package_list = list()
        for id in range(1, self.TOTAL + 1):
            package = self.package_id_lookup(str(id))
            if package.deadline == deadline:
                package_list.append(package)
        return package_list

    def package_address_lookup(self, address):
        package_list = list()
        for id in range(1, self.TOTAL + 1):
            package = self.package_id_lookup(str(id))
            if package.delivery_address == address:
                package_list.append(package)
        return package_list

    def package_city_lookup(self, city):
        package_list = list()
        for id in range(1, self.TOTAL + 1):
            package = self.package_id_lookup(str(id))
            if package.delivery_city == city:
                package_list.append(package)
        return package_list

    def package_zip_lookup(self, zip):
        package_list = list()
        for id in range(1, self.TOTAL + 1):
            package = self.package_id_lookup(str(id))
            if package.delivery_zip == zip:
                package_list.append(package)
        return package_list

    def package_weight_lookup(self, weight):
        package_list = list()
        for id in range(1, self.TOTAL + 1):
            package = self.package_id_lookup(str(id))
            if package.weight == weight:
                package_list.append(package)
        return package_list

    def package_status_lookup(self, status):
        package_list = list()
        for id in range(1, self.TOTAL + 1):
            package = self.package_id_lookup(str(id))
            if package.status == status:
                package_list.append(package)
        return package_list
