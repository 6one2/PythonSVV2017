import glob
import pandas as pd

class Sub_SVV:
    
    def __init__(self, path: str):
        self.base_path = path
        self._id = path.split('/')[-1]
        self.trials = [x.split('/')[-1] for x in glob.glob(path+'/RES*')]
        
    def read_dat(self, trial_num: int):
        pathfile = self.base_path+'/'+self.trials[trial_num]
        cond = self.trials[trial_num].strip('.txt').split('_')
        data = open(pathfile, 'rt').read()
        ndata = data.split(' ')
    
        if len(ndata) != 3:
            return f'wrong number of output in data file'
        
        if cond[6]=='NA':
            cond[6]=0
        
        res =  { 
            'id' : [self._id],
            'trial' : [cond[4]],
            'stim' : [cond[5]],
            'freq' : [float(cond[6])],
            'rep': [cond[1]],
            'Angle_init' : [float(ndata[0].split('=')[-1])],
            'SVV' : [float(ndata[1].split('=')[-1])],
            'Reaction_time' : [float(ndata[2].split('=')[-1])]
        }

        return res
    
    def create_table(self):
        df = pd.DataFrame()
        df = df.append([pd.DataFrame.from_dict(self.read_dat(i)) for i in range(len(self.trials))], ignore_index=True)
        
        return df