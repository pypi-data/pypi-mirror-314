import sys
from PyQt5.QtWidgets import QApplication

# Use absolute import
from tcia_download_manager.gui import PathologyDownloadManager

def main():
    app = QApplication(sys.argv)
    ex = PathologyDownloadManager()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
