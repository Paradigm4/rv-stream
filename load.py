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

    sys.stderr.write('df_in: {}\n'.format(len(df_in)))
    sys.stderr.write('df_in.dtype[:5]: {}\n'.format(df_in.dtypes[:5]))
    sys.stderr.write('df_in.dtype[-5:]: {}\n'.format(df_in.dtypes[-5:]))

    lst = []
    for line in df_in.itertuples(index=False):
        for j in range(500):
            if line[9 + j] != '0/0':
                lst.append(
                    [line[510], # chrom
                     line[511], # pos
                     1 + j,
                     int(line[9 + j][:1]),
                     int(line[9 + j][2:]),
                     0 if line[9 + j][1:2] == '/' else 1])

    df_out = pandas.DataFrame(
        lst,
        columns='chrom pos p gt1 gt2 phase'.split())

    # Write DataFrame
    scidbstrm.write(df_out)


sys.stderr.write('-- - stop - --\n')
scidbstrm.write()
