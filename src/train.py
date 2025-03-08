# flake8: noqa
import os.path as osp

#from edited_scripts.basicsr_train import train_pipeline
from edited_scripts.basicsr import train_pipeline
import edited_scripts.realesrgan.data.realesrgan_paired_dataset

if __name__ == '__main__':
    
    params = {
        "opt": "C:\\repos\\Real-ESRGAN\\options\\experements\\finetune_realesrgan_x2plus_pairdata.yml",
        "launcher": 'none', #'none', 'pytorch', 'slurm'
        "auto_resume": True,
        "debug": True,
        "local_rank": 0,
        "force_yml": None
    }

    #root_path = osp.abspath(osp.join(__file__, osp.pardir, osp.pardir))
    root_path = "C:\\repos\\Real-ESRGAN\\"
    train_pipeline(params, root_path)