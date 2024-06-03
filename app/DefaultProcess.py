import time
import pandas as pd
from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item
from qrlib.QRRunItem import QRRunItem
from WhonetComponent import WhonetComponent
from ExcelConverter import ExcelConverter
from WhonetDataComponent import WhonetDataComponent
from app.Constants import *

class DefaultProcess(QRProcess):

    def __init__(self):
        super().__init__()
        self.whonet_component = WhonetComponent()
        self.register(self.whonet_component)

        self.excel_component = ExcelConverter()
        self.register(self.excel_component)

        self.final_data_component = WhonetDataComponent()
        self.register(self.final_data_component)



        self.data = []

    @run_item(is_ticket=False)
    def before_run(self, *args, **kwargs):

        self.excel_component.process_amr_data()

        self.whonet_component.login()
        self.whonet_component.opening_data_entry()
        data = {'Antibiotic': ['Ampicillin', 'Amoxicillin', 'Cloxacillin'], 'Result': ['R', 'S', 'I']}
        df = pd.DataFrame(data)
        time.sleep(2)
        
        # Assuming self.whonet_component.get_dataframe() returns a DataFrame
        df = self.whonet_component.get_dataframe()
        self.whonet_component.entering_data(df)
        time.sleep(2)
        


        # Set self.data to the rows of the DataFrame
        # self.data = df.to_dict(orient='records')

        # Get run item created by decorator. Then notify to all components about new run item.
        # run_item: QRRunItem = kwargs["run_item"]
        # self.notify(run_item)
        # for i in range(1,100):
        #     run_item.logger.info(i)
        #     time.sleep(1)
        # self.whonet_component.login()
        # self.whonet_component.opening_data_entry()
        # data = {'apple': [1, 2, 3, 4, 5]}
        # df= pd.DataFrame(data) 
        # time.sleep(2)
        # df = self.whonet_component.get_dataframe()
        # self.whonet_component.entering_data(df)
        # time.sleep(2)
        # self.data = ["a", "b"]

    @run_item(is_ticket=False, post_success=False)
    def before_run_item(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

    @run_item(is_ticket=True)
    def execute_run_item(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)
       

        # self.default_component.test()
        run_item.report_data["test"] = args[0]

    @run_item(is_ticket=False, post_success=False)
    def after_run_item(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

    @run_item(is_ticket=False, post_success=False)
    def after_run(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

        self.final_data_component.whonetdata()
        self.whonet_component.close_application()
        # self.default_component.logout()
 
    def execute_run(self):
        for x in self.data:
            self.before_run_item(x)
            self.execute_run_item(x)
            self.after_run_item(x)

