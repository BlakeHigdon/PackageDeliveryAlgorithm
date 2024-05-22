# student id -> 011015090
from Packages import Package
from handler import Handler
from DeliveryTruck import DeliveryTruck
from time import sleep
from operator import itemgetter
import datetime
import collections
from graph import Graph
import time
import sys

# creating a nested dictionary to hold the statuses of each package over time
pkg_statuses = dict(dict())

# initialize handler and graph
graph = Graph()
handler = Handler()

truck1 = DeliveryTruck("1")
truck1_trip2 = DeliveryTruck("1_trip2")
truck2 = DeliveryTruck("2")

year_month_day = datetime.datetime(2024, 5, 7)


def delivery_truck1():
    truck1.delivery_addresses.clear()
    truck1.add_package(handler.package_id_lookup('1'))
    truck1.add_package(handler.package_id_lookup('29'))
    truck1.add_package(handler.package_id_lookup('7'))
    truck1.add_package(handler.package_id_lookup('30'))
    truck1.add_package(handler.package_id_lookup('8'))
    truck1.add_package(handler.package_id_lookup('34'))
    truck1.add_package(handler.package_id_lookup('40'))
    truck1.add_package(handler.package_id_lookup('39'))
    truck1.add_package(handler.package_id_lookup('37'))

    # the 6 packages below all have requirements that require them to be on the same truck.
    truck1.add_package(handler.package_id_lookup('13'))
    truck1.add_package(handler.package_id_lookup('14'))
    truck1.add_package(handler.package_id_lookup('15'))
    truck1.add_package(handler.package_id_lookup('16'))
    truck1.add_package(handler.package_id_lookup('19'))
    truck1.add_package(handler.package_id_lookup('20'))

    truck1.nearest_neighbor(graph.adjacency_matrix)


def delivery_truck1_trip2():
    truck1_trip2.delivery_addresses.clear()
    truck1_trip2.add_package(handler.package_id_lookup('5'))
    truck1_trip2.add_package(handler.package_id_lookup('21'))
    truck1_trip2.add_package(handler.package_id_lookup('4'))
    truck1_trip2.add_package(handler.package_id_lookup('24'))
    truck1_trip2.add_package(handler.package_id_lookup('23'))
    truck1_trip2.add_package(handler.package_id_lookup('26'))
    truck1_trip2.add_package(handler.package_id_lookup('22'))

    # the 4 packages below all arrive to the hub late so picking them up on the second trip is best.
    truck1_trip2.add_package(handler.package_id_lookup('6'))
    truck1_trip2.add_package(handler.package_id_lookup('32'))
    truck1_trip2.add_package(handler.package_id_lookup('28'))
    truck1_trip2.add_package(handler.package_id_lookup('25'))

    truck1_trip2.nearest_neighbor(graph.adjacency_matrix)


def delivery_truck2():
    truck2.delivery_addresses.clear()
    truck2.add_package(handler.package_id_lookup('17'))
    truck2.add_package(handler.package_id_lookup('12'))
    truck2.add_package(handler.package_id_lookup('31'))
    truck2.add_package(handler.package_id_lookup('11'))
    truck2.add_package(handler.package_id_lookup('10'))
    truck2.add_package(handler.package_id_lookup('18'))
    truck2.add_package(handler.package_id_lookup('27'))
    truck2.add_package(handler.package_id_lookup('35'))
    truck2.add_package(handler.package_id_lookup('2'))
    truck2.add_package(handler.package_id_lookup('33'))
    truck2.add_package(handler.package_id_lookup('9'))

    # the 3 packages below can only be on truck2.
    truck2.add_package(handler.package_id_lookup('3'))
    truck2.add_package(handler.package_id_lookup('36'))
    truck2.add_package(handler.package_id_lookup('38'))
    truck2.nearest_neighbor(graph.adjacency_matrix)


def initialize_graph():
    graph.initialize_name_data()
    graph.initialize_distance_data()
    graph.initialize_addresses()


# route trucks
initialize_graph()

# delivery_truck1()
# delivery_truck1_trip2()
# delivery_truck2()

updated_nine = False


