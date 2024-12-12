import datetime
import os

__description__ = 'Data Post-Processing Package for Angle-resolved photoemission spectroscopy (ARPES) Data'
__author__ = 'Bin Cao, Advanced Materials Thrust, Hong Kong University of Science and Technology (Guangzhou)'
__author_email__ = 'binjacobcao@gmail.com'
__url__ = 'https://github.com/Bin-Cao/PyArpes'

os.makedirs('PyArpes', exist_ok=True)
now = datetime.datetime.now()
formatted_date_time = now.strftime('%Y-%m-%d %H:%M:%S')
print('PyArpes, Bin CAO, HKUST(GZ)' )
print('URL : https://github.com/Bin-Cao/PyArpes')
print('Executed on :',formatted_date_time, ' | Have a great day.')  
print('='*80)