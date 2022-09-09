import sqlite3
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QPushButton,
    QWidget,
)
from PyQt6.QtCore import Qt
import database.vocabulary_db
from model.session import Session
from model.vocabulary import Vocabulary
from datetime import datetime

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import urllib.parse
from bs4 import BeautifulSoup


class SessionDetailsPanel(QWidget):
    def __init__(self, parentObject, session: Session) -> None:
        super().__init__()

        self.parentObject = parentObject
        self.session = session
    
        outer_layout = QVBoxLayout()

        # session details
        # session source
        self.session_details_layout = QGridLayout()
        self.session_details_layout.addWidget(QLabel('<b>Source:</b>'), 0, 0, Qt.AlignmentFlag.AlignTop)
        self.session_source_qle = QLineEdit()
        self.session_source_qle.setPlaceholderText('Untitled')
        self.session_source_qle.setText(session.source)
        self.session_source_qle.textChanged.connect(self.update_session_details)
        self.session_details_layout.addWidget(self.session_source_qle, 0, 1, Qt.AlignmentFlag.AlignTop)

        # session last updated timestamp
        self.session_details_layout.addWidget(QLabel('<b>Last updated:</b>'), 1, 0, Qt.AlignmentFlag.AlignTop)
        self.session_updated_date_ql = QLabel('') if len(self.parentObject.get_sessions_list()) == 0 else QLabel(session.get_updated_at_str())
        self.session_details_layout.addWidget(self.session_updated_date_ql, 1, 1, Qt.AlignmentFlag.AlignTop)

        # session notes
        self.session_notes_qpte = QLineEdit()
        self.session_notes_qpte.setPlaceholderText('Enter notes here')
        self.session_notes_qpte.setText(session.notes)
        self.session_notes_qpte.textChanged.connect(self.update_session_details)
        self.session_details_layout.addWidget(QLabel('<b>Notes:</b>'), 2, 0, Qt.AlignmentFlag.AlignTop)
        self.session_details_layout.addWidget(self.session_notes_qpte, 3, 0, 1, 2, Qt.AlignmentFlag.AlignTop)
        outer_layout.addLayout(self.session_details_layout)

        # session vocabulary list
        vocabulary_list = self.get_session_vocabularies_from_db(session.id)
        self.vocabulary_list_qlw = QListWidget()
        self.vocabulary_list_qlw.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.vocabulary_list_qlw.itemClicked.connect(self.vocabulary_clicked)
        for vocab in vocabulary_list:
            vocab_item = QListWidgetItem(vocab.vocabulary)
            vocab_item.setData(1, vocab)
            self.vocabulary_list_qlw.addItem(vocab_item)
        # self.vocabulary_list_qlw.setEditTriggers(QAbstractItemView.EditTrigger.AnyKeyPressed)
        outer_layout.addWidget(self.vocabulary_list_qlw)
        # vocab entry widget
        self.vocabulary_entry_qle = QLineEdit()
        self.vocabulary_entry_qle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vocabulary_entry_qle.setPlaceholderText("Enter vocab here")
        # connect enter key press with add vocabulary function
        self.vocabulary_entry_qle.returnPressed.connect(self.add_vocabulary)
        outer_layout.addWidget(self.vocabulary_entry_qle)

        # vocabulary add/remove buttons
        vocabulary_list_button_group = QHBoxLayout()
        self.add_vocabulary_qpb = QPushButton('+ add vocab', clicked=lambda: self.add_vocabulary())
        self.remove_vocabulary_qpb = QPushButton('- remove vocab', clicked=lambda: self.remove_vocabulary())
        self.remove_vocabulary_qpb.setEnabled(False)
        vocabulary_list_button_group.addWidget(self.add_vocabulary_qpb)
        vocabulary_list_button_group.addWidget(self.remove_vocabulary_qpb)

        self.vocabulary_list_qlw.itemSelectionChanged.connect(self.vocabulary_list_items_selected)
        outer_layout.addLayout(vocabulary_list_button_group)

        if self.vocabulary_list_qlw.count() > 0:
            self.vocabulary_list_qlw.item(0).setSelected(True)
        else:
            # if no vocab present in list then disable remove vocab button
            self.remove_vocabulary_qpb.setEnabled(False)

        if len(self.parentObject.get_sessions_list()) == 0:
            self.session_source_qle.setEnabled(False)
            self.session_notes_qpte.setEnabled(False)
            self.vocabulary_entry_qle.setEnabled(False)
            self.add_vocabulary_qpb.setEnabled(False)
            self.remove_vocabulary_qpb.setEnabled(False)

        self.setLayout(outer_layout)


    def vocabulary_clicked(self, item: QListWidgetItem):
        """
        Call parent object to update vocabulary details panel to the vocab item clicked

        Args:
            item (QListWidgetItem): the vocab list item clicked
        """
        self.parentObject.update_vocabulary_details_panel(item.data(1))


    def get_selected_vocabularies(self) -> list[Vocabulary]:
        return [vocab.data(1) for vocab in self.vocabulary_list_qlw.selectedItems()]


    def remove_vocabulary(self) -> None:
        vocab_id_list = [(item.data(1).id,) for item in self.vocabulary_list_qlw.selectedItems()]

        try:
            connection = database.vocabulary_db.connect()
            cursor = connection.cursor()

            delete_query = """DELETE FROM Vocabularies 
                              WHERE VocabularyId=?;
                              """
            cursor.executemany(delete_query, vocab_id_list)

            update_query = """UPDATE MiningSessions
                              SET UpdatedAt=?
                              WHERE SessionId=?;
                              """
            cursor.execute(update_query, (datetime.now().replace(microsecond=0), self.session.id))
            connection.commit()
            connection.close()
            print("Deleted vocab(s).")
        except sqlite3.Error as e:
            print(e)
        
        # update UI to include new session object
        self.parentObject.update_sessions_list_panel()
        self.parentObject.update_session_details_panel(self.parentObject.get_sessions_list()[0])
        self.parentObject.update_vocabulary_details_panel_with_top_item()


    def scrape_chinese_vocab_details(self, vocab: str) -> tuple[str, str]:
        reading = ''
        meaning = ''

        try:
            html = urlopen(f'https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb=*{urllib.parse.quote(vocab)}*')
        except HTTPError as e:
            print(e)
        except URLError as e:
            print(e)

        bs = BeautifulSoup(html, 'lxml')
        try:
            if not bs.findAll(text='No results found searching for'):
                table_element = bs.find('table', {'class': 'wordresults'})
                search_result_tr_elements = table_element.tbody.find_all('tr', {'class': 'row'})
                for tr in search_result_tr_elements:
                    if tr.find('div', {'class': 'hanzi'}).get_text(strip=True) == vocab:
                        reading = tr.find('div', {'class': 'pinyin'}).get_text()
                        meaning = tr.find('td', {'class': 'details'}).get_text()
                        break
        except AttributeError as e:
            print(e)
        
        return (reading, meaning)


    def add_vocabulary(self) -> None:
        vocab_to_insert = self.vocabulary_entry_qle.text()
        if not vocab_to_insert: return # ignore empty inputs
        
        reading, meaning = self.scrape_chinese_vocab_details(vocab_to_insert)

        try:
            connection = database.vocabulary_db.connect()
            cursor = connection.cursor()

            insert_query = """INSERT INTO Vocabularies (Vocabulary, Reading, Meaning, SessionId)
                              VALUES (?, ?, ?, ?);
                              """
            cursor.execute(insert_query, (vocab_to_insert, reading, meaning, self.session.id))

            update_query = """UPDATE MiningSessions
                              SET UpdatedAt=?
                              WHERE SessionId=?;
                              """
            cursor.execute(update_query, (datetime.now().replace(microsecond=0), self.session.id))
            connection.commit()
            connection.close()
            print(f"Inserted vocab {vocab_to_insert}.")
        except sqlite3.Error as e:
            print(e)
        
        # update UI to include new session object
        self.parentObject.update_sessions_list_panel()
        self.parentObject.update_session_details_panel(self.parentObject.get_sessions_list()[0])
        self.parentObject.update_vocabulary_details_panel_with_top_item()

        
    def vocabulary_list_items_selected(self) -> None:
        if len(self.vocabulary_list_qlw.selectedItems()) > 0:
            self.remove_vocabulary_qpb.setEnabled(True)
        else:
            self.remove_vocabulary_qpb.setEnabled(False)


    def update_session_details(self, line_edit: str) -> None:
        """
        Update session records in database whenever details inside source or notes has changed
        """
        try:
            connection = database.vocabulary_db.connect()
            cursor = connection.cursor()

            update_query = """UPDATE MiningSessions
                              SET Source=?, Notes=?, UpdatedAt=?
                              WHERE SessionId=?;
                              """
            cursor.execute(update_query, 
                (self.session_source_qle.text(), 
                self.session_notes_qpte.text(), 
                datetime.now().replace(microsecond=0), 
                self.session.id))
            connection.commit()
            connection.close()
            print("Updated session details.")
        except sqlite3.Error as e:
            print(e)
        
        # update UI with updated session details
        self.parentObject.update_sessions_list_panel()
        self.update_last_updated_timestamp()


    def update_last_updated_timestamp(self) -> None:
        """
        Update last updated timestamp label
        """
        self.session_updated_date_ql.deleteLater()
        self.session_updated_date_ql = QLabel(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.session_details_layout.addWidget(self.session_updated_date_ql, 1, 1, Qt.AlignmentFlag.AlignTop)


    def get_session_vocabularies_from_db(self, session_id: int) -> list[Vocabulary]:
        """
        Args:
            session_id (int): id for the session vocabulary to select

        Returns:
            a list of Vocabulary objects obtained from the database
        """
        try:
            connection = database.vocabulary_db.connect()
            cursor = connection.cursor()

            select_query = """SELECT * FROM Vocabularies
                              WHERE SessionId=?
                              ORDER BY VocabularyID DESC;
                              """
            # https://stackoverflow.com/questions/11853167/parameter-unsupported-when-inserting-int-in-sqlite
            # need comma after if only one argument in tuple
            cursor.execute(select_query, (session_id,))
            
            vocabulary_rows = cursor.fetchall()
            vocabulary_list = [Vocabulary(v[0], v[1], v[2], v[3], v[4], v[5], v[6]) for v in vocabulary_rows]

            connection.close()
            # print("Selected all vocabulary.")

            return vocabulary_list
        except sqlite3.Error as e:
            print(e)
    
    def get_session(self) -> Session:
        return self.session
    
    def update_vocabulary_list_widget(self, new_vocab: Vocabulary):
        """
        Find the id of updated vocab in list widget and update with new details from 
        """
        for i in range(len(self.vocabulary_list_qlw)):
            if self.vocabulary_list_qlw.item(i).data(1).id == new_vocab.id:
                self.vocabulary_list_qlw.item(i).setData(1, new_vocab)
                break
    