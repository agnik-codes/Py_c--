import heapq
class QueueManager:
    def __init__(self):
        self.queues = {}
    def add_request(self, request):
        key = (request.destination, request.time_slot)
        if key not in self.queues:
            self.queues[key] = []
        priority_item = (
            -request.year,
            request.request_order,
            request
        )
        heapq.heappush(self.queues[key], priority_item)
    def get_sorted_requests(self, destination, time_slot):
        key = (destination, time_slot)
        if key not in self.queues:
            return []
        return sorted(
            self.queues[key],
            key=lambda item: (item[0], item[1])
        )
    def remove_requests(self, destination, time_slot, count):
        key = (destination, time_slot)
        if key not in self.queues:
            return []
        removed = []
        for _ in range(min(count, len(self.queues[key]))):
            item = heapq.heappop(self.queues[key])
            removed.append(item[2])
        return removed
    def get_all_queues(self):
        return self.queues