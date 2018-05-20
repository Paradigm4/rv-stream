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

    df_out = pandas.DataFrame(
      columns='chrom pos p id ref alt qual flt info fmt gt'.split())
    i = 0
    for line in df_in.itertuples(index=False):
      for j in range(500):
        df_out.loc[i] = [line[510], # chrom
                         line[511], # pos
                         1 + j,
                         line[2],   # id
                         line[3],   # ref
                         line[4],   # pos
                         line[512], # qual
                         line[6],   # flt
                         line[7],   # info
                         line[8],   # fmt
                         line[9 + j]]
        i += 1

    # Write DataFrame
    scidbstrm.write(df_out)


sys.stderr.write('-- - stop - --\n')
scidbstrm.write()
