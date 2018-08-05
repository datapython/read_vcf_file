# read vcf file and convert to csv.
# For convenience, change working directory to the directory containing the vcf file.
# 2018_8_2 @8:24 AM By Shengguo, email: sghello2000@yahoo.com.

import pandas as pd


def read_vcf(file):
    # Read the comments of vcf file.
    with open(file, 'r') as f:
        comments = []
        for line in f:
            if line.startswith('#'):
                comments.append(line.strip())
    
    # Read the tsv of vcf file.
    vcf = pd.read_csv(file, delimiter = '\t', header = (len(comments) - 1))

    # Update column names.
    vcf.rename(columns = dict(zip(list(vcf.columns), [a.replace("#", '') for a in list(vcf.columns)])), inplace = True)
    return (comments, vcf)


def get_info_column_value():
     # Convert row of INFO to list.
    vcf = read_vcf(file)[1]
    info = vcf['INFO']
    info = [i.split(';') for i in info]
    info = [[j.split('=') for j in k] for k in info]
    
    # Collect all unique values from all rows of INFO column.
    all_values = []
    [all_values.append(a[0]) for b in info for a in b if a[0] not in all_values]
    return (info, all_values)


def transform_info_column():
    info = get_info_column_value()[0]
    values = get_info_column_value()[1]

    # Fill out all unique values for all the rows. The missing ones take NaN.
    [k.append([l, 'NaN']) for l in values for k in info if l not in [m[0] for m in k]]

    infos =[[(i[0], i[1]) if (len(i) > 1) else (i[0], i[0]) for i in j] for j in info]
    return (values, infos)


def update_vcf():
    """
    Update vcf dataframe file by adding new columns. Each of them represents a INFO value appeared at least once in the vcf dataset.
    """
    vcf = read_vcf(file)[1]
    cNames = transform_info_column()[0]
    xcols = transform_info_column()[1]   
    xcols = [dict(row) for row in xcols]

    # Add new columns to vcf dataframe.
    for name in cNames:
        vcf[name] = [r[name] for r in xcols]
    return vcf


def cleanup():
    """
    Drop the INFO column and update all missing symbol "." to NaN.
    """
    df = pd.DataFrame(update_vcf())
    df.drop(columns = ['INFO'], inplace = True)
    df.replace({'.': 'NaN'}, inplace = True)

    # Save to csv file to the current working directory.
    fName = file.split('.')[0] + '.csv'
    df.to_csv(fName)
    print(f"{'*'*25}\nIt is all done. You can find your saved file named {fName} in the current working directory.")
   

def main():
    print(f"Welcome to use this python snippet for reading your vcf file!\n{'*'*25}")
    file = input('Please input your file name: ')  
    return file


if __name__ == "__main__":    
    file = main()
    cleanup()

    
