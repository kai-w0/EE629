from ParkingManagementSystem import *
from Car import *


def main():
    p = ParkingManagementSystem()
    car = Car()
    while True:
        print("")
        print("**************************** Welcome! ***************************")
        print("------------------- 1.All Parking Information ------------------")
        print("---------------- 2.Search for vehicle information --------------")
        print("------------------------ 3.Vehicle Entry -----------------------")
        print("---------------------- 4.Deleted vehicles ----------------------")
        print("---------------------------- 5.Exit ----------------------------")
        try:
            # insert command
            cmd = int(input("Please enter the instruction number："))
            # 1.Browse all information
            if cmd == 1:
                p.show_all_information()
            # 2.Search for vehicle information
            elif cmd == 2:
                while True:
                    print("------ 1.Search by plate number ------")
                    print("------ 2.Search by vehicle type ------")
                    print("------ 3.Search by date of usage -----")
                    print("------ 4.Search by handler -----------")
                    print("------ 5.Search history data ---------")
                    print("------ 6.Back to the previous menu ---")
                    query = int(input("Please enter the instruction number："))
                    # 1.Search by plate number
                    if query == 1:
                        query_results = p.query_by_car_number()
                        if query_results:
                            decide = input("Do you need to save the search results?（yes/no):")
                            if decide == "yes":
                                p.save_query_results_to_file(query_results)
                    # 2.Search by vehicle type
                    elif query == 2:
                        query_results = p.query_by_car_type()
                        if query_results:
                            decide = input("Do you need to save the search results?（yes/no):")
                            if decide == "yes":
                                p.save_query_results_to_file(query_results)
                    # 3.Search by date of usage
                    elif query == 3:
                        query_results = p.query_by_date()
                        if query_results:
                            decide = input("Do you need to save the search results?（yes/no):")
                            if decide == "yes":
                                p.save_query_results_to_file(query_results)
                    # 4.Search by handler
                    elif query == 4:
                        query_results = p.query_by_handler()
                        if query_results:
                            decide = input("Do you need to save the search results?（yes/no):")
                            if decide == "yes":
                                p.save_query_results_to_file(query_results)
                    # 5.Search history data
                    elif query == 5:
                        p.query_history_results()
                    else:
                        break
            # 3.Vehicle Entry
            elif cmd == 3:
                # Receive parking vehicle information
                parking_info = car.get_parking_info()
                p.parking(parking_info)
            # 4.Delete vehicle information
            elif cmd == 4:
                p.driving_out()
            # 5.Exit
            else:
                # Maximum number of parking information id
                car.save_id_to_file()
                print("Thanks for using the parking management system, bye!")
                break
        except Exception as result:
            car.save_id_to_file()
            # Save parking information
            p.save_to_file()
            print("Thanks for using the parking management system, bye!")
            break


if __name__ == "__main__":
    main()