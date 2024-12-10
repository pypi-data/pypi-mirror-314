import NUTS_calkit as nc
case=nc.Beam(E=210000,G=80770,L=5000,fpl=320,d=320,w=140,ft=10,wt=5,t_dist=[[600, 0], [500, 1]])
a=case.Mpl()
case.Mcr()