def deliver_the_packages(pkg_statuses):
    # create time objects
    eight = datetime.datetime(2024, 5, 7, 8, 0, 0, 0)
    nine_zero_five = datetime.datetime(2024, 5, 7, 9, 5, 0, 0)
    ten_twenty = datetime.datetime(2024, 5, 7, 10, 20, 0, 0)

    delivery_truck1()
    truck1_stats = truck1.delivery(eight, handler, pkg_statuses, updated_nine)

    delivery_truck1_trip2()
    truck1_trip2_stats = truck1_trip2.delivery(truck1_stats[0], handler, pkg_statuses, truck1_stats[3])

    delivery_truck2()
    truck2_stats = truck2.delivery(ten_twenty, handler, pkg_statuses, truck1_trip2_stats[3])

    begin_delivery = eight
    end_delivery = truck2_stats[0]
    end_delivery = end_delivery - begin_delivery
    total_hours = end_delivery.seconds // 3600
    total_minutes = (end_delivery.seconds % 3600) // 60
    total_time = str(total_hours) + ":" + str(total_minutes)

    total_delivery_time = round(float(truck2_stats[1] + truck1_trip2_stats[1]), 2)
    total_delivery_time = datetime.datetime(2024, 5, 7, 0, 0, 0, 0) + datetime.timedelta(hours=total_delivery_time)

    total_miles = truck2_stats[2] + truck1_trip2_stats[2] + truck1_trip2_stats[2]
    print('\n')
    print("Delivery Truck 1 Ending Stats: ")
    print("Left the hub at: ", eight)
    print("Returned to the hub at:", truck1_stats[0])
    print("Time on the road: ", round(float(truck1_stats[1]), 2), " hours")
    print("Miles traveled: ", round(float(truck1_stats[2]), 2))
    print("\n")

    print("Delivery Truck 1, Second Trip Ending Stats: ")
    print("Left the hub at:", truck1_stats[0])
    print("Returned to the hub at: ", truck1_trip2_stats[0])
    print("Time on the road: ", round(float(truck1_trip2_stats[1]), 2), " hours")
    print("Miles traveled:", round(float(truck1_trip2_stats[2]), 2))
    print("\n")

    print("Delivery Truck 2 Ending Stats: ")
    print("Left the hub at:", ten_twenty)
    print("Returned to the hub at:", truck2_stats[0])
    print("Time on the road:", round(float(truck2_stats[1]), 2), " hours")
    print("Miles traveled:", round(float(truck2_stats[2]), 2))
    print("\n")

    print("Total Miles Driven:", round(float(total_miles), 2), " miles")
    print("Total Time on the road: (HH:MM)", total_time)

    # clear statuses
    pkg_statuses = list()

    # create usr interface


usr_in = ""
while usr_in != 'end':
    print("\n")
    print("Student Name: Blake Higdon")
    print("Student ID: 011015090")
    print("Class: C950")
    print('\n')
    print("\t What should I do?")
    print("\n")
    print("\t begin - Begin Simulation & Stat Lookup")
    print("\t end - Terminate the simulation")
    # sys.stdout.flush()
    pkg_statuses.clear()
    usr_in = input(">>")

    if usr_in.lower() == 'begin':
        print("Gearing up for delivery!")
        sleep(0.5)

        for i in range(0, 102, 2):
            sleep(0.1)
            print('\r[%s%s]' % ('#' * (i // 2) + '-' * (50 - i // 2), str(i) + '%'), end='')

        print("\n")
        deliver_the_packages(pkg_statuses)
        print("\n")

        while usr_in.lower != "info" or "back":
            print("What should I do now, human overlord?")
            print("\t back - back to main menu")
            print("\t info - look up packages and all related information")
            print("\n")
            usr_in = input(">>")

            usr_time = None
            if usr_in == "info":
                while usr_time is None:
                    while True:
                        print("For what time should I find package information?")
                        print("\n")
                        usr_time = input("Time(enter in HH:MM format): ")
                        user_time_input = usr_time
                        time_struct = time.strptime(user_time_input, "%H:%M")
                        user_time = year_month_day.replace(hour=time_struct.tm_hour, minute=time_struct.tm_min)
                        try:
                            if time.strptime(usr_time, "%H:%M"):
                                usr_time = time.strptime(usr_time, "%H:%M")

                                break

                        except ValueError:
                            print("Invalid time. Try again using the format: hh:mm")
                            continue

                    print("\n")
                    print("How should I sort packages?")
                    print(f'\t all - Show ALL package statuses as of {time.strftime("%H:%M", usr_time)}')
                    print("\t id - Lookup by package ID")
                    print("\t address - Lookup by package ADDRESS")
                    print("\t deadline - Lookup by package DEADLINE")
                    print("\t city - Lookup by package CITY")
                    print("\t zip - Lookup by package ZIP")
                    print("\t weight - Lookup by package WEIGHT")
                    print("\t status - Lookup by package STATUS")
                    print("\n")
                    sort_by = input(">>")

                    while sort_by != "all" and sort_by != "id" and sort_by != "address" and sort_by != "deadline" and sort_by != "city" and sort_by != "zip" and sort_by != "weight" and sort_by != "status":
                        print("Nice Try! Invalid input. Try again using the format:")
                        print(f'\t all - Show ALL package statuses as of {time.strftime("%H:%M", usr_time)}')
                        print("\t id - Lookup by package ID")
                        print("\t address - Lookup by package ADDRESS")
                        print("\t deadline - Lookup by package DEADLINE")
                        print("\t city - Lookup by package CITY")
                        print("\t zip - Lookup by package ZIP")
                        print("\t weight - Lookup by package WEIGHT")
                        print("\t status - Lookup by package STATUS")
                        print("\n")
                        sort_by = input(">>")

                    if sort_by == "all":
                        sorted_packages = dict()

                        user_time_hr_min = time.strftime("%H:%M", usr_time)
                        user_time_int = int(user_time_hr_min.replace(":", ""))
                        package_9_update_time = 1020  # 10:20 AM

                        package_9 = handler.package_id_lookup(str(9))
                        if user_time_int < package_9_update_time:
                            package_9_data = {
                                'new_delivery_address': '300 State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84103',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)
                        else:
                            package_9_data = {
                                'new_delivery_address': '410 S. State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84111',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)

                        for package_id in sorted(pkg_statuses["DELIVERED_TIME"]):

                            if time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                             "%H:%M:%S") <= usr_time:
                                delivered_time = pkg_statuses["DELIVERED_TIME"][package_id]
                                handler.package_id_lookup(str(package_id)).set_status(
                                    'DELIVERED @ (' + delivered_time + ')')
                                sorted_packages[int(package_id)] = handler.package_id_lookup(str(package_id))

                            elif ((time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                                 "%H:%M:%S") > usr_time) and
                                  (time.strptime(pkg_statuses["LEFT_HUB"][package_id],
                                                 "%H:%M:%S") <= usr_time)):
                                handler.package_id_lookup(
                                    str(package_id)).set_status('EN ROUTE')
                                sorted_packages[int(package_id)] = handler.package_id_lookup(str(package_id))

                            elif (time.strptime(pkg_statuses["LEFT_HUB"][package_id],
                                                "%H:%M:%S") > usr_time):

                                handler.package_id_lookup(

                                    str(package_id)).set_status('AT THE HUB')

                                sorted_packages[int(package_id)] = handler.package_id_lookup(

                                    str(package_id))

                        print("\n")
                        print(f"Loading in all statuses as of   {time.strftime("%H:%M:%S", usr_time)}")
                        sleep(0.5)
                        for i in range(0, 102, 2):
                            sleep(0.1)
                            print('\r[%s%s]' % ('#' * (i // 2) + '-' * (50 - i // 2), str(i) + '%'), end='')
                        print('\n')

                        # print out all packages to user
                        for key in sorted_packages:
                            if "DELIVERED" in str(sorted_packages[key]):
                                print(str(sorted_packages[key]))
                            elif "EN ROUTE" in str(sorted_packages[key]):
                                print(str(sorted_packages[key]))
                            elif "AT THE HUB" in str(sorted_packages[key]):
                                print(str(sorted_packages[key]))
                        # return user back to main menu after printing is completed
                        print('\n')
                        usr_in = 'back'

                    elif sort_by == 'id':
                        print("\n")
                        print("Enter the ID you would like to sort by")
                        usr_id = input(">>")
                        print('\n')
                        sorted_packages = dict()

                        user_time_hr_min = time.strftime("%H:%M", usr_time)
                        user_time_int = int(user_time_hr_min.replace(":", ""))
                        package_9_update_time = 1020  # 10:20 AM

                        package_9 = handler.package_id_lookup(str(9))
                        if user_time_int < package_9_update_time:
                            package_9_data = {
                                'new_delivery_address': '300 State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84103',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)
                        else:
                            package_9_data = {
                                'new_delivery_address': '410 S. State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84111',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)

                        for package_id in sorted(pkg_statuses["DELIVERED_TIME"]):
                            if (time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                              "%H:%M:%S") <= usr_time):
                                delivered_time = pkg_statuses["DELIVERED_TIME"][package_id]
                                handler.package_id_lookup(str(package_id)).set_status(
                                    'DELIVERED @ (' + delivered_time + ')')

                            elif ((time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                                 "%H:%M:%S") > usr_time) and (
                                          time.strptime(pkg_statuses["LEFT_HUB"][package_id],
                                                        "%H:%M:%S") <= usr_time)):
                                handler.package_id_lookup(str(package_id)).set_status('EN ROUTE')

                            elif time.strptime(pkg_statuses["LEFT_HUB"][package_id], "%H:%M:%S") > usr_time:
                                handler.package_id_lookup(str(package_id)).set_status('AT THE HUB')

                            if str(package_id) == usr_id:
                                sorted_packages[int(package_id)] = handler.package_id_lookup(str(package_id))

                        print('\n')
                        print(f'Loading data for package ID: {usr_id} at time '
                              f'(' + time.strftime("%H:%M", usr_time) + ')')
                        sleep(0.5)
                        for i in range(0, 102, 2):
                            sleep(0.1)
                            print('\r[%s%s]' % ('#' * (i // 2) + '-' * (50 - i // 2), str(i) + '%'), end='')
                        print('\n')

                        if 'DELIVERED' in str(sorted_packages[int(usr_id)]):
                            print(sorted_packages[int(usr_id)])
                        elif 'EN ROUTE' in str(sorted_packages[int(usr_id)]):
                            print(sorted_packages[int(usr_id)])
                        elif 'AT THE HUB' in str(sorted_packages[int(usr_id)]):
                            print(sorted_packages[int(usr_id)])
                        print('\n')
                        usr_in = 'back'

                    elif sort_by == 'deadline':
                        print('Enter the deadline you would like to sort by')
                        print('\n')
                        usr_deadline = input('Target Deadline: ')
                        print('\n')
                        sorted_packages = dict()

                        for package_id in sorted(pkg_statuses["DELIVERED_TIME"]):
                            if (time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                              "%H:%M:%S") <= usr_time):
                                delivered_time = pkg_statuses["DELIVERED_TIME"][package_id]
                                handler.package_id_lookup(str(package_id)).set_status(
                                    'DELIVERED @ (' + delivered_time + ')')

                            elif ((time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                                 "%H:%M:%S") > usr_time) and (
                                          time.strptime(pkg_statuses["LEFT_HUB"][package_id], "%H:%M:%S")
                                          <= usr_time)):
                                handler.package_id_lookup(str(package_id)).set_status('EN ROUTE')

                            elif (time.strptime(pkg_statuses["LEFT_HUB"][package_id], "%H:%M:%S")
                                  > usr_time):
                                handler.package_id_lookup(str(package_id)).set_status('AT THE HUB')

                        print('\n')
                        print(f'Given the deadline of {usr_deadline} all package(s) '
                              f'that meet the deadline criteria at  ' + time.strftime("%H:%M", usr_time) + ' are:')
                        sleep(0.5)
                        for i in range(0, 102, 2):
                            sleep(0.1)
                            print('\r[%s%s]' % ('#' * (i // 2) + '-' * (50 - i // 2), str(i) + '%'), end='')
                        print('\n')
                        sorted_packages = handler.package_deadline_lookup(usr_deadline)
                        for deadline in sorted_packages:
                            if 'DELIVERED' in str(deadline):
                                print(str(deadline))
                            elif 'EN ROUTE' in str(deadline):
                                print(str(deadline))
                            elif 'AT THE HUB' in str(deadline):
                                print(str(deadline))
                        print('\n')
                        usr_in = 'back'

                    elif sort_by == 'address':
                        print('\n')
                        print('What address would you like to sort by?')
                        print('\n')
                        usr_address = input('Target Address: ')
                        sorted_packages = dict()

                        user_time_hr_min = time.strftime("%H:%M", usr_time)
                        user_time_int = int(user_time_hr_min.replace(":", ""))
                        package_9_update_time = 1020  # 10:20 AM

                        package_9 = handler.package_id_lookup(str(9))
                        if user_time_int < package_9_update_time:
                            package_9_data = {
                                'new_delivery_address': '300 State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84103',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)
                        else:
                            package_9_data = {
                                'new_delivery_address': '410 S. State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84111',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)

                        for package_id in sorted(pkg_statuses["DELIVERED_TIME"]):
                            if (time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                              "%H:%M:%S") <= usr_time):
                                delivered_time = pkg_statuses["DELIVERED_TIME"][package_id]
                                handler.package_id_lookup(str(package_id)).set_status(
                                    'DELIVERED (' + delivered_time + ')')

                            elif ((time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                                 "%H:%M:%S") > usr_time) and (
                                          time.strptime(pkg_statuses["LEFT_HUB"][package_id],
                                                        "%H:%M:%S") <= usr_time)):
                                handler.package_id_lookup(
                                    str(package_id)).set_status('EN ROUTE')

                            elif (time.strptime(pkg_statuses["LEFT_HUB"][package_id],
                                                "%H:%M:%S") > usr_time):
                                handler.package_id_lookup(str(package_id)).set_status('AT THE HUB')

                            if str(package_id) == usr_address:
                                sorted_packages[int(package_id)] = handler.package_id_lookup(str(package_id))

                        print(f'Loading packages with the address of {usr_address} at time',
                              time.strftime("%H:%M", usr_time))
                        sleep(0.5)
                        for i in range(0, 102, 2):
                            sleep(0.1)
                            print('\r[%s%s]' % ('#' * (i // 2) + '-' * (50 - i // 2), str(i) + '%'), end='')
                        print('\n')
                        sorted_packages = handler.package_address_lookup(usr_address)
                        for package in sorted_packages:
                            if 'DELIVERED' in str(package):
                                print(str(package))
                            elif 'EN ROUTE' in str(package):
                                print(str(package))
                            elif 'AT THE HUB' in str(package):
                                print(str(package))
                        print('\n')
                        usr_in = 'back'

                    elif sort_by == 'city':
                        print('\n')
                        print('What city would you like to sort by?')
                        usr_city = input('City:')
                        sorted_packages = dict()

                        user_time_hr_min = time.strftime("%H:%M", usr_time)
                        user_time_int = int(user_time_hr_min.replace(":", ""))
                        package_9_update_time = 1020  # 10:20 AM

                        package_9 = handler.package_id_lookup(str(9))
                        if user_time_int < package_9_update_time:
                            package_9_data = {
                                'new_delivery_address': '300 State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84103',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)
                        else:
                            package_9_data = {
                                'new_delivery_address': '410 S. State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84111',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)

                        for package_id in sorted(pkg_statuses["DELIVERED_TIME"]):
                            if (time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                              "%H:%M:%S") <= usr_time):
                                delivered_time = pkg_statuses["DELIVERED_TIME"][package_id]
                                handler.package_id_lookup(str(package_id)).set_status(
                                    'DELIVERED (' + delivered_time + ')')

                            elif ((time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                                 "%H:%M:%S") > usr_time) and (
                                          time.strptime(pkg_statuses["LEFT_HUB"][package_id],
                                                        "%H:%M:%S") <= usr_time)):
                                handler.package_id_lookup(str(package_id)).set_status('EN ROUTE')

                            elif (time.strptime(pkg_statuses["LEFT_HUB"][package_id],
                                                "%H:%M:%S") > usr_time):
                                handler.package_id_lookup(str(package_id)).set_status('AT THE HUB')

                        print('\n')
                        print(f'Loading all packages with the destination {usr_city} at time',
                              time.strftime("%H:%M", usr_time))
                        for i in range(0, 102, 2):
                            sleep(0.1)
                            print('\r[%s%s]' % ('#' * (i // 2) + '-' * (50 - i // 2), str(i) + '%'), end='')
                        print('\n')

                        sorted_packages = handler.package_city_lookup(usr_city)
                        for package in sorted_packages:
                            if 'DELIVERED' in str(package):
                                print(str(package))
                            elif 'EN ROUTE' in str(package):
                                print(str(package))
                            elif 'AT THE HUB' in str(package):
                                print(str(package))
                        usr_in = 'back'

                    elif sort_by == 'zip':
                        print('\n')
                        print('What zip code would you like to sort by?')
                        print('\n')
                        usr_zip = input('Enter a 5 digit zip code using only digits: ')
                        print('\n')
                        sorted_packages = dict()

                        user_time_hr_min = time.strftime("%H:%M", usr_time)
                        user_time_int = int(user_time_hr_min.replace(":", ""))
                        package_9_update_time = 1020  # 10:20 AM

                        package_9 = handler.package_id_lookup(str(9))
                        if user_time_int < package_9_update_time:
                            package_9_data = {
                                'new_delivery_address': '300 State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84103',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)
                        else:
                            package_9_data = {
                                'new_delivery_address': '410 S. State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84111',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)

                        for package_id in sorted(pkg_statuses["DELIVERED_TIME"]):
                            if (time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                              "%H:%M:%S") <= usr_time):
                                delivered_time = pkg_statuses["DELIVERED_TIME"][package_id]
                                handler.package_id_lookup(str(package_id)).set_status(
                                    'DELIVERED (' + delivered_time + ')')

                            elif ((time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                                 "%H:%M:%S") > usr_time) and (
                                          time.strptime(pkg_statuses["LEFT_HUB"][package_id],
                                                        "%H:%M:%S") <= usr_time)):
                                handler.package_id_lookup(str(package_id)).set_status('EN ROUTE')

                            elif (time.strptime(pkg_statuses["LEFT_HUB"][package_id],
                                                "%H:%M:%S") > usr_time):
                                handler.package_id_lookup(str(package_id)).set_status('AT THE HUB')
                        print('\n')
                        print(f'Loading all packages with the zip code of {usr_zip} at time',
                              time.strftime("%H:%M", usr_time))

                        for i in range(0, 102, 2):
                            sleep(0.1)

                            print('\r[%s%s]' % ('#' * (i // 2) + '-' * (50 - i // 2), str(i) + '%'), end='')
                        print('\n')
                        sorted_packages = handler.package_zip_lookup(usr_zip)
                        for package in sorted_packages:
                            if 'DELIVERED' in str(package):
                                print(str(package))
                            elif 'EN ROUTE' in str(package):
                                print(str(package))
                            elif 'AT THE HUB' in str(package):
                                print(str(package))
                        usr_in = 'back'

                    elif sort_by == 'weight':
                        print('\n')
                        print('What weight would you like to sort by?')
                        print('\n')
                        usr_weight = input('Enter a weight: ')
                        print('\n')
                        sorted_packages = dict()

                        user_time_hr_min = time.strftime("%H:%M", usr_time)
                        user_time_int = int(user_time_hr_min.replace(":", ""))
                        package_9_update_time = 1020  # 10:20 AM

                        package_9 = handler.package_id_lookup(str(9))
                        if user_time_int < package_9_update_time:
                            package_9_data = {
                                'new_delivery_address': '300 State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84103',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)
                        else:
                            package_9_data = {
                                'new_delivery_address': '410 S. State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84111',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)

                        for package_id in sorted(pkg_statuses["DELIVERED_TIME"]):
                            if (time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                              "%H:%M:%S") <= usr_time):
                                delivered_time = pkg_statuses["DELIVERED_TIME"][package_id]
                                handler.package_id_lookup(str(package_id)).set_status(
                                    'DELIVERED (' + delivered_time + ')')

                            elif ((time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                                 "%H:%M:%S") > usr_time) and (
                                          time.strptime(pkg_statuses["LEFT_HUB"][package_id],
                                                        "%H:%M:%S") <= usr_time)):
                                handler.package_id_lookup(str(package_id)).set_status('EN ROUTE')

                            elif (time.strptime(pkg_statuses["LEFT_HUB"][package_id],
                                                "%H:%M:%S") > usr_time):
                                handler.package_id_lookup(str(package_id)).set_status('AT THE HUB')
                        print('\n')
                        print(f'Loading all packages that meet the weight criteria of {usr_weight} '
                              f'at time', time.strftime("%H:%M", usr_time))

                        for i in range(0, 102, 2):
                            sleep(0.1)
                            print('\r[%s%s]' % ('#' * (i // 2) + '-' * (50 - i // 2), str(i) + '%'), end='')
                        print('\n')

                        sorted_packages = handler.package_weight_lookup(usr_weight)
                        for package in sorted_packages:
                            if 'DELIVERED' in str(package):
                                print(str(package))
                            elif 'EN ROUTE' in str(package):
                                print(str(package))
                            elif 'AT THE HUB' in str(package):
                                print(str(package))
                        usr_in = 'back'

                    elif sort_by == 'status':
                        print('\n')
                        print('What status would you like to sort by?')
                        print('\n')
                        usr_status = input('Enter the desired status: ')
                        print('\n')
                        sorted_packages = dict()

                        user_time_hr_min = time.strftime("%H:%M", usr_time)
                        user_time_int = int(user_time_hr_min.replace(":", ""))
                        package_9_update_time = 1020  # 10:20 AM

                        package_9 = handler.package_id_lookup(str(9))
                        if user_time_int < package_9_update_time:
                            package_9_data = {
                                'new_delivery_address': '300 State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84103',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)
                        else:
                            package_9_data = {
                                'new_delivery_address': '410 S. State St',
                                'new_address_name': package_9.address_name,
                                'new_city': package_9.delivery_city,
                                'new_zip': '84111',
                                'new_status': package_9.status
                            }
                            package_9.update(**package_9_data)

                        for package_id in sorted(pkg_statuses["DELIVERED_TIME"]):
                            if (time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                              "%H:%M:%S") <= usr_time):
                                delivered_time = pkg_statuses["DELIVERED_TIME"][package_id]
                                handler.package_id_lookup(str(package_id)).set_status(
                                    'DELIVERED @ (' + delivered_time + ')')

                            elif ((time.strptime(pkg_statuses["DELIVERED_TIME"][package_id],
                                                 "%H:%M:%S") > usr_time) and (
                                          time.strptime(pkg_statuses["LEFT_HUB"][package_id],
                                                        "%H:%M:%S") <= usr_time)):
                                handler.package_id_lookup(str(package_id)).set_status('EN ROUTE')

                            elif (time.strptime(pkg_statuses["LEFT_HUB"][package_id],
                                                "%H:%M:%S") > usr_time):
                                handler.package_id_lookup(str(package_id)).set_status('AT THE HUB')
                        print('\n')
                        print(f'Loading all packages that meet the  criteria of {usr_status} '
                              f'at time', time.strftime("%H:%M", usr_time))

                        for i in range(0, 102, 2):
                            sleep(0.1)
                            print('\r[%s%s]' % ('#' * (i // 2) + '-' * (50 - i // 2), str(i) + '%'), end='')
                        print('\n')
                        sorted_packages = handler.package_status_lookup(usr_status)
                        for package in sorted_packages:
                            if 'DELIVERED' in str(package):
                                print(str(package))
                            elif 'EN ROUTE' in str(package):
                                print(str(package))
                            elif 'AT THE HUB' in str(package):
                                print(str(package))
                        usr_in = 'back'
