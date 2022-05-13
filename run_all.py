import numpy as np
import os

for model in ["pagnn", "gcnmf", "lp"]:
    for i in list(np.arange(0,10)/10)+[0.99]:
        cmd = f"CUDA_VISIBLE_DEVICES=2 python src/run.py --dataset_name PubMed --model {model} --missing_rate {i}"
        print (cmd)
        os.system(cmd)

for method in ["zero", "random", "mean", "neighborhood_mean", "feature_propagation"]:
    for i in list(np.arange(0,10)/10)+[0.99]:
        cmd = f"CUDA_VISIBLE_DEVICES=2 python src/run.py --dataset_name PubMed --filling_method {method} --missing_rate {i}"
        print (cmd)
        os.system(cmd)
