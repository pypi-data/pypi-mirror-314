import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QProgressDialog, QApplication, QWidget


class QProgressBarWindow(QWidget):

    def __init__(self, iterable, label="Processing"):
        super().__init__()
        self.iterable = iterable
        self.iterator = iter(iterable)
        self.progress_dialog = QProgressDialog(label, "Cancel", 0, 0)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.show()
        QApplication.processEvents()
        self.total_items = len(iterable)
        self.current_item = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.progress_dialog.setMaximum(self.total_items)

        if self.current_item >= self.total_items:
            self.progress_dialog.close()  # Close the progress dialog
            raise StopIteration

        item = next(self.iterator)
        self.current_item += 1
        self.progress_dialog.setValue(self.current_item-1)  # Update the progress dialog

        return self.current_item, item, self

    def print(self, text):
        if self.progress_dialog is not None:
            self.progress_dialog.setLabelText(text)

# Example usage
if __name__ == "__main__":
    app = QApplication([])
    items = ["apple", "banana", "orange", "grape", "kiwi"]

    #it = tqdm(items)
    for i, item, it in QProgressBarWindow(items):
        # Simulate some time-consuming operation
        time.sleep(1)
        it.print(f"Iteration: {i}, Item: {item}")

    app.exec()