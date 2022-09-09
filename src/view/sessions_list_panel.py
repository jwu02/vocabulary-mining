import sqlite3
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QStyle,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView
)
import database.vocabulary_db
from model.session import Session


class SessionsListPanel(QWidget):
    def __init__(self, parentObject) -> None:
        super().__init__()

        self.parentObject = parentObject
        self.sessions_list = self.get_sessions_list_from_db()

        outer_layout = QVBoxLayout()

        self.sessions_list_top_button_group = QHBoxLayout()
        add_session_qpb = QPushButton('+ new session', clicked=lambda: self.add_new_session())
        self.delete_session_qpb = QPushButton('- delete session', clicked=lambda: self.delete_session())
        self.sessions_list_top_button_group.addWidget(self.delete_session_qpb)
        self.sessions_list_top_button_group.addWidget(add_session_qpb)
        outer_layout.addLayout(self.sessions_list_top_button_group)

        self.export_as_anki_deck_qpb = QPushButton('> export as anki deck', clicked=lambda: self.export_as_anki_deck())
        self.export_as_anki_deck_qpb.setEnabled(False)
        outer_layout.addWidget(self.export_as_anki_deck_qpb)

        # sessions_list_panel = QGridLayout()
        # delete_session_btn_list = [] # list for storing all delete button objects with slightly different behaviour
        # for i in range(len(sessions_list)):
        #     if sessions_list[i].source == '':
        #         session_label = QLabel('Untitled')
        #     else:
        #         session_label = QLabel(sessions_list[i].source)

        #     sessions_list_panel.addWidget(session_label, i, 0)
            
        #     # delete icon for deleting sessions
        #     delete_icon = self.style().standardIcon(getattr(QStyle.StandardPixmap, 'SP_DialogCancelButton'))
        #     # delete_session_btn = QPushButton(clicked=lambda: self.delete_session(sessions_list[i].id))
        #     delete_session_btn_list.append(QPushButton(clicked=lambda: self.delete_session(sessions_list[i].id)))
        #     delete_session_btn_list[i].setIcon(delete_icon)
        #     sessions_list_panel.addWidget(delete_session_btn_list[i], i, 1)

        # sessions list widget
        self.sessions_list_qlw = QListWidget()
        self.sessions_list_qlw.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.sessions_list_qlw.itemClicked.connect(self.session_clicked)
        self.sessions_list_qlw.itemSelectionChanged.connect(self.session_list_items_selected)
        for session in self.sessions_list:
            session_item = QListWidgetItem(session.source)
            session_item.setData(1, session) # role 0 set with value of item's text by default
            if session.source == '':
                session_item.setData(0, session.get_updated_at_str())
            self.sessions_list_qlw.addItem(session_item)
        
        if self.sessions_list_qlw.count() > 0:
            self.sessions_list_qlw.item(0).setSelected(True)

        outer_layout.addWidget(self.sessions_list_qlw)

        if not self.sessions_list:
            self.delete_session_qpb.setDisabled(1)

        self.setLayout(outer_layout)


    def get_sessions_list_from_db(self) -> list[Session]:
        """
        Returns:
            list of all Session objects obtained from database
        """
        try:
            connection = database.vocabulary_db.connect()
            cursor = connection.cursor()
        except sqlite3.Error as e:
            print(e)
        
        select_query = """SELECT * FROM MiningSessions
                          ORDER BY UpdatedAt DESC;
                          """
        cursor.execute(select_query)
        rows = cursor.fetchall()
        sessions_list = [Session(row[0], row[1], row[2], row[3]) for row in rows]
        
        connection.close()
        # print("Selected all sessions!")

        return sessions_list


    def get_sessions_list(self) -> list[Session]:
        return self.sessions_list


    def session_list_items_selected(self) -> None:
        """
        Disable delete session and export to anki button if no items are selected
        otherwise enable them
        """
        if self.sessions_list_qlw.selectedItems():
            self.delete_session_qpb.setEnabled(1)
            self.export_as_anki_deck_qpb.setEnabled(1)
        else:
            self.delete_session_qpb.setDisabled(1)
            self.export_as_anki_deck_qpb.setDisabled(1)


    def session_clicked(self, item: QListWidgetItem) -> None:
        """
        Call parent object to update session details panel to the session item clicked

        Args:
            item (QListWidgetItem): the session list item clicked
        """
        self.parentObject.update_session_details_panel(item.data(1))
        self.parentObject.update_vocabulary_details_panel_with_top_item()


    def add_new_session(self) -> None:
        """
        Add a new vocabulary mining session
        """
        try:
            connection = database.vocabulary_db.connect()
            cursor = connection.cursor()

            insert_query = """INSERT INTO MiningSessions (Source, Notes) 
                              VALUES ('', '');
                              """
            cursor.execute(insert_query)
            connection.commit()
            connection.close()
            print("Added new session.")
        except sqlite3.Error as e:
            print(e)

        # update UI to include new session object
        self.parentObject.update_sessions_list_panel()
        self.parentObject.update_session_details_panel(self.parentObject.get_sessions_list_panel().get_sessions_list()[0])
        self.parentObject.update_vocabulary_details_panel_with_top_item()


    def delete_session(self) -> None:
        session_id_list = [(item.data(1).id,) for item in self.sessions_list_qlw.selectedItems()]

        try:
            connection = database.vocabulary_db.connect()
            cursor = connection.cursor()

            delete_query = """DELETE FROM MiningSessions 
                              WHERE SessionId=?;
                              """
            cursor.executemany(delete_query, session_id_list)
            connection.commit()
            connection.close()
            print("Deleted session(s).")
        except sqlite3.Error as e:
            print(e)

        # update UI to remove session object
        self.parentObject.update_sessions_list_panel()
        if self.parentObject.get_sessions_list_panel().get_sessions_list():
            self.parentObject.update_session_details_panel(self.parentObject.get_sessions_list_panel().get_sessions_list()[0])
        else:
            self.parentObject.update_session_details_panel(Session())
        self.parentObject.update_vocabulary_details_panel_with_top_item()
    

    def export_as_anki_deck(self) -> None:
        print("Mining sessions exported as anki deck.")
