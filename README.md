# Overview and purpose
$\mathbf{Dataset name:}$ CoDiG-dataset
$\mathbf{Primary goal:}$ Train the diffusion model proposed in [Hao et al., 2025](https://arxiv.org/abs/2505.13131) to achieve real-time obstacle avoidance for autonomous racing.

What this dataset is
- A collection of planar racing scenarios defined on a fixed track in the $x$-$y$ plane with randomly generated obstacles placed within track bounds.
- For each scenario, the training trajectory is produced offline by a time-optimal solver (i.e., it solves a minimum-time problem subject to track and obstacle constraints).
- The dataset is intended for conditional generative modeling (e.g., diffusion) where the model learns to sample collision-free, near time-optimal trajectories conditioned on the track/obstacles.

Intended uses
- Train and evaluate diffusion-based planners/controllers for autonomous racing.
- Imitation learning or behavior cloning from time-optimal expert trajectories.
- Data-driven planning research: ablations on obstacle density, starting states, and timing constraints.
  
# Getting the data
Because the dataset is large, we provide a single ZIP via an external host.
After downloading, extract it to:
~~~
CoDiG-dataset/
└─ data/
    <extracted files here>
└─ src/
└─ scripts/
~~~

Direct download
- Latest release (ZIP): https://huggingface.co/datasets/hma2/CoDiG-dataset/resolve/main/codig-dataset_v0.1.0.zip
- Version: v0.1.0
- Estimated size: 19.5G

$\mathbf{macOS / Linux}$
~~~
wget -c "https://huggingface.co/datasets/hma2/CoDiG-dataset/resolve/main/codig-dataset_v0.1.0.zip" -O codig-dataset_v0.1.0.zip
unzip -q codig-dataset_v0.1.0.zip -d CoDiG-dataset/data/
mv CoDiG-dataset/data/codig-dataset_v0.1.0/TOC CoDiG-dataset/data/
rmdir CoDiG-dataset/data/codig-dataset_v0.1.0 
~~~

# File structure and contents
~~~
CoDiG-dataset/
└─ data/
   └─ TOC/ 
       # 11,985 individual files (raw scenario/trajectory data)
~~~

What’s inside `TOC/`
- The dataset resides entirely in the `TOC/` folder, containing 11,985 independent files.
- Files are organized for fast loading; the recommended loading API is shown in the next section: see the section `Quick start`.

Objects returned by the reader (after loading a file)

| Key       | Type / Shape  | Description                    |
| ----------| ------------- | ------------------------------ |
| `roots`   | `list`        | Augmentation lineage from base feasible scenario to the current scenario (files in order).   |
| `track`   | `dict`        | Track-level structure (fixed x–y centerline plus per-scenario info such as curvature, width, obstacles). |
| `flatten_track` | `numpy.ndarray` `(51, 3467)` | Flattened track representation in the local Frenet frame (occupancy grid including obstacles).   |
| `global_states` | `numpy.ndarray` `(8, 3467)`  | Global-frame state sequence (rows: `x, y, vx, vy, yaw, dyaw, torque, steer`).   |
| `local_states`  | `numpy.ndarray` `(8, 3467)`  | Local-frame state sequence (matching the above ordering in the local Frenet frame).   |


## Data generation

Collecting expert trajectories is costly: even with a mature offline TOC solver, a single scenario (fixed track + a specific obstacle set) takes around 10 minutes to solve on our setup. To scale the dataset, we adopt the following augmentation strategy:

1. Base scenarios (file: 0–100).
    We generate scenarios indexed 0…100 and solve the TOC problem offline to obtain a time-optimal trajectory for each.
    - Any scenario that is infeasible or results in a collision is discarded.
    - Consequently, some files in 0–100 are missing.
2. Obstacle augmentation chains (`roots`).
    - For each remaining base scenario (a “root”), we iteratively add random obstacles that do not induce collisions along the existing solution.
    - By construction, this does not change the time-optimal solution for that scenario (the previous solution remains optimal under the augmented constraints), and each augmentation step receives a new scenario.
    - We record the entire chain in the roots list.

Example
~~~
roots = ["94", "1758", "2687", "11010"]
~~~
This means: starting from root `94`, we add obstacles (no new collisions) to obtain `1758`; from `1758` we add more to obtain `2687`; and so on until `11010`.

To solve TOC we first discretize the entire track along the centerline. After obtaining a solution on the solver’s grid, we linearly interpolate the centerline (and the solution) to a single-lap grid of $N = 3466$ anchor indices.

Because we consider multi-lap scenarios and want the solution to be head-to-tail continuous, for certain arrays we append the first sample to the end, yielding a closed loop with $N = 3467$. This makes the last point equal to the first point (for position-like quantities), which is convenient for plotting and rolling indices.

## track
The track object is a dictionary that contains all necessary information to describe the fixed racing track and its obstacles in the global frame:

| Key  | Type / Shape | Description  |
| ---- | ------------ | ------------ |
| `x_original` | `np.ndarray`, `(3466,)` | Centerline **x** coordinates in the global frame (sampled along the track). |
| `y_original` | `np.ndarray`, `(3466,)` | Centerline **y** coordinates in the global frame (aligned with `x_original`). |
| `x_rate`     | `np.ndarray`, `(3466,)` | Curvature information of the centerline in the global frame (per centerline index). |
| `y_rate`     | `np.ndarray`, `(3466,)` | Curvature information of the centerline in the global frame (per centerline index).  |
| `TRACK_WIDTH` | `float` | Track width (assumed **constant** along the centerline).  |
| `obstacles`   | `list` of `np.ndarray (n, 3)` | Each obstacle contour is an array with **n** samples; **col0 = x**, **col1 = y** (global frame), **col2 = centerline index** associated with that point. Here **n** is the length of the obstacle along the centerline. |

## flatten_track

`flattened_track` (`np.ndarray`, shape (51, 3467)) is a Frenet-frame occupancy grid for the track including obstacles, stored as a binary matrix:
- Frame: local Frenet coordinates $(s, n)$
  - $s$ $\rightarrow$  longitudinal progress along the centerline (closed loop with 3467 columns).
  - $n$ $\rightarrow$ lateral offset across the track width (discretized into 51 rows).
- Values: 0 = free space, 1 = obstacle.
- Construction: we discretize laterally at a fixed step $\Delta n = 0.01$ (track units, typically meters), then transform obstacle contours from global $(x, y)$ into Frenet $(s, n)$ and rasterize onto this grid.

Axis semantics
- Rows $(0\dots50)$: evenly spaced lateral samples across the track (step ~ 0.01).
(Exact origin - left/inner vs right/outer - and the mapping from row index to $n$ will be specified in the Schema.)
- Columns $(0\dots3466)$: longitudinal samples along one lap; column 3466 duplicates column 0 to enforce a closed loop (see Track discretization & closed-loop convention).


## global_states

`global_states` (`np.ndarray`, shape (8, 3467)) are time-aligned vehicle states in the global frame for one closed lap (the last column duplicates the first to enforce head-to-tail continuity).


| Row idx | Name     | Frame        | Typical unit | Notes                                        |
| ------: | -------- | ------------ | ------------ | -------------------------------------------- |
|       0 | `x`      | global (XY)  | m            | Vehicle position **x** on the track plane    |
|       1 | `y`      | global (XY)  | m            | Vehicle position **y** on the track plane    |
|       2 | `vx`     | global (XY)  | m/s          | Time derivative of **x**                     |
|       3 | `vy`     | global (XY)  | m/s          | Time derivative of **y**                     |
|       4 | `yaw`    | global (yaw) | rad          | Heading angle (global frame)                 |
|       5 | `dyaw`   | global (yaw) | rad/s        | Yaw rate                                     |
|       6 | `torque` | control      | N·m          | Drive/brake torque                           |
|       7 | `steer`  | control      | rad          | Steering angle                               |


## local_states
Local-frame state sequence (matching the above ordering in the local Frenet frame). 



# Quick start

# Visualization

# Citation
