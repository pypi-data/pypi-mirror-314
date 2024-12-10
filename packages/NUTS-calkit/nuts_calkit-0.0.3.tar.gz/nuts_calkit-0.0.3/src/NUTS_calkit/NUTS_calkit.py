from sympy import symbols, solve
from math import pi
class Beam:
    def __init__(self,*args, **kwargs):
        self.t_dist=kwargs.get('t_dist', None)
        self.L=kwargs.get('L',None)
        self.E=kwargs.get('E',None)
        self.G=kwargs.get('G',None)
        self.fpl=kwargs.get('fpl', None)
        self.d=kwargs.get('d', None)
        self.w=kwargs.get('w', None)
        self.ft=kwargs.get('ft', None)
        self.wt=kwargs.get('wt', None)
    def ela_red(self,temp):
        coefficient=[[20,1],[100,1],[200,0.9],[300,0.8],[400,0.7],[500,0.6],[600,0.31],[700,0.13],[800,0.09],[900,0.0675],[1000,0.045],[1100,0.0225],[1200,0]]
        for i in range(len(coefficient)-1):
            if temp >= coefficient[i][0] and temp < coefficient[i+1][0]:
                co_of_red = (temp-coefficient[i][0])/(coefficient[i+1][0]-coefficient[i][0])*(coefficient[i+1][1]-coefficient[i][1])+coefficient[i][1]
        return co_of_red
    def y_neutral_stre(self,y_neutral,stre_dist):
        for i in range(len(stre_dist)-1):
            if stre_dist[i][1]<=y_neutral and stre_dist[i+1][1]>y_neutral:
                y_neutral_stre=(y_neutral-stre_dist[i][1])*(stre_dist[i+1][0]-stre_dist[i][0])/(stre_dist[i+1][1]-stre_dist[i][1])+stre_dist[i][0]
        return y_neutral_stre
    def interpolation(self,a,stre_dist):
        for i in  range(len(stre_dist)-1):
            if stre_dist[i][1] <= a and stre_dist[i+1][1] > a:
                y_inter = (a-stre_dist[i][1])*(stre_dist[i+1][0]-stre_dist[i][0])/(stre_dist[i+1][1]-stre_dist[i][1])+stre_dist[i][0]
        return y_inter
    def stre_red(self,temp):
        coefficient=[[20,1],[100,1],[200,1],[300,1],[400,1],[500,0.78],[600,0.47],[700,0.23],[800,0.11],[900,0.06],[1000,0.04],[1100,0.02],[1200,0]]
        for i in range(len(coefficient)-1):
            if temp >= coefficient[i][0] and temp < coefficient[i+1][0]:
                co_of_red = (temp-coefficient[i][0])/(coefficient[i+1][0]-coefficient[i][0])*(coefficient[i+1][1]-coefficient[i][1])+coefficient[i][1]
        return co_of_red
    def intemp(self,a,b,c):
        d_temp=(a-b[0])*(b[1]-c[1])/(b[0]-c[0])+b[1]
        return d_temp
    def Sort(self,sub_li):
        sub_li.sort(key = lambda x: x[1])
        return sub_li
    def elastic_neutral_axis(self):
        d=self.d
        w=self.w
        tf=self.ft
        tw=self.wt
        tempdist=self.t_dist
        temp=[]
        int_temp=[]
        rev_int_temp=[]
        # temperatures
        for i in range(len(tempdist)):
            temp.append(tempdist[i][0])
        temp.sort()
        for i in range(len(temp)-1):
            for j in range(1,13):
                if 100*j<tempdist[i][0] and 100*j>tempdist[i+1][0] or 100*j>tempdist[i][0] and 100*j<tempdist[i+1][0]:
                    int_temp.append(100*j)
        rev_int_temp=int_temp.copy()
        rev_int_temp.reverse()
        # Interpolation of temperatures and positions
        for k in range(len(tempdist)+len(int_temp)-1):
            if tempdist[k][0]>tempdist[k+1][0]:
                for j in range(1,13):
                    if tempdist[k][0]>j*100 and tempdist[k+1][0]<j*100:
                        pos=self.intemp(j*100,tempdist[k],tempdist[k+1])
                        tempdist.insert(k+1,[j*100,pos])
            elif tempdist[k][0]<tempdist[k+1][0]:
                for j in range(1,13):
                    if tempdist[k][0]<j*100 and tempdist[k+1][0]>j*100:
                        pos=self.intemp(j*100,tempdist[k],tempdist[k+1])
        disp_tempdist=[]
        for i in tempdist:
            disp_tempdist.append([i[0],round(i[1],2)])
        ela_dist=[]
        i=0
        for i in range(len(tempdist)):
            ela_dist.append(tempdist[i].copy())
        i=0
        for ela_pt in ela_dist:
            co_of_red=self.ela_red(ela_pt[0])
            ela_dist[i][0]=co_of_red
            i=i+1
        a_s=tf/d
        b_s=(d-tf)/d
        uf_lower_ela=self.interpolation(a_s,ela_dist)
        lf_upper_ela=self.interpolation(b_s,ela_dist)
        uf_lower_temp=self.interpolation(a_s,tempdist)
        lf_upper_temp=self.interpolation(b_s,tempdist) 
        num_d_uf=0
        num_d_lf=0
        num_temp_uf=0
        num_temp_lf=0
        for i in range(len(tempdist)):
            if tempdist[i][1]==a_s:
                num_temp_uf+=1
        for i in range(len(tempdist)):
            if tempdist[i][1]==b_s:
                num_temp_lf+=1
        if num_temp_uf==0:
            tempdist.append([uf_lower_temp,a_s])
        if num_temp_lf==0:
            tempdist.append([lf_upper_temp,b_s])
        tempdist=self.Sort(tempdist)  
        for i in range(len(ela_dist)):
            if ela_dist[i][1]==a_s:
                num_d_uf+=1 
        for i in range(len(ela_dist)):
            if ela_dist[i][1]==b_s:
                num_d_lf+=1
        if num_d_uf==0:
            ela_dist.append([uf_lower_ela,a_s])
        if num_d_lf==0:
            ela_dist.append([lf_upper_ela,b_s])
        ela_dist=self.Sort(ela_dist)
        print('Temperature distribution [temp(°C),deepness/depth]:',tempdist)
        print('Elasticity distribution [Elasticity reduction factor,deepness/depth]:',ela_dist)
        counter_half=0
        for i in range(len(ela_dist)-1):
            if ela_dist[i+1][1]==0.5:
                break
            else:
                counter_half=counter_half+1
        i=0
        disp_ela_dist=[]
        for i in ela_dist:
            disp_ela_dist.append([round(i[0],2),round(i[1],2)])
        for i in range(len(ela_dist)): 
            area1=0
            area2=0
            area3=0
            area4=0 
            area_t=0
            area_b=0    
            for j in range(i):
                if ela_dist[j+1][1]<=tf/d :
                    area1=area1+((ela_dist[j][0]-(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*ela_dist[i][1]*(ela_dist[j+1][1]-ela_dist[j][1])+0.5*(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)*ela_dist[i][1]-0.5*(ela_dist[j][0]-(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)-1/3*(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**3-ela_dist[j][1]**3))*w
                    #area1=area1+(ela_dist[j][0]*((ela_dist[j][1]-ela_dist[i][1])**2)**0.5+ela_dist[j+1][0]*((ela_dist[j+1][1]-ela_dist[i][1])**2)**0.5)*(ela_dist[j+1][1]-ela_dist[j][1])/2*w
                elif ela_dist[j][1]>=(d-tf)/d and ela_dist[j+1][1]<=1:
                    area1=area1+((ela_dist[j][0]-(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*ela_dist[i][1]*(ela_dist[j+1][1]-ela_dist[j][1])+0.5*(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)*ela_dist[i][1]-0.5*(ela_dist[j][0]-(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)-1/3*(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**3-ela_dist[j][1]**3))*w
                elif ela_dist[j][1]>=tf/d and ela_dist[j+1][1]<=(d-tf)/d:
                    area1=area1+((ela_dist[j][0]-(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*ela_dist[i][1]*(ela_dist[j+1][1]-ela_dist[j][1])+0.5*(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)*ela_dist[i][1]-0.5*(ela_dist[j][0]-(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)-1/3*(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**3-ela_dist[j][1]**3))*tw
                    #area1=area1+(ela_dist[j][0]*((ela_dist[j][1]-ela_dist[i][1])**2)**0.5+ela_dist[j+1][0]*((ela_dist[j+1][1]-ela_dist[i][1])**2)**0.5)*(ela_dist[j+1][1]-ela_dist[j][1])/2*tw 
            for k in range(i,len(ela_dist)-1):
                if ela_dist[k+1][1]<=tf/d :
                    area2=area2+(0.5*(ela_dist[k][0]-(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)+1/3*(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**3-ela_dist[k][1]**3)-(ela_dist[k][0]-(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*ela_dist[i][1]*(ela_dist[k+1][1]-ela_dist[k][1])-0.5*(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)*ela_dist[i][1])*w
                    #area2=area2+(ela_dist[k][0]*((ela_dist[k][1]-ela_dist[i][1])**2)**0.5+ela_dist[k+1][0]*((ela_dist[k+1][1]-ela_dist[i][1])**2)**0.5)*(ela_dist[k+1][1]-ela_dist[k][1])/2*w
                elif ela_dist[k][1]>=(d-tf)/d and ela_dist[k+1][1]<=1:
                    area2=area2+(0.5*(ela_dist[k][0]-(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)+1/3*(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**3-ela_dist[k][1]**3)-(ela_dist[k][0]-(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*ela_dist[i][1]*(ela_dist[k+1][1]-ela_dist[k][1])-0.5*(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)*ela_dist[i][1])*w
                elif ela_dist[k][1]>=tf/d and ela_dist[k+1][1]<=(d-tf)/d:
                    area2=area2+(0.5*(ela_dist[k][0]-(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)+1/3*(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**3-ela_dist[k][1]**3)-(ela_dist[k][0]-(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*ela_dist[i][1]*(ela_dist[k+1][1]-ela_dist[k][1])-0.5*(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)*ela_dist[i][1])*tw
                    #area2=area2+(ela_dist[k][0]*((ela_dist[k][1]-ela_dist[i][1])**2)**0.5+ela_dist[k+1][0]*((ela_dist[k+1][1]-ela_dist[i][1])**2)**0.5)*(ela_dist[k+1][1]-ela_dist[k][1])/2*tw
            for j in range(i-1):
                if ela_dist[j+1][1]<=tf/d :
                    area3=area3+((ela_dist[0][0]-(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*ela_dist[i-1][1]*(ela_dist[j+1][1]-ela_dist[j][1])+0.5*(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)*ela_dist[i-1][1]-0.5*(ela_dist[0][0]-(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)-1/3*(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**3-ela_dist[j][1]**3))*w
                    #area3=area3+(ela_dist[j][0]*((ela_dist[j][1]-ela_dist[i-1][1])**2)**0.5+ela_dist[j+1][0]*((ela_dist[j+1][1]-ela_dist[i-1][1])**2)**0.5)*(ela_dist[j+1][1]-ela_dist[j][1])/2*w
                elif ela_dist[j][1]>=(d-tf)/d and ela_dist[j+1][1]<=1:
                    area3=area3+((ela_dist[-1][0]-(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*ela_dist[i-1][1]*(ela_dist[j+1][1]-ela_dist[j][1])+0.5*(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)*ela_dist[i-1][1]-0.5*(ela_dist[-1][0]-(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)-1/3*(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**3-ela_dist[j][1]**3))*w
                elif ela_dist[j][1]>=tf/d and ela_dist[j+1][1]<=(d-tf)/d:
                    area3=area3+((ela_dist[j][0]-(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*ela_dist[i-1][1]*(ela_dist[j+1][1]-ela_dist[j][1])+0.5*(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)*ela_dist[i-1][1]-0.5*(ela_dist[j][0]-(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)-1/3*(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**3-ela_dist[j][1]**3))*tw
                    #area3=area3+(ela_dist[j][0]*((ela_dist[j][1]-ela_dist[i-1][1])**2)**0.5+ela_dist[j+1][0]*((ela_dist[j+1][1]-ela_dist[i-1][1])**2)**0.5)*(ela_dist[j+1][1]-ela_dist[j][1])/2*tw
            for k in range(i-1,len(ela_dist)-1):
                if ela_dist[k+1][1]<=tf/d :
                    area4=area4+(0.5*(ela_dist[0][0]-(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)+1/3*(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**3-ela_dist[k][1]**3)-(ela_dist[0][0]-(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*ela_dist[i-1][1]*(ela_dist[k+1][1]-ela_dist[k][1])-0.5*(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)*ela_dist[i-1][1])*w 
                    #area4=area4+(ela_dist[k][0]*((ela_dist[k][1]-ela_dist[i-1][1])**2)**0.5+ela_dist[k+1][0]*((ela_dist[k+1][1]-ela_dist[i-1][1])**2)**0.5)*(ela_dist[k+1][1]-ela_dist[k][1])/2*w
                elif ela_dist[k][1]>=(d-tf)/d and ela_dist[k+1][1]<=1:
                    area4=area4+(0.5*(ela_dist[-1][0]-(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)+1/3*(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**3-ela_dist[k][1]**3)-(ela_dist[-1][0]-(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*ela_dist[i-1][1]*(ela_dist[k+1][1]-ela_dist[k][1])-0.5*(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)*ela_dist[i-1][1])*w 
                elif ela_dist[k][1]>=tf/d and ela_dist[k+1][1]<=(d-tf)/d:
                    area4=area4+(0.5*(ela_dist[k][0]-(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)+1/3*(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**3-ela_dist[k][1]**3)-(ela_dist[k][0]-(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*ela_dist[i-1][1]*(ela_dist[k+1][1]-ela_dist[k][1])-0.5*(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)*ela_dist[i-1][1])*tw 
                    #area4=area4+(ela_dist[k][0]*((ela_dist[k][1]-ela_dist[i-1][1])**2)**0.5+ela_dist[k+1][0]*((ela_dist[k+1][1]-ela_dist[i-1][1])**2)**0.5)*(ela_dist[k+1][1]-ela_dist[k][1])/2*tw    
            if area1>=area2 and area3<=area4:
                x = symbols('x',real=True)
                for j in range(i-1):
                    if ela_dist[j+1][1]<=tf/d :
                        #area_t=area_t+(ela_dist[j][0]*((ela_dist[j][1]-x)**2)**0.5+ela_dist[j+1][0]*((ela_dist[j+1][1]-x)**2)**0.5)*(ela_dist[j+1][1]-ela_dist[j][1])/2*w
                        area_t=area_t+((ela_dist[0][0]-(ela_dist[0][0]-ela_dist[0][0])*(ela_dist[j][1]-ela_dist[j+1][1])**(-1)*ela_dist[j][1])*x*(ela_dist[j+1][1]-ela_dist[j][1])+0.5*(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)*x-0.5*(ela_dist[0][0]-(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)-1/3*(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**3-ela_dist[j][1]**3))*w
                    elif ela_dist[j][1]>=(d-tf)/d and ela_dist[j+1][1]<=1:
                        area_t=area_t+((ela_dist[-1][0]-(ela_dist[-1][0]-ela_dist[-1][0])*(ela_dist[j][1]-ela_dist[j+1][1])**(-1)*ela_dist[j][1])*x*(ela_dist[j+1][1]-ela_dist[j][1])+0.5*(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)*x-0.5*(ela_dist[-1][0]-(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)-1/3*(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**3-ela_dist[j][1]**3))*w
                    elif ela_dist[j][1]>=tf/d and ela_dist[j+1][1]<=(d-tf)/d:
                        #area_t=area_t+(ela_dist[j][0]*((ela_dist[j][1]-x)**2)**0.5+ela_dist[j+1][0]*((ela_dist[j+1][1]-x)**2)**0.5)*(ela_dist[j+1][1]-ela_dist[j][1])/2*tw
                        area_t=area_t+((ela_dist[j][0]-(ela_dist[j][0]-ela_dist[j+1][0])*(ela_dist[j][1]-ela_dist[j+1][1])**(-1)*ela_dist[j][1])*x*(ela_dist[j+1][1]-ela_dist[j][1])+0.5*(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)*x-0.5*(ela_dist[j][0]-(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*ela_dist[j][1])*(ela_dist[j+1][1]**2-ela_dist[j][1]**2)-1/3*(ela_dist[j][0]-ela_dist[j+1][0])/(ela_dist[j][1]-ela_dist[j+1][1])*(ela_dist[j+1][1]**3-ela_dist[j][1]**3))*tw
                for k in range(i,len(ela_dist)-1):                                                                                                                       
                    if ela_dist[k+1][1]<=tf/d :
                        area_b=area_b+(0.5*(ela_dist[0][0]-(ela_dist[0][0]-ela_dist[0][0])*(ela_dist[k][1]-ela_dist[k+1][1])**(-1)*ela_dist[k][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)+1/3*(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**3-ela_dist[k][1]**3)-(ela_dist[0][0]-(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*x*(ela_dist[k+1][1]-ela_dist[k][1])-0.5*(ela_dist[0][0]-ela_dist[0][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)*x)*w 
                        #area_b=area_b+(ela_dist[k][0]*((ela_dist[k][1]-x)**2)**0.5+ela_dist[k+1][0]*((ela_dist[j+1][1]-x)**2)**0.5)*(ela_dist[j+1][1]-ela_dist[j][1])/2*w
                    elif ela_dist[k][1]>=(d-tf)/d and ela_dist[k+1][1]<=1:
                        area_b=area_b+(0.5*(ela_dist[-1][0]-(ela_dist[-1][0]-ela_dist[-1][0])*(ela_dist[k][1]-ela_dist[k+1][1])**(-1)*ela_dist[k][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)+1/3*(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**3-ela_dist[k][1]**3)-(ela_dist[-1][0]-(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*x*(ela_dist[k+1][1]-ela_dist[k][1])-0.5*(ela_dist[-1][0]-ela_dist[-1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)*x)*w 
                    elif ela_dist[k][1]>=tf/d and ela_dist[k+1][1]<=(d-tf)/d:
                        area_b=area_b+(0.5*(ela_dist[k][0]-(ela_dist[k][0]-ela_dist[k+1][0])*(ela_dist[k][1]-ela_dist[k+1][1])**(-1)*ela_dist[k][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)+1/3*(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**3-ela_dist[k][1]**3)-(ela_dist[k][0]-(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*ela_dist[k][1])*x*(ela_dist[k+1][1]-ela_dist[k][1])-0.5*(ela_dist[k][0]-ela_dist[k+1][0])/(ela_dist[k][1]-ela_dist[k+1][1])*(ela_dist[k+1][1]**2-ela_dist[k][1]**2)*x)*tw 
                        #area_b=area_b+(ela_dist[j][0]*((ela_dist[j][1]-x)**2)**0.5+ela_dist[j+1][0]*((ela_dist[j+1][1]-x)**2)**0.5)*(ela_dist[j+1][1]-ela_dist[j][1])/2*tw
                print(ela_dist[i][1],ela_dist[i-1][1])
                if ela_dist[i][1] <= tf/d :
                    area_t=area_t+((ela_dist[i-1][0]-(ela_dist[i-1][0]-ela_dist[i][0])*(ela_dist[i-1][1]-ela_dist[i][1])**(-1)*ela_dist[i-1][1])*x*(x-ela_dist[i-1][1])+0.5*(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*(x**2-ela_dist[i-1][1]**2)*x-0.5*(ela_dist[i-1][0]-(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*ela_dist[i-1][1])*(x**2-ela_dist[i-1][1]**2)-1/3*(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*(x**3-ela_dist[i-1][1]**3))*w
                    #area_t=area_t+ela_dist[0][0]*((ela_dist[i-1][1]-x)**2)/2*w
                    area_b=area_b+(0.5*(ela_dist[i-1][0]-(ela_dist[i-1][0]-ela_dist[i][0])*(ela_dist[i-1][1]-ela_dist[i][1])**(-1)*ela_dist[i-1][1])*(ela_dist[i][1]**2-x**2)+1/3*(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*(ela_dist[i][1]**3-x**3)-(ela_dist[i-1][0]-(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*ela_dist[i-1][1])*x*(ela_dist[i][1]-x)-0.5*(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*(ela_dist[i][1]**2-x**2)*x)*w
                elif ela_dist[i-1][1]>=(d-tf)/d and ela_dist[i][1]<=1:
                    area_t=area_t+((ela_dist[i-1][0]-(ela_dist[i-1][0]-ela_dist[i][0])*(ela_dist[i-1][1]-ela_dist[i][1])**(-1)*ela_dist[i-1][1])*x*(x-ela_dist[i-1][1])+0.5*(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*(x**2-ela_dist[i-1][1]**2)*x-0.5*(ela_dist[i-1][0]-(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*ela_dist[i-1][1])*(x**2-ela_dist[i-1][1]**2)-1/3*(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*(x**3-ela_dist[i-1][1]**3))*w
                    #area_t=area_t+ela_dist[i-1][0]*((ela_dist[i-1][1]-x)**2)/2*w
                    area_b=area_b+(0.5*(ela_dist[i-1][0]-(ela_dist[i-1][0]-ela_dist[i][0])*(ela_dist[i-1][1]-ela_dist[i][1])**(-1)*ela_dist[i-1][1])*(ela_dist[i][1]**2-x**2)+1/3*(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*(ela_dist[i][1]**3-x**3)-(ela_dist[i-1][0]-(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*ela_dist[i-1][1])*x*(ela_dist[i][1]-x)-0.5*(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*(ela_dist[i][1]**2-x**2)*x)*w
                elif ela_dist[i-1][1]>=tf/d and ela_dist[i][1]<=(d-tf)/d:
                    area_t=area_t+((ela_dist[i-1][0]-(ela_dist[i-1][0]-ela_dist[i][0])*(ela_dist[i-1][1]-ela_dist[i][1])**(-1)*ela_dist[i-1][1])*x*(x-ela_dist[i-1][1])+0.5*(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*(x**2-ela_dist[i-1][1]**2)*x-0.5*(ela_dist[i-1][0]-(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*ela_dist[i-1][1])*(x**2-ela_dist[i-1][1]**2)-1/3*(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*(x**3-ela_dist[i-1][1]**3))*tw
                    area_b=area_b+(0.5*(ela_dist[i-1][0]-(ela_dist[i-1][0]-ela_dist[i][0])*(ela_dist[i-1][1]-ela_dist[i][1])**(-1)*ela_dist[i-1][1])*(ela_dist[i][1]**2-x**2)+1/3*(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*(ela_dist[i][1]**3-x**3)-(ela_dist[i-1][0]-(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*ela_dist[i-1][1])*x*(ela_dist[i][1]-x)-0.5*(ela_dist[i-1][0]-ela_dist[i][0])/(ela_dist[i-1][1]-ela_dist[i][1])*(ela_dist[i][1]**2-x**2)*x)*tw
                expr=area_t-area_b
                #print('Equation of neutral axis',expr)
                y_neu=solve(expr)
                y_neu_set=[]
                for sol in y_neu:
                    sol=round(sol,14)
                    y_neu_set.append(sol) 
                for k in y_neu_set:
                    if k<=ela_dist[i][1] and k>=ela_dist[i-1][1]: 
                        y_neutral=k
                        break
        print('Elastic neutral axis (deepness/depth):',y_neutral)
        return ela_dist,y_neutral,tempdist
    def E_I_z(self,E,d,w,tw,tf,ela_dist):
        E_I_z1=0
        E_I_z=0                                                                                                                                                                                                                             
        for i in range(len(ela_dist)-1):                                                                            
            if ela_dist[i+1][1] <= tf/d:
                E_I_z=E*(ela_dist[i][0]+ela_dist[i+1][0])/2*d*(ela_dist[i+1][1]-ela_dist[i][1])*(w)**3/12
                #E_I_z=E*(1/3*(0.25*w**3)*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))+1/6*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*0.25*w**3)
                print('E_I_z=E*(k_E['+str(i)+']+k_E['+str(i+1)+'])/2*d*(d_r['+str(i+1)+']-d_r['+str(i)+'])*(w)**3/12')
                print('E_I_z'+str(i)+'='+str(E)+'*('+str(ela_dist[i][0])+'+'+str(ela_dist[i+1][0])+')/2*'+str(d)+'*('+str(ela_dist[i+1][1])+'-'+str(ela_dist[i][1])+')*'+str(w)+'**3/12')
                E_I_z1=E_I_z1+E_I_z
                print('E_I_z'+str(i)+'='+str(E_I_z))
            elif  ela_dist[i][1]>=(d-tf)/d:
                E_I_z=E*(ela_dist[i][0]+ela_dist[i+1][0])/2*d*(ela_dist[i+1][1]-ela_dist[i][1])*(w)**3/12
                #E_I_z=E*(1/3*(0.25*w**3)*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))+1/6*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*0.25*w**3)
                print('E_I_z=E*(k_E['+str(i)+']+k_E['+str(i+1)+'])/2*d*(d_r['+str(i+1)+']-d_r['+str(i)+'])*(w)**3/12')
                print('E_I_z'+str(i)+'='+str(E)+'*('+str(ela_dist[i][0])+'+'+str(ela_dist[i+1][0])+')/2*'+str(d)+'*('+str(ela_dist[i+1][1])+'-'+str(ela_dist[i][1])+')*'+str(w)+'**3/12')
                E_I_z1=E_I_z1+E_I_z
                print('E_I_z'+str(i)+'='+str(E_I_z))            
            elif ela_dist[i][1] >= tf/d and ela_dist[i+1][1]<=(d-tf)/d:
                E_I_z=E*(ela_dist[i][0]+ela_dist[i+1][0])/2*d*(ela_dist[i+1][1]-ela_dist[i][1])*(tw)**3/12
                #I_z+=d*(ela_dist[i+1][1]-ela_dist[i][1])*(tw*((ela_dist[i][0]+ela_dist[i+1][0])/2))**3/12
                #E_I_z=E*(1/3*(0.25*tw**3)*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))+1/6*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*0.25*tw**3)
                print('E_I_z=E*(k_E['+str(i)+']+k_E['+str(i+1)+'])/2*d*(d_r['+str(i+1)+']-d_r['+str(i)+'])*(tw)**3/12')
                print('E_I_z'+str(i)+'='+str(E)+'*('+str(ela_dist[i][0])+'+'+str(ela_dist[i+1][0])+')/2*'+str(d)+'*('+str(ela_dist[i+1][1])+'-'+str(ela_dist[i][1])+')*'+str(tw)+'**3/12')
                print('E_I_z'+str(i)+'='+str(E_I_z))
                E_I_z1=E_I_z1+E_I_z
        print('E_I_z='+str(E_I_z1))
        return E_I_z1
    def shear_centre(self,ela_dist,w,tf,tw,d):
        s_c=0
        e_t=0
        e_b=0
        # Calculation of bending moment
        z = symbols('z',real=True)
        #expr=(245.1-z)*(ela_dist[-1][0])**3-z*(ela_dist[0][0])**3
        # expr
        #expr=(((0.25*(ela_dist[0][0]-ela_dist[1][0])/(ela_dist[0][1]-ela_dist[1][1])*(ela_dist[1][1]**2-ela_dist[0][1]**2)*((0.5*w)**2*(0.5*w-0.5*tw)-1/3*((0.5*w)**3-(0.5*tw)**3))+0.5*(ela_dist[0][0]-(ela_dist[0][0]-ela_dist[1][0])/(ela_dist[0][1]-ela_dist[1][1])*ela_dist[0][1])*(tf)*((0.5*w)**2*(0.5*w-0.5*tw)-1/3*((0.5*w)**3-(0.5*tw)**3)))/tf)*tf+(0.25*(ela_dist[0][0]-ela_dist[-1][0])/(ela_dist[0][1]-ela_dist[-1][1])*(ela_dist[-1][1]**2-ela_dist[0][1]**2)*((0.5*tw)**2*(0.5*tw)-1/3*(0.5*tw)**3)+0.5*(ela_dist[0][0]-(ela_dist[0][0]-ela_dist[-1][0])/(ela_dist[0][1]-ela_dist[-1][1])*ela_dist[0][1])*(ela_dist[-1][1]-ela_dist[0][1])*((0.5*tw)**2*(0.5*tw)-1/3*((0.5*tw)**3)))/d*tf)*z-((0.25*(ela_dist[-2][0]-ela_dist[-1][0])/(ela_dist[-2][1]-ela_dist[-1][1])*(ela_dist[-1][1]**2-ela_dist[-2][1]**2)*((0.5*w)**2*(0.5*w-0.5*tw)-1/3*((0.5*w)**3-(0.5*tw)**3))+0.5*(ela_dist[-2][0]-(ela_dist[-2][0]-ela_dist[-1][0])/(ela_dist[-2][1]-ela_dist[-1][1])*ela_dist[-2][1])*(tf)*((0.5*w)**2*(0.5*w-0.5*tw)-1/3*((0.5*w)**3-(0.5*tw)**3)))/tf*tf+(0.25*(ela_dist[0][0]-ela_dist[-1][0])/(ela_dist[0][1]-ela_dist[-1][1])*(ela_dist[-1][1]**2-ela_dist[0][1]**2)*((0.5*tw)**2*(0.5*tw)-1/3*(0.5*tw)**3)+0.5*(ela_dist[0][0]-(ela_dist[0][0]-ela_dist[-1][0])/(ela_dist[0][1]-ela_dist[-1][1])*ela_dist[0][1])*(d)*((0.5*tw)**2*(0.5*tw)-1/3*((0.5*tw)**3)))/d*tf)*(d-tf-z)
        for i in range(len(ela_dist)-1):
            if ela_dist[i+1][1]<=tf/d:
                e_t+=(ela_dist[i+1][0]+ela_dist[i][0])/2*(ela_dist[i+1][1]-ela_dist[i][1])
            elif ela_dist[i][1]>=(d-tf)/d:
                e_b+=(ela_dist[i+1][0]+ela_dist[i][0])/2*(ela_dist[i+1][1]-ela_dist[i][1])
        rou=e_t/e_b
        expr=(d-tf-z)*e_t-z*e_b      
        #expr=(256-z)*(ela_dist[-1][0]+ela_dist[-2][0])-z*(ela_dist[0][0]+ela_dist[1][0])

        s_c=solve(expr)
        print('s_c=',s_c)
        s_c=round(s_c[0])+tf/2
        return s_c
    def beta_x(self,E,d,tw,tf,ela_dist,w,s_c,y_neu):
        E_Ix1=0
        E_Ix=0
        num_up=0
        num_up1=0
        beta=0
        centroid=0
        E_A_y=0
        E_A_y1=0
        E_A=0
        E_A1=0
        for i in range(len(ela_dist)-1):
            if ela_dist[i+1][1] <= tf/d:
                # Ix+=w*((ela_dist[i][0]+ela_dist[i+1][0])/2)*((ela_dist[i+1][1]-ela_dist[i][1])*d)**3/12+(w*((ela_dist[i][0]+ela_dist[i+1][0])/2)*(ela_dist[i+1][1]-ela_dist[i][1])*d)*(((ela_dist[i][1]+ela_dist[i+1][1])/2-y_neu)*d)**2
                # E_Ix1=E*(1/3*ela_dist[i][0]*((d-d*ela_dist[i][1])**3-(d-d*ela_dist[i+1][1])**3)*(w)-1/3*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d)*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*w+0.25*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)*w-ela_dist[i][0]*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*(d-y_neu*d)*w+(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*(d-y_neu*d)*(w)*(d-ela_dist[i][1]*d)-2/3*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*(d-y_neu*d)*w+ela_dist[i][0]*(d-y_neu*d)**2*((d-d*ela_dist[i][1])-(d-d*ela_dist[i+1][1]))*w-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-d*ela_dist[i][1])*(d-y_neu*d)**2*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*w+0.5*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*(d*(1-y_neu))**2*(w))
                E_Ix1=w*E*(0.25*(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-1/3*(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+1/3*ela_dist[i][0]*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-2/3*d*y_neu*(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*y_neu*d*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-ela_dist[i][0]*y_neu*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+0.5*(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*(y_neu*d)**2-(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*ela_dist[i][1]*d*(y_neu*d)**2*(ela_dist[i+1][1]*d-ela_dist[i][1]*d)+ela_dist[i][0]*(y_neu*d)**2*(ela_dist[i+1][1]-ela_dist[i][1])*d)
                print('E_Ix1=w*E'+'*(0.25*(kE('+str(i)+')-kE('+str(i+1)+'))/((d_r'+str(i)+'-d_r'+str(i+1)+'))*((d_r'+str(i+1)+'*d)**4-(d_r'+str(i)+'*d)**4)-1/3*(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*d_r'+str(i)+'*d*((d_r'+str(i+1)+'*d)**3-(d_r'+str(i)+'*d)**3)+1/3*kE'+str(i)+'*((d_r'+str(i+1)+'*d)**3-(d_r'+str(i)+'*d)**3)-2/3*d*y_neu*(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*((d_r'+str(i+1)+'*d)**3-(d_r'+str(i)+'*d)**3)+(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*y_neu*d*d_r'+str(i)+'*d*((d_r'+str(i+1)+'*d)**2-(d_r'+str(i)+'*d)**2)-kE'+str(i)+'*y_neu*d*((d_r'+str(i+1)+'*d)**2-(d_r'+str(i)+'*d)**2)+0.5*(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*((d_r'+str(i+1)+'*d)**2-(d_r'+str(i)+'*d)**2)*(y_neu*d)**2-(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*d_r'+str(i)+'*d*(y_neu*d)**2*(d_r'+str(i+1)+'*d-d_r'+str(i)+'*d)+kE'+str(i)+'*(y_neu*d)**2*(d_r'+str(i+1)+'-d_r'+str(i)+'*d)*d')
                print('E_Ix'+str(i)+'='+str(E)+'*(0.25*('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*('+str(ela_dist[i+1][1])+'*'+str(d)+')**4-('+str(ela_dist[i][1])+'*'+str(d)+')**4)-1/3*('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*'+str(ela_dist[i][1])+'*'+str(d)+'(('+str(ela_dist[i+1][1])+'*'+str(d)+')**3-('+str(ela_dist[i][1])+'*'+str(d)+')**3)+1/3*'+str(ela_dist[i][0])+'(('+str(ela_dist[i+1][1])+'*'+str(d)+')**3-('+str(ela_dist[i][1])+'*'+str(d)+')**3)-2/3*'+str(d)+'*'+str(y_neu)+'*('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*(('+str(ela_dist[i+1][1])+'*'+str(d)+')**3-('+str(ela_dist[i][1])+'*'+str(d)+')**3)+('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*'+str(y_neu)+'*'+str(d)+'*'+str(ela_dist[i][1])+'*'+str(d)+'*(('+str(ela_dist[i+1][1])+'*'+str(d)+')**2-('+str(ela_dist[i][1])+'*'+str(d)+')**2)-'+str(ela_dist[i][0])+'*'+str(y_neu)+'*'+str(d)+'*(('+str(ela_dist[i+1][1])+'*'+str(d)+')**2-('+str(ela_dist[i][1])+'*'+str(d)+')**2)+0.5*('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+')-'+str(ela_dist[i+1][1])+')*(('+str(ela_dist[i+1][1])+'*'+str(d)+')**2-('+str(ela_dist[i][1])+'*'+str(d)+')**2)*('+str(y_neu)+'*'+str(d)+')**2-('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*'+str(ela_dist[i][1])+'*'+str(d)+'*('+str(y_neu)+'*'+str(d)+')**2*(('+str(ela_dist[i+1][1])+'*'+str(d)+')-('+str(ela_dist[i][1])+'*'+str(d)+'))+'+str(ela_dist[i][0])+'*('+str(y_neu)+'*'+str(d)+')**2*('+str(ela_dist[i+1][1])+'-'+str(ela_dist[i][1])+')*'+str(d))
                # E_Ix1=E*(ela_dist[0][0])*(w*(((ela_dist[i+1][1]-ela_dist[i][1])*d))**3/12+(w*(ela_dist[i+1][1]-ela_dist[i][1])*d)*((0-y_neu)*d)**2)
                E_Ix=E_Ix+E_Ix1
                print('y_neu=',y_neu)
                print('tf/d,(d-tf)/d'+str(tf/d)+str((d-tf)/d))
                print('h1=',ela_dist[i][1])
                print('E_Ix'+str(i)+'='+str(E_Ix)+str(E_Ix1))
            elif ela_dist[i][1]>=(d-tf)/d:
                E_Ix1=w*E*(0.25*(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-1/3*(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+1/3*ela_dist[i][0]*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-2/3*d*y_neu*(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*y_neu*d*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-ela_dist[i][0]*y_neu*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+0.5*(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*(y_neu*d)**2-(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*ela_dist[i][1]*d*(y_neu*d)**2*(ela_dist[i+1][1]*d-ela_dist[i][1]*d)+ela_dist[i][0]*(y_neu*d)**2*(ela_dist[i+1][1]-ela_dist[i][1])*d)
                # E_Ix1=E*(ela_dist[-1][0])*(w*(((ela_dist[i+1][1]-ela_dist[i][1])*d))**3/12+(w*(ela_dist[i+1][1]-ela_dist[i][1])*d)*((1-y_neu)*d)**2)
                print('E_Ix1=w*E'+'*(0.25*(kE('+str(i)+')-kE('+str(i+1)+'))/((d_r'+str(i)+'-d_r'+str(i+1)+'))*((d_r'+str(i+1)+'*d)**4-(d_r'+str(i)+'*d)**4)-1/3*(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*d_r'+str(i)+'*d*((d_r'+str(i+1)+'*d)**3-(d_r'+str(i)+'*d)**3)+1/3*kE'+str(i)+'*((d_r'+str(i+1)+'*d)**3-(d_r'+str(i)+'*d)**3)-2/3*d*y_neu*(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*((d_r'+str(i+1)+'*d)**3-(d_r'+str(i)+'*d)**3)+(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*y_neu*d*d_r'+str(i)+'*d*((d_r'+str(i+1)+'*d)**2-(d_r'+str(i)+'*d)**2)-kE'+str(i)+'*y_neu*d*((d_r'+str(i+1)+'*d)**2-(d_r'+str(i)+'*d)**2)+0.5*(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*((d_r'+str(i+1)+'*d)**2-(d_r'+str(i)+'*d)**2)*(y_neu*d)**2-(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*d_r'+str(i)+'*d*(y_neu*d)**2*(d_r'+str(i+1)+'*d-d_r'+str(i)+'*d)+kE'+str(i)+'*(y_neu*d)**2*(d_r'+str(i+1)+'-d_r'+str(i)+'*d)*d')
                print('E_Ix'+str(i)+'='+str(E)+'*(0.25*('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*('+str(ela_dist[i+1][1])+'*'+str(d)+')**4-('+str(ela_dist[i][1])+'*'+str(d)+')**4)-1/3*('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*'+str(ela_dist[i][1])+'*'+str(d)+'(('+str(ela_dist[i+1][1])+'*'+str(d)+')**3-('+str(ela_dist[i][1])+'*'+str(d)+')**3)+1/3*'+str(ela_dist[i][0])+'(('+str(ela_dist[i+1][1])+'*'+str(d)+')**3-('+str(ela_dist[i][1])+'*'+str(d)+')**3)-2/3*'+str(d)+'*'+str(y_neu)+'*('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*(('+str(ela_dist[i+1][1])+'*'+str(d)+')**3-('+str(ela_dist[i][1])+'*'+str(d)+')**3)+('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*'+str(y_neu)+'*'+str(d)+'*'+str(ela_dist[i][1])+'*'+str(d)+'*(('+str(ela_dist[i+1][1])+'*'+str(d)+')**2-('+str(ela_dist[i][1])+'*'+str(d)+')**2)-'+str(ela_dist[i][0])+'*'+str(y_neu)+'*'+str(d)+'*(('+str(ela_dist[i+1][1])+'*'+str(d)+')**2-('+str(ela_dist[i][1])+'*'+str(d)+')**2)+0.5*('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+')-'+str(ela_dist[i+1][1])+')*(('+str(ela_dist[i+1][1])+'*'+str(d)+')**2-('+str(ela_dist[i][1])+'*'+str(d)+')**2)*('+str(y_neu)+'*'+str(d)+')**2-('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*'+str(ela_dist[i][1])+'*'+str(d)+'*('+str(y_neu)+'*'+str(d)+')**2*(('+str(ela_dist[i+1][1])+'*'+str(d)+')-('+str(ela_dist[i][1])+'*'+str(d)+'))+'+str(ela_dist[i][0])+'*('+str(y_neu)+'*'+str(d)+')**2*('+str(ela_dist[i+1][1])+'-'+str(ela_dist[i][1])+')*'+str(d))
                E_Ix=E_Ix+E_Ix1
                print('y_neu=',y_neu)
                print('h1=',ela_dist[i][1])
                print('E_Ix'+str(i)+'='+str(E_Ix)+str(E_Ix1))       
            elif ela_dist[i][1] >= tf/d and ela_dist[i+1][1]<=(d-tf)/d:
                # Ix+=tw*((ela_dist[i][0]+ela_dist[i+1][0])/2)*((ela_dist[i+1][1]-ela_dist[i][1])*d)**3/12+(tw*((ela_dist[i][0]+ela_dist[i+1][0])/2)*(ela_dist[i+1][1]-ela_dist[i][1])*d)*(((ela_dist[i][1]+ela_dist[i+1][1])/2-y_neu)*d)**2
                E_Ix1=tw*E*(0.25*(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-1/3*(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+1/3*ela_dist[i][0]*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-2/3*d*y_neu*(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*y_neu*d*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-ela_dist[i][0]*y_neu*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+0.5*(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*(y_neu*d)**2-(ela_dist[i][0]-ela_dist[i+1][0])/((ela_dist[i][1]*d-ela_dist[i+1][1]*d))*ela_dist[i][1]*d*(y_neu*d)**2*(ela_dist[i+1][1]*d-ela_dist[i][1]*d)+ela_dist[i][0]*(y_neu*d)**2*(ela_dist[i+1][1]-ela_dist[i][1])*d)
                # E_Ix1=E*(1/3*ela_dist[i][0]*((d-d*ela_dist[i][1])**3-(d-d*ela_dist[i+1][1])**3)*(tw)-1/3*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d)*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*tw+0.25*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)*tw-ela_dist[i][0]*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*(d-y_neu*d)*tw+(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*(d-y_neu*d)*(tw)*(d-ela_dist[i][1]*d)-2/3*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*(d-y_neu*d)*tw+ela_dist[i][0]*(d-y_neu*d)**2*((d-d*ela_dist[i][1])-(d-d*ela_dist[i+1][1]))*tw-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-d*ela_dist[i][1])*(d-y_neu*d)**2*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*tw+0.5*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*(d-y_neu*d)**2*(tw))
                print('E_Ix1=tw*E'+'*(0.25*(kE('+str(i)+')-kE('+str(i+1)+'))/((d_r'+str(i)+'-d_r'+str(i+1)+'))*((d_r'+str(i+1)+'*d)**4-(d_r'+str(i)+'*d)**4)-1/3*(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*d_r'+str(i)+'*d*((d_r'+str(i+1)+'*d)**3-(d_r'+str(i)+'*d)**3)+1/3*kE'+str(i)+'*((d_r'+str(i+1)+'*d)**3-(d_r'+str(i)+'*d)**3)-2/3*d*y_neu*(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*((d_r'+str(i+1)+'*d)**3-(d_r'+str(i)+'*d)**3)+(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*y_neu*d*d_r'+str(i)+'*d*((d_r'+str(i+1)+'*d)**2-(d_r'+str(i)+'*d)**2)-kE'+str(i)+'*y_neu*d*((d_r'+str(i+1)+'*d)**2-(d_r'+str(i)+'*d)**2)+0.5*(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*((d_r'+str(i+1)+'*d)**2-(d_r'+str(i)+'*d)**2)*(y_neu*d)**2-(kE'+str(i)+'-kE'+str(i+1)+')/((d_r'+str(i)+'*d-d_r'+str(i+1)+'*d))*d_r'+str(i)+'*d*(y_neu*d)**2*(d_r'+str(i+1)+'*d-d_r'+str(i)+'*d)+kE'+str(i)+'*(y_neu*d)**2*(d_r'+str(i+1)+'-d_r'+str(i)+'*d)*d')
                print('E_Ix'+str(i)+'='+str(E)+'*(0.25*('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*('+str(ela_dist[i+1][1])+'*'+str(d)+')**4-('+str(ela_dist[i][1])+'*'+str(d)+')**4)-1/3*('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*'+str(ela_dist[i][1])+'*'+str(d)+'(('+str(ela_dist[i+1][1])+'*'+str(d)+')**3-('+str(ela_dist[i][1])+'*'+str(d)+')**3)+1/3*'+str(ela_dist[i][0])+'(('+str(ela_dist[i+1][1])+'*'+str(d)+')**3-('+str(ela_dist[i][1])+'*'+str(d)+')**3)-2/3*'+str(d)+'*'+str(y_neu)+'*('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*(('+str(ela_dist[i+1][1])+'*'+str(d)+')**3-('+str(ela_dist[i][1])+'*'+str(d)+')**3)+('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*'+str(y_neu)+'*'+str(d)+'*'+str(ela_dist[i][1])+'*'+str(d)+'*(('+str(ela_dist[i+1][1])+'*'+str(d)+')**2-('+str(ela_dist[i][1])+'*'+str(d)+')**2)-'+str(ela_dist[i][0])+'*'+str(y_neu)+'*'+str(d)+'*(('+str(ela_dist[i+1][1])+'*'+str(d)+')**2-('+str(ela_dist[i][1])+'*'+str(d)+')**2)+0.5*('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+')-'+str(ela_dist[i+1][1])+')*(('+str(ela_dist[i+1][1])+'*'+str(d)+')**2-('+str(ela_dist[i][1])+'*'+str(d)+')**2)*('+str(y_neu)+'*'+str(d)+')**2-('+str(ela_dist[i][0])+'-'+str(ela_dist[i+1][0])+')/('+str(ela_dist[i][1])+'-'+str(ela_dist[i+1][1])+')*'+str(ela_dist[i][1])+'*'+str(d)+'*('+str(y_neu)+'*'+str(d)+')**2*(('+str(ela_dist[i+1][1])+'*'+str(d)+')-('+str(ela_dist[i][1])+'*'+str(d)+'))+'+str(ela_dist[i][0])+'*('+str(y_neu)+'*'+str(d)+')**2*('+str(ela_dist[i+1][1])+'-'+str(ela_dist[i][1])+')*'+str(d))
                print('y_neu=',y_neu)
                print('h1=',ela_dist[i][1])
                print('E_Ix'+str(i)+'='+str(E_Ix1))
                # E_Ix1=E*((ela_dist[i][0]+ela_dist[i+1][0])/2)*(tw*((ela_dist[i+1][1]-ela_dist[i][1])*d)**3/12+(tw*(ela_dist[i+1][1]-ela_dist[i][1])*d)*(((ela_dist[i][1]+ela_dist[i+1][1])/2-y_neu)*d)**2)
                E_Ix=E_Ix+E_Ix1
                print('E_Ix'+str(i)+'='+str(E_Ix)+str(E_Ix1))
        print('E_Ix='+str(E_Ix)) 
        # Calcualte centroid
        for i in range(len(ela_dist)-1):
            if ela_dist[i+1][1] <= tf/d :
                #A_y+=w*((ela_dist[i][0]+ela_dist[i+1][0])/2)*((ela_dist[i+1][1]-ela_dist[i][1])*d)*(ela_dist[i+1][1]+ela_dist[i][1])/2*d
                E_A_y1=E*(0.5*ela_dist[i][0]*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+1/3*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)-0.5*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d)*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2))*w
                #E_A_y1=E*(ela_dist[0][0])*w*((ela_dist[i+1][1]-ela_dist[i][1])*d)*(0)/2*d
                E_A_y=E_A_y+E_A_y1
                print('E_A_y'+str(i)+'='+str(E_A_y1))
                #A+=w*((ela_dist[i][0]+ela_dist[i+1][0])/2)*((ela_dist[i+1][1]-ela_dist[i][1])*d)
                E_A1=E*(ela_dist[i][0]+ela_dist[i+1][0])/2*w*(ela_dist[i+1][1]-ela_dist[i][1])*d
                print('E_A'+str(i)+'='+str(E_A1))
                E_A=E_A+E_A1
            elif ela_dist[i][1]>=(d-tf)/d:
                #A_y+=w*((ela_dist[i][0]+ela_dist[i+1][0])/2)*((ela_dist[i+1][1]-ela_dist[i][1])*d)*(ela_dist[i+1][1]+ela_dist[i][1])/2*d
                E_A_y1=E*(0.5*ela_dist[i][0]*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+1/3*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)-0.5*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d)*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2))*w
                #E_A_y1=E*(ela_dist[-1][0])*w*((ela_dist[i+1][1]-ela_dist[i][1])*d)*(1)/2*d
                E_A_y=E_A_y+E_A_y1
                print('E_A_y'+str(i)+'='+str(E_A_y1))
                #A+=w*((ela_dist[i][0]+ela_dist[i+1][0])/2)*((ela_dist[i+1][1]-ela_dist[i][1])*d)
                E_A1=E*(ela_dist[i][0]+ela_dist[i+1][0])/2*w*(ela_dist[i+1][1]-ela_dist[i][1])*d
                print('E_A'+str(i)+'='+str(E_A1))
                E_A=E_A+E_A1
            elif ela_dist[i][1] >= tf/d and ela_dist[i+1][1]<=(d-tf)/d:
                #A_y+=tw*((ela_dist[i][0]+ela_dist[i+1][0])/2)*((ela_dist[i+1][1]-ela_dist[i][1])*d)*(ela_dist[i+1][1]+ela_dist[i][1])/2*d         
                E_A_y1=E*(0.5*ela_dist[i][0]*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+1/3*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)-0.5*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d)*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2))*tw
                print('E_A_y'+str(i)+'='+str(E_A_y1))
                #E_A_y1=E*((ela_dist[i][0]+ela_dist[i+1][0])/2)*tw*((ela_dist[i+1][1]-ela_dist[i][1])*d)*(ela_dist[i+1][1]+ela_dist[i][1])/2*d
                E_A_y=E_A_y+E_A_y1
                print('E_A_y'+str(i)+'='+str(E_A_y1))
                #A+=tw*((ela_dist[i][0]+ela_dist[i+1][0])/2)*((ela_dist[i+1][1]-ela_dist[i][1])*d)
                E_A1=E*((ela_dist[i][0]+ela_dist[i+1][0])/2)*tw*((ela_dist[i+1][1]-ela_dist[i][1])*d)
                E_A=E_A+E_A1
                print('E_A'+str(i)+'='+str(E_A1))
        centroid=E_A_y/E_A
        print('E_A_y=',E_A_y)
        print('E_A=',E_A)
        print('E_A_y/E_A='+str(E_A_y)+'/'+str(E_A)+'='+str(centroid))
        centroid=round(centroid,8)
        print('centroid=',centroid)
        #centroid=128
        count=0
        a=0
        for i in range(len(ela_dist)-1):
            if ela_dist[i+1][1] <= tf/d :
                # Realistic method using neutral axis and shear centre in the integration
                #num_up1=E*((ela_dist[0][0]))*2*(1/6*(w/2)**3*(d-ela_dist[i][1]*d)**2+0.25*(w/2)*(d-ela_dist[i][1]*d)**4-2/3*(d-ela_dist[i][1]*d)**3*(w/2)*(d-s_c)+0.5*(w/2)*(d-ela_dist[i][1]*d)**2*(d-s_c)**2-1/3*(w/2)**3*(d-y_neu*d)*(d-ela_dist[i][1]*d)-1/3*(d-ela_dist[i][1]*d)**3*(w/2)*(d-d*y_neu)+(w/2)*(d-ela_dist[i][1]*d)**2*(d-s_c)*(d-y_neu*d)-(w/2)*(d-s_c)**2*(d-y_neu*d)*(d-ela_dist[i][1]*d)-(1/6*(w/2)**3*(d-ela_dist[i+1][1]*d)**2+0.25*(w/2)*(d-ela_dist[i+1][1]*d)**4-2/3*(d-ela_dist[i+1][1]*d)**3*(w/2)*(d-s_c)+0.5*(w/2)*(d-ela_dist[i+1][1]*d)**2*(d-s_c)**2-1/3*(w/2)**3*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)-1/3*(d-ela_dist[i+1][1]*d)**3*(w/2)*(d-d*y_neu)+(w/2)*(d-ela_dist[i+1][1]*d)**2*(d-s_c)*(d-y_neu*d)-(w/2)*(d-s_c)**2*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)))
                #a=(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*2*(1/9*(d-ela_dist[i][1]*d)**3*(w/2)**3-1/6*(d-y_neu*d)*(w/2)**3*(d-ela_dist[i][1]*d)**2+0.2*(d-ela_dist[i][1]*d)**5*(w/2)-0.5*(d-ela_dist[i][1]*d)**4*(w/2)*(d-s_c)-(d-y_neu*d)*(d-ela_dist[i][1]*d)**4*(w/2)-2/3*(d-y_neu*d)*(d-s_c)*(d-ela_dist[i][1]*d)**3*(w/2)+1/3*(d-s_c)**2*(d-ela_dist[i][1]*d)**3*(w/2)-0.5*(d-y_neu*d)*(d-s_c)**2*(d-ela_dist[i][1]*d)**2*(w/2)-(1/9*(d-ela_dist[i+1][1]*d)**3*(w/2)**3-1/6*(d-y_neu*d)*(w/2)**3*(d-ela_dist[i+1][1]*d)**2+0.2*(d-ela_dist[i+1][1]*d)**5*(w/2)-0.5*(d-ela_dist[i+1][1]*d)**4*(w/2)*(d-s_c)-(d-y_neu*d)*(d-ela_dist[i+1][1]*d)**4*(w/2)-2/3*(d-y_neu*d)*(d-s_c)*(d-ela_dist[i+1][1]*d)**3*(w/2)+1/3*(d-s_c)**2*(d-ela_dist[i+1][1]*d)**3*(w/2)-0.5*(d-y_neu*d)*(d-s_c)**2*(d-ela_dist[i+1][1]*d)**2*(w/2)))
                #c=-1/3*(w/2)**3*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)-1/3*(w/2)*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)**3-(w/2)*(d-ela_dist[i+1][1]*d)**2*(d-s_c)*(d-y_neu*d)+0.5*(d-s_c)**2*(d-ela_dist[i+1][1]*d)**2*(w/2)-(d-s_c)**2*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)*(w/2)
                #b=(1/6*(w/2)**3*(d-ela_dist[i+1][1]*d)**2+0.25*(w/2)*(d-ela_dist[i+1][1]*d)**4-2/3*(d-ela_dist[i+1][1]*d)**3*(w/2)*(d-s_c)-1/3*(w/2)**3*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)-1/3*(w/2)*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)**3-(w/2)*(d-ela_dist[i+1][1]*d)**2*(d-s_c)*(d-y_neu*d)+0.5*(d-s_c)**2*(d-ela_dist[i+1][1]*d)**2*(w/2)-(d-s_c)**2*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)*(w/2))
                # num_up1=E*((ela_dist[0][0]-(ela_dist[0][0]-ela_dist[0][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(1/6*0.25*w**3*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+0.25*w*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)-2/3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*w*(d-s_c))+(ela_dist[0][0]-ela_dist[0][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(1/9*0.25*w**3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)+0.2*(w)*((d-ela_dist[i][1]*d)**5-(d-ela_dist[i+1][1]*d)**5)-0.5*w*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)*(d-s_c))-(ela_dist[0][0]-(ela_dist[0][0]-ela_dist[0][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(d-d*y_neu)*(1/3*(0.25*w**3)*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))+1/3*w*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)-w*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*(d-s_c))-(d-d*y_neu)*(ela_dist[0][0]-ela_dist[0][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(1/6*0.25*w**3*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+0.25*w*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)-2/3*w*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*(d-s_c))+(ela_dist[0][0]-(ela_dist[0][0]-ela_dist[0][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*w*(d-s_c)**2+1/3*(ela_dist[0][0]-ela_dist[0][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*w*(d-s_c)**2-(d-d*y_neu)*(d-s_c)**2*(ela_dist[0][0]-(ela_dist[0][0]-ela_dist[0][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*w*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))-0.5*(d-d*y_neu)*(d-s_c)**2*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*w*((ela_dist[0][0]-ela_dist[0][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))))
                
                # New
                num_up1=E*(ela_dist[i][0]*(0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-y_neu*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d))+(ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]*d-ela_dist[i+1][1]*d)*(1/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-0.5*y_neu*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-0.5*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+ela_dist[i][1]*d*y_neu*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d)))*1/3*(w**3/4)+E*(ela_dist[i][0]*(0.25*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-2/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)*s_c+0.5*(s_c)**2*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-1/3*y_neu*d*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+s_c*y_neu*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-s_c**2*y_neu*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d))+(ela_dist[i+1][0]-ela_dist[i][0])/(ela_dist[i+1][1]*d-ela_dist[i][1]*d)*(0.2*((ela_dist[i+1][1]*d)**5-(ela_dist[i][1]*d)**5)-0.25*y_neu*d*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-0.25*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)+1/3*(ela_dist[i][1]*d)*y_neu*d*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-0.5*s_c*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)+2/3*s_c*y_neu*d*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+2/3*s_c*(ela_dist[i][1]*d)*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-s_c*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*y_neu*d+1/3*s_c**2*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-0.5*y_neu*d*s_c**2*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-0.5*s_c**2*(ela_dist[i][1]*d)*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+s_c**2*ela_dist[i][1]*d*y_neu*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d)))*w
                #num_up1=E*((ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]-ela_dist[i+1][1])/d*(1/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*(ela_dist[i][1]*d))+0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]*d-ela_dist[i+1][1]*d)*(y_neu*d)*(0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-ela_dist[i][1]*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d))-ela_dist[i][0]*(y_neu*d)*(ela_dist[i+1][1]*d-ela_dist[i][1]*d))*1/3*(w**3/4)+((ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]-ela_dist[i+1][1])/d*(0.2*((ela_dist[i+1][1]*d)**5-(ela_dist[i][1]*d)**5)-0.25*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)*ela_dist[i][1]*d-0.5*s_c*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)+2/3*s_c*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)*ela_dist[i][1]*d+1/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)*s_c**2-0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*(ela_dist[i][1]*d)*s_c**2)+ela_dist[i][0]*(0.25*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-2/3*s_c*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+0.5*s_c*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-(ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]-ela_dist[i+1][1])/d*(0.25*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-1/3*(ela_dist[i][1]*d)*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-2/3*s_c*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+s_c*(ela_dist[i][1]*d)*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*s_c**2-(ela_dist[i][1]*d*s_c**2*(ela_dist[i+1][1]*d-ela_dist[i][1]*d)))*y_neu*d-ela_dist[i][0]*(1/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-s_c**2*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+s_c**2*((ela_dist[i+1][1]*d)-(ela_dist[i][1]*d)))*y_neu*d)*w)
                
                # num_up1=E*((ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(1/6*0.25*w**3*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+0.25*w*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)-2/3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*w*(d-s[1_*c))+(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(1/9*0.25*w**3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)+0.2*(w)*((d-ela_dist[i][1]*d)**5-(d-ela_dist[i+1][1]*d)**5)-0.5*w*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)*(d-s_c))-(ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(d-d*y_neu)*(1/3*(0.25*w**3)*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))+1/3*w*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)-w*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*(d-s_c))-(d-d*y_neu)*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(1/6*0.25*w**3*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+0.25*w*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)-2/3*w*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*(d-s_c))+(ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*w*(d-s_c)**2+1/3*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*w*(d-s_c)**2-(d-d*y_neu)*(d-s_c)**2*(ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*w*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))-0.5*(d-d*y_neu)*(d-s_c)**2*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*w*((ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))))
                # Old version
                #num_up1=E*((ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*2*(1/6*(w/2)**3*(d-ela_dist[i][1]*d)**2+0.25*(w/2)*(d-ela_dist[i][1]*d)**4-2/3*(d-ela_dist[i][1]*d)**3*(w/2)*(d-s_c)-1/3*(w/2)**3*(d-y_neu*d)*(d-ela_dist[i][1]*d)-1/3*(w/2)*(d-y_neu*d)*(d-ela_dist[i][1]*d)**3-(w/2)*(d-ela_dist[i][1]*d)**2*(d-s_c)*(d-y_neu*d)+0.5*(d-s_c)**2*(d-ela_dist[i][1]*d)**2*(w/2)-(d-s_c)**2*(d-y_neu*d)*(d-ela_dist[i][1]*d)*(w/2)-(1/6*(w/2)**3*(d-ela_dist[i+1][1]*d)**2+0.25*(w/2)*(d-ela_dist[i+1][1]*d)**4-2/3*(d-ela_dist[i+1][1]*d)**3*(w/2)*(d-s_c)-1/3*(w/2)**3*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)-1/3*(w/2)*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)**3-(w/2)*(d-ela_dist[i+1][1]*d)**2*(d-s_c)*(d-y_neu*d)+0.5*(d-s_c)**2*(d-ela_dist[i+1][1]*d)**2*(w/2)-(d-s_c)**2*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)*(w/2)))+(ela_dist[i][0]-ela_dist[i+1][0])/(d-ela_dist[i][1]*d-(d-ela_dist[i+1][1]*d))*2*(1/9*(d-ela_dist[i][1]*d)**3*(w/2)**3-1/6*(d-y_neu*d)*(w/2)**3*(d-ela_dist[i][1]*d)**2+0.2*(d-ela_dist[i][1]*d)**5*(w/2)-0.5*(d-ela_dist[i][1]*d)**4*(w/2)*(d-s_c)-0.25*(d-y_neu*d)*(d-ela_dist[i][1]*d)**4*(w/2)-2/3*(d-y_neu*d)*(d-s_c)*(d-ela_dist[i][1]*d)**3*(w/2)+1/3*(d-s_c)**2*(d-ela_dist[i][1]*d)**3*(w/2)-0.5*(d-y_neu*d)*(d-s_c)**2*(d-ela_dist[i][1]*d)**2*(w/2)-(1/9*(d-ela_dist[i+1][1]*d)**3*(w/2)**3-1/6*(d-y_neu*d)*(w/2)**3*(d-ela_dist[i+1][1]*d)**2+0.2*(d-ela_dist[i+1][1]*d)**5*(w/2)-0.5*(d-ela_dist[i+1][1]*d)**4*(w/2)*(d-s_c)-0.25*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)**4*(w/2)-2/3*(d-y_neu*d)*(d-s_c)*(d-ela_dist[i+1][1]*d)**3*(w/2)+1/3*(d-s_c)**2*(d-ela_dist[i+1][1]*d)**3*(w/2)-0.5*(d-y_neu*d)*(d-s_c)**2*(d-ela_dist[i+1][1]*d)**2*(w/2))))
                # Simplified method by usiaiming atng shear centre and neutral axis in the calcualtion of stress
                #num_up1=E*(ela_dist[i][0])*(1/6*(s_c-ela_dist[i][1]*d)**2*(w/2)**3+1/4*(s_c-ela_dist[i][1]*d)**4*(w/2)-1/6*(s_c-ela_dist[i+1][1]*d)**2*(w/2)**3-1/4*(s_c-ela_dist[i+1][1]*d)**4*(w/2)-(1/6*(s_c-ela_dist[i][1]*d)**2*(-w/2)**3+1/4*(s_c-ela_dist[i][1]*d)**4*(-w/2)-1/6*(s_c-ela_dist[i+1][1]*d)**2*(-w/2)**3-1/4*(s_c-ela_dist[i+1][1]*d)**4*(-w/2)))
                #num_up+=1/6*(tf/2*(1+((ela_dist[i][0]+ela_dist[i+1][0])/2)**(1/3))-s_c)**2*(w/2)**3+1/4*(tf/2*(1+((ela_dist[i][0]+ela_dist[i+1][0])/2)**(1/3))-s_c)**4*(w/2)-1/6*(tf/2*(1-((ela_dist[i][0]+ela_dist[i+1][0])/2)**(1/3))-centroid)**2*(w/2)**3-1/4*(tf/2*(1-((ela_dist[i][0]+ela_dist[i+1][0])/2)**(1/3))-centroid)**4*(w/2)-1/6*(tf/2*(1+((ela_dist[i][0]+ela_dist[i+1][0])/2)**(1/3))-centroid)**2*(-w/2)**3-1/4*(tf/2*(1+((ela_dist[i][0]+ela_dist[i+1][0])/2)**(1/3))-centroid)**4*(-w/2)+1/6*(tf/2*(1-((ela_dist[i][0]+ela_dist[i+1][0])/2)**(1/3))-centroid)**2*(-w/2)**3+1/4*(tf/2*(1-((ela_dist[i][0]+ela_dist[i+1][0])/2)**(1/3))-centroid)**4*(-w/2)     
                #print('centroid_lf',centroid)
                num_up+=num_up1
                print('num_up'+str(i)+'='+str(num_up1))
                #print('num_up='+str(num_up))
            elif ela_dist[i][1]>=(d-tf)/d:
                
                
                # num_up1=E*((ela_dist[-1][0]-(ela_dist[-1][0]-ela_dist[-1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(1/6*0.25*w**3*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+0.25*w*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)-2/3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*w*(d-s_c))+(ela_dist[-1][0]-ela_dist[-1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(1/9*0.25*w**3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)+0.2*(w)*((d-ela_dist[i][1]*d)**5-(d-ela_dist[i+1][1]*d)**5)-0.5*w*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)*(d-s_c))-(ela_dist[-1][0]-(ela_dist[-1][0]-ela_dist[-1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(d-d*y_neu)*(1/3*(0.25*w**3)*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))+1/3*w*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)-w*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*(d-s_c))-(d-d*y_neu)*(ela_dist[-1][0]-ela_dist[-1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(1/6*0.25*w**3*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+0.25*w*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)-2/3*w*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*(d-s_c))+(ela_dist[-1][0]-(ela_dist[-1][0]-ela_dist[-1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*w*(d-s_c)**2+1/3*(ela_dist[-1][0]-ela_dist[-1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*w*(d-s_c)**2-(d-d*y_neu)*(d-s_c)**2*(ela_dist[-1][0]-(ela_dist[-1][0]-ela_dist[-1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*w*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))-0.5*(d-d*y_neu)*(d-s_c)**2*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*w*((ela_dist[-1][0]-ela_dist[-1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))))
                # New 
                num_up1=E*(ela_dist[i][0]*(0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-y_neu*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d))+(ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]*d-ela_dist[i+1][1]*d)*(1/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-0.5*y_neu*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-0.5*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+ela_dist[i][1]*d*y_neu*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d)))*1/3*(w**3/4)+E*(ela_dist[i][0]*(0.25*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-2/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)*s_c+0.5*(s_c)**2*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-1/3*y_neu*d*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+s_c*y_neu*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-s_c**2*y_neu*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d))+(ela_dist[i+1][0]-ela_dist[i][0])/(ela_dist[i+1][1]*d-ela_dist[i][1]*d)*(0.2*((ela_dist[i+1][1]*d)**5-(ela_dist[i][1]*d)**5)-0.25*y_neu*d*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-0.25*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)+1/3*(ela_dist[i][1]*d)*y_neu*d*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-0.5*s_c*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)+2/3*s_c*y_neu*d*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+2/3*s_c*(ela_dist[i][1]*d)*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-s_c*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*y_neu*d+1/3*s_c**2*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-0.5*y_neu*d*s_c**2*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-0.5*s_c**2*(ela_dist[i][1]*d)*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+s_c**2*ela_dist[i][1]*d*y_neu*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d)))*w
                
                #num_up1=E*((ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]-ela_dist[i+1][1])/d*(1/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*(ela_dist[i][1]*d))+0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]*d-ela_dist[i+1][1]*d)*(y_neu*d)*(0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-ela_dist[i][1]*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d))-ela_dist[i][0]*(y_neu*d)*(ela_dist[i+1][1]*d-ela_dist[i][1]*d))*1/3*(w**3/4)+((ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]-ela_dist[i+1][1])/d*(0.2*((ela_dist[i+1][1]*d)**5-(ela_dist[i][1]*d)**5)-0.25*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)*ela_dist[i][1]*d-0.5*s_c*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)+2/3*s_c*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)*ela_dist[i][1]*d+1/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)*s_c**2-0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*(ela_dist[i][1]*d)*s_c**2)+ela_dist[i][0]*(0.25*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-2/3*s_c*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+0.5*s_c*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-(ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]-ela_dist[i+1][1])/d*(0.25*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-1/3*(ela_dist[i][1]*d)*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-2/3*s_c*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+s_c*(ela_dist[i][1]*d)*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*s_c**2-(ela_dist[i][1]*d*s_c**2*(ela_dist[i+1][1]*d-ela_dist[i][1]*d)))*y_neu*d-ela_dist[i][0]*(1/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-s_c**2*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+s_c**2*((ela_dist[i+1][1]*d)-(ela_dist[i][1]*d)))*y_neu*d)*w)
                
                # num_up1=E*((ela_dist[-1][0]))*2*(1/6*(w/2)**3*(d-ela_dist[i][1]*d)**2+0.25*(w/2)*(d-ela_dist[i][1]*d)**4-2/3*(d-ela_dist[i][1]*d)**3*(w/2)*(d-s_c)+0.5*(w/2)*(d-ela_dist[i][1]*d)**2*(d-s_c)**2-1/3*(w/2)**3*(d-y_neu*d)*(d-ela_dist[i][1]*d)-1/3*(d-ela_dist[i][1]*d)**3*(w/2)*(d-d*y_neu)+(w/2)*(d-ela_dist[i][1]*d)**2*(d-s_c)*(d-y_neu*d)-(w/2)*(d-s_c)**2*(d-y_neu*d)*(d-ela_dist[i][1]*d)-(1/6*(w/2)**3*(d-ela_dist[i+1][1]*d)**2+0.25*(w/2)*(d-ela_dist[i+1][1]*d)**4-2/3*(d-ela_dist[i+1][1]*d)**3*(w/2)*(d-s_c)+0.5*(w/2)*(d-ela_dist[i+1][1]*d)**2*(d-s_c)**2-1/3*(w/2)**3*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)-1/3*(d-ela_dist[i+1][1]*d)**3*(w/2)*(d-d*y_neu)+(w/2)*(d-ela_dist[i+1][1]*d)**2*(d-s_c)*(d-y_neu*d)-(w/2)*(d-s_c)**2*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)))
                num_up+=num_up1
                print('num_up'+str(i)+'='+str(num_up1))           
            elif ela_dist[i][1] >= tf/d and ela_dist[i+1][1]<=(d-tf)/d:
                # Realistic method using neutral axis and shear centre in the integration
                #num_up1=E*((ela_dist[i+1][0]))*2*(1/6*(tw/2)**3*(d-ela_dist[i][1]*d)**2+0.25*(tw/2)*(d-ela_dist[i][1]*d)**4-2/3*(d-ela_dist[i][1]*d)**3*(tw/2)*(d-s_c)+0.5*(tw/2)*(d-ela_dist[i][1]*d)**2*(d-s_c)**2-1/3*(tw/2)**3*(d-y_neu*d)*(d-ela_dist[i][1]*d)-1/3*(d-ela_dist[i][1]*d)**3*(tw/2)*(d-d*y_neu)+(tw/2)*(d-ela_dist[i][1]*d)**2*(d-s_c)*(d-y_neu*d)-(tw/2)*(d-s_c)**2*(d-y_neu*d)*(d-ela_dist[i][1]*d)-(1/6*(tw/2)**3*(d-ela_dist[i+1][1]*d)**2+0.25*(tw/2)*(d-ela_dist[i+1][1]*d)**4-2/3*(d-ela_dist[i+1][1]*d)**3*(tw/2)*(d-s_c)+0.5*(tw/2)*(d-ela_dist[i+1][1]*d)**2*(d-s_c)**2-1/3*(tw/2)**3*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)-1/3*(d-ela_dist[i+1][1]*d)**3*(tw/2)*(d-d*y_neu)+(tw/2)*(d-ela_dist[i+1][1]*d)**2*(d-s_c)*(d-y_neu*d)-(tw/2)*(d-s_c)**2*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)))
                # num_up1=E*((ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(1/6*0.25*tw**3*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+0.25*tw*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)-2/3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*tw*(d-s_c))+(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(1/9*0.25*tw**3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)+0.2*(tw)*((d-ela_dist[i][1]*d)**5-(d-ela_dist[i+1][1]*d)**5)-0.5*tw*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)*(d-s_c))-(ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(d-d*y_neu)*(1/3*(0.25*tw**3)*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))+1/3*tw*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)-tw*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*(d-s_c))-(d-d*y_neu)*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(1/6*0.25*tw**3*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+0.25*tw*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)-2/3*tw*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*(d-s_c))+(ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*tw*(d-s_c)**2+1/3*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*tw*(d-s_c)**2-(d-d*y_neu)*(d-s_c)**2*(ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*tw*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))-0.5*(d-d*y_neu)*(d-s_c)**2*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*tw*((ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))))
                # New
                
                num_up1=E*(ela_dist[i][0]*(0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-y_neu*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d))+(ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]*d-ela_dist[i+1][1]*d)*(1/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-0.5*y_neu*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-0.5*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+ela_dist[i][1]*d*y_neu*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d)))*1/3*(tw**3/4)+E*(ela_dist[i][0]*(0.25*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-2/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)*s_c+0.5*(s_c)**2*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-1/3*y_neu*d*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+s_c*y_neu*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-s_c**2*y_neu*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d))+(ela_dist[i+1][0]-ela_dist[i][0])/(ela_dist[i+1][1]*d-ela_dist[i][1]*d)*(0.2*((ela_dist[i+1][1]*d)**5-(ela_dist[i][1]*d)**5)-0.25*y_neu*d*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-0.25*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)+1/3*(ela_dist[i][1]*d)*y_neu*d*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-0.5*s_c*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)+2/3*s_c*y_neu*d*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+2/3*s_c*(ela_dist[i][1]*d)*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-s_c*ela_dist[i][1]*d*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*y_neu*d+1/3*s_c**2*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-0.5*y_neu*d*s_c**2*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-0.5*s_c**2*(ela_dist[i][1]*d)*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+s_c**2*ela_dist[i][1]*d*y_neu*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d)))*tw
                
                #num_up1=E*((ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]-ela_dist[i+1][1])/d*(1/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*(ela_dist[i][1]*d))+0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]*d-ela_dist[i+1][1]*d)*(y_neu*d)*(0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-ela_dist[i][1]*d*(ela_dist[i+1][1]*d-ela_dist[i][1]*d))-ela_dist[i][0]*(y_neu*d)*(ela_dist[i+1][1]*d-ela_dist[i][1]*d))*1/3*(tw**3/4)+((ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]-ela_dist[i+1][1])/d*(0.2*((ela_dist[i+1][1]*d)**5-(ela_dist[i][1]*d)**5)-0.25*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)*ela_dist[i][1]*d-0.5*s_c*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)+2/3*s_c*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)*ela_dist[i][1]*d+1/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)*s_c**2-0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*(ela_dist[i][1]*d)*s_c**2)+ela_dist[i][0]*(0.25*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-2/3*s_c*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+0.5*s_c*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)-(ela_dist[i][0]-ela_dist[i+1][0])/(ela_dist[i][1]-ela_dist[i+1][1])/d*(0.25*((ela_dist[i+1][1]*d)**4-(ela_dist[i][1]*d)**4)-1/3*(ela_dist[i][1]*d)*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-2/3*s_c*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)+s_c*(ela_dist[i][1]*d)*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+0.5*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)*s_c**2-(ela_dist[i][1]*d*s_c**2*(ela_dist[i+1][1]*d-ela_dist[i][1]*d)))*y_neu*d-ela_dist[i][0]*(1/3*((ela_dist[i+1][1]*d)**3-(ela_dist[i][1]*d)**3)-s_c**2*((ela_dist[i+1][1]*d)**2-(ela_dist[i][1]*d)**2)+s_c**2*((ela_dist[i+1][1]*d)-(ela_dist[i][1]*d)))*y_neu*d)*tw)
                # Old version
                #num_up1=E*((ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*2*(1/6*(tw/2)**3*(d-ela_dist[i][1]*d)**2+0.25*(tw/2)*(d-ela_dist[i][1]*d)**4-2/3*(d-ela_dist[i][1]*d)**3*(tw/2)*(d-s_c)-1/3*(tw/2)**3*(d-y_neu*d)*(d-ela_dist[i][1]*d)-1/3*(tw/2)*(d-y_neu*d)*(d-ela_dist[i][1]*d)**3-(tw/2)*(d-ela_dist[i][1]*d)**2*(d-s_c)*(d-y_neu*d)+0.5*(d-s_c)**2*(d-ela_dist[i][1]*d)**2*(tw/2)-(d-s_c)**2*(d-y_neu*d)*(d-ela_dist[i][1]*d)*(tw/2)-(1/6*(tw/2)**3*(d-ela_dist[i+1][1]*d)**2+0.25*(tw/2)*(d-ela_dist[i+1][1]*d)**4-2/3*(d-ela_dist[i+1][1]*d)**3*(tw/2)*(d-s_c)-1/3*(tw/2)**3*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)-1/3*(tw/2)*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)**3-(tw/2)*(d-ela_dist[i+1][1]*d)**2*(d-s_c)*(d-y_neu*d)+0.5*(d-s_c)**2*(d-ela_dist[i+1][1]*d)**2*(tw/2)-(d-s_c)**2*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)*(tw/2)))+(ela_dist[i][0]-ela_dist[i+1][0])/(d-ela_dist[i][1]*d-(d-ela_dist[i+1][1]*d))*2*(1/9*(d-ela_dist[i][1]*d)**3*(tw/2)**3-1/6*(d-y_neu*d)*(tw/2)**3*(d-ela_dist[i][1]*d)**2+0.2*(d-ela_dist[i][1]*d)**5*(tw/2)-0.5*(d-ela_dist[i][1]*d)**4*(tw/2)*(d-s_c)-0.25*(d-y_neu*d)*(d-ela_dist[i][1]*d)**4*(tw/2)-2/3*(d-y_neu*d)*(d-s_c)*(d-ela_dist[i][1]*d)**3*(tw/2)+1/3*(d-s_c)**2*(d-ela_dist[i][1]*d)**3*(tw/2)-0.5*(d-y_neu*d)*(d-s_c)**2*(d-ela_dist[i][1]*d)**2*(tw/2)-(1/9*(d-ela_dist[i+1][1]*d)**3*(tw/2)**3-1/6*(d-y_neu*d)*(tw/2)**3*(d-ela_dist[i+1][1]*d)**2+0.2*(d-ela_dist[i+1][1]*d)**5*(tw/2)-0.5*(d-s_c)*(d-ela_dist[i+1][1]*d)**4*(tw/2)-0.25*(d-y_neu*d)*(d-ela_dist[i+1][1]*d)**4*(tw/2)-2/3*(d-y_neu*d)*(d-s_c)*(d-ela_dist[i+1][1]*d)**3*(tw/2)+1/3*(d-s_c)**2*(d-ela_dist[i+1][1]*d)**3*(tw/2)-0.5*(d-y_neu*d)*(d-s_c)**2*(d-ela_dist[i+1][1]*d)**2*(tw/2))))
                # Simplified method by using shear centre and neutral axis in the calcualtion of stress
                #num_up1=E*((ela_dist[i][0]))*(1/6*(s_c-ela_dist[i][1]*d)**2*(tw/2)**3+1/4*(s_c-ela_dist[i][1]*d)**4*(tw/2)-1/6*(s_c-ela_dist[i+1][1]*d)**2*(tw/2)**3-1/4*(s_c-ela_dist[i+1][1]*d)**4*(tw/2)-(1/6*(s_c-ela_dist[i][1]*d)**2*(-tw/2)**3+1/4*(s_c-ela_dist[i][1]*d)**4*(-tw/2)-1/6*(s_c-ela_dist[i+1][1]*d)**2*(-tw/2)**3-1/4*(s_c-ela_dist[i+1][1]*d)**4*(-tw/2)))
                #num_up=num_up+1/6*((s_c-ela_dist[i][1]*d)*(inter_ela)**(0.25))**2*(tw/2*(inter_ela)**(0.25))**3+1/4*((s_c-ela_dist[i][1]*d)*(inter_ela)**(0.25))**4*((inter_ela)**(0.25)*tw/2)-1/6*((centroid-ela_dist[i+1][1]*d)*(inter_ela)**(0.25))**2*((inter_ela)**(0.25)*tw/2)**3-1/4*((centroid-ela_dist[i+1][1]*d)*(inter_ela)**(0.25))**4*((inter_ela)**(0.25)*tw/2)-(1/6*((centroid-ela_dist[i][1]*d)*(inter_ela)**(0.25))**2*(-1*(inter_ela)**(0.25)*tw/2)**3+1/4*((centroid-ela_dist[i][1]*d)*(inter_ela)**(0.25))**4*(-1*(inter_ela)**(0.25)*tw/2)-1/6*((centroid-ela_dist[i+1][1]*d)*(inter_ela)**(0.25))**2*(-1*(inter_ela)**(0.25)*tw/2)**3-1/4*((centroid-ela_dist[i+1][1]*d)*(inter_ela)**(0.25))**4*(-1*(inter_ela)**(0.25)*tw/2))
                print('num_up'+str(i)+'='+str(num_up1))
                num_up+=num_up1
                #num_up+=1/6*(tf/ 2*(1-(ela_dist[i][0]+ela_dist[i+1][0])/2)-centnum_up+=1/6*(tbf/2*(1-(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**2*(w/2)**3+1/4*(tf/2*(1-(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**4*(w/2)-1/6*(tf/2*(1+(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**2*(w/2)**3-1/4*(tf/2*(1+(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**4*(w/2)-1/6*(tf/2*(1-(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**2*(-1*w/2)**3-1/4*(tf/2*(1-(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**4*(-1*w/2)+1/6*(tf/2*(1+(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**2*(-1*w/2)**3+1/4*(tf/2*(1+(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**4*(-1*w/2)roid)**2*(w/2)**3+1/4*(tf/2*(1-(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**4*(w/2)-1/6*(tf/2*(1+(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**2*(w/2)**3-1/4*(tf/2*(1+(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**4*(w/2)-1/6*(tf/2*(1-(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**2*(-1*w/2)**3-1/4*(tf/2*(1-(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**4*(-1*w/2)+1/6*(tf/2*(1+(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**2*(-1*w/2)**3+1/4*(tf/2*(1+(ela_dist[i][0]+ela_dist[i+1][0])/2)-centroid)**4*(-1*w/2)
        # Calculate Ix
        print('num_up='+str(num_up))
        print('E_Ix='+str(E_Ix))
        print('centroid='+str(centroid))
        print('s_c='+str(s_c))
        # Realistic method using neutral axis and shear centre in the integration
        beta=num_up/E_Ix
        # Simplified method by using shear centre and neutral axis in the calcualtion of stress
        #beta=num_up/E_Ix+2*(s_c-y_neu*d)
        return beta
    def Mpl(self):
        tempdist=self.t_dist
        d=self.d
        w=self.w
        tf=self.ft
        tw=self.wt
        fpl=self.fpl
        temp=[]
        int_temp=[]
        rev_int_temp=[]
        # temperatures
        for i in range(len(tempdist)):
            temp.append(tempdist[i][0])
        temp.sort()
        for i in range(len(tempdist)-1):
            for j in range(1,13):
                if 100*j<tempdist[i][0] and 100*j>tempdist[i+1][0] or 100*j>tempdist[i][0] and 100*j<tempdist[i+1][0]:
                    int_temp.append(100*j)
        print('int_temp',int_temp)
        rev_int_temp=int_temp.copy()
        rev_int_temp.reverse()
        # Interpolation of temperatures and positions
        for k in range(len(tempdist)+len(int_temp)-1):
            if tempdist[k][0]>tempdist[k+1][0]:
                for j in range(1,13):
                    if tempdist[k][0]>j*100 and tempdist[k+1][0]<j*100:
                        pos=self.intemp(j*100,tempdist[k],tempdist[k+1])
                        tempdist.insert(k+1,[j*100,pos])
            elif tempdist[k][0]<tempdist[k+1][0]:
                for j in range(1,13):
                    if tempdist[k][0]<j*100 and tempdist[k+1][0]>j*100:
                        pos=self.intemp(j*100,tempdist[k],tempdist[k+1])
                        tempdist.insert(k+1,[j*100,pos])
        print('temp_dist',tempdist)
        disp_tempdist=[]
        for i in tempdist:
            disp_tempdist.append([i[0],round(i[1],2)])
        #print('Temp.distribution =',disp_tempdist)
        stre_dist=[]
        i=0
        for i in range(len(tempdist)):
            stre_dist.append(tempdist[i].copy())
        i=0
        # Strength Reduction according to EC3
        i=0
        for stre_pt in stre_dist:
            co_of_red=self.stre_red(stre_pt[0])
            stre_dist[i][0]=co_of_red
            i=i+1
        a_s=tf/d
        b_s=(d-tf)/d
        uf_lower_stre=self.interpolation(a_s,stre_dist)
        lf_upper_stre=self.interpolation(b_s,stre_dist)
        stre_dist.append([uf_lower_stre,a_s])
        stre_dist.append([lf_upper_stre,b_s])
        stre_dist=self.Sort(stre_dist)
        counter_half=0
        area1=0
        area2=0
        area3=0
        area4=0
        y_neu=[]
        y_neutral=0
        for i in range(len(stre_dist)-1):
            if stre_dist[i+1][1]==0.5:
                break
            else:
                counter_half=counter_half+1
        i=0
        disp_stre_dist=[]
        for i in stre_dist:
            disp_stre_dist.append([round(i[0],2),round(i[1],2)])

        for i in range(1,len(stre_dist)): 
            area1=0
            area2=0
            area3=0
            area4=0     
            for j in range(i):
                if stre_dist[j+1][1]<=tf/d or stre_dist[j][1]>=(d-tf)/d and stre_dist[j+1][1]<=1:
                    area1=area1+(stre_dist[j][0]+stre_dist[j+1][0])*(stre_dist[j+1][1]-stre_dist[j][1])/2*w
                elif stre_dist[j][1]>=tf/d and stre_dist[j+1][1]<=(d-tf)/d:
                    area1=area1+(stre_dist[j][0]+stre_dist[j+1][0])*(stre_dist[j+1][1]-stre_dist[j][1])/2*tw
            #if i==len(stre_dist)-1:
            #    if stre_dist[i+1][1]<=tf/d or stre_dist[i][1]>=(d-tf)/d and stre_dist[i+1][1]<=1:
            #        area2=area2+(stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*w
            #    elif stre_dist[i][1]>=tf/d and stre_dist[i+1][1]<=(d-tf)/d:
            #        area2=area2+(stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*tw
            #else:    
            for k in range(i,len(stre_dist)-1):
                if stre_dist[k+1][1]<=tf/d or stre_dist[k][1]>=(d-tf)/d and stre_dist[k+1][1]<=1:
                    area2=area2+(stre_dist[k][0]+stre_dist[k+1][0])*(stre_dist[k+1][1]-stre_dist[k][1])/2*w
                elif stre_dist[k][1]>=tf/d and stre_dist[k+1][1]<=(d-tf)/d:
                    area2=area2+(stre_dist[k][0]+stre_dist[k+1][0])*(stre_dist[k+1][1]-stre_dist[k][1])/2*tw
            for j in range(i-1):
                if stre_dist[j+1][1]<=tf/d or stre_dist[j][1]>=(d-tf)/d and stre_dist[j+1][1]<=1:
                    area3=area3+(stre_dist[j][0]+stre_dist[j+1][0])*(stre_dist[j+1][1]-stre_dist[j][1])/2*w
                elif stre_dist[j][1]>=tf/d and stre_dist[j+1][1]<=(d-tf)/d:
                    area3=area3+(stre_dist[j][0]+stre_dist[j+1][0])*(stre_dist[j+1][1]-stre_dist[j][1])/2*tw
            for k in range(i-1,len(stre_dist)-1):
                if stre_dist[k+1][1]<=tf/d or stre_dist[k][1]>=(d-tf)/d and stre_dist[k+1][1]<=1:
                    area4=area4+(stre_dist[k][0]+stre_dist[k+1][0])*(stre_dist[k+1][1]-stre_dist[k][1])/2*w
                elif stre_dist[k][1]>=tf/d and stre_dist[k+1][1]<=(d-tf)/d:
                    area4=area4+(stre_dist[k][0]+stre_dist[k+1][0])*(stre_dist[k+1][1]-stre_dist[k][1])/2*tw     
            if area1>=area2 and area3<=area4:
                x = symbols('x')
                f_y_inter = (x-stre_dist[i-1][1])*(stre_dist[i][0]-stre_dist[i-1][0])/(stre_dist[i][1]-stre_dist[i-1][1])+stre_dist[i-1][0]
                if stre_dist[i][1]<=tf/d or stre_dist[i-1][1]>=(d-tf)/d and stre_dist[i][1]<=1:
                    expr = area3+ w*(x-stre_dist[i-1][1])*(f_y_inter+stre_dist[i-1][0])/2-(area2+w*(stre_dist[i][1]-x)*(f_y_inter+stre_dist[i][0])/2)
                elif stre_dist[i-1][1]>=tf/d and stre_dist[i][1]<=(d-tf)/d:
                    expr = area3+ tw*(x-stre_dist[i-1][1])*(f_y_inter+stre_dist[i-1][0])/2-(area2+tw*(stre_dist[i][1]-x)*(f_y_inter+stre_dist[i][0])/2)
                #print('Equation of neutral axis',expr)
                y_neu=solve(expr)
                y_neu_set=[]
                for sol in y_neu:
                    y_neu_set.append(sol)
                    print('y_neu_set',y_neu_set)
                    if sol<=stre_dist[i][1] and sol>=stre_dist[i-1][1]: 
                        y_neutral=sol

        y_neutral=round(y_neutral,8)
        print('plastic_neutral_axis_position='+str(y_neutral))
        #print('\n<<<<<<  Non_dimensional_plastic_neutral_axis_position  >>>>>>')
        #print('Equation of neutral axis = ',expr)
        #print('plastic_neutral_axis_position='+str(y_neutral))  
        flag=0
        for i in tempdist:
            if i[1]==y_neutral:
                flag=1
                break  
        y_neutral_stre1=self.y_neutral_stre(y_neutral,stre_dist)
        if flag==0:
            stre_dist.append([y_neutral_stre1,y_neutral])
        stre_dist=self.Sort(stre_dist)
        print('stre_dist=',stre_dist)
        i=0
        #print('\n<<<<<<  Strength Distribution  >>>>>>')
        #print('Strength distribution = [[Strength reduction factor,Position (x/d, x is the distance from top of the beam)],...]')
        #print('Strength distribution =',disp_stre_dist)
        m=0
        #print('\n<<<<<<  Calculate the plastic bending moment of each part  >>>>>>')
        #print('x is the distance from top of the beam')
        for i in range(len(stre_dist)-1):
            #print('\nPosition of calculation point (x/d)=',round(stre_dist[i][1],2))
            if i==0:
                if stre_dist[i][0]>=stre_dist[i+1][0]:
                    #print('Current strength reduction factor >= the next strength reduction factor')
                    if stre_dist[i][1] < tf/d:
                        #print('the next calculation point is in the upper flange')
                        m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*w*d*d)*fpl+m
                        #print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-((2*min('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+')+max('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+'))/(('+str(round(stre_dist[i+1][0],2))+')+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                    elif stre_dist[i][1] >= tf/d and stre_dist[i][1] < (d-tf)/d:
                        #print('the next calculation point is in the web')
                        m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*tw*d*d)*fpl+m
                        #print( 'Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-((2*min('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+')+max('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+'))/(('+str(round(stre_dist[i+1][0],2))+')+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                    elif stre_dist[i][1] >= (d-tf)/d and stre_dist[i][1] < 1:
                        #print('the next calculation point is in the lower flange')
                        m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*w*d*d)*fpl+m
                        #print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-((2*min('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+')+max('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+'))/(('+str(round(stre_dist[i+1][0],2))+')+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')      
                elif stre_dist[i][0]<stre_dist[i+1][0]:
                    #print('Current strength reduction factor < the next strength reduction factor')
                    if stre_dist[i][1] < tf/d:
                        #print('the next calculation point is in the upper flange')
                        m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-stre_dist[i+1][1]+((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*w*d*d)*fpl+m
                        #print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*min('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+')+max('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+'))/(('+str(round(stre_dist[i+1][0],2))+')+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                    elif stre_dist[i][1] >= tf/d and stre_dist[i][1] < (d-tf)/d:
                        #print('the next calculation point is in the web')
                        m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-stre_dist[i+1][1]+((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*tw*d*d)*fpl+m
                        #print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*min('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+')+max('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+'))/(('+str(round(stre_dist[i+1][0],2))+')+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                    elif stre_dist[i][1] >= (d-tf)/d and stre_dist[i][1] < 1:
                        #print('the next calculation point is in the lower flange')
                        m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-stre_dist[i+1][1]+((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*w*d*d)*fpl+m
                        #print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*min('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+')+max('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+'))/(('+str(round(stre_dist[i+1][0],2))+')+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
            elif i>0:
                if stre_dist[i][0]>=stre_dist[i+1][0]:
                    #print('Current strength reduction factor >= the next strength reduction factor')
                    if stre_dist[i][1] < tf/d:
                        #print('the next calculation point is in the upper flange')
                        m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3+stre_dist[i][1]))*w*d*d)*fpl+m
                        #print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*'+str(min(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+'+'+str(max(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+')/('+str(round(stre_dist[i+1][0],2))+'+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                    elif stre_dist[i][1] >= tf/d and stre_dist[i][1] < (d-tf)/d:
                        #print('the next calculation point is in the web')
                        m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3+stre_dist[i][1]))*tw*d*d)*fpl+m
                        #print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*'+str(min(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+'+'+str(max(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+')/('+str(round(stre_dist[i+1][0],2))+'+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(tw)+'*'+str(d)+'*'+str(d)+'*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                    elif stre_dist[i][1] >= (d-tf)/d and stre_dist[i][1] < 1:
                        #print('the next calculation point is in the lower flange')
                        m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3+stre_dist[i][1]))*w*d*d)*fpl+m
                        #print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*'+str(min(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+'+'+str(max(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+')/('+str(round(stre_dist[i+1][0],2))+'+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(w)+'*'+str(d)+'*'+str(d)+'*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                elif stre_dist[i][0]<stre_dist[i+1][0]:
                    #print('Current strength reduction factor < the next strength reduction factor')
                    if stre_dist[i][1] < tf/d:
                        #print('the next calculation point is in the upper flange')
                        m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-stre_dist[i+1][1]+((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*w*d*d)*fpl+m
                        #print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*'+str(min(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+'+'+str(max(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+')/('+str(round(stre_dist[i+1][0],2))+'+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(w)+'*'+str(d)+'*'+str(d)+'*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                    elif stre_dist[i][1] >= tf/d and stre_dist[i][1] < (d-tf)/d:
                        #print('the next calculation point is in the web')
                        m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-stre_dist[i+1][1]+((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*tw*d*d)*fpl+m
                        #print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*'+str(min(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+'+'+str(max(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+')/('+str(round(stre_dist[i+1][0],2))+'+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(tw)+'*'+str(d)+'*'+str(d)+'*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                    elif stre_dist[i][1] >= (d-tf)/d and stre_dist[i][1] < 1:
                        #print('the next calculation point is in the lower flange')
                        m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-stre_dist[i+1][1]+((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*w*d*d)*fpl+m

                        #print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*'+str(min(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+'+'+str(max(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+')/('+str(round(stre_dist[i+1][0],2))+'+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(w)+'*'+str(d)+'*'+str(d)+'*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
        #print('Overall plastic bending moment = Sum Plastic bending moment * 2 = '+str(round(m*1e-6,2))+'kN*m\n')
        #print('<<<<<<<<<  Calculation finnished  >>>>>>>>>\n        **************************')
        print('Plastic bending moment='+str(round(m*1e-6,2))+'kN*m')
    def G_KT(self,G,ela_dist,d,tw,w,tf):
        G_K_T=0
        G_K_T1=0
        for i in range(len(ela_dist)-1):
            if ela_dist[i+1][1] <= tf/d:
                # G_K_T1=G*((ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(1/3*(0.25*w**3)*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))+1/3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*w-((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*w*(d-s_c))+(ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(d-s_c)**2*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*w+(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(1/6*0.25*w**3*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+0.25*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)*w-2/3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*w*(d-s_c))+0.5*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*w*(d-s_c)**2)
                #G_K_T1=G*(   *(1-0.63*tf/w)
                #G_K_T1=G*((ela_dist[0][0]))*w*(((ela_dist[1][1]-ela_dist[0][1])*d))**3/3   *(1-0.63*tf/w)
                G_K_T1=G*((ela_dist[i+1][0]+ela_dist[i][0])/2)*w*(((ela_dist[i+1][1]-ela_dist[i][1])*d))**3/3*(1-0.63*tf/w)
                G_K_T=G_K_T+G_K_T1
                print('G_K_T'+str(i)+'='+str(G_K_T1))
            elif ela_dist[i][1]>=(d-tf)/d:
                #G_K_T1=G*((ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(1/3*(0.25*w**3)*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))+1/3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*w-((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*w*(d-s_c))+(ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(d-s_c)**2*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*w+(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(1/6*0.25*w**3*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+0.25*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)*w-2/3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*w*(d-s_c))+0.5*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*w*(d-s_c)**2)
                #G_K_T1=G*((ela_dist[i+1][0]+ela_dist[i][0])/2)*w*(((ela_dist[i+1][1]-ela_dist[i][1])*d))**3/3 (1-0.63*tf/w)
                G_K_T1=G*((ela_dist[i+1][0]+ela_dist[i][0])/2)*w*(((ela_dist[i+1][1]-ela_dist[i][1])*d))**3/3*(1-0.63*tf/w)
                G_K_T=G_K_T+G_K_T1
                print('G_K_T'+str(i)+'='+str(G_K_T1))
            elif ela_dist[i][1]  >= tf/d and ela_dist[i+1][1]<=(d-tf)/d:
                #s_c=(ela_dist[i][1]*d+ela_dist[i+1][1]*d)/2
                #G_K_T1=G*((ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(1/3*(0.25*tw**3)*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))+1/3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*tw-((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*tw*(d-s_c))+(ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(d-s_c)**2*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*tw+(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(1/6*0.25*tw**3*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+0.25*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)*tw-2/3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*tw*(d-s_c))+0.5*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*tw*(d-s_c)**2)
                #G_K_T1=G*((ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*((tw)*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))+1/3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*tw-((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*tw*(d-s_c))+(ela_dist[i][0]-(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(d-ela_dist[i][1]*d))*(d-s_c)**2*((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*tw+(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*(1/2*tw*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)+0.25*((d-ela_dist[i][1]*d)**4-(d-ela_dist[i+1][1]*d)**4)*tw-2/3*((d-ela_dist[i][1]*d)**3-(d-ela_dist[i+1][1]*d)**3)*tw*(d-s_c))+0.5*(ela_dist[i][0]-ela_dist[i+1][0])/((d-ela_dist[i][1]*d)-(d-ela_dist[i+1][1]*d))*((d-ela_dist[i][1]*d)**2-(d-ela_dist[i+1][1]*d)**2)*tw*(d-s_c)**2)
                G_K_T1=G*((ela_dist[i+1][0]+ela_dist[i][0])/2)*(tw)**3*((ela_dist[i+1][1]-ela_dist[i][1])*d)/3
                G_K_T=G_K_T+G_K_T1
                print('G_K_T'+str(i)+'='+str(G_K_T1))
        print('G_K_T='+str(G_K_T))
        return G_K_T
    def E_c_w(self,d,w,tf,ela_dist,E):
        E_c_w=0
        d_dot=d-tf
        # E_c_w=E_I_z*(d-((ela_dist[0][0])*tf+(ela_dist[-1][0])*tf)/2)**2/4  
        E_c_w=(d_dot)**2*E*tf*(w)**3*(ela_dist[0][0])*(1/(1+(((ela_dist[0][0]+ela_dist[1][0])/2)/((ela_dist[-1][0]+ela_dist[-2][0])/2))**0.01))/12
        return E_c_w

    def Mcr(self):
        tempdist=self.t_dist
        d=self.d
        w=self.w
        tf=self.ft
        tw=self.wt
        fpl=self.fpl
        E=self.E
        G=self.G
        L=self.L
        k=1
        kw=0.14
        a=k/kw
        
        # W10x49 0.4624
        b2=0.7921
        ela_dist,ela_axis,tempdist=self.elastic_neutral_axis()
        print(ela_axis)
        print(ela_dist)
        s_c=self.shear_centre(ela_dist,w,tf,tw,d)
        print('shear centre='+str(s_c))
        beta=self.beta_x(E,d,tw,tf,ela_dist,w,s_c,ela_axis)
        G_I_t=self.G_KT(G,ela_dist,d,tw,w,tf)
        E_I_w=self.E_c_w(d,w,tf,ela_dist,E)
        E_I_z=self.E_I_z(E,d,w,tw,tf,ela_dist)
        Mcr=0.7056*(pi)**2*E_I_z*beta/2/L**2*(1-(1+4/beta**2*(L**2/(0.7056*pi**2)*G_I_t/E_I_z+E_I_w/E_I_z*(a)**2))**0.5)
        Mcr=abs(Mcr)
        print('Mcr='+str(round(Mcr*1e-6,2))+'kN*m')
        return Mcr