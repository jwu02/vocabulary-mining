import sqlite3
from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QStyle,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView
)
from PyQt6.QtCore import Qt
import database.vocabulary_db
from model.session import Session
from model.vocabulary import Vocabulary

class VocabularyDetailsPanel(QWidget):
    def __init__(self, parentObject, vocabulary: Vocabulary) -> None:
        super().__init__()

        self.parentObject = parentObject
        self.vocabulary = vocabulary

        outer_layout_qgl = QFormLayout()

        self.vocabulary_qle = QLineEdit()
        self.reading_qle = QLineEdit()
        self.meaning_qle = QLineEdit()
        self.sentence_qle = QLineEdit()
        self.notes_qle = QLineEdit()

        self.vocabulary_qle.setText(self.vocabulary.vocabulary)
        self.reading_qle.setText(self.vocabulary.reading)
        self.meaning_qle.setText(self.vocabulary.meaning)
        self.sentence_qle.setText(self.vocabulary.sentence)
        self.notes_qle.setText(self.vocabulary.notes)

        outer_layout_qgl.addRow('Vocabulary', self.vocabulary_qle)
        outer_layout_qgl.addRow('Reading', self.reading_qle)
        outer_layout_qgl.addRow('Meaning', self.meaning_qle)
        outer_layout_qgl.addRow('Sentence', self.sentence_qle)
        outer_layout_qgl.addRow('Notes', self.notes_qle)

        self.setLayout(outer_layout_qgl)


    def disable_all_fields(self) -> None:
        self.vocabulary_qle.setDisabled(1)
        self.reading_qle.setDisabled(1)
        self.meaning_qle.setDisabled(1)
        self.sentence_qle.setDisabled(1)
        self.notes_qle.setDisabled(1)
    

    def enable_all_fields(self) -> None:
        self.vocabulary_qle.setEnabled(1)
        self.reading_qle.setEnabled(1)
        self.meaning_qle.setEnabled(1)
        self.sentence_qle.setEnabled(1)
        self.notes_qle.setEnabled(1)
    