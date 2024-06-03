import shutil
from qrlib.QRComponent import QRComponent
from robot.libraries.BuiltIn import BuiltIn

# Define the source and destination paths
source_path = r'C:\WHONET\Data\NPL-BIR-2024-3.sqlite'
destination_path = r'C:\Users\acer\Desktop\whonet_entry\NPL-BIR-2024-3.sqlite'

class WhonetDataComponent(QRComponent):

    def __init__(self):
        super().__init__()
        pass

    def whonetdata(self):
        shutil.copyfile(source_path, destination_path)
        BuiltIn().log_to_console("File copied")