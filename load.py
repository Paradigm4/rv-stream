import pandas
import scidbstrm
import sys


sys.stderr.write('-- - start - --\n')

while True:
    # Read DataFrame
    df_in = scidbstrm.read()

    if df_in is None:
        # End of stream
        break

    # sys.stderr.write('df_in: {}\n'.format(len(df_in)))
    # sys.stderr.write('df_in.dtype: {}\n'.format(df_in.dtypes))

    lst = []
    for line in df_in.itertuples(index=False):
        j = 1
        for gt in line[9].split()[1:]:
            if gt != '0/0':
                lst.append(
                    [int(line[0]), # chrom
                     int(line[1]), # pos
                     j,
                     int(gt[:1]),
                     int(gt[2:]),
                     0 if gt[1:2] == '/' else 1])
            j += 1

    df_out = pandas.DataFrame(
        lst,
        columns='chrom pos p gt1 gt2 phase'.split())

    # Write DataFrame
    scidbstrm.write(df_out)


sys.stderr.write('-- - stop - --\n')
scidbstrm.write()
