from datetime import datetime

class Session:
    def __init__(self, id: int=0, source: str='', notes: str='', 
        updated_at: datetime=datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')) -> None:
        self.id = id
        self.source = source
        self.notes = notes
        self.DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        self.updated_at = datetime.strptime(updated_at, self.DATETIME_FORMAT)
    

    def get_updated_at_str(self):
        return self.updated_at.strftime(self.DATETIME_FORMAT)


    def __str__(self) -> str:
        if self.source == '':
            return 'Untitled'
            
        return self.source
