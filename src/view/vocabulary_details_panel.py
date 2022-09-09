from locale import strcoll
from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
)
from PyQt6.QtCore import Qt
from model.vocabulary import Vocabulary
from datetime import datetime
import database.vocabulary_db
import sqlite3

class VocabularyDetailsPanel(QWidget):
    def __init__(self, parentObject, vocabulary: Vocabulary) -> None:
        super().__init__()

        self.parentObject = parentObject
        self.vocabulary = vocabulary

        outer_layout_qgl = QFormLayout()

        self.vocabulary_ql = QLabel(self.vocabulary.vocabulary)
        self.vocabulary_ql.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.reading_qle = QLineEdit()
        self.meaning_qle = QPlainTextEdit()
        self.sentence_qle = QLineEdit()
        self.notes_qle = QPlainTextEdit()

        self.reading_qle.setText(self.vocabulary.reading)
        self.meaning_qle.setPlainText(self.vocabulary.meaning)
        self.sentence_qle.setText(self.vocabulary.sentence)
        self.notes_qle.setPlainText(self.vocabulary.notes)

        self.reading_qle.textChanged.connect(self.update_vocabulary_details)
        self.meaning_qle.textChanged.connect(self.update_vocabulary_details)
        self.sentence_qle.textChanged.connect(self.update_vocabulary_details)
        self.notes_qle.textChanged.connect(self.update_vocabulary_details)

        outer_layout_qgl.addRow('<b>Vocabulary:</b>', self.vocabulary_ql)
        outer_layout_qgl.addRow('<b>Reading:</b>', self.reading_qle)
        outer_layout_qgl.addRow('<b>Meaning:</b>', self.meaning_qle)
        outer_layout_qgl.addRow('<b>Sentence:</b>', self.sentence_qle)
        outer_layout_qgl.addRow('<b>Notes:</b>', self.notes_qle)

        self.setLayout(outer_layout_qgl)


    def update_vocabulary_details(self, updated_text: str='') -> None:
        try:
            connection = database.vocabulary_db.connect()
            cursor = connection.cursor()

            update_query = """UPDATE Vocabularies
                              SET Reading=?, Meaning=?, Sentence=?, Notes=?
                              WHERE VocabularyId=?;
                              """
            cursor.execute(update_query, 
                (self.reading_qle.text(), 
                self.meaning_qle.toPlainText(), 
                self.sentence_qle.text(), 
                self.notes_qle.toPlainText(), 
                self.vocabulary.id))
            connection.commit()
            connection.close()
            print("Updated vocabulary details.")
        except sqlite3.Error as e:
            print(e)
        
        self.parentObject.get_session_details_panel().update_last_updated_timestamp_db()
        
        # update vocab assigned to this instance of a vocab details panel
        self.vocabulary = Vocabulary(
            self.vocabulary.id,
            self.vocabulary.vocabulary,
            self.reading_qle.text(), 
            self.meaning_qle.toPlainText(), 
            self.sentence_qle.text(), 
            self.notes_qle.toPlainText(), 
            self.parentObject.get_session_details_panel().get_current_session().id
        )

        # update UI and internal data
        self.parentObject.update_sessions_list_panel()
        self.parentObject.get_session_details_panel().update_last_updated_timestamp_label()
        self.parentObject.get_session_details_panel().update_vocabulary_list_widget(self.vocabulary)


    def disable_all_fields(self) -> None:
        self.reading_qle.setDisabled(1)
        self.meaning_qle.setDisabled(1)
        self.sentence_qle.setDisabled(1)
        self.notes_qle.setDisabled(1)
    

    def enable_all_fields(self) -> None:
        self.reading_qle.setEnabled(1)
        self.meaning_qle.setEnabled(1)
        self.sentence_qle.setEnabled(1)
        self.notes_qle.setEnabled(1)
    