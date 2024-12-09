import sys
import os
import requests
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFileDialog,
                             QProgressBar, QTextEdit, QLineEdit, QTableWidget,
                             QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QColor

def load_manifest(excel_path):
    """
    Load pathology manifest from Excel, with more robust parsing

    Attempts to find columns flexibly:
    - Looks for 'imageUrl' or similar columns
    - Tries multiple patient ID column names
    """
    # Read the Excel file
    df = pd.read_excel(excel_path)

    # List of possible URL column names
    url_columns = ['imageUrl', 'image_url', 'url', 'Image URL']

    # List of possible patient ID column names
    patient_id_columns = ['Case ID', 'Patient ID', 'case_id', 'Case ID']

    # List of possible image ID column names
    image_id_columns = ['imageId', 'image_id', 'Image ID']

    # Find the first matching URL column
    url_column = next((col for col in url_columns if col in df.columns), None)

    # Find the first matching patient ID column
    patient_id_column = next((col for col in patient_id_columns if col in df.columns), None)

    # Find the first matching image ID column
    image_id_column = next((col for col in image_id_columns if col in df.columns), None)

    if not url_column:
        raise ValueError("Could not find image URL column in the Excel file.")

    if not patient_id_column:
        raise ValueError("Could not find patient ID column in the Excel file.")

    if not image_id_column:
        raise ValueError("Could not find image ID column in the Excel file.")

    # Rename columns to standard names for consistency
    df = df.rename(columns={
        url_column: 'imageUrl',
        patient_id_column: 'Case ID',
        image_id_column: 'imageId'
    })

    return df[['Case ID', 'imageId', 'imageUrl']]

