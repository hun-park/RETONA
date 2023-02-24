import random

f = open('data/control_bits.csv', 'w')

for pi in range(0,180,5):
    for theta in range(0,180,5):
        rand = random.randint(1,63)
        f.write(str(pi)+','+str(theta)+','+
        '{0:06b}'.format(rand)+','+'{0:06b}'.format(rand)+','+'{0:06b}'.format(rand)+','+'{0:06b}'.format(rand)+','+'{0:06b}'.format(rand)+','+'{0:06b}'.format(rand)+'\n')

f.close