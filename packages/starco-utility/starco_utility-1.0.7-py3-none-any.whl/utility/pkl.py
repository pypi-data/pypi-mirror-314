from cryptography.fernet import Fernet
import pickle,os,json
from time import time

class Pkl:
    def __init__(self, path='setting', encrypt=False, real_time=True):
        self.data = {}
        self.path = path
        self.real_time = real_time
        self.encryption = False
        self.BASE_ENCODE_KEY = '95AuiJk_wGQT9xcEZ6Xlymgh67LZyxHt34LShTkRO9w='
        
        if encrypt:
            self.encryption = True
            self.fernet = Fernet(self.BASE_ENCODE_KEY.encode())

    def reset(self):
        try:
            os.remove(self.path)
            self.data = {}
            return True
        except:
            pass
        return False

    def pkl(self, key=None, value=None, empty_return='', expir_sec: int = 0):
        if type(key) != type(None):
            pfx= '_set_timefpkl'
            if pfx in key:
                return
            set_time_label = key+pfx
        if not self.data:
            try:
                with open(self.path, "rb") as f:
                    save_data = pickle.load(f)
                    if self.encryption:
                        save_data = json.loads(
                            self.fernet.decrypt(save_data).decode())
            except Exception as e:
                save_data = {}
        else:
            save_data = self.data
        
            
        if type(value) != type(None):
            save_data[key] = value
            save_data[set_time_label] = int(time())
            if self.real_time:
                self.data = save_data
            with open(self.path, "wb") as fh:
                if self.encryption:
                    save_data = self.fernet.encrypt(
                        json.dumps(save_data).encode())
                pickle.dump(save_data, fh)
        elif type(key) != type(None):
            expir_time = 0
            if expir_sec > 0:
                set_time = save_data.get(set_time_label, 0)
                if set_time != 0:
                    expir_time = set_time + expir_sec
            if expir_time > 0:
                if int(time()) > expir_time:
                    return empty_return
            return save_data.get(key, empty_return)
        else:
            return save_data