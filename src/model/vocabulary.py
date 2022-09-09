class Vocabulary:
    def __init__(self, id: int=0, vocabulary: str='', reading: str='', meaning: str='', 
            sentence: str='', notes: str='', session_id: int=0) -> None:
        self.id = id
        self.vocabulary = vocabulary
        self.reading = reading
        self.meaning = meaning
        self.sentence = sentence
        self.notes = notes
        self.session_id = session_id
    
    def __str__(self) -> str:
        return f"""{self.id}, {self.vocabulary}, {self.reading}, 
                   {self.meaning}, 
                   {self.sentence},
                   {self.notes}, 
                   {self.session_id}
                   """
    