from typing import List


class Solution:
    def carFleet(
        self,
        target: int,
        position: List[int],
        speed: List[int]
    ) -> int:
        """
        Return the number of car fleets that reach the destination.

        A car joins the fleet ahead when its independent arrival time is
        less than or equal to that fleet's arrival time.
        """

        # Pair each car's position with its corresponding speed.
        cars: List[tuple[int, int]] = list(zip(position, speed))

        # Process cars from closest to the target to farthest away.
        cars.sort(reverse=True)

        # Each value represents the arrival time of one distinct fleet.
        fleet_times: List[float] = []

        for car_position, car_speed in cars:
            distance_remaining: int = target - car_position
            arrival_time: float = distance_remaining / car_speed

            # A later arrival time means this car cannot catch the fleet ahead,
            # so it forms a new fleet.
            if not fleet_times or arrival_time > fleet_times[-1]:
                fleet_times.append(arrival_time)

            # Otherwise, arrival_time <= fleet_times[-1].
            # The current car catches the fleet ahead and merges into it.

        return len(fleet_times)