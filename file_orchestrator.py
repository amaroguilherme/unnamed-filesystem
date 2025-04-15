import logging
import queue
import threading

log = logging.getLogger()
log.setLevel(logging.INFO)

class Orchestrator:
    def __init__(self, file):
        self.file = file
        self.queue = queue.Queue()
        
class FileConsumer(threading.Thread):

    def __init__(self, orchestrator: Orchestrator):
        super().__init__()
        self.orchestrator = orchestrator
        
    def run(self):
        try:
            file = self.orchestrator.queue.get()
            filename: str = file.filename 
            
            file.save(dst=f'files/{filename}')
        
        except Exception as e:
            log.error(e)
            return False
        
        return True
    
    
class FileProducer():
    
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        
    def producer(self):
        self.orchestrator.queue.put(self.orchestrator.file)
        
    