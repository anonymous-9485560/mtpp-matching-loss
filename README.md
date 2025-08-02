The code uses the HoTPP benchmark for evaluation.

DEF implementation is located at hotpp/losses/detection.py

Configuration files can be found at experiments/dataset/configs/detection_hybrid.yaml

# Installation
Install via pip:
```sh
pip install .
```

Sometimes the following parameters are necessary for successful dependency installation:
```sh
CXX=<c++-compiler> CC=<gcc-compiler> pip install .
```

# Training and evaluation
The code is divided into the core library and dataset-specific scripts and configuration files.

The dataset-specific part is located in the `experiments` folder. Each subfolder includes data preparation scripts, model configuration files, and a README file. Data files and logs are usually stored in the same directory. All scripts must be executed from the directory of the specific dataset. Refer to the individual README files for more details.

To train the model, use the following command:
```sh
python3 -m hotpp.train --config-dir configs --config-name <model>
```

To evaluate a specific checkpoint, use the following command:
```sh
python3 -m hotpp.evaluate --config-dir configs --config-name <model>
```

To run multiseed training and evaluation:
```sh
python3 -m hotpp.train_multiseed --config-dir configs --config-name <model>
```
