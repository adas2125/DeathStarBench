import pandas as pd
import matplotlib.pyplot as plt
import argparse

# add duration and RPS as command line arguments
parser = argparse.ArgumentParser(description="Plot arrivals and attempted requests.")
parser.add_argument("--rps", type=int, default=1000, help="Requests per second (default: 1000)")
parser.add_argument("--duration", type=int, default=20, help="Duration in seconds (default: 20)")
args = parser.parse_args()

RPS = args.rps
DURATION = args.duration
ALL_CONNECTIONS = [1]

plt.figure(figsize=(10, 5))

for c in ALL_CONNECTIONS:
    arrivals_path = f"arrivals.csv"
    attempted_path = f"attempted_requests.csv"

    arrivals = pd.read_csv(arrivals_path)
    attempted = pd.read_csv(attempted_path)

    # ---- Convert timestamps ----
    arrivals["time"] = pd.to_datetime(arrivals["timestamp_rfc3339"]).dt.tz_localize(None)
    attempted["time"] = pd.to_datetime(attempted["timestamp"], unit="us")

    # ---- Remove initial idle period (no arrivals yet) ----
    first_active_idx = arrivals[arrivals["arrivals_since_last"] > 0].index[0]
    start_idx = max(first_active_idx - 1, 0)
    arrivals = arrivals.loc[start_idx:].reset_index(drop=True)

    # remove initial idle period from attempted requests as well
    first_attempted_idx = attempted[attempted["attempted"] > 0].index[0]
    start_attempted_idx = max(first_attempted_idx - 1, 0)
    attempted = attempted.loc[start_attempted_idx:].reset_index(drop=True)

    # ---- Relative time within each dataset ----
    arrivals["t"] = (arrivals["time"] - arrivals["time"].iloc[0]).dt.total_seconds()
    attempted["t"] = (attempted["time"] - attempted["time"].iloc[0]).dt.total_seconds()

    arrivals = arrivals[arrivals["t"] <= DURATION]
    attempted = attempted[attempted["t"] <= DURATION]

    # ---- Relative time within each dataset ----
    arrivals["t"] = (arrivals["time"] - arrivals["time"].iloc[0]).dt.total_seconds()
    attempted["t"] = (attempted["time"] - attempted["time"].iloc[0]).dt.total_seconds()

    # ---- Clip all data to duration ----
    arrivals = arrivals[arrivals["t"] <= DURATION]
    attempted = attempted[attempted["t"] <= DURATION]

    # ---- Plot ----
    plt.plot(arrivals["t"], arrivals["total_arrivals"], label=f"Arrivals c={c}", linewidth=2)
    plt.plot(attempted["t"], attempted["attempted"], label=f"Attempted c={c}", linewidth=2)

# expected line (plotted once, using the ideal schedule for [0, DURATION])
t_expected = pd.Series([0, DURATION], dtype=float)
plt.plot(
    t_expected,
    RPS * t_expected,
    label="Expected Attempted",
    linestyle="--",
    color="green",
    linewidth=1,
)

plt.xlabel("Time (seconds since first arrival)")
plt.ylabel("Requests")
plt.title("Attempted vs Arrivals (varying connections)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()