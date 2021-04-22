from flask import render_template, redirect, url_for, flash, abort

from simlab import app
from simlab.filters import low_pass_filter,high_pass_filter
from simlab.torque_slip import torque_vs_slip

import io
from flask import Response, request
from matplotlib.backends.backend_svg import FigureCanvasSVG
import cmath

import matplotlib
from matplotlib.figure import Figure
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt

experiments={
    'aE':{
        'name'         :  'Analog Electronics',
        'experiments'  :  [
                                ['aE/ae01','pn junction diode iv characterstics',' description', 'image']
                            ]
    },
    'dcM1':{
        'name'          : 'DC Machines 1',
        'experiments'   :  [
                                ['dcM1/dcm01','Torque-Slip characterstics', 'description', 'image']
                            ]
    },
    'eMes':{
        'name'          : 'Electrical Measurements',
        'experiments'   : [
                                ['ohmlaw',"Ohm's Law", 'description', 'image'],
                                ['desauty',"DeSauty's Bridge", 'description''image'],
                                ['wheatstone',"WheatStone Bridge", 'description''image'],
                                
                            ]
    },
    'icApp':{
    'name'          : 'IC Applications',
    'experiments'   : [
                            ['icApp/icApp01','Low Pass Filter', 'description', 'image'],
                            ['icApp/icApp02','High Pass Filter', 'description', 'image'],
                        ]
    },
    'drives':{
    'name'          : 'Electrical Drives',
    'experiments'   : [
                            ['chopper','Speed Control of DC Motor using TYPE-A Chopper', 'description', 'image'],
                        ]
    },

}


class Ohm:
    def __init__(self):
        self.disabled_set=""
        self.disabled_append="disabled"
        self.allrecord=[]
        self.setvalue=0
        self.record={}
        self.circ=0
    def plot_graph(self):
        a=[]
        b=[]
        reco={}
        for reco in self.allrecord:
            b.append(reco['voltage'])
            a.append(reco['current'])
        figure = plt.figure(figsize = (10,5))
        plt.xlabel("Current in ampere")
        plt.ylabel("Voltage (volt)")
        plt.plot(a,b,linestyle='--', marker='o', color='b')
        plt.grid()

    def empty_graph(self):
        self.circ=0
        self.disabled_set = ""
        self.disabled_append = "disabled"
        self.allrecord = []
        self.plot_graph()

ohm=Ohm()
ohm.empty_graph()


#General Bridge
class Bridge:
    def _init_(self):
        self.z1=0
        self.z2=0
        self.z3=0
        self.z4=0
        self.acvol=0
        self.freq=0
        self.detector_mag_mV=0
        self.balanced='not balanced'
        self.z1_calc=0
    def put(self,z1=0,z2=0,z3=0,z4=0,acvol=12,freq=1000):
        self.z1=z1
        self.z2=z2
        self.z3=z3
        self.z4=z4
        self.acvol=acvol
        self.freq=freq
    def self_calc(self):
        detector = ( self.acvol * ( (self.z1*self.z4) - (self.z2*self.z3) ) )/( (self.z1+self.z3) * (self.z2+self.z4) )
        phase_bal_detect = round( float( 180*( cmath.phase(self.z1)+cmath.phase(self.z4) - cmath.phase(self.z2)+cmath.phase(self.z3) )/cmath.pi ), 5 )
        self.detector_mag_mV = round( float(1000*abs(detector)), 1)
        if self.detector_mag_mV<5 and phase_bal_detect<1:
            self.balanced='balanced'
            print('balanced')
        else:
            self.balanced='not balanced'
        self.z1_calc = self.z2*self.z3/self.z4
bridge=Bridge()

#Bridges to be used
class Desauty:
    def __init__(self):
        #fixed unknowns
        self.C1=0
        self.r1=0
        #variable knowns
        self.ind=0
        self.R2=0
        self.R3=0
        self.hide='disabled'
    def setunknown(self):
        C1val = [0.10e-6, 0.22e-6, 0.47e-6]
        r1val = [70, 24, 5]
        self.C1 = C1val[self.ind]
        self.r1 = r1val[self.ind]
        print('Desauty C1 is set at ' + str(self.C1))
        print('Desauty r1 is set at ' + str(self.r1))
    def calc(self):
        z = bridge.z1_calc
        self.C1_calc = round( 1 /( 2*cmath.pi*bridge.freq*(z.imag) ), 9 )
        self.r1_calc = round( z.real - 10, 3 )
        self.dissip2 = round( 2*cmath.pi*1000*0.47e-6*5, 5)
        self.dissip1 = round( 2*cmath.pi*1000*self.C1_calc*self.r1_calc, 5)
    def bridgify(self):
        z1 = float(10 + self.r1) + (1/(2*cmath.pi*1000*self.C1))*1j
        z2 = float(5 + self.R2) + (1/(2*cmath.pi*1000*0.47e-6))*1j
        z3 = self.R3
        z4 = float(1000)
        bridge.put(z1,z2,z3,z4,12,1000)
        bridge.self_calc()
        if bridge.balanced=='balanced':
            self.calc()
            self.hide=''
        elif bridge.balanced=='not balanced':
            self.hide = 'disabled'
des=Desauty()
des.setunknown()


class Wheat:
    def __init__(self):
        #fixed unknowns
        self.R1=0
        #variable knowns
        self.ind=0
        self.R2=0
        self.R3=0
        self.hide='disabled'
    def setunknown(self):
        R1val = [60, 370, 730]
        self.R1 = R1val[self.ind]
        print('Wheatstone R1 is set at' + str(self.R1))
    def calc(self):
        z = bridge.z1_calc
        self.R1_calc = round( z.real, 3 )
    def bridgify(self):
        z1 = float(self.R1)
        z2 = self.R2
        z3 = self.R3
        z4 = float(1000)
        bridge.put(z1,z2,z3,z4,12,1000)
        bridge.self_calc()
        if bridge.balanced=='balanced':
            self.calc()
            self.hide=''
        elif bridge.balanced=='not balanced':
            self.hide = 'disabled'
w=Wheat()
w.setunknown()

#DC machine
#Step down chopper
class Chopper:
    def __init__(self):
        self.state = 1 #first time run
        #ra=0.14 ohm
        #Ia=300 amp
        self.alpha=50
        #k = 4e-3 N-m/A^2 and Ia = 300 amp
        self.Te = int( 4e-3 * 300 * 300 )
        self.allrecord = []
        self.record = {}
    def motor_speed(self):
        n = ( (self.alpha/100)*600 - (300)*(0.14) ) / (4e-3 * 300)
        self.omega = round(n, 2)
        self.Vt = int( (self.alpha/100)*600 )
        self.Eb = int( 4e-3 * self.omega * 300 )
        self.N = int( ( self.omega * 60 )/( 2 * np.pi ) ) 
    
    def plot_graph(self):
        t=0
        t_array = np.arange(0,8,0.01)
        V=0
        Vt = []
        for t in np.arange(0, 8, 0.01):
            if (t - int(t)) <= (self.alpha/100):
                Vt.append(600)
            else:
                Vt.append(0)

        return t_array,Vt


    def reset_graph(self):
        self.alpha=7
        self.motor_speed()
        self.plot_graph()
c=Chopper()
c.reset_graph()




@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    return render_template('home.html', title='HOME')
    
    
# in the same fashion go on adding respective html files and route to run that


#--------------------------------------------------------------------------------------------------
#analog routes
@app.route('/aE')
def analog():
    return render_template('experiments.html', title='Analog Electronics', course=experiments['aE'])

@app.route('/aE/ae01')
def ae1():
    return render_template('pnJunction.html', title='AE1')









#------------------------------------------------------------------------------------------------
# dcM1 routes
@app.route('/dcM1')
def dcM1():
    return render_template('experiments.html', title='DC Machines I', course= experiments['dcM1'])


@app.route('/dcM1/dcm01')
def dcm01():
    V = int(request.args.get("num_v_points", 200))
    f = int(request.args.get("num_f_points", 50))
    return render_template('torqueSlip.html', title="Torque-Slip", V=V, f=f)

@app.route("/matploteMes01-<int:V>,<int:f>.svg")
def plot_emes01g(V,f):
    fig = Figure()
    fig.set_size_inches(15, 12)
    Torq,slip, Nr= torque_vs_slip(V,f)
    axis = fig.add_subplot(2, 1, 1)
    axis.xlabel ='Nr'
    axis.ylabel= 'Torque'
    axis.plot(Nr, Torq, c='red', linewidth=4)
    axis.grid()
    
    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")








#-------------------------------------------------------------------------------------------------
#eMes routes
@app.route('/eMes')
def eMes():
    return render_template('experiments.html', title='Electrical Measurements', course= experiments['eMes'])


# in the same fashion go on adding respective html files and route to run that
@app.route('/ohmlaw', methods=['GET', 'POST'])
def ohmlaw():
    if request.method == 'POST':
        if request.form['CRDohm'] == 'Set':
            ohm.allrecord = []
            ohm.setvalue = round(float(request.form['resistance']), 1)
            ohm.disabled_set = "disabled"
            ohm.disabled_append = ""
            return redirect('/ohmlaw')
        else:
            if request.form['CRDohm'] == 'Append':
                ohm.circ=1
                ohm.record = {}
                ohm.record['voltage'] = round(float(request.form['voltage']), 1)
                ohm.record['current'] = round((ohm.record['voltage']/ohm.setvalue), 1)
                ohm.allrecord.append(ohm.record)
                ohm.plot_graph()
                return redirect('/ohmlaw')
            elif request.form['CRDohm'] == 'Delete':
                ohm.record = {}
                index = int(request.form['reference'])
                ohm.allrecord.pop(index-1)
                ohm.plot_graph()
                return redirect('/ohmlaw')
            elif request.form['CRDohm'] == 'Reset':
                ohm.empty_graph()
                return redirect('/ohmlaw')
    return render_template('ohmlaw.html', title='ohmlaw', circ=ohm.circ, setvalue=ohm.setvalue, allrecord=ohm.allrecord, record=ohm.record, disabled_set=ohm.disabled_set, disabled_append=ohm.disabled_append)

# Bridges of deSauty and Wheatstone
@app.route('/desauty', methods=['GET', 'POST'])
def desauty():
    if request.method == 'POST':
        if request.form.get('Resetkar'):
            des.R2 = des.R3 = des.C1_calc = des.r1_calc = bridge.detector_mag_mV = 0
            des.hide = 'disabled'
            des.ind = int(request.form['Resetkar']) - 1
            des.setunknown()
        else:
            des.R2 = float(request.form['R2'])
            des.R3 = float(request.form['R3'])
            des.bridgify()
        return redirect('/desauty')
    return render_template('desauty.html', des=des, bridge=bridge, title='desauty' )

@app.route('/wheatstone', methods=['GET', 'POST'])
def wheatstone():
    if request.method == 'POST':
        if request.form.get('Resetkar'):
            w.R2 = w.R3 = w.R1_calc = bridge.detector_mag_mV = 0
            w.hide = 'disabled'
            w.ind = int(request.form['Resetkar']) - 1
            w.setunknown()
        else:
            w.R2 = float(request.form['R2'])
            w.R3 = float(request.form['R3'])
            w.bridgify()
        return redirect('/wheatstone')
    return render_template('wheatstone.html', w=w, bridge=bridge, title='wheatstone' )





#-------------------------------------------------------------------------------------------------
#icApp routes
@app.route('/icApp')
def icApp():
    return render_template('experiments.html', title="IC Applications", course=experiments['icApp'])

@app.route('/icApp/icApp01')
def lowPassFilter():
    R = int(request.args.get("num_x_points", 50))
    C = int(request.args.get("num_c_points", 50))
    return render_template('low_pass.html', title="Low pass filter", R=R, C=C)

@app.route('/icApp/icApp02')
def highPassFilter():
    R = int(request.args.get("num_x_points", 50))
    C = int(request.args.get("num_c_points", 50))
    return render_template('high_pass.html', title="High pass filter", R=R, C=C)

#for RC filters
@app.route("/matplot-as-image-<int:R>,<int:C>.svg")
def plot_svg(R,C):
    C= C*1e-6
    fig = Figure()
    f, Gain ,phase = low_pass_filter(R, C)
    axis = fig.add_subplot(2, 1, 1)
    axis.semilogx(f, Gain)

    axis = fig.add_subplot(2, 1, 2)
    axis.semilogx(f, phase)

    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")

@app.route("/matplot-as-imagehigh-<int:R>,<int:C>.svg")
def plot_hvg(R,C):
    C*=1e-6
    fig = Figure()
    f, Gain ,phase = high_pass_filter(R, C)
    axis = fig.add_subplot(2, 1, 1)
    axis.semilogx(f, Gain)

    axis = fig.add_subplot(2, 1, 2)
    axis.semilogx(f, phase)

    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")


#-------------------------------------------------------------------
#drives
@app.route('/drives')
def drives():
    return render_template('experiments.html', title="Electrical Drives", course=experiments['drives'])

@app.route('/chopper', methods=['GET','POST'])
def chopper():
    if request.method == 'POST':
        if request.form.get('CRD'):
            if request.form['CRD'] == 'Append':
                c.state = 0 #not first time
                c.record = {}
                c.record['alpha'] = c.alpha
                c.record['N'] = c.N
                c.record['Eb'] = c.Eb
                c.record['Vt'] = c.Vt
                c.allrecord.append(c.record)
                print(c.allrecord)
                return redirect('/chopper')
            elif request.form['CRD'] == 'Delete':
                c.state = 0 #not first time
                c.record = {}
                index = int(request.form['reference'])
                c.allrecord.pop(index-1)
                print(c.allrecord)
                return redirect('/chopper')
            elif request.form['CRD'] == 'Reset':
                c.state = 0 #not first time
                c.allrecord = []
                c.reset_graph()
                return redirect('/chopper')
        else:
            c.state = 0 #not first time
            c.alpha = int(request.form['alpha'])
            c.motor_speed()
            c.plot_graph()
            return redirect('/chopper')

    return render_template('chopper.html', c=c, rec=c.record, allrec=c.allrecord, title='chopper')