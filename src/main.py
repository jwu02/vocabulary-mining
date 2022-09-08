from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QApplication
)
from view.sessions_list_panel import SessionsListPanel
from view.session_details_panel import SessionDetailsPanel
import sqlite3
import database.vocabulary_db
from model.session import Session

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle("Vocabulary Mining")

        outer_layout = QVBoxLayout()
        self.window_body_layout = QHBoxLayout()

        self.sessions_list = self.get_sessions_list_from_db()
        
        # side panel with list of sessions
        self.sessions_list_panel = SessionsListPanel(self)
        self.window_body_layout.addWidget(self.sessions_list_panel)

        # initialise interface with details of the last updated session
        self.session_details_panel = SessionDetailsPanel(self, Session())
        if len(self.sessions_list) > 0:
            self.session_details_panel = SessionDetailsPanel(self, self.sessions_list[0])
        self.window_body_layout.addWidget(self.session_details_panel)
        
        outer_layout.addLayout(self.window_body_layout)
        outer_layout.addStretch() # align elemnts to the top when specified at the end
        self.setLayout(outer_layout) # set window's main layout

        self.show()


    def get_sessions_list(self) -> list[Session]:
        return self.sessions_list


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
        print("Selected all sessions!")

        return sessions_list


    def update_session_details_panel(self, session: Session) -> None:
        """
        Update session details panel to the session clicked

        Args:
            session (Session): session object clicked in session list
        """
        self.session_details_panel.deleteLater()
        self.session_details_panel = SessionDetailsPanel(self, session)
        self.window_body_layout.addWidget(self.session_details_panel)
        self.session_details_panel.vocabulary_entry_qle.setFocus()

    
    def update_sessions_list_panel(self) -> None:
        """
        Update sessions list panel with updated set of sessions
        """
        self.sessions_list = self.get_sessions_list_from_db()

        self.sessions_list_panel.deleteLater()
        self.sessions_list_panel = SessionsListPanel(self)
        self.window_body_layout.insertWidget(0, self.sessions_list_panel)
    

app = QApplication([])
mw = MainWindow()

# Run the app
app.exec()