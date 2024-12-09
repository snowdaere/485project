# This code was modified from Carter J. Humphrey's bufkit-api
# https://github.com/HumphreysCarter/bufkit-api

# BSD 3-Clause License

# Copyright (c) 2024, Carter J. Humphreys
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy as np
import pandas as pd


def parse_file(surface_data):
    """
    """
    data_array, tmp_str = [], ''

    for line in surface_data:
        # Break for new section
        if '/' in line:
            data_array.append(tmp_str.split(' '))
            tmp_str = line
        # Append current section
        else:
            tmp_str += (' ' + line)

    # Capture last section
    data_array.append(tmp_str.split(' '))

    # Get headers from data array
    headers = data_array.pop(1)

    # Change YYMMDD/HHMM header to TIME
    i = headers.index('YYMMDD/HHMM')
    headers[i] = 'TIME'

    # Remove empty row
    data_array.remove([''])

    # Create Pandas Dataframe
    df = pd.DataFrame(data_array, columns=headers)

    # Change time to datatime object
    df['TIME'] = pd.to_datetime(df['TIME'], format='%y%m%d/%H%M')

    # Change station ID to int
    df = df.astype({'STN': 'int64'})

    # Change data to be float64
    float_headers = headers[2:]
    df[float_headers] = df[float_headers].astype('float64')

    # Set null values
    df[float_headers] = df[float_headers].replace(-9999.00, np.nan)

    return df


def read_file(file_data):
    # Create temp data list and record trigger
    tmp_data, record_surface = [], False

    # Loop over each line in data file
    for line in file_data:

        # check for presence of HTML, which indicates that the data retrieval failed
        if line[0] == '<':
            raise Exception('Original Bufkit File failed to Download, is HTML')
        # clean \n from line - note that this will cause the reading to fail partially
        # through the file if an \n is present between surface data times
        line = line.replace('\n', '')

        # Find start of surface data section
        if 'STN YYMMDD/HHMM' in line:
            record_surface = True

        # Write surface data to temporary data string
        if record_surface and line != '':
            tmp_data.append(line)

        # Break out of loop when end key reached
        elif record_surface and line == '':
            break

    return tmp_data


class surface:

    def __new__(cls, file_data):
        # Create a new instance of the class
        instance = super(surface, cls)

        # Read data from file
        tmp_data = read_file(file_data)

        # Call parser for data list
        df = parse_file(tmp_data)

        # Return the DataFrame object
        return df
