# # Student data collected on 17 July 2014
# # Researcher: Dr Wicks, University College Newbury
#
# # The following data relate to N = 20 students. It
# # has been totally made up and so therefore is 100%
# # anonymous.
#
# Subject Sex    DOB      Height  Weight       BP     VO2max
# (ID)    M/F  dd/mm/yy     m       kg        mmHg  mL.kg-1.min-1
# JW-1     M    19/12/95    1.82     92.4    119/76   39.3
# JW-2     M    11/1/96     1.77     80.9    114/73   35.5
# JW-3     F    2/10/95     1.68     69.7    124/79   29.1
# JW-6     M    6/7/95      1.72     75.5    110/60   45.5
# # JW-7    F    28/3/96     1.66     72.4    101/68   -
# JW-9     F    11/12/95    1.78     82.1    115/75   32.3
# JW-10    F    7/4/96      1.60     -       -/-      30.1
# JW-11    M    22/8/95     1.72     77.2    97/63    48.8
# JW-12    M    23/5/96     1.83     88.9    105/70   37.7
# JW-14    F    12/1/96     1.56     56.3    108/72   26.0
# JW-15    F    1/6/96      1.64     65.0    99/67    35.7
# JW-16    M    10/9/95     1.63     73.0    131/84   29.9
# JW-17    M    17/2/96     1.67     89.8    101/76   40.2
# JW-18    M    31/7/96     1.66     75.1    -/-      -
# JW-19    F    30/10/95    1.59     67.3    103/69   33.5
# JW-22    F    9/3/96      1.70     -       119/80   30.9
# JW-23    M    15/5/95     1.97     89.2    124/82   -
# JW-24    F    1/12/95     1.66     63.8    100/78   -
# JW-25    F    25/10/95    1.63     64.4    -/-      28.0
# JW-26    M    17/4/96     1.69     -       121/82   39.


'''
Let's find the average heights of the male and female students.
The columns we need are the second and fourth, and there's no missing data in these columns so we can use np.loadtxt.
'''

# -*- coding: utf-8 -*-
import numpy as np

#  First construct a record dtype for the two fields, then read the relevant columns after skipping the first 9 header lines
fname = 'eg6-a-student-data.txt'
dtype1 = np.dtype([('gender', '|S1'), ('height', 'f8')]) # 自定义数据类型（f8对应float64）。int8，int16，int32，int64 可替换为等价的字符串 'i1'，'i2'，'i4'以及其他。
a = np.loadtxt(fname, dtype=dtype1, skiprows=9, usecols=(1, 3)) # [(b'M', 1.826) (b'M', 1.77) …… (b'F', 1.3) (b'M', 1.69)]
print(a.dtype) # [('gender', 'S1'), ('height', '<f8')]  # byteorder '=':native   '<':little-endian小字节序/低字节序   '>':big-endian大字节序/高字节序 '|':not applicable
'''
The |S1 and |S2 strings are data type descriptors; the first means the array holds strings of length 1, the second of length 2.
The | pipe symbol is the byteorder flag; in this case there is no byte order flag needed, so it's set to |, meaning not applicable.
So '|S1' means a string of length 1.
'''
'''
To find the average heights of the male students, 
we only want to index the records with the gender field as M, for which we can create a boolean array.
'''
m = a['gender'] == b'M'
print(m) # [ True  True False  True …… True False False  True]
print(m.dtype) # bool
'''
m has entries that are True or False for each of the 19 valid records (one is commented out) according to whether the student is male or female.
So the heights of the male and female students can be seen to be:
'''
Lm = a['height'][m] # [1.82 1.77 1.72 1.72 1.83 1.63 1.67 1.66 1.97 1.69]
Lf = a['height'][~m] # [1.68 1.78 1.6  1.56 1.64 1.59 1.7  1.66 1.63]
'''
Therefore, the averages we need are:
'''
m_hav = Lm.mean() # 1.748
f_hav = Lf.mean() # 1.6488888888888888
print('Male Average Height:{:.2f} m, Female Average Height:{:.2f} m.'.format(m_hav, f_hav)) # Male Average:1.75 m, Female Average:1.65 m.

'''
To perform the same analysis on the student weights we have a bit more work to do because there are some missing values (denoted by '-'). 
We could use np.genfromtxt (see Section 6.2.3 of the book), but let's write a converter method instead. 
We'll replace the missing values with the nicely unphysical value of -99. 
The function parse_weight expects a string argument and returns a float:
'''
dtype2 = np.dtype([('gender', '|S1'), ('weight', 'f8')])
def parse_weight(s):
    try:
        return float(s)
    except ValueError:
        return -99
'''
This is the function we want to pass as a converter for column 4:
'''
b = np.loadtxt(fname, dtype=dtype2, skiprows=9, usecols=(1, 4), converters={4:parse_weight}) # 注意parse_weight后没有()，只有函数名
mv = b['weight'] > 0 # elements only True for valid data （将'-'表示的missing数据剔除掉）
m_wav = b['weight'][mv & m].mean() # valid and male （注意不能漏掉b）
f_wav = b['weight'][mv & ~m].mean() # valid and female
print('Male Average Weight: {:.2f} kg, Female Average Weight: {:.2f} kg.'.format(m_wav, f_wav))