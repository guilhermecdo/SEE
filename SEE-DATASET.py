import numpy as np
import json
import math
import torch
from torch.utils.data import Dataset
from torchvision.transforms import Compose

class SEE(Dataset):
    def __init__(self,filelist_path,sonar_model:str="P900"):
        
        with open(filelist_path, 'r') as f:
            self.filelist = f.read().splitlines()
        
        sonar_configuration = json.load(open( self.dataset_path+'/sonar-configuration.json'))
        self.sonar_model=sonar_configuration[sonar_model]

    def __getitem__(self, item):
        img_path=self.filelist[item].split(' ')[0]
        pl_path=self.filelist[item].split(' ')[0]

        image=np.load(img_path)
        
        gt_mask=np.load(pl_path)
        theta, phi = gt_mask.shape
        gt=np.zeros(shape=(theta,phi,self.sonar_model["RangeBins"]),dtype=np.uint8)

        for t in range(theta):
            for p in range(phi):
                r_index = int(math.floor(((gt_mask[t][p]-(self.sonar_model["RangeMin"]))*self.sonar_model["RangeBins"])/self.sonar_model["RangeMax"]))
                gt[t][p][r_index]=1

        sample={'image':torch.from_numpy(image),'depth':torch.from_numpy(gt)}
        
        return sample