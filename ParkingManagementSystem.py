__all__ = ['ParkingManagementSystem']
import time


class ParkingManagementSystem(object):

    def __init__(self):
        # Parking space number storage list
        self.car_stall = []
        self.truck_stall = []
        # All parking information storage list
        self.total_info = []

        # Read parking lot data
        try:
            with open("parking_data.txt", "r") as file:
                for line in file.readlines():
                    try:
                        info_dict = eval(line)
                        self.total_info.append(info_dict)
                        if info_dict["car_type"] == "car":
                            self.car_stall.append(info_dict["p_number"])
                        else:
                            self.truck_stall.append(info_dict["p_number"])
                    except Exception as result:
                        continue
        except Exception as result:
            print("The parking information data file does not exist！")


    def parking(self, parking_info):
        """Parking: incoming parking information, adding vehicle information to empty parking spaces,
         and updating data files"""
        # Determine whether the incoming parking information is: None
        if parking_info is None:
            return
        else:
            # Pass in parking information and save new parking information to the list
            self.total_info.append(parking_info)
            #print(self.total_info)
            # Update the data to the file
            self.save_to_file()

    def show_all_information(self):
        """Output all parking information, sorted by parking space usage, and sorted in ascending order by number
        in the same category"""
        self.__init__()
        # Sort the number of parking spaces for cars of car type
        self.car_stall.sort()
        # print(self.car_stall)
        print("")
        print("car_type  p_number  car_number  handler   price   entrance_time")
        # Display parking information in order of parking space number
        for i in self.car_stall:
            for info_dict in self.total_info:
                if info_dict['p_number'] == i:
                    print("  %s       %s        %s     %s       %s     %s" %
                          (info_dict["car_type"], info_dict["p_number"], info_dict["car_number"],
                           info_dict["handler"], info_dict["price"], info_dict["entrance_time"]))
        print("")
        # Sort the number of parking spaces for trucks
        self.truck_stall.sort()
        # print(self.truck_stall)
        print("car_type  p_number  car_number  handler   price   entrance_time")
        # Display parking information in order of parking space number
        for i in self.truck_stall:
            for info_dict in self.total_info:
                if info_dict['p_number'] == i:
                    # print(info_dict)
                    print("  %s     %s      %s     %s       %s     %s" %
                          (info_dict["car_type"], info_dict["p_number"], info_dict["car_number"],
                           info_dict["handler"], info_dict["price"], info_dict["entrance_time"]))

    def query_by_car_number(self):
        """Search parking information by plate number"""
        # Receive license plate number
        car_number = input("Please enter the license plate number(i.g：CA12345)：")
        # Save query results
        query_results = []
        print("car_type  p_number  car_number  handler   price   entrance_time")
        # Match the parking information that meets the conditions and add it to the query result list
        for info_dict in self.total_info:
            if info_dict["car_number"] == car_number:
                self.print_func(info_dict, query_results)
        # Determine whether the results that meet the conditions are found
        if len(query_results) > 0:
            return query_results
        else:
            print("No relevant parking information found！")
            return False

    def query_by_car_type(self):
        """Find parking information by vehicle type"""
        car_type = input("Please enter the car type(car or truck)：")
        query_results = []
        print("car_type  p_number  car_number  handler   price   entrance_time")
        for info_dict in self.total_info:
            if info_dict["car_type"] == car_type:
                self.print_func(info_dict, query_results)
        if len(query_results) > 0:
            return query_results
        else:
            print("No relevant parking information found！")
            return False

    def query_by_date(self):
        date = input("Please enter the query date（i.g：2020-06-06）：")
        query_results = []
        print("car_type  p_number  car_number  handler   price   entrance_time")
        for info_dict in self.total_info:
            if info_dict["date"] == date:
                self.print_func(info_dict, query_results)
        if len(query_results) > 0:
            return query_results
        else:
            print("No relevant parking information found！")
            return False

    def query_by_handler(self):
        handler = input("Please enter the name of the handler：")
        query_results = []
        print("car_type  p_number  car_number  handler   price   entrance_time")
        for info_dict in self.total_info:
            if info_dict["handler"] == handler:
                self.print_func(info_dict, query_results)
        if len(query_results) > 0:
            return query_results
        else:
            print("No relevant parking information found！")
            return False

    def query_history_results(self):
        print("id  car_type  p_number  car_number   handler   price    cost     entrance_time            exit_time")
        try:
            with open("history_data.txt", "r") as file:
                for line in file.readlines():
                    try:
                        info_dict = eval(line)
                        if info_dict["car_type"] == "car":
                            print("%s   %s        %s        %s     %s       %s      %s    %s       %s" %
                                  (info_dict["id"], info_dict["car_type"], info_dict["p_number"], info_dict["car_number"],
                                   info_dict["handler"], info_dict["price"], info_dict["cost"],
                                   info_dict["entrance_time"], info_dict["exit_time"]))
                        else:
                            print("%s  %s      %s       %s     %s       %s      %s    %s       %s" %
                                  (info_dict["id"], info_dict["car_type"], info_dict["p_number"],
                                   info_dict["car_number"],
                                   info_dict["handler"], info_dict["price"], info_dict["cost"],
                                   info_dict["entrance_time"], info_dict["exit_time"]))
                    except Exception as result:
                        continue
        except Exception as result:
            print("No history data found！")

    def driving_out(self):
        exit_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        car_number = input("Please enter the vehicle license plate number：")
        for info_dict in self.total_info:
            if info_dict["car_number"] == car_number:
                info_dict["exit_time"] = exit_time
                cost = self.charging(info_dict)
                info_dict["cost"] = cost
                if info_dict["car_type"] == "car":
                    self.car_stall.remove(info_dict["p_number"])
                elif info_dict["car_type"] == "truck":
                    self.truck_stall.remove(info_dict["p_number"])
                self.total_info.remove(info_dict)
                self.save_to_file()
                self.save_history_to_file(info_dict)
                print("The vehicle leave successfully！")
                break
        else:
            print("Did not find a vehicle that meets the requirements, please confirm and enter！")

    def charging(self, info_dict):
        """Billing: incoming parking information, billed by the hour"""
        exit_time = time.mktime(time.strptime(info_dict["exit_time"], "%Y-%m-%d %H:%M:%S"))
        entrance_time = time.mktime(time.strptime(info_dict["entrance_time"], "%Y-%m-%d %H:%M:%S"))
        # Calculate the parking time and convert the unit to hours
        parking_time = (exit_time - entrance_time)/3600
        # Calculate the consumption amount
        cost = round(info_dict["price"] * parking_time, 0)
        print("Parking time is：%.2f hours， The parking fee is：%d dollars" % (parking_time, cost))
        return cost

    def save_to_file(self):
        with open("parking_data.txt", "w") as file:
            for info_dict in self.total_info:
                file.write(str(info_dict))
                file.write("\n")

    def save_history_to_file(self, info_dict):
        with open("history_data.txt", "a") as file:
            file.write(str(info_dict))
            file.write("\n")

    def save_query_results_to_file(self, query_results):
        file_name = input("Please enter the file name to save the data(i.g：xxx.txt )：")
        with open(file_name, "a") as file:
            file.write(str(query_results))
            file.write("\n")
        print("The query result is saved successfully, and the file name is：%s" % file_name)

    def print_func(self, info_dict, query_results):
        if info_dict["car_type"] == "car":
            # print(info_dict)
            print("  %s       %s        %s     %s       %s     %s" %
                  (info_dict["car_type"], info_dict["p_number"], info_dict["car_number"],
                   info_dict["handler"], info_dict["price"], info_dict["entrance_time"]))
            query_results.append(info_dict)
        elif info_dict["car_type"] == "truck":
            print("  %s     %s      %s     %s       %s     %s" %
                  (info_dict["car_type"], info_dict["p_number"], info_dict["car_number"],
                   info_dict["handler"], info_dict["price"], info_dict["entrance_time"]))
            query_results.append(info_dict)