import sys
from ui_interface import *
from Custom_Widgets.Widgets import *
from main_profile import ProfileMainWindow
# FOR YOLO PROJECT
from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *
import mysql.connector 
import datetime
#FOR DATA ANALYST
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import matplotlib.ticker as ticker
from PySide2.QtWidgets import QGraphicsScene
from db_connection import get_db_connection
video_file_path = ""


class MainWindow(QMainWindow):
    resizedSignal = Signal(QSize)
    # profileClosed = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        loadJsonStyle(self, self.ui)
        # EXPAND CENTRAL MENU WIDGET 
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.infoBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.helpBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.closeCenterMenuBtn.clicked.connect(lambda: self.ui.centerMenuContainer.collapseMenu())
        self.ui.moreMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())
        self.ui.closeRightMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.collapseMenu())
        self.ui.closeNotificationBtn.clicked.connect(lambda: self.ui.popupNotificationContainer.collapseMenu())
        
        self.ui.logoutBtn.clicked.connect(self.logout)
        self.ui.browseBtn.clicked.connect(self.open_file_dialog) 
        self.ui.listWidget.clicked.connect(self.handle_video_item_clicked)
        self.ui.startBtn.clicked.connect(self.start_open_cv_project)
        self.ui.videoComboBox.currentIndexChanged.connect(self.handle_video_selection)
        self.ui.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listWidget.customContextMenuRequested.connect(self.handle_context_menu)
        # OPEN PROFILE WINDOW 
        self.ui.profileMenuBtn.clicked.connect(self.open_profile_window)
        self.profile_window = None
        self.is_logged_in = False
        self.update_ui_visibility()


    def start_open_cv_project(self, video_id):
        if self.is_logged_in:
            video_info = self.get_video_info(video_id)
            if video_info is not None:
                user_id = video_info['user_id']
                video_file_path = video_info['video_file_path']
                run_open_cv_project(user_id, video_file_path, video_id)
                self.ui.label_13.setText("Video processing has finished, please check the Data Analysis.")
                self.ui.popupNotificationContainer.expandMenu()
                self.dataAnalyst(video_id)
        else:
            QMessageBox.warning(self, "Warning", "<font color='white'>Please log in first.</font>", QMessageBox.Ok)
    
    def open_profile_window(self):
       if not self.is_logged_in:
            if not self.profile_window:
                self.profile_window = ProfileMainWindow()
                self.resizedSignal.connect(self.profile_window.on_main_window_resized)
            try:
                self.profile_window.usernameChanged.disconnect(self.update_username_with_id)
            except RuntimeError:
                pass
            self.profile_window.usernameChanged.connect(self.update_username_with_id)
            self.profile_window.show()
       else:
            self.ui.rightMenuContainer.expandMenu()

    def resizeEvent(self, event):
        if self.profile_window:
            self.resizedSignal.emit(event.size())
            profile_x = self.pos().x() + (self.width() - self.profile_window.width()) / 2
            profile_y = self.pos().y() + (self.height() - self.profile_window.height()) / 2
            self.profile_window.move(QPoint(profile_x, profile_y))
            self.profile_window.raise_()
        return super().resizeEvent(event)
    
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange and self.profile_window:
            profile_x = self.pos().x() + (self.width() - self.profile_window.width()) / 2
            profile_y = self.pos().y() + (self.height() - self.profile_window.height()) / 2
            self.profile_window.move(QPoint(profile_x, profile_y))
            self.profile_window.raise_()
        super().changeEvent(event)
    
    def update_username_with_id(self, username, user_id):
        self.ui.label_8.setText(username)
        self.current_user_id = user_id
        # self.ui.logoutBtn.show()
        self.is_logged_in = True
        self.ui.rightMenuContainer.expandMenu()
        self.update_ui_visibility()
        self.profile_window.close()

    def update_ui_visibility(self):
        if self.is_logged_in:
            self.ui.mainPages.setCurrentWidget(self.ui.page_6)
            self.ui.page_6.show()
            self.ui.videoComboBox.clear()
            if self.current_user_id:
                video_info_list = self.get_user_videos(self.current_user_id)
                for video_info in video_info_list:
                    self.display_uploaded_video(video_info)
                    self.display_processed_video(video_info)
        else:
            self.ui.page_6.hide()
            self.ui.page_7.hide()

    def logout(self):
        self.is_logged_in = False
        QMessageBox.information(self, "Information", "<font color='white'>Successful log out.</font>")
        self.ui.listWidget.clear()
        self.ui.page_6.hide()
        self.ui.page_7.hide()
        self.ui.rightMenuContainer.collapseMenu()

    def open_file_dialog(self):
        global video_file_path
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Video files (*.mp4 *.avi)")
        if self.is_logged_in:
            if file_dialog.exec_():
                selected_files = file_dialog.selectedFiles()
                if selected_files:
                    video_file_path = selected_files[0]
                    self.ui.label_13.setText("Video file successful selected.")
                    print(f"Odabrani video: {video_file_path}")

                    # Spasavanje video zapisa u bazu podataka
                    user_id = self.profile_window.get_user_id(self.ui.label_8.text())
                    video_id = self.save_video_to_database(user_id, video_file_path)
                    if video_id is not None:
                        video_info = self.get_video_info(video_id)
                        self.display_uploaded_video(video_info)
                        self.ui.startBtn.clicked.disconnect()  
                        self.ui.startBtn.clicked.connect(lambda: self.start_open_cv_project(video_id)) 
                    else:
                        self.ui.label_13.setText("Video already exists on the list.")

                self.ui.popupNotificationContainer.expandMenu()
        else: QMessageBox.warning(self, "Warning", "<font color='white'>Please log in first.</font>", QMessageBox.Ok)

    def display_uploaded_video(self, video_info):
        video_id = video_info['video_id']
        video_file_path = video_info['video_file_path']

        video_name = os.path.basename(video_file_path)
        video_item = QListWidgetItem(QIcon(":/icons/icons/eye.svg"), video_name)
        video_item.setData(Qt.UserRole, video_id)  

        self.ui.listWidget.addItem(video_item)
        font = video_item.font()
        font.setPointSize(10)  
        video_item.setFont(font)

        self.ui.listWidget.setIconSize(QSize(34, 34)) 

    def handle_video_item_clicked(self, item):
        video_id = item.data(Qt.UserRole)  
        self.start_open_cv_project(video_id)
    
    def handle_context_menu(self, pos):
        video_item = self.ui.listWidget.itemAt(pos)
        if video_item is not None:
            menu = QMenu(self.ui.listWidget)
            delete_action = QAction("Delete video", self.ui.listWidget)
            delete_action.triggered.connect(lambda: self.delete_video_item(video_item))
            menu.addAction(delete_action)
            menu.exec_(self.ui.listWidget.viewport().mapToGlobal(pos))
            self.ui.label_13.setText("Video successfully deleted.")
            self.ui.popupNotificationContainer.expandMenu()
                
    def delete_video_item(self, video_item):
        video_id = video_item.data(Qt.UserRole)
        user_id = self.current_user_id 

        connection = get_db_connection()
        cursor = connection.cursor()

        # Provjera pripadnosti videozapisa korisniku
        select_query = "SELECT user_id FROM videos WHERE id = %s"
        cursor.execute(select_query, (video_id,))
        result = cursor.fetchone()
        if result and result[0] == user_id:
            delete_query = "DELETE FROM videos WHERE id = %s"
            cursor.execute(delete_query, (video_id,))

            connection.commit()
            connection.close()

            self.ui.listWidget.takeItem(self.ui.listWidget.row(video_item))
        else:
            pass
        return True
        
    def get_video_info(self, video_id):
        connection = get_db_connection()

        query = "SELECT id, user_id, video_file_path FROM videos WHERE id = %s"
        cursor = connection.cursor()
        cursor.execute(query, (video_id,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()
        if result:
            video_info = {
                'video_id': result[0],
                'user_id': result[1],
                'video_file_path': result[2]
            }
            return video_info
        else:
            return None
        
    def save_video_to_database(self, user_id, video_file_path):
        if self.check_existing_video(user_id, video_file_path):
            return None
        
        connection = get_db_connection()

        try:
            query_insert = "INSERT INTO videos (user_id, video_file_path) VALUES (%s, %s)"
            values = (user_id, video_file_path)
            cursor_insert = connection.cursor()
            cursor_insert.execute(query_insert, values)

            # Dohvaćanje dodijeljenog video_id
            video_id = cursor_insert.lastrowid

            query_update = "UPDATE users SET has_uploaded_videos = 1 WHERE id = %s"
            cursor_update = connection.cursor()
            cursor_update.execute(query_update, (user_id,))

            connection.commit()

        finally:
            if 'cursor_insert' in locals():
                cursor_insert.close()
            if 'cursor_update' in locals():
                cursor_update.close()
            connection.close()

        return video_id

    def check_existing_video(self, user_id, video_file_path):
        connection = get_db_connection()

        query = "SELECT COUNT(*) FROM videos WHERE user_id = %s AND video_file_path = %s"
        values = (user_id, video_file_path)
        cursor = connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result and result[0] > 0:
            return True
        else:
            return False
        
    def get_user_videos(self, user_id):
        connection = get_db_connection()

        try:
            query_check = "SELECT has_uploaded_videos FROM users WHERE id = %s"
            cursor_check = connection.cursor()
            cursor_check.execute(query_check, (user_id,))
            result = cursor_check.fetchone()

            if result and result[0] == 1:
                query_videos = "SELECT id, video_file_path FROM videos WHERE user_id = %s"
                cursor_videos = connection.cursor()
                cursor_videos.execute(query_videos, (user_id,))
                videos = cursor_videos.fetchall()

                user_videos = []
                for video in videos:
                    video_info = {
                        'video_id': video[0],
                        'video_file_path': video[1]
                    }
                    user_videos.append(video_info)

                return user_videos

        finally:
            if 'cursor_check' in locals():
                cursor_check.close()
            if 'cursor_videos' in locals():
                cursor_videos.close()
            connection.close()
        return []

    def dataAnalyst(self, video_id):
        if self.is_logged_in:
            username = self.ui.label_8.text()
            user_id = self.profile_window.get_user_id(username)

            connection = get_db_connection()

            if video_id is not None:
                query = f"SELECT cars, execution_time, current_datetime FROM statistics WHERE user_id = {user_id} AND video_id = {video_id}"
            else:
                query = f"SELECT cars, execution_time, current_datetime FROM statistics WHERE user_id = {user_id}"
            

            df = pd.read_sql_query(query, connection)
            connection.close()

            video_info = self.get_video_info(video_id)
            video_name = ""
            if video_info is not None:
                video_name = os.path.basename(video_info['video_file_path'])

            # Stvaranje grafa
            fig, ax = plt.subplots()

            if len(df) == 1:
                execution_time = df['execution_time'].values[0]
                x_ticks = [execution_time]
                y_values = [df['cars'].values[0]]

                ax.bar(x_ticks, y_values)
                ax.set_xlim([execution_time - 2, execution_time + 2])
                ax.set_ylim([0, max(y_values) + 1])
                ax.set_xlabel('Execution Time [s]')
                ax.set_ylabel('Number of Vehicles')
                ax.set_title(f'Data Analysis for {video_name}')
            else:
                ax.bar(df['execution_time'], df['cars'])
                ax.set_xlabel('Execution Time [s]')
                ax.set_ylabel('Number of Vehicles')
                ax.set_title(f'Data Analysis for {video_name}')

            for i, (execution_time, car, current_datetime) in enumerate(zip(df['execution_time'], df['cars'], df['current_datetime'])):
                datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                ax.text(execution_time, car, datetime_string, ha='center', va='bottom')
            
            plt.close()
            
            ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
            ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

            # Stvaranje QGraphicsScene za prikaz grafa
            scene = QGraphicsScene()
            scene.addWidget(FigureCanvas(fig))
            
            # Postavljanje QGraphicsScene u QGraphicsView
            self.ui.graphicsView.setScene(scene)

            self.add_videos_to_combobox()
        else:
            QMessageBox.warning(self, "Warning", "<font color='white'>Please log in first.</font>", QMessageBox.Ok)
    
    def handle_video_selection(self, index):
        video_id = self.ui.videoComboBox.itemData(index)
        self.dataAnalyst(video_id)

    def display_processed_video(self, video_info):
        video_id = video_info['video_id']
        video_file_path = video_info['video_file_path']
        video_name = os.path.basename(video_file_path)

        if self.ui.videoComboBox.findData(video_id) == -1 and self.ui.videoComboBox.findText(video_name) == -1:
            self.ui.videoComboBox.addItem(video_name, video_id)

    def add_videos_to_combobox(self):
        video_info_list = self.get_user_videos(self.current_user_id)
        for video_info in video_info_list:
            video_file_path = video_info['video_file_path']
            video_name = os.path.basename(video_file_path)
            video_id = video_info['video_id']
            if video_name and self.ui.videoComboBox.findData(video_id) ==-1  and self.ui.videoComboBox.findText(video_name) == -1:
                self.ui.videoComboBox.addItem(video_name, video_id)

    
def run_open_cv_project(user_id, video_file_path, video_id):
    global totalCountCars
    cap = cv2.VideoCapture(video_file_path)
    current_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    current_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    model = YOLO("../Yolo-Weights/yolov8l.pt")

    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                "teddy bear", "hair drier", "toothbrush"
                ]
    # Tracking
    tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

    limits = [150, 400, 1200, 400]
    totalCount = []
    totalCountCars = 0

    start_time = time.time()

    while True:
        success, img = cap.read()
        results = model(img, stream = True)

        detections = np.empty((0,5))
        for r in results:
            if current_width != 1280 or current_height != 720:
                img = cv2.resize(img, (1280, 720))
            boxes = r.boxes
            for box in boxes:
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1

                # Confidence
                conf = math.ceil((box.conf[0] * 100)) / 100
                # Class Name
                cls = int(box.cls[0])

                currentClass = classNames[cls]
                if currentClass == "car" or currentClass == "truck" or currentClass == "bus" or currentClass == "motorbike" and conf > 0.3:
                    currentArray = np.array([x1, y1, x2, y2, conf])
                    detections = np.vstack((detections, currentArray))
                    
        resultsTracker = tracker.update(detections)
        cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0,0,255), 4)

        for result in resultsTracker:
            x1, y1, x2, y2, id = result
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h), l=3, rt=2, colorR=(255,0,0))
            cvzone.putTextRect(img, f'{int(id)}', (max(0, x1), max(35, y1)), scale=1, thickness=1, offset=5)

            cx, cy = x1 + w // 2, y1 + h // 2
            cv2.circle(img, (cx,cy), 5, (255,0,0), cv2.FILLED)

            if limits[0] < cx < limits[2] and limits[1] - 15 < cy < limits[2] + 15:
                if totalCount.count(id) == 0: 
                    totalCount.append(id)
                    totalCountCars += 1
                    cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0,255,0), 4)

        cvzone.putTextRect(img, f'Count: {len(totalCount)} - Press "q" for break', (50, 50))

        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'):
            break

    end_time = time.time()
    execution_time = end_time - start_time
    current_datetime = datetime.datetime.now()
    rounded_datetime = current_datetime.replace(microsecond=0)  

    cv2.destroyAllWindows()
    insert_into_mysql(user_id, totalCountCars, execution_time, rounded_datetime, video_id)

def insert_into_mysql(user_id, totalCountCars, execution_time, rounded_datetime, video_id):
    connection = get_db_connection()
    query = "INSERT INTO statistics (user_id, cars, execution_time, current_datetime, video_id) VALUES (%s, %s, %s, %s, %s)"
    values = (user_id, totalCountCars, execution_time, rounded_datetime, video_id)

    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()
    
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())