import csv
from datetime import datetime
from models import RideRequest, Cab
from queue_manager import QueueManager
from cab_manager import CabManager
from storage import save_data, load_data
# Load cabs from the CSV file when no saved cabs exist
def load_cabs_from_csv(filename="cabs.csv"):
    cabs = []
    try:
        with open(filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cab = Cab(
                    driver=row["driver"],
                    seats=int(row["seats"]),
                    destination=row["destination"],
                    time_slot=row["time_slot"]
                )
                cabs.append(cab)
    except FileNotFoundError:
        print("Warning: cabs.csv was not found.")
    except (KeyError, ValueError):
        print("Error: Please check the columns and values in cabs.csv.")
    return cabs
# Display all waiting students
def view_waiting_students(queue_manager):
    queues = queue_manager.get_all_queues()
    if not queues:
        print("\nNo students are waiting.")
        return
    print("\n--- Waiting Students ---")
    for key, queue in queues.items():
        destination, time_slot = key
        print(f"\nDestination: {destination}")
        print(f"Time slot: {time_slot}")
        sorted_requests = queue_manager.get_sorted_requests(
            destination,
            time_slot
        )
        for position, item in enumerate(sorted_requests, start=1):
            request = item[2]
            print(
                f"{position}. {request.name} "
                f"(Year {request.year}, "
                f"Request #{request.request_order})"
            )
# Display all cabs
def view_cabs(cabs):
    if not cabs:
        print("\nNo cabs are available.")
        return
    print("\n--- Cab Details ---")
    for index, cab in enumerate(cabs, start=1):
        status = "Departed" if cab.has_left else "Available"
        print(f"\nCab {index}")
        print(f"Driver: {cab.driver}")
        print(f"Destination: {cab.destination}")
        print(f"Time slot: {cab.time_slot}")
        print(f"Seats: {cab.seats}")
        print(f"Seats occupied: {cab.seats_taken}")
        print(f"Seats free: {cab.seats_free}")
        print(f"Status: {status}")
        if cab.passengers:
            print("Passengers:")
            for passenger in cab.passengers:
                print(f"- {passenger.name}")
# Add a new student ride request
def add_ride_request(queue_manager, next_request_order):
    print("\n--- Register for a Ride ---")
    name = input("Enter student name: ").strip()
    destination = input("Enter destination: ").strip()
    time_slot = input("Enter time slot (Morning/Evening): ").strip()
    if not name or not destination or not time_slot:
        print("Please enter all the required details.")
        return next_request_order
    try:
        year = int(input("Enter academic year: "))
        if year < 1:
            print("Academic year must be a positive number.")
            return next_request_order
    except ValueError:
        print("Please enter a valid number for academic year.")
        return next_request_order
    request = RideRequest(
        name=name,
        destination=destination,
        time_slot=time_slot,
        year=year,
        request_order=next_request_order,
        submitted_at=datetime.now().isoformat(timespec="seconds")
    )
    queue_manager.add_request(request)
    print(f"\nRide request registered for {name}!")
    print(f"Your request number is {next_request_order}.")
    return next_request_order + 1
# Preview a possible cab match
def preview_match(cab_manager, destination, time_slot):
    result = cab_manager.find_match(destination, time_slot)
    if result is None:
        print("\nNo matching cab or waiting students found.")
        return
    cab, selected_students = result
    print("\n--- Matching Preview ---")
    print(f"Driver: {cab.driver}")
    print(f"Destination: {cab.destination}")
    print(f"Available seats: {cab.seats_free}")
    print("\nSelected students:")
    for student in selected_students:
        print(f"- {student.name} (Year {student.year})")
    print("\nThis is only a preview. No students have been removed from the queue.")
# Main application
def main():
    print("================================")
    print("       CAB POOL MATCHER")
    print("================================")
    # Load previously saved information
    requests, cabs = load_data()
    # If no saved cabs exist, load them from CSV
    if not cabs:
        cabs = load_cabs_from_csv()
# Create the queue manager
    queue_manager = QueueManager()
# Restore waiting student requests
    for request in requests:
        queue_manager.add_request(request)
# Create the cab manager
    cab_manager = CabManager(queue_manager, cabs)
# Find the next request number
    all_request_numbers = [
        request.request_order for request in requests
    ]
    for cab in cabs:
        for passenger in cab.passengers:
            all_request_numbers.append(passenger.request_order)
    next_request_order = max(all_request_numbers, default=0) + 1
    print("\nWelcome to the Cab Pool Matcher!")
    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Register for a ride")
        print("2. View waiting students")
        print("3. View cabs")
        print("4. Preview a cab match")
        print("5. Dispatch a cab")
        print("6. Mark a cab as departed")
        print("7. Save and exit")
        print("===============================")
        choice = input("Enter your choice (1-7): ").strip()
        if choice == "1":
            next_request_order = add_ride_request(
                queue_manager,
                next_request_order
            )
            save_data(queue_manager, cabs)
        elif choice == "2":
            view_waiting_students(queue_manager)
        elif choice == "3":
            view_cabs(cabs)
        elif choice == "4":
            destination = input("Enter destination: ").strip()
            time_slot = input("Enter time slot: ").strip()

            preview_match(
                cab_manager,
                destination,
                time_slot
            )
        elif choice == "5":
            destination = input("Enter destination: ").strip()
            time_slot = input("Enter time slot: ").strip()
            cab = cab_manager.dispatch_cab(
                destination,
                time_slot
            )
            if cab is None:
                print("\nNo cab could be dispatched.")
            else:
                print(f"\nCab driven by {cab.driver} has been assigned!")
                print("Passengers:")
                for passenger in cab.passengers:
                    print(f"- {passenger.name}")
                save_data(queue_manager, cabs)
        elif choice == "6":
            view_cabs(cabs)
            try:
                cab_number = int(
                    input("\nEnter the cab number to mark as departed: ")
                )
                if cab_number < 1 or cab_number > len(cabs):
                    print("Invalid cab number.")
                else:
                    selected_cab = cabs[cab_number - 1]
                    success = cab_manager.mark_cab_departed(selected_cab)
                    if success:
                        print("Cab marked as departed.")
                        save_data(queue_manager, cabs)
            except ValueError:
                print("Please enter a valid cab number.")
        elif choice == "7":
            save_data(queue_manager, cabs)
            print("\nYour data has been saved.")
            print("Thank you for using Cab Pool Matcher!")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 7.")
if __name__ == "__main__":
    main()
