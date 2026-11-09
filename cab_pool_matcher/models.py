from dataclasses import dataclass, field
@dataclass
class RideRequest:
    name: str
    destination: str
    time_slot: str
    year: int
    request_order: int
    submitted_at: str = ""
    def __str__(self):
        return (
            f"{self.name} (Year {self.year}, "
            f"request #{self.request_order})"
        )

@dataclass
class Cab:
    driver: str
    seats: int
    destination: str
    time_slot: str
    has_left: bool = False
    passengers: list = field(default_factory=list)
    @property
    def seats_taken(self):
        return len(self.passengers)
    @property
    def seats_free(self):
        return self.seats - self.seats_taken