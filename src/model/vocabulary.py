class Vocabulary:
    def __init__(
        self, 
        id: int, 
        vocabulary: str, 
        pinyin: str,
        definition: str,
        sentence: str,
        notes: str,
        session_id: int
    ) -> None:
        self.id = id,
        self.vocabulary = vocabulary,
        self.pinyin = pinyin,
        self.definition = definition,
        self.sentence = sentence,
        self.notes = notes
        self.session_id = session_id
    
    def __str__(self) -> str:
        return f"""
            {self.id}, 
            {self.vocabulary},
            {self.pinyin},
            {self.definition},
            {self.sentence},
            {self.notes},
            {self.session_id},
        """