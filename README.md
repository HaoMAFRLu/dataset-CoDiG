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

# Quick start

# Visualization

# Citation
