from random import randint
with open('selfshares.txt','w') as f:
    for _ in range(100):
        s = str('0 '*365)
        #if _ in [0]:
        #    s = ' '.join([str(1) for i in range(365)])
        #print(s)
        #s = '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'
        f.write(s)
        f.write('\n')