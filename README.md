## ERP Analysis (ECoG Finger Movement)

Compute and plot mean event-related potentials (ERPs) from an ECoG time series, aligned to finger movement onset, and return a 5×1201 matrix (finger 1–5).

## Brief Instruction

Loads:
- trial_points.csv: 3 columns [starting_point, peak_point, finger_number] (imported as int)
- ecog_data.csv: 1 column ECoG signal (float)

Extracts an ERP window for each trial: 200 samples before, start sample, 1000 samples after → 1201 points
- Averages ERPs per finger (1–5)
- Plots the mean ERP curve for each finger
- Returns fingers_erp_mean with shape (5, 1201) (row 0 = finger 1 … row 4 = finger 5)

## Usage
Put your CSVs next to main.py (or edit filenames in __main__)
```python
python main.py
```

## Example outputs
<img width="1000" height="600" alt="finger_ERPs" src="https://github.com/user-attachments/assets/5b962851-2d7f-4689-a81b-1f746a3d936a" />