class PathologyDownloadThread(QThread):
    # Signals for overall progress and download status
    overall_progress_signal = pyqtSignal(int, int)
    download_status_signal = pyqtSignal(str, str, str, int)  # case_id, image_id, status, progress
    log_signal = pyqtSignal(str)
    complete_signal = pyqtSignal(bool)

    def __init__(self, data, download_dir):
        super().__init__()
        self.data = data
        self.download_dir = download_dir

    def download_file(self, url, file_path):
        """
        Download a single file with progress tracking

        Args:
            url (str): URL of the file to download
            file_path (str): Local path to save the file

        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            # Stream the download to track progress
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            downloaded_size = 0

            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)

                        # Calculate and emit progress percentage
                        if total_size > 0:
                            progress = int((downloaded_size / total_size) * 100)
                            # Yield progress so it can be used for the specific file
                            yield progress

            return True
        except Exception as e:
            self.log_signal.emit(f"Download error: {str(e)}")
            return False

    def run(self):
        total_images = len(self.data)

        for idx, (_, row) in enumerate(self.data.iterrows(), 1):
            url = row['imageUrl']
            patient_id = row['Case ID']
            image_id = row['imageId']

            # Emit initial status for this file
            self.download_status_signal.emit(patient_id, image_id, 'Pending', 0)

            # Extract path after '/ross/' to create subdirectory structure
            try:
                sub_path = url.split('/ross/', 1)[-1]
                file_path = os.path.join(self.download_dir, sub_path)

                # Create directories if they don't exist
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                # Log the current file being downloaded
                self.log_signal.emit(f"Downloading {patient_id} - {image_id}: {url}")

                # Attempt to download the file
                download_generator = self.download_file(url, file_path)

                if isinstance(download_generator, bool):
                    # Download failed
                    self.log_signal.emit(f"Failed to download: {patient_id} - {image_id}")
                    self.download_status_signal.emit(patient_id, image_id, 'Failed', 0)
                else:
                    # Track progress for this specific file
                    for progress in download_generator:
                        self.download_status_signal.emit(patient_id, image_id, 'Downloading', progress)

                    # Download completed successfully
                    self.log_signal.emit(f"Successfully downloaded: {file_path}")
                    self.download_status_signal.emit(patient_id, image_id, 'Complete', 100)

                # Update overall progress
                self.overall_progress_signal.emit(idx, total_images)

            except Exception as e:
                self.log_signal.emit(f"Error processing {patient_id} - {image_id}: {str(e)}")
                # Emit error status
                self.download_status_signal.emit(patient_id, image_id, 'Error', 0)

        # Signal download completion
        self.complete_signal.emit(True)

class PathologyDownloadManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        # Track if a download is in progress
        self.download_in_progress = False

    def initUI(self):
        self.setWindowTitle('TCIA Download Manager')
        self.setGeometry(100, 100, 1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Excel File Selection
        file_layout = QHBoxLayout()
        self.file_path_input = QLineEdit()
        file_path_button = QPushButton('Select Manifest File')
        file_path_button.clicked.connect(self.select_excel_file)
        file_layout.addWidget(self.file_path_input)
        file_layout.addWidget(file_path_button)
        main_layout.addLayout(file_layout)

        # Download Directory Selection
        dir_layout = QHBoxLayout()
        self.download_dir_input = QLineEdit()
        download_dir_button = QPushButton('Select Download Directory')
        download_dir_button.clicked.connect(self.select_download_directory)
        dir_layout.addWidget(self.download_dir_input)
        dir_layout.addWidget(download_dir_button)
        main_layout.addLayout(dir_layout)

        # Start Download Button
        download_button = QPushButton('Start Download')
        download_button.clicked.connect(self.start_download)
        main_layout.addWidget(download_button)

        # Add Cancel Download Button
        self.cancel_button = QPushButton('Cancel Download')
        self.cancel_button.clicked.connect(self.cancel_download)
        self.cancel_button.setEnabled(False)  # Initially disabled
        main_layout.addWidget(self.cancel_button)

        # Overall Progress Bar
        overall_progress_label = QLabel('Overall Download Progress:')
        main_layout.addWidget(overall_progress_label)
        self.overall_progress_bar = QProgressBar()
        main_layout.addWidget(self.overall_progress_bar)

        # Download Status Table
        self.download_table = QTableWidget()
        self.download_table.setColumnCount(4)
        self.download_table.setHorizontalHeaderLabels(['Case ID', 'Image ID', 'Status', 'Progress'])
        self.download_table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.download_table)

        # Log Display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        main_layout.addWidget(self.log_display)

    def select_excel_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Excel File', '', 'Excel Files (*.xlsx *.xls)')
        if file_path:
            self.file_path_input.setText(file_path)

    def select_download_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Download Directory')
        if directory:
            self.download_dir_input.setText(directory)

    def start_download(self):
        excel_path = self.file_path_input.text()
        download_dir = self.download_dir_input.text()

        if not excel_path or not download_dir:
            self.log_display.append("Please select both Excel file and download directory.")
            return

        try:
            # Load pathology data with enhanced error handling
            try:
                pathology_data = load_manifest(excel_path)
            except ValueError as ve:
                # More informative error handling for manifest loading
                QMessageBox.critical(self, "Excel File Error",
                    f"Error reading Excel file: {str(ve)}\n\n"
                    "Possible reasons:\n"
                    "- Incorrect file format\n"
                    "- Missing required columns\n"
                    "- Corrupt or incompatible Excel file")
                return
            except Exception as e:
                QMessageBox.critical(self, "Unexpected Error",
                    f"An unexpected error occurred: {str(e)}")
                return

            # Clear previous download data
            self.clear_download_table()

            # Setup download status table
            self.download_table.setRowCount(len(pathology_data))
            self.download_status_map = {}

            # Populate table with initial data
            for row, (_, data_row) in enumerate(pathology_data.iterrows()):
                case_id_item = QTableWidgetItem(str(data_row['Case ID']))
                case_id_item.setFlags(case_id_item.flags() & ~Qt.ItemIsEditable)
                self.download_table.setItem(row, 0, case_id_item)

                image_id_item = QTableWidgetItem(str(data_row['imageId']))
                image_id_item.setFlags(image_id_item.flags() & ~Qt.ItemIsEditable)
                self.download_table.setItem(row, 1, image_id_item)

                status_item = QTableWidgetItem('Pending')
                status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
                self.download_table.setItem(row, 2, status_item)

                progress_item = QTableWidgetItem('0%')
                progress_item.setFlags(progress_item.flags() & ~Qt.ItemIsEditable)
                self.download_table.setItem(row, 3, progress_item)

                # Create a mapping for quick updates
                self.download_status_map[(str(data_row['Case ID']), str(data_row['imageId']))] = row

            # Create download thread
            self.download_thread = PathologyDownloadThread(pathology_data, download_dir)

            # Connect signals
            self.download_thread.overall_progress_signal.connect(self.update_overall_progress)
            self.download_thread.download_status_signal.connect(self.update_download_status)
            self.download_thread.log_signal.connect(self.update_log)
            self.download_thread.complete_signal.connect(self.download_complete)

            # Update UI for download in progress
            self.download_in_progress = True
            self.cancel_button.setEnabled(True)

            # Start the thread
            self.download_thread.start()

        except Exception as e:
            self.log_display.append(f"Unexpected error: {str(e)}")
            QMessageBox.critical(self, "Download Error", str(e))

    def clear_download_table(self):
        """
        Clear the download status table and reset associated data
        """
        self.download_table.clearContents()
        self.download_table.setRowCount(0)
        self.download_status_map = {}
        self.log_display.clear()
        self.overall_progress_bar.setValue(0)

    def cancel_download(self):
        """
        Cancel the ongoing download
        """
        if hasattr(self, 'download_thread') and self.download_thread.isRunning():
            self.download_thread.terminate()
            self.download_thread.wait()

            # Update UI to reflect cancellation
            self.log_display.append("Download cancelled by user.")
            self.download_in_progress = False
            self.cancel_button.setEnabled(False)

            # Update any pending status items to 'Cancelled'
            for row in range(self.download_table.rowCount()):
                status_item = self.download_table.item(row, 2)
                if status_item.text() in ['Pending', 'Downloading']:
                    status_item.setText('Cancelled')
                    status_item.setBackground(QColor(255, 200, 200))  # Light red

    def update_overall_progress(self, current, total):
        progress_percent = int((current / total) * 100)
        self.overall_progress_bar.setValue(progress_percent)

    def update_download_status(self, case_id, image_id, status, progress):
        # Convert case_id and image_id to strings to ensure consistent matching
        case_id = str(case_id)
        image_id = str(image_id)

        # Find the row for this case ID and image ID
        if (case_id, image_id) in self.download_status_map:
            row = self.download_status_map[(case_id, image_id)]

            # Update status column
            status_item = self.download_table.item(row, 2)
            status_item.setText(status)

            # Set color based on status
            if status == 'Complete':
                status_item.setBackground(QColor(200, 255, 200))  # Light green
            elif status == 'Failed' or status == 'Error':
                status_item.setBackground(QColor(255, 200, 200))  # Light red
            elif status == 'Downloading':
                status_item.setBackground(QColor(200, 200, 255))  # Light blue
            else:
                status_item.setBackground(QColor(255, 255, 255))  # White

            # Update progress column
            progress_item = self.download_table.item(row, 3)
            progress_item.setText(f"{progress}%")

    def update_log(self, message):
        self.log_display.append(message)

    def download_complete(self, success):
        self.download_in_progress = False
        self.cancel_button.setEnabled(False)

        if success:
            self.log_display.append("Download process completed!")
            QMessageBox.information(self, "Download Complete", "All files downloaded successfully.")
        else:
            self.log_display.append("Download process failed.")
            QMessageBox.warning(self, "Download Incomplete", "The download process did not complete successfully.")

def main():
    app = QApplication(sys.argv)
    ex = PathologyDownloadManager()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
