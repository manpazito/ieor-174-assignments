import numpy as np

### Combined Logic from Discussion 5 and Assignment 1 Problem 3 ###
class FoodTruck:
    def __init__(self, arrival_rate_per_min, service_mean_seconds, t0, t1, rng=None):
        self.arrival_rate = arrival_rate_per_min          # λ [per minute]
        self.service_mean_min = service_mean_seconds/60.0 # E[S] in minutes
        self.t0 = t0
        self.t1 = t1
        self.rng = np.random.default_rng(rng)

    def simulate_day(self, BALKING=False, BALKING_THRESHOLD=5):
        # 1) Generate arrivals and service times (unchanged)
        arrival_ls = []
        serve_ls = []
        t = self.t0
        while True:
            t += self.rng.exponential(1 / self.arrival_rate)
            s = self.rng.exponential(self.service_mean_min)
            if t > self.t1:
                break
            arrival_ls.append(t)
            serve_ls.append(s)

        n_arrivals = len(arrival_ls)

        # 2) Prepare outputs
        waiting_ls = []        # waiting times (minutes)
        departure_times = []   # departure times (minutes)
        balked_flags = []      # True if the customer balked

        # 3) Internal state for FCFS service
        last_departure = 0.0            # the server's completion time of the last SERVED customer
        served_departures = []          # departure times of served customers only (monotone nondecreasing)
        head = 0                        # index of first still-in-system served customer

        for i in range(n_arrivals):
            a_i = arrival_ls[i]
            s_i = serve_ls[i]

            # Remove all served customers who have already departed by arrival a_i
            while head < len(served_departures) and served_departures[head] <= a_i:
                head += 1
            in_system = len(served_departures) - head  # number still in system at time a_i

            # Balking decision: if queue > threshold (including the one being served)
            if BALKING and (in_system > BALKING_THRESHOLD):
                # Customer leaves immediately; does NOT consume service or move the server clock
                balked_flags.append(True)
                waiting_ls.append(0.0)
                departure_times.append(np.nan)
                # keep service time for record-keeping (do not use it)
                continue

            # Otherwise, they stay and get served (FCFS)
            start_service = max(a_i, last_departure)
            d_i = start_service + s_i
            w_i = start_service - a_i

            last_departure = d_i
            served_departures.append(d_i)

            balked_flags.append(False)
            waiting_ls.append(round(w_i, 3))
            departure_times.append(round(d_i, 5))

        return (np.array(arrival_ls),
                np.array(waiting_ls),
                np.array(departure_times),
                np.array(balked_flags, dtype=bool))
    
def format_time_from_minutes(t):
    m = int(t)
    s = int((t - m) * 60)
    return m, s
    