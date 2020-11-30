__all__ = ['Car']
import time
from ParkingManagementSystem import *


class Car(ParkingManagementSystem):

    def __init__(self):
        self.exit_time = None
        self.cost = None
        # Initial id
        self.id = 1
        try:
            with open("count_id.txt", "r") as file:
                self.id = int(file.read())
        except Exception as result:
            pass
        print(self.id)

    def get_parking_info(self):
        ParkingManagementSystem.__init__(self)
        car_type = input("Please enter the car type(car or truck)：")
        # Determine whether the parking space is full, if it is full, prompt the customer to go to another parking lot,
        # if not, allocate a parking space to the customer
        if car_type == "car":
            if len(self.car_stall) >= 100:
                print("The car parking spaces are full, please go to other parking lots.")
                return
            else:
                price = 10
                for i in range(100):
                    if i + 1 not in self.car_stall:
                        p_number = i + 1
                        self.car_stall.append(p_number)
                        print(self.car_stall)
                        break
        elif car_type == "truck":
            if len(self.truck_stall) >= 50:
                print("The truck parking space is full, please go to another parking lot.")
                return
            else:
                price = 20
                for i in range(100, 150):
                    if i + 1 not in self.truck_stall:
                        p_number = i + 1
                        self.truck_stall.append(p_number)
                        print(self.truck_stall)
                        break
        else:
            print("This parking lot does not have a parking space suitable for this model, please re-enter!")
            return
        car_number = input("Please enter the license plate number(i.g：CA12345)：")
        handler = input("Please enter the name of the handler：")
        entrance_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        date = time.strftime("%Y-%m-%d", time.localtime())
        self.id += 1
        parking_info = {
            "id": self.id,
            "car_type": car_type,
            "car_number": car_number,
            "handler": handler,
            "p_number": p_number,
            "date": date,
            "entrance_time": entrance_time,
            "exit_time": self.exit_time,
            "price": price,
            "cost": self.cost
        }
        print(parking_info)
        return parking_info

    def save_id_to_file(self):
        with open("count_id.txt", "w") as file:
            file.write(str(self.id))