
from queue_manager import QueueManager
class CabManager:
    def __init__(self, queue_manager, cabs):
        self.queue_manager = queue_manager
        self.cabs = cabs
    def find_matching_cab(self, destination, time_slot):
        matching_cabs = []
        for cab in self.cabs:
            if (
                cab.destination == destination
                and cab.time_slot == time_slot
                and not cab.has_left
                and cab.seats_free > 0
            ):
                matching_cabs.append(cab)
        if not matching_cabs:
            return None
        return matching_cabs[0]

    def find_match(self, destination, time_slot):
        cab = self.find_matching_cab(destination, time_slot)
        if cab is None:
            return None
        requests = self.queue_manager.get_sorted_requests(
            destination,
            time_slot
        )
        if not requests:
            return None
        selected_students = []
        for item in requests:
            if len(selected_students) == cab.seats_free:
                break
            selected_students.append(item[2])
        return cab, selected_students
    def dispatch_cab(self, destination, time_slot):
        result = self.find_match(destination, time_slot)
        if result is None:
            return None
        cab, selected_students = result
        passengers = self.queue_manager.remove_requests(
            destination,
            time_slot,
            len(selected_students)
        )
        cab.passengers.extend(passengers)
        return cab
    def mark_cab_departed(self, cab):
        if cab is None:
            return False
        cab.has_left = True
        return True
