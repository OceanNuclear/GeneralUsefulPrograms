#!/home/ocean/anaconda3/bin/python3
from numpy import cos,log10, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from numpy import log as ln
#file reading part
inFile = str(input("Please type in the input filename (without .txt):\n"))
inFile += str(".txt")
numLines = sum(1 for line in open(inFile))
x = []
y = []
dy= []
f = open(inFile, "r")
line=["" for x in range (numLines)]
for n in range (numLines):
	line[n]=(str(f.readline()))
	if (len(line[n].split()) != 3):
		pass
	else:
		x.append( float(line[n].split()[0]) )
		y.append( float(line[n].split()[1]) )
		dy.append(float(line[n].split()[2]) )
numData = len(x)
assert numData==numLines
print("Parsed ", numData, " data points.")
x = np.array(x)
y = np.array(y)
dy = np.array(dy)

#function fitting part
	#methods to fit to the function
def variablePFunction(func,xdata,popt):
	numParam = len(popt)
	if numParam==0:
		return func(xdata)
	if numParam==1:
		return func(xdata,popt[0])
	if numParam==2:
		return func(xdata,popt[0],popt[1])
	if numParam==3:
		return func(xdata,popt[0],popt[1],popt[2])
	if numParam==4:
		return func(xdata,popt[0],popt[1],popt[2],popt[3])
	else:
		raise ValueError("Bruh there's too many variables in the model, are you sure you want to do that?")
def s(num):#turning a floating point number into a reader-friendly format
	assert isinstance(num,float)
	if 1<=log10(abs(num))<3:
		#10 -> 10.0
		#100->100.0
		#999->999.0
		string = "{:.1f}".format(num)
	elif 0<=log10(abs(num))<1 :
		#1  ->  1.00
		string = "{:.2f}".format(num)
	elif -1<=log10(abs(num))<0 :
		#0.1->  0.100
		string = "{:.3f}".format(num)
	else:
		string = ('%3.2e'%num)
		place  = string[-3:]#can only handle numbers between 10^+-100
		string = string[:-3]
		for char in place[:-1]:
			if (char!="+") and (char!="0"):
				string+=char
		string+= place[-1]
	return string
def offdiag(matrix):
	assert matrix.ndim==2
	assert len(matrix)==len(matrix[0])#ensure it is a square matrix
	offdiagElem = []
	for i in range (len(matrix)):
		for j in range(i,len(matrix)-1):
			offdiagElem.append(matrix[i,j+1])
	return offdiagElem
#<CHANGE THIS________________________________________________________________________>
def fittedFunc(x, a,b):
	# yCalc = a*x**b
	yCalc = sqrt(a+b*(x))/x
	# yCalc = a+b*x
	return yCalc
# equation="(a+b*sqrt(x))/x"
equation = "sqrt(a+b*(x))/x"
guess = [1,6]
# title = "Centroid of the 1.3MeV peak of Co-60 wrt. applied voltage"
title = input("Please input the title(press enter to dismiss): ")
if title=="": title="Resolution Fit"
#</CHANGE THIS_______________________________________________________________________>
numParam = len(guess)
popt, pcov = curve_fit(fittedFunc, x, y, sigma=dy, p0=guess,absolute_sigma=True, check_finite=True)
σ = np.diag(pcov)
if numParam>1:
	cov = offdiag(pcov)
	print("covariances=",cov)
	[print("warning: covariance is a bit pathological!!!!!!!!!!!!!!!!!!!!!!!") for n in cov if abs(n)>900]
residual = y - variablePFunction(fittedFunc,x,popt)
chiSq = sum( (residual/dy)**2 )
chiSqPerDoF = s( chiSq/(len(x)-numParam) )
for n in range(len(popt)):
	equation += "\n"+chr(97+n)+"=" + s(popt[n])#optimum value
	equation += r'$\pm$'      + s(σ[n])#error
equation += '\n'+(r'$\frac{\chi^2}{DoF}$' +"=" +chiSqPerDoF)
print(equation)

#plotting
res = 400
x_smooth=np.linspace(min(x),max(x),res)
y_smooth=variablePFunction(fittedFunc,x_smooth,popt)
dummy, (ax1, ax2) = plt.subplots(2, sharex=True,gridspec_kw={'height_ratios':[3,2]})
if len(title)==0:
	ax1.set_title("Custom function fitting using scipy")
else:
	ax1.set_title(title)
ax1.errorbar(x, y, yerr = dy,ecolor="black",fmt ='o',color="orange",capsize=5,)
ax1.plot(x_smooth,y_smooth,label=equation,)
ax2.set_title("Residuals")
ax2.errorbar(x,residual,yerr=dy,capsize=4,linestyle="",)
ax1.legend()
ax2.set_xlabel(r"E(keV)")
ax2.set_ylabel(r"R(E)")
# ax1.set_ylabel(r"log($\epsilon_{peak}(\frac{\Omega}{4\pi})=\epsilon_{abs}r$)")
ax2.axhline(color="black")
plt.show()