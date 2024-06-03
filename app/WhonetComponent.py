from qrlib.QRComponent import QRComponent
from robot.libraries.BuiltIn import BuiltIn
from RPA.Desktop.Clipboard import Clipboard
from RPA.Desktop import Desktop
from fuzzywuzzy import process
from Constants import *
import time
from RPA.Windows import Windows
from Utils import *
import pandas as pd
import numpy as np
import os
import nepali_datetime as ndt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "image/")


class WhonetComponent(QRComponent):
    
    def __init__(self):
        super().__init__()
        self.desktop = Desktop()
        self.library = Windows()

        self.clip = Clipboard()
    
    def wait_and_click(self, path, time_out=30):
        self.desktop.wait_for_element(f'{path}', timeout=time_out)
        self.desktop.click(f"{path}")
        
    def click_image_and_input(self, image_path, text, key_='', enter=False):
        self.wait_and_click(image_path)
        if key_:
            self.desk.press_keys(key_)
        input_text(text, self.desk, enter=enter)

    def login(self):
        try:
            self.library.windows_run(r"C:\Users\Public\Desktop\WHONET 2023.lnk")
            self.wait_and_click(f'image:"templates/nepal_bir.png"')
            time.sleep(2)
            self.wait_and_click(f'image:"templates/open_lab.png"')
        except:
            pass
    
    def opening_data_entry(self):
        try:
            BuiltIn().log_to_console('pressing alt')
            self.desktop.press_keys("ALT")
            time.sleep(1)
            self.desktop.press_keys("E")
            time.sleep(1)
            self.desktop.press_keys("O")
            time.sleep(2)
            self.desktop.type_text('NPL-BIR-2024-3.sqlite')
            time.sleep(1)
            self.desktop.press_keys("ENTER")
        except:
            pass
    
    def close_application(self):
        try:
            BuiltIn().log_to_console('Closing application')
            self.desktop.press_keys("ALT")
            time.sleep(1)
            self.desktop.press_keys("F4")
            time.sleep(1)
            self.desktop.press_keys("ALT")
            time.sleep(2)
            self.desktop.press_keys("F4")
            time.sleep(1)
        except:
            pass
        
        
    def get_dataframe(self):
        BuiltIn().log_to_console('pressing alt')
        df = pd.read_excel(r"C:\Users\acer\Desktop\whonet_entry\data1.xlsx")
        BuiltIn().log_to_console(df.columns)
        print(df.columns)
        return df

    def entering_data(self, dataframe: pd.DataFrame):
        try:
            # Read organism mapping file
            mapping_df = pd.read_excel(r'C:\Users\acer\Desktop\whonet_entry\Organism Mapping.xlsx', sheet_name='Mapping')
            BuiltIn().log_to_console("Read organism mapping")

            for index, row in dataframe.iterrows():
                id_no = str(row['Patient identification number'])
                self.desktop.type_text(id_no)
                time.sleep(1)

                self.desktop.press_keys('ENTER')
                self.desktop.press_keys('ENTER')
                self.desktop.press_keys('ENTER')


                
                gender = str(row['Gender'])
                if gender.lower().strip() == 'male':
                    gender_whonet = 'm'
                elif gender.lower().strip() == 'female':
                    gender_whonet = 'f'
                elif gender.lower().strip() == 'other':
                    gender_whonet = 'o'
                else:
                    gender_whonet = 'u'
                self.desktop.press_keys(gender_whonet)
                time.sleep(1)

                self.desktop.press_keys('ENTER')
                self.desktop.press_keys('ENTER')

                age = str(row['Age'])
                self.desktop.type_text(age)
                time.sleep(1)
                self.desktop.press_keys('ENTER')
                self.desktop.press_keys('ENTER')

                self.desktop.type_text('lab')
                self.desktop.press_keys('ENTER')

                # Read the column value and process it
                lab_text = str(row['Institution'])  # Replace 'LabColumn' with the actual column name
                first_part = lab_text.split(',')[0].split()[0].upper()  # Extract the first part before a comma or space and capitalize it
                self.desktop.type_text(first_part)    
                self.desktop.press_keys('ENTER')
                self.desktop.type_text('lab')


                # for _ in range(6):
                #     self.desktop.press_keys('ENTER')

                self.desktop.press_keys('ENTER')
                self.desktop.press_keys('ENTER')


                sample_received_date = self.convert_nepal_date_to_english(str(row['Specimendate']).split(' ')[0])
                BuiltIn().log_to_console(sample_received_date)
                # sample_received_date = str(row['SampleReceivedDate']).split(' ')[0]
                self.desktop.type_text(sample_received_date)
                # self.desktop.press_keys('ENTER')

                for _ in range(3):
                    self.desktop.press_keys('ENTER')


                specimen_type = str(row['Specimen'])
                specimen_code = self.map_specimen_type(specimen_type)
                self.desktop.type_text(specimen_code)
                BuiltIn().log_to_console('Specimen type entered')
                # self.desktop.press_keys('ENTER')
                # self.desktop.press_keys('ENTER')

                for _ in range(2):
                    self.desktop.press_keys('ENTER')


                time.sleep(2)

                organism = str(row['Organism'])
                whonet_code = self.map_organism(mapping_df, organism)
                BuiltIn().log_to_console(whonet_code)
                
                if isinstance(whonet_code, float) and np.isnan(whonet_code):
                    BuiltIn().log_to_console('whonet code is NaN, pressing ENTER')
                    self.desktop.press_keys("ENTER")
                else:
                    if whonet_code:  # Check if whonet_code is not empty or None
                        self.desktop.type_text(whonet_code)
                        BuiltIn().log_to_console('typed whonet code')
                        self.desktop.press_keys("ENTER")
                        time.sleep(2)
                        try:
                            self.desktop.find_element(r'image:templates/confirm_whonet.png')
                            self.desktop.press_keys("ENTER")
                        except:
                            pass
                time.sleep(1)


                # organism = str(row['Organism'])
                # whonet_code = self.map_organism(mapping_df, organism)
                # BuiltIn().log_to_console(whonet_code)
                # if whonet_code:
                #     self.desktop.type_text(whonet_code)
                #     BuiltIn().log_to_console('typed whonet code')
                #     self.desktop.press_keys("ENTER")
                #     time.sleep(2)
                #     try:
                #         self.desktop.find_element(r'image:templates/confirm_whonet.png')
                #         self.desktop.press_keys("ENTER")
                #     except:
                #         pass
                # elif whonet_code == 'nan':
                #     self.desktop.press_keys("ENTER")
                #     BuiltIn().log_to_console("No whonet code")
                # time.sleep(1)


                for _ in range(8):
                    self.desktop.press_keys('ENTER')
                
                self.enter_antibiotic_results(row)
                
                time.sleep(2)

                # self.desktop.press_keys('ENTER')
                BuiltIn().log_to_console("HEREEEEEEEEEE")
                local_spec = str(row['Organism']).replace('.', '')
                BuiltIn().log_to_console(local_spec)
                self.desktop.type_text(local_spec)
                time.sleep(2)

                BuiltIn().log_to_console("Entered organism into LOCAL_SPEC")

                
                # self.desktop.press_keys('ENTER')
                time.sleep(.5)

                BuiltIn().log_to_console("HEREEEEEEEEEE")

                # self.desktop.press_keys('ENTER')
                # time.sleep(.5)
                # self.desktop.press_keys('ENTER')

                time.sleep(5)

                self.wait_and_click(f'image:"templates/save_isolate.png"')
                time.sleep(2)
                self.wait_and_click(f'image:"templates/ok_press.png"')
                time.sleep(2)
                # self.desktop.press_keys("ENTER")
                
        except Exception as e:
            BuiltIn().log_to_console(e)
            raise e
    
  
    def convert_nepal_date_to_english(self, nepal_date):
        try:
            # Assuming the date format is 'YYYY-MM-DD'
            year, month, day = map(str, nepal_date.split('-'))
            bs_date = ndt.date(year, month, day)
            ad_date = bs_date.to_datetime_date()
            return ad_date.strftime('%d-%m-%Y')
        except Exception as e:
            BuiltIn().log_to_console(f"Error converting date: {e}")
            return nepal_date


    def map_specimen_type(self, specimen_type):
        specimen_code_map = {
            'urine': 'ur', 'pus': 'ps', 'swab': 'sb', 'aspirate': 'at',
            'plueral': 'pf', 'fluid': 'fl', 'tissue': 'ti', 'blood': 'bl',
            'sputum': 'sp', 'stool': 'st', 'urethra': 'ue', 'tracheal': 'tr',
            'bile': 'bi'
        }
        for key in specimen_code_map:
            if key in specimen_type.lower():
                return specimen_code_map[key]
        return ''

    def map_organism(self, mapping_df, organism):
        filtered_row = mapping_df.loc[mapping_df['MIDAS'] == organism, 'WHO Code']
        if not filtered_row.empty:
            return filtered_row.values[0]
        return None
    
    def enter_antibiotic_results(self, row):
        antibiotics_mapping = {
        'Ampicillin': 'AMP',
        'Amoxycillin': 'AMX',
        'Cloxacillin': 'CLO',
        'Penicillin G': 'PEN',
        'Piperacillin': 'PIP',
        'Amoxycillin Clavulanic Acid': 'AMC',
        'Ampillicin Sulbactam' : 'SAM',
        'Cefoperazone Sulbactam' : 'CSL',
        'Piperacillin Tazobactam': 'TZP',
        'Cephalexin': 'LEX',
        'Cefoxitin': 'FOX',
        'Cefuroxime':'CXM',
        'Cefixime': 'CFM',
        'Cefotaxime': 'CTX',
        'Cefpodoxime': 'CPD',
        'Ceftazidime': 'CAZ',
        'Ceftriaxone': 'CRO',
        'Cefepime':'FEP',
        'Aztreonam': 'ATM',
        'Imipenem': 'IPM',
        'Ertapenem':'ETP',
        'Meropenem': 'MEM',
        'Azithromycin': 'AZM',
        'Clindamycin': 'CLI',
        'Erythromycin': 'ERY',
        'Amikacin': 'AMK',
        'Gentamicin (10 mg)' : 'GEN',
        'Gentamicin (120 mg)' : 'GEH',
        'Streptomycin' : 'STR',
        'Tobramycin': 'TOB',
        'Nalidixic Acid': 'NAL',
        'Ciprofloxacin': 'CIP',
        'Levofloxacin': 'LVX',
        'Moxifloxacin': 'MFX',
        'Norfloxacin': 'NOR',
        'Ofloxacin': 'OFX',
        'Doxycycline':'DOX',
        'Tetracycline':'TCY',
        'Tigecycline': 'TGC',
        'Chloramphenicol': 'CHL',
        'Nitrofurantion':'NIT',
        'Linezolid': 'LNZ',
        'Colistin Sulphate': 'COL',
        'Polymyxin B':'POL',
        'Teicoplanin': 'TEC',
        'Vancomycin': 'VAN',
        
            }

        for antibiotic, whonet_code in antibiotics_mapping.items():
            try:
                result = str(row.get(antibiotic, '')).strip().upper()
                BuiltIn().log_to_console(f"Processing antibiotic: {antibiotic}, Result: {result}")

                if result in ['R', 'S', 'I']:
                    self.desktop.press_keys(result)
                    BuiltIn().log_to_console(f"Entered result for {antibiotic}: {result}")
                elif result == '' or 'NAN':
                    BuiltIn().log_to_console(f"No data for {antibiotic}, leaving it empty.")
                else:
                #     self.desktop.press_keys('U')  # Unknown or unreported
                    BuiltIn().log_to_console(f"Entered unknown result for {antibiotic}")

                self.desktop.press_keys('ENTER')
                time.sleep(0.5)  # Adding a small delay to ensure the key press is registered

            except Exception as e:
                BuiltIn().log_to_console(f"Error processing {antibiotic}: {e}")
                raise e


        # for antibiotic, column_name in antibiotics.items():
        #     result = str(row[column_name])
        #     if result.lower().strip() in ['r', 's', 'i']:
        #         self.desktop.press_keys(result)
        #     self.desktop.press_keys('ENTER')

    # def enter_antibiotic_results(self, row):
    #     antibiotics = [
    #         'AMIKACIN', 'Amoxycillin', 'Ampicillin', 'Aztreonam', 'Cefipime',
    #         'Cefotaxime', 'Cefoxitin', 'Ceftazidime', 'Ceftriaxone', 'Chloramphenicol',
    #         'Ciprofloxacin', 'Clindamycin', 'Doxycyclin', 'Erythromycin', 'Gentamycin',
    #         'Imipenem', 'Meropenem', 'NalidixicAcid', 'Nitrofurantoin', 'Norfloxacin',
    #         'Oxacillin', 'Ofloxacin', 'PolymixinB', 'PiperacillinTazobactam',
    #         'Teicoplanin', 'Tetracyclin', 'Tobramycin', 'Trimethoprim', 'Vancomycin'
    #     ]

    #     for antibiotic in antibiotics:
    #         result = str(row[antibiotic])
    #         if result.lower().strip() in ['r', 's', 'i']:
    #             self.desktop.press_keys(result)
    #         self.desktop.press_keys('ENTER')
    
    # def entering_data(self, dataframe: pd.DataFrame):
    #     try:
    #         df = pd.read_excel(r'C:\Users\acer\Desktop\whonet_entry\Organism Mapping.xlsx', sheet_name='Mapping')
    #         BuiltIn().log_to_console("read organism")

    #         for row in dataframe.iterrows():
    #             id_no = str(row['PatientNo'])
    #             self.desktop.type_text(id_no)
    #             time.sleep(1)
    #             self.desktop.press_keys('ENTER')
    #             self.desktop.press_keys('ENTER')
    #             # last_name = full_name[last_index+1:]
    #             # self.desktop.type_text(last_name)
    #             # for letter in last_name:
    #             #     self.desktop.press_keys(letter)
    #             self.desktop.press_keys('ENTER')
                
    #             gender = str(row['Sex'])
    #             if gender.lower().strip() == 'male':
    #                 gender_whonet = 'm'
    #             elif gender.lower().strip() == 'female':
    #                 gender_whonet = 'f'
    #             elif gender.lower().strip() == 'other':
    #                 gender_whonet = 'o'
    #             else:
    #                 gender_whonet = 'u'
    #             self.desktop.press_keys(gender_whonet)
    #             time.sleep(1)
                
    #             self.desktop.press_keys('ENTER')
    #             self.desktop.press_keys('ENTER')

                

    #             age = str(row['Age'])
    #             self.desktop.type_text(age)
    #             time.sleep(1)
    #             self.desktop.press_keys('ENTER')
    #             self.desktop.press_keys('ENTER')
                
    #             self.desktop.press_keys('ENTER')
    #             self.desktop.press_keys('ENTER')
    #             self.desktop.press_keys('ENTER')
    #             self.desktop.press_keys('ENTER')
                
    #             self.desktop.press_keys('ENTER')
                   
    #             # sample_received_no = str(row['sampleno'])
    #             # self.desktop.type_text(sample_received_no)
                
    #             # for i in sample_received_no:
    #             #     self.desktop.press_keys(i) 
    #             self.desktop.press_keys('ENTER')
                
    #             sample_received_date = str(row['SampleReceivedDate']).split(' ')[0]
    #             BuiltIn().log_to_console(sample_received_date)
    #             self.desktop.type_text(sample_received_date)
    #             self.desktop.press_keys('ENTER')
                
    #             # for i in sample_received_date:
    #             specimen_type = str(row['Specimen'])
    #             if 'urine' in str(specimen_type).lower():
    #                 specimen_code = 'ur'
    #             elif 'pus' in str(specimen_type).lower():
    #                 specimen_code = 'ps'
    #             elif 'swab' in str(specimen_type).lower():
    #                 specimen_code = 'sb'
    #             elif 'aspirate' in str(specimen_type).lower():
    #                 specimen_code = 'at'
    #             elif 'plueral' in str(specimen_type).lower():
    #                 specimen_code = 'pf'
    #             elif 'fluid' in str(specimen_type).lower():
    #                 specimen_code = 'fl'
    #             elif 'tissue' in str(specimen_type).lower():
    #                 specimen_code = 'ti'
    #             elif 'blood' in str(specimen_type).lower():
    #                 specimen_code = 'bl'
    #             elif 'sputum' in str(specimen_type).lower():
    #                 specimen_code = 'sp'
    #             elif 'stool' in str(specimen_type).lower():
    #                 specimen_code = 'st'
    #             elif 'urethra' in str(specimen_type).lower():
    #                 specimen_code = 'ue'
    #             elif 'tracheal' in str(specimen_type).lower():
    #                 specimen_code = 'tr'
    #             elif 'bile' in str(specimen_type).lower():
    #                 specimen_code = 'bi'
                    
    #             else:
    #                 specimen_code = ''
                    
                
    #             self.desktop.type_text(specimen_code)
    #             #     self.desktop.press_keys(i)
    #             BuiltIn().log_to_console('upto date')
    #             self.desktop.press_keys('ENTER')
    #             self.desktop.press_keys('ENTER')
                
    #             organism = str(row['Result'])
    #             filtered_row = df.loc[df['MIDAS']==organism, 'WHO Code']
    #             if not filtered_row.empty:
    #                 value = filtered_row.values[0]
    #                 self.desktop.type_text(str(value))
    #                 self.desktop.press_keys("ENTER")
    #                 time.sleep(2)
    #                 try:
    #                     self.desktop.find_element(r'image:templates/confirm_whonet.png')
    #                     self.desktop.press_keys("ENTER")
    #                 except:
    #                     pass
    #             else:
    #                 pass
    #             time.sleep(1)


    #             #TODO: Organism mapping
    #             for _ in range(9):
    #                 self.desktop.press_keys('ENTER')
                
    #             amk = str(row['AMIKACIN'])
    #             BuiltIn().log_to_console(amk)
    #             if amk.lower().strip() in ['r', 's', 'i']:
    #                 BuiltIn().log_to_console('ka bata ya aayo')
    #                 self.desktop.press_keys(amk)
    #             self.desktop.press_keys('ENTER')
                
    #             amc = str(row['Amoxycillin'])
    #             if amc.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(amc)
    #             self.desktop.press_keys('ENTER')
                
    #             amp = str(row['Ampicillin'])
    #             if amp.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(amp)
    #             self.desktop.press_keys('ENTER')
                
    #             atm = str(row['Aztreonam'])
    #             if atm.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(atm)
    #             self.desktop.press_keys('ENTER')
                
    #             fep = str(row['Cefipime'])
    #             if fep.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(fep)
    #             self.desktop.press_keys('ENTER')
                
    #             ctx = str(row['Cefotaxime'])
    #             if ctx.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(ctx)
    #             self.desktop.press_keys('ENTER')
                
    #             # ctc = str(row['Cefotaxime'])
    #             # if ctc.lower().strip() in ['r', 's', 'i']:
    #             #     self.desktop.press_keys(ctc)
    #             self.desktop.press_keys('ENTER')
                
    #             fox = str(row['Cefoxitin'])
    #             if fox.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(fox)
    #             self.desktop.press_keys('ENTER')
                
    #             caz = str(row['Ceftazidime'])
    #             if caz.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(caz)
    #             self.desktop.press_keys('ENTER')
                
    #             # caz = str(row['Ceftazidime'])
    #             # if caz.lower().strip() in ['r', 's', 'i']:
    #             #     self.desktop.press_keys(caz)
    #             self.desktop.press_keys('ENTER')
                
    #             # caz = str(row['Ceftazidime'])
    #             # if caz.lower().strip() in ['r', 's', 'i']:
    #             #     self.desktop.press_keys(caz)
    #             self.desktop.press_keys('ENTER')
                
    #             cro = str(row['Ceftriaxone'])
    #             if cro.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(cro)
    #             self.desktop.press_keys('ENTER')
                
    #             # cro = str(row['Ceftriaxone'])
    #             # if cro.lower().strip() in ['r', 's', 'i']:
    #             #     self.desktop.press_keys(cro)
    #             self.desktop.press_keys('ENTER')
                
    #             chl = str(row['Chloramphenicol'])
    #             if chl.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(chl)
    #             self.desktop.press_keys('ENTER')
                
    #             cip = str(row['Ciprofloxacin'])
    #             if cip.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(cip)
    #             self.desktop.press_keys('ENTER')
                
    #             cli = str(row['Clindamycin'])
    #             if cli.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(cli)
    #             self.desktop.press_keys('ENTER')
                
    #             dox = str(row['Doxycyclin'])
    #             if dox.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(dox)
    #             self.desktop.press_keys('ENTER')
                
    #             ery = str(row['Erythromycin'])
    #             if ery.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(ery)
    #             self.desktop.press_keys('ENTER')
                
    #             gen = str(row['Gentamycin'])
    #             if gen.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(gen)
    #             self.desktop.press_keys('ENTER')
    #             self.desktop.press_keys('ENTER')
                
    #             ipm = str(row['Imipenem'])
    #             if ipm.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(ipm)
    #             self.desktop.press_keys('ENTER')
                
    #             mem = str(row['Meropenem'])
    #             if mem.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(mem)
    #             self.desktop.press_keys('ENTER')
    #             self.desktop.press_keys('ENTER')
                
    #             nal = str(row['NalidixicAcid'])
    #             if nal.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(nal)
    #             self.desktop.press_keys('ENTER')
                
    #             nit = str(row['Nitrofurantoin'])
    #             if nit.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(nit)
    #             self.desktop.press_keys('ENTER')
                
    #             nor = str(row['Norfloxacin'])
    #             if nor.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(nor)
    #             self.desktop.press_keys('ENTER')
                
    #             oxa = str(row['Oxacillin'])
    #             if oxa.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(oxa)
    #             self.desktop.press_keys('ENTER')
                
    #             ofx = str(row['Ofloxacin'])
    #             if ofx.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(ofx)
    #             self.desktop.press_keys('ENTER')
                
    #             pen = str(row['PolymixinB'])
    #             if pen.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(pen)
    #             self.desktop.press_keys('ENTER')
                
    #             tzp = str(row['PiperacillinTazobactam'])
    #             if tzp.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(tzp)
    #             self.desktop.press_keys('ENTER')
    #             self.desktop.press_keys('ENTER')
    #             self.desktop.press_keys('ENTER')
                
    #             tec = str(row['Teicoplanin'])
    #             if tec.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(tec)
    #             self.desktop.press_keys('ENTER')
                
    #             tcy = str(row['Tetracyclin'])
    #             if tcy.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(tcy)
    #             self.desktop.press_keys('ENTER')
    #             self.desktop.press_keys('ENTER')
                
    #             tob = str(row['Tobramycin'])
    #             if tob.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(tob)
    #             self.desktop.press_keys('ENTER')
                
    #             sxt = str(row['Trimethoprim'])
    #             if sxt.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(sxt)
    #             self.desktop.press_keys('ENTER')
                
    #             van = str(row['Vancomycin'])
    #             if van.lower().strip() in ['r', 's', 'i']:
    #                 self.desktop.press_keys(van)
    #             self.desktop.press_keys('ENTER')
                
    #             time.sleep(2)
                
    #             for _ in range(18):
    #                 self.desktop.press_keys('TAB')
    #             # self.desktop.type_text('bir')
    #             # self.desktop.press_keys('ENTER')
    #             # self.desktop.type_text('lab')    
    #             # self.desktop.press_keys('ENTER')
    #             # self.desktop.type_text('lab')    
    #             for _ in range(6):
    #                 self.desktop.press_keys('TAB')
                
                
    #             time.sleep(5)
                
                
    #             self.wait_and_click(f'image:"templates/save_isolate.png"')
                
    #             # for _ in range(48):
    #             #     self.desktop.press_keys('TAB')
    #             time.sleep(2)
                
    #             self.desktop.press_keys("ENTER")
    #             # BuiltIn().log_to_console(first_name)
    #             # BuiltIn().log_to_console(last_name)
    #             # time.sleep(100)
                
    #     except Exception as e:
    #         BuiltIn().log_to_console(e)
    

    
    
    

