import json
from models import RideRequest, Cab
def save_data(queue_manager, cabs, filename="data.json"):
    data = {
        "requests": [],
        "cabs": []
    }
    # Save all waiting student requests
    for queue in queue_manager.get_all_queues().values():
        for item in queue:
            request = item[2]
            data["requests"].append({
                "name": request.name,
                "destination": request.destination,
                "time_slot": request.time_slot,
                "year": request.year,
                "request_order": request.request_order,
                "submitted_at": request.submitted_at
            })
    # Save all cab information
    for cab in cabs:
        passengers_data = []
        for passenger in cab.passengers:
            passengers_data.append({
                "name": passenger.name,
                "destination": passenger.destination,
                "time_slot": passenger.time_slot,
                "year": passenger.year,
                "request_order": passenger.request_order,
                "submitted_at": passenger.submitted_at
            })
        data["cabs"].append({
            "driver": cab.driver,
            "seats": cab.seats,
            "destination": cab.destination,
            "time_slot": cab.time_slot,
            "has_left": cab.has_left,
            "passengers": passengers_data
        })
    # Write the information into a JSON file
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
def load_data(filename="data.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return [], []
    # Re-create student request objects
    requests = []
    for item in data["requests"]:
        request = RideRequest(
            name=item["name"],
            destination=item["destination"],
            time_slot=item["time_slot"],
            year=item["year"],
            request_order=item["request_order"],
            submitted_at=item.get("submitted_at", "")
        )
        requests.append(request)
    # Re-create cab objects
    cabs = []
    for item in data["cabs"]:
        cab = Cab(
            driver=item["driver"],
            seats=item["seats"],
            destination=item["destination"],
            time_slot=item["time_slot"],
            has_left=item["has_left"]
        )
        for passenger_data in item["passengers"]:
            passenger = RideRequest(
                name=passenger_data["name"],
                destination=passenger_data["destination"],
                time_slot=passenger_data["time_slot"],
                year=passenger_data["year"],
                request_order=passenger_data["request_order"],
                submitted_at=passenger_data.get("submitted_at", "")
            )
            cab.passengers.append(passenger)
        cabs.append(cab)
    return requests, cabs
