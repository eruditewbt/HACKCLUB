import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.entry_finder = {}
        self.REMOVED = '<removed-task>'
        self.counter = 0

    def update(self, item, priority):
        if item in self.entry_finder:
            # Remove the old entry
            self.remove_item(item)
        count = self.counter
        entry = [priority, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.heap, entry)
        self.counter += 1

    def remove_item(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED

    def removeMin(self):
        while self.heap:
            priority, count, item = heapq.heappop(self.heap)
            if item is not self.REMOVED:
                del self.entry_finder[item]
                return item, priority
        raise KeyError("pop from an empty priority queue")