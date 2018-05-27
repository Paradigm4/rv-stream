import pandas
import random
import sys


def vcf(sample=10, chrom=1, pos=3):
  with open('gen.vcf', 'w') as f:
    f.write('\t'.join('#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT'.split() +
                      ['P{}'.format(1 + i) for i in range(sample)]) + '\n')

    for c in range(chrom):
      for p in range(pos):

        ind = []
        for j in range(sample):
          v = random.random()
          if v <= 404/500.:
            ind.append('0/0')
          elif v <= 494/500.:
            ind.append('0/1')
          else:
            ind.append('1/1')

        f.write('\t'.join(str(e) for e in ([1 + c,
                                            1 + p,
                                            '.',
                                            'A',
                                            'G',
                                            100,
                                            '.',
                                            '.',
                                            'GT'] + ind)) + '\n')


def pheno(sample=10):
  with open('gen.pheno', 'w') as f:
    f.write('fid iid fatid matid sex y1 y2 y3 y4\n')

    for i in range(sample):

      j = random.uniform(0, 9)
      if j <= 4:
        sex = 1
      elif j <= 8:
        sex = 2
      else:
        sex = 0

      y1 = random.random() * 4
      y2 = random.random() * 6 - 4
      y3 = random.random() * 5 - 3
      y4 = random.randint(1, 2)

      f.write(' '.join(str(e) for e in ['P{}'.format(1 + i),
                                        'P{}'.format(1 + i),
                                        0,
                                        0,
                                        sex,
                                        '{:.3f}'.format(y1),
                                        '{:.3f}'.format(y2),
                                        '{:.3f}'.format(y3),
                                        y4]) + '\n')


if __name__ == '__main__':
  args = {}
  try:
    args['sample'] = int(sys.argv[2])
  except:
    pass
  if sys.argv[1] == 'var':
    try:
      args['chrom'] = int(sys.argv[3])
    except:
      pass
    try:
      args['pos'] = int(sys.argv[4])
    except:
      pass
    vcf(**args)
  elif sys.argv[1] == 'pheno':
    pheno(**args)
