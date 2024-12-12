from datetime import datetime

class Logger:
    def __init__(self, logfile='log.txt', interrupt=True):
        if type(logfile) == str:
            self.file_pointer = False
            self.file = False
            self.file_name = logfile
        else:
            self.file_pointer = True
            self.file = logfile
            self.file_name = False

        self.interrupt = interrupt

    def log(self, msg):
        time = datetime.now().strftime('%d-%m-%Y  %H:%M:%S:%f')
        log_msg = f'{time}\t{msg}\n'
        if self.file_pointer:
            print(log_msg.strip(), file=self.file)  
        else:
            with open(self.file_name, 'a') as outfile:
                outfile.write(log_msg)
        
    def run(self, function, parameters=(), secret=False):
        if not secret:
            self.log(f'executing {function} with parameters: {parameters}')
        else:
            self.log(f'executing {function}')
        try:
            if type(parameters) == tuple:
                result = function(*parameters)
            if type(parameters) == dict:
                result = function(**parameters)
            self.log(f'concluded {function}')
            return result
        except Exception as e:
            self.log(f'Error: {e}')
            if self.interrupt:
                exit()
            else:
                return None

