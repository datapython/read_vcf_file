# read vcf file 
# For convenience, change working directory to the directory containing the vcf file
# 2018_8_2 @8:24 AM By Shengguo, email: sghello2000@yahoo.com. 

import pandas as pd
import time

def read_vcf(file):
    # read the comments section of the vcf file
    with open(file, 'r') as f:
        comments = []
        for line in f:
            if line.startswith('#'):
                comments.append(line.strip())
    
    # read the tsv portion of vcf file
    vcf = pd.read_csv(file, delimiter = '\t', header = (len(comments) - 1))

    # In general, the vcf has the 1st column named #CHROM, we'd like to change it to CHROM.
    vcf.rename(columns = dict(zip(list(vcf.columns), [a.replace("#", '') for a in list(vcf.columns)])), inplace = True)

    return (comments, vcf)


def get_info_column_value():
    # Since the column INFO contains multiple values, we'd like to separate them and extract the values into a list.

    vcf = read_vcf(file)[1]
    info = vcf['INFO']

    # Convert each row as a list from INFO column.
    info = [i.split(';') for i in info]
    info = [[j.split('=') for j in k] for k in info]
    
    # Collect all values in order from all rows of INFO column
    
    all_values = []
    [all_values.append(a[0]) for b in info for a in b if a[0] not in all_values]
    
    return (info, all_values)


def transform_info_column():
    """
    Try to turn the original INFO column values into a list of dicts (row) for later easier picking up values to add new columns.
    """
    info = get_info_column_value()[0]
    values = get_info_column_value()[1]

    # Compare values in each row, any one is missing from the list of values in that row will be added to that row with NaN value. It is inplace update.
    [k.append([l, 'NaN']) for l in values for k in info if l not in [m[0] for m in k]]

    infos =[[(i[0], i[1]) if (len(i) > 1) else (i[0], i[0]) for i in j] for j in info]

    return (values, infos)


def update_vcf():
    """
    Using the above function generated infos for INFO column to integrate the splitted info values to the primarily read_in vcf dataframe file by adding new columns. Each of them represents a INFO value appeared at least once in the vcf dataset.
    """
    vcf = read_vcf(file)[1]
    cNames = transform_info_column()[0]
    xcols = transform_info_column()[1]   
        
    # To make it easier to integrate into vcf dataframe, we 'd transform xcols evry row into a list of dicts.
    xcols = [dict(row) for row in xcols]

    # Adding new columns to vcf dataframe.
    for name in cNames:
        vcf[name] = [r[name] for r in xcols]

    return vcf


def cleanup():
    """
    Drop the INFO column and update all missing symbol "." into NaN.
    """
    df = pd.DataFrame(update_vcf())
    df.drop(columns = ['INFO'], inplace = True)
    df.replace({'.': 'NaN'}, inplace = True)

    # SAve the df as csv to the current working dir with timestamp
    df.to_csv('clean_df_' + time.strftime("%Y%m%d_%H%M%S" + '.csv'))

    print('It is all done. You can find your file in the current working directory.')
    return df


def main():
    print("Welcome to use this python snippet for reading your vcf file!\nThe returned csv file is save in your current working directory with name vcf_timestamp.")

    file = input('Please input file name: ')  
    return file


if __name__ == "__main__":    
    file = main()
    cleanup()

    
