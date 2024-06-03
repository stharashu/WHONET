import pandas as pd
from app.Constants import *
import os
from qrlib.QRComponent import QRComponent
from robot.libraries.BuiltIn import BuiltIn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "image/")

class ExcelConverter(QRComponent):

    def __init__(self):
        self.input_file = input_file
        self.output_file = output_file
        self.output_file_csv = output_file_csv
        self.output_file_txt = output_file_txt


    def process_amr_data(self):
        df = pd.read_excel(self.input_file,skiprows=3)

        # Define key columns explicitly
        key_columns = [
            "Patient identification number", "Address", "Age", "Gender", "Institution", 
            "OPD/IPD/ER", "Department", "Date of admission", "Specimen", "Specimendate", 
            "Organism"
        ]
        
        # Rename the columns dynamically
        df.columns = key_columns + df.columns[len(key_columns):].tolist()
        
        # Ensure 'Patient identification number' is not separated by commas
        if 'Patient identification number' in df.columns:
            df['Patient identification number'] = df['Patient identification number'].apply(lambda x: str(int(float(x))) if pd.notna(x) else x)
        
        # Ensure 'Specimen date' is in the correct date format and matches 'SampleReceivedDate'
        if 'Specimen date' in df.columns:
            df['SampleReceivedDate'] = pd.to_datetime(df['Specimen date'], errors='coerce').dt.strftime('%d-%m-%Y')
            df['Specimen date'] = df['SampleReceivedDate']
            df = df.drop(columns=['SampleReceivedDate'])
        
        # Fill down the patient identification number to fill gaps
        df['Patient identification number'] = df['Patient identification number'].ffill()

        # Group by 'Patient identification number' and concatenate antibiotic results
        df_grouped = df.groupby('Patient identification number').apply(lambda x: x.ffill().bfill().iloc[0])

        # Reset the index
        df_grouped.reset_index(drop=True, inplace=True)
        
        # Write processed data to output file
        df_grouped.to_excel(self.output_file, index=False)
        
        # Write processed data to output CSV file
        df_grouped.to_csv(self.output_file_csv, index=False)
        
        # Write processed data to output text file (tab-separated)
        df_grouped.to_csv(self.output_file_txt, sep='\t', index=False)




        # New column names mapping
        # column_names = [
        #     "PatientNo", "Address", "Age", "Gender", "Institution", "OPD/IPD/ER", "Department", 
        #     "Date of admission", "Specimen", "Specimendate", "Organism", "Ampicillin", "Amoxycillin", 
        #     "Cloxacillin", "Penicillin G", "Piperacillin", "Amoxycillin Clavulanic Acid", 
        #     "Ampillicin Sulbactam", "Cefoperazone Sulbactam", "Piperacillin Tazobactam", "Cefalothin", 
        #     "Cephalexin", "Cephazolin", "Cefoxitin", "Cefuroxime", "Cefixime", "Cefotaxime", 
        #     "Cefpodoxime", "Ceftazidime", "Ceftriaxone", "Cefepime", "Aztreonam", "Imipenem", 
        #     "Ertapenem", "Meropenem", "Azithromycin", "Clindamycin", "Erythromycin", "Amikacin", 
        #     "Gentamicin (10 mg)", "Gentamicin (120 mg)", "Streptomycin", "Tobramycin", 
        #     "Nalidixic Acid", "Ciprofloxacin", "Levofloxacin", "Moxifloxacin", "Norfloxacin", 
        #     "Ofloxacin", "Cotrimoxazole", "Doxycycline", "Tetracycline", "Tigecycline", 
        #     "Chloramphenicol", "Nitrofurantion", "Linezolid", "Colistin Sulphate", "Polymyxin B", 
        #     "Teicoplanin", "Vancomycin"
        # ]

        # # Drop the first two rows
        # df = df.drop([0, 1])
        
        # Assign new column names, handle any additional columns as 'Unnamed'
        # df.columns = column_names + ['Unnamed: {}'.format(i) for i in range(len(column_names), len(df.columns))]

        # # Ensure 'PatientNo' is not separated by commas
        # patient_id_column = 'PatientNo'
        # # df[patient_id_column] = df[patient_id_column].astype(str).str.replace(',', '')
        # df[patient_id_column] = df[patient_id_column].apply(lambda x: str(int(float(x))) if pd.notna(x) else x)


        # # Ensure 'SampleReceivedDate' is in the correct date format and matches 'Specimen date'
        # specimen_date_column = 'Specimendate'
        # sample_received_date_column = 'SampleReceivedDate'
        # # df[sample_received_date_column] = pd.to_datetime(df[specimen_date_column], format='%d/%m/%Y', errors='coerce')

        # df[sample_received_date_column] = pd.to_datetime(df[specimen_date_column], errors='coerce').dt.strftime('%d-%m-%Y')

        # # Replace 'Specimen date' with 'SampleReceivedDate' values
        # df[specimen_date_column] = df[sample_received_date_column]

        # # Drop the 'SampleReceivedDate' column at the end
        # df = df.drop(columns=[sample_received_date_column])


        # with open(self.output_file, 'w') as f:
        #     pass
        # # Write processed data to output file
        # df.to_excel(self.output_file, index=False)

        # # Write processed data to output CSV file
        # df.to_csv(self.output_file_csv, index=False)

        # # Write processed data to output text file (tab-separated)
        # df.to_csv(self.output_file_txt, sep='\t', index=False)



        