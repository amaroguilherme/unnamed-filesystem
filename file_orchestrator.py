import logging
import queue
import threading

log = logging.getLogger()
log.setLevel(logging.INFO)

class Orchestrator:
    def __init__(self, file):
        self.file = file
        self.queue = queue.Queue()
        
    def orchestrate(self) -> bool:
        try:
            file_producer: FileProducer = FileProducer(self)
            file_consumer: FileConsumer = FileConsumer(self)
            
            thread: threading.Thread = threading.Thread(target=file_producer.producer)
            thread.start()
            
            file_consumer.start()
            
        except Exception as e:
            log.error(e)
            return False
        
        return True
        
class FileConsumer(threading.Thread):

    def __init__(self, orchestrator: Orchestrator):
        super().__init__()
        self.orchestrator = orchestrator
        
    def run(self) -> bool:
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
        
    def producer(self) -> None:
        self.orchestrator.queue.put(self.orchestrator.file)
        
    