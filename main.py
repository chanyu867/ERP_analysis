import numpy as np
import pandas as pd
import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calc_mean_erp(trial_points, ecog_data):
    # ---- load trial_points (handle header or no-header) ----
    trials = pd.read_csv(trial_points)
    trials[['starting_point', 'peak_point', 'finger']] = trials[['starting_point', 'peak_point', 'finger']].astype(int)
    logger.info(f"[debug] - Trial points columns: {trials.columns.tolist()}") #['starting_point', 'peak_point', 'finger']

    # ---- load ecog ----
    ecog = pd.read_csv(ecog_data, header=None).iloc[:, 0].to_numpy(dtype=float)
    start_points = trials["starting_point"].to_numpy() #(632,) -> the same number of data as the trials
    finger_nums = trials["finger"].to_numpy() #(632,) -> each trial has each finger ID, and the data is already sorted.
    logger.info(f"[debug] - each data shapes: {start_points.shape}, {finger_nums.shape}, {ecog.shape}") #(632,) (632,) (465840,)

    # ---- calculate mean ERP for each finger ----
    pre=200
    post=1000
    fingers_erp_mean = np.zeros((5, (pre + 1 + post)), dtype=float)
    for finger in range(1, 6): #process for each finger (1 to 5)
        finger_starts = start_points[finger_nums == finger]

        epochs = []
        for s in finger_starts:
            a, b = s - pre, s + post
            if a < 0 or b >= len(ecog):
                continue
            epochs.append(ecog[a:b + 1]) #collect epochs for the current finger

        if len(epochs) > 0: #once all the epochs for current finger are collected, calculate the mean ERP
            fingers_erp_mean[finger - 1] = np.vstack(epochs).mean(axis=0)

    # plot
    t = np.arange(-pre, post + 1)
    plt.figure(figsize=(10, 6))
    for finger in range(1, 6):
        plt.plot(t, fingers_erp_mean[finger - 1], label=f"Finger {finger}")
    plt.axvline(0, linestyle="--")
    plt.xlabel("Time (ms) relative to movement start")
    plt.ylabel("ECOG signal")
    plt.title("Mean ERP aligned to movement start")
    plt.legend()
    plt.tight_layout()
    plt.show()

    return fingers_erp_mean


if __name__ == "__main__":
    trial_points_file = "source/events_file_ordered.csv"
    ecog_data_file = "source/brain_data_channel_one.csv"

    fingers_erp_mean = calc_mean_erp(trial_points_file, ecog_data_file)
    logger.info(f"fingers_erp_mean shape: {fingers_erp_mean.shape}")  # should be (5, 1201)
