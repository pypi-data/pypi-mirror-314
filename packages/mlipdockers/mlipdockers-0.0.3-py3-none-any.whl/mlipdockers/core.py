from pymatgen.core.structure import Structure
from mlipdockers.dkreq import DockerSocket
import json

def image(inm):
    """
    MLIP images made by Yaoshu Xie.
    
    options: mace, orb-models, sevenn, chgnet, grace-2l
    """
    rp = 'crpi-aqvrppj8ebnguc34.cn-shenzhen.personal.cr.aliyuncs.com/jinlhr542'
    if inm == 'mace':
        print('default settings')
        print({'model':'medium', 'device':'cpu'})
        return f'{rp}/mace:0.0.1', {'model':'medium', 'device':'cpu', 'dispersion':0}
        
    elif inm == 'orb-models':
        print('default settings')
        print({'device':'cpu'})
        return f'{rp}/orb-models:0.0.1', {'device':'cpu'}
        
    elif inm == 'sevenn':
        print('default settings')
        print({'version':'7net-0_11July2024', 'device':'cpu'})
        return f'{rp}/sevenn:0.0.1', {'version':'7net-0_11July2024', 'device':'cpu'}
        
    elif inm == 'chgnet':
        print('default settings')
        print({'device':'cpu'})
        return f'{rp}/chgnet:0.0.1', {'device':'cpu'}
        
    elif inm == 'grace-2l':
        print('default settings')
        print({})
        return f'{rp}/grace-2l:0.0.1', {}
        
    else:
        raise ValueError('only for mace, orb-models, sevenn, chgnet or grace-2l')
        

class MlipCalc:
    """
    MLIP calculator
    """
    def __init__(self, image_name, user_settings = None):
        """
        Args:
        image_name (str): MLIP image name
        user_settings (dict): mlip version, device to use (cpu, gpu) ...
        """
        self.mlip = image_name
        self.image_name, self.dinput = image(image_name)
        self.dinput['start_port'] = 5000
        self.dinput['end_port'] = 6000
        if user_settings != None:
            for i in user_settings.keys():
                self.dinput[i] = user_settings[i]
        self.dkskt = DockerSocket(self.image_name, self.dinput['start_port'], self.dinput['end_port'])
        
        #initializing by first calculation
        lattice = [[5.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 5.0]]
        atoms = [("Si", [0, 0, 0]), ("Si", [1.5, 1.5, 1.5])]
        print('Performing initialization calculation ...')
        structure = Structure(lattice, [atom[0] for atom in atoms], [atom[1] for atom in atoms])
        _ = self.calculate(structure)
        print('initialization completed')
        
    def calculate(self, structure):
        """
        predict potential energy of a structure
        
        Args:
        structure (Structure)
        """
        self.dinput['structure'] = json.loads(structure.to_json())
        if self.mlip == 'chgnet':
            return self.dkskt.request(self.dinput)['energy'] * len(structure)
        else:
            return self.dkskt.request(self.dinput)['energy']
    
    def close(self):
        """
        shut down container
        """
        self.dkskt.close()
    
    
        
