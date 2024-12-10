# Manuscript of NUTS_calkit
**Non-Uniform Temperature Steel beam Calculation toolKit**  
_Yang. Li, Yong. Wang et al. May 2024, The University of Manchester_

## 1. Python commands:

### 1.1 Creating Beam Object
### Access
*from NUTS_cakit import NUTS_cakit as nc*
*nc.Beam()*

**<<<<< Required arguments >>>>>**  
d:  Section depth  
w:  Section width  
ft: Flange thickness  
wt: Web thickness  
fpl: Plastic strength of beam  
E: Elastic modulus  
G: Shear modulus  
L: Length  
t_dist: Temperature distribtuion in the section  
    Dataformat: [temperature, ratio of the distance from beam top/section depth], 20C <= temperature <= 1200C.  
    Example: [[600,0],[270,0.7],[100,1]]  

**<<<<< Returning objects >>>>>**  
Beam object
 
*b1=nc.Beam(E=210000,G=80770,L=5000,fpl=320,d=320,w=140,ft=10,wt=5,t_dist=[[600, 0], [500, 1]])*

### 1.1.1 Mpl()
 -Beam plastic bending moment

**<<<<< Required arguments >>>>>**  
 -Beam: A NUTS_calkit beam objects

  -*nc.Beam.Mpl()*

### 1.1.2 Mcr()
 -Beam Elastic Critical Bending Moment

**<<<<< Required arguments >>>>>**  
 -Beam: A NUTS_calkit beam objects

  -*nc.Beam.Mcr()*

