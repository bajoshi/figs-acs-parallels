import numpy as np

# c1 and c2 are the catalogs for chip1 and chip2

c2 = np.genfromtxt('/Users/bhavinjoshi/acspar/DATA_gs1_28/jcoi1mjvq_flc_2.cat', dtype=None, names=['num','mag','x','y','ra','dec','xw','yw','a_im','b_im','theta_im','theta_w','aw','bw'], skip_header=14)

fh_c2 = open('jcoi1mjvq_flc_2.cat', 'wa')

idx_keep_c2 = np.where(c2['mag'] < 23)[0]

for i in range(len(c2)):
    if i in idx_keep_c2:
        fh_c2.write(str(c2[i]) + '\n')
    else:
        continue
    

fh_c2.close()