
import argparse
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pytz

from geopy import geocoders
from mpl_toolkits.mplot3d import Axes3D
from numpy import sin,cos,arctan,arccos
from tzwhere import tzwhere


def get_inputs(args):
	'''
	Purpose: Return command line inputs, return custom inputs, or return default inputs
	Inputs 
		args: command line arguments
	Outputs
		date_time_local: Aware datetime obj (has timezone) of time at location you're interested in)
		LA: latitude in decimal format
		LO: longitude in decimal format
		city
	'''

	# if there is city input, it will override LA, LO input
	if args.city == None:
		#default LA, LO, city
		LA = 37.7749 #Latitude, decimal degrees -90 to 90
		LO = -122.4194 #Longitude, decimal degrees -180 to 180 
		city = 'San Francisco, CA'
		print('Using default location:', city, 'Lat:', LA, 'Lon:', LO)
	else:
		city = args.city
		geolocator = geocoders.Nominatim(user_agent='Sun')  #geopy city->LA,LO locator
		location = geolocator.geocode(city)
		if location == None:
			print('Error with city input, please revise')
			exit()
		LA = location.latitude
		LO = location.longitude
		print('Using city input:', location)
		print('Lat:', LA, 'Lon:', LO)

	# get timezone from LA and LO
	tz = tzwhere.tzwhere(forceTZ=True)  #initialize timezone finder  
	timezone = pytz.timezone(tz.tzNameAt(LA, LO, forceTZ=True))

	#date and time input
	if args.date_time == None:
		date_time_local = dt.datetime.now(timezone)    
		print('Using defaut time (current time at location):', date_time_local)
	else:  #default datetime input
		date_time = dt.datetime.strptime(args.date_time, '%Y-%m-%d %H:%M:%S')
		date_time_local = timezone.localize(date_time)
		print('Using time input:', date_time_local)

	
	print('Using timezone:', timezone)
	   #attach timezone to date_time making it aware

	return date_time_local, LA, LO, city


def sun_coords(date_time_local, LA, LO):
	'''
	Purpose: Calculate sun angles from time and position on earth
	Inputs 
		date_time_local: date_time_object with timezone attached
		LA: decimal latitude
		LO: decimal longitude
	Outputs
		Theta: [radians] Angle measured clockwise from due east to the point on the horizon underneath the sun
		Phi: [radians] Angle from the vertical pointing to the sun from the perspective of a person standing on the surface
		Theta_from_North: [deg] Clockwise angle from due north to the point on the horizon underneath the sun
		Phi_from_Horizon: [deg] Vertical angle from horizon to sun  
	'''
	
	date_time_utc = date_time_local.astimezone(pytz.utc) #get date_time_local time in utc timezone
	t_input = date_time_utc.replace(tzinfo=None) #eliminate timezone attribute to make time subtraction simpler

	#define constants we'll need for orbital calculations

	PI = np.pi
	rEO = 149600000 #radius earth orbit, km
	rE = (6378 + 6357)/2 #radius earth, km
	phiE = 23.4*PI/180 #earth tilt, degrees
	tday = 86164.0905 # seconds in a sidereal day (time needed for earth to rotate 360 degrees, but everyday it actually rotates a little bit more because of the earth's orbit around the sun
	tyear = 366.25*tday #seconds in a year, note: there are 366.25 sidereal days in a year

	t0 = dt.datetime(2020, 3, 20, 12, 0, 0) #initial condition - when sun was directly overhead of latitude 0, longitude 0 on the spring equinox of 2020
	tdiff = t_input - t0 #the difference in time between this initial condition and the time we're calculating forms the basis of our calculations 
	t = tdiff.total_seconds() 


	####Thetas and Phis######

	TLL = PI/180*LO + 2*PI/tday*t + PI #Theta of the latitude longitude coordinates in the earth's reference frame
	PLL = PI/2 - 2*PI/360*LA #Phi of the Latitude Longitude in the earth's reference frame
	TEO = 2*PI/tyear*t #Theta of earth orbit in the sun's reference frame, 0 radians is spring equinox

	# Three componenets of a vector pointing to the sun in the reference frame of a person standing on the earth's surface
	Perp = rEO*(sin(phiE)*sin(TEO)*cos(PLL) - cos(phiE)*sin(TEO)*sin(TLL)*sin(PLL) - cos(TEO)*cos(TLL)*sin(PLL)) - rE    
	North = rEO*(sin(phiE)*sin(TEO)*sin(PLL) + cos(phiE)*sin(TEO)*sin(TLL)*cos(PLL) + cos(TEO)*cos(TLL)*cos(PLL))
	East = rEO*(cos(TEO)*sin(TLL) - cos(phiE)*sin(TEO)*cos(TLL))

	
	Theta_raw = arctan(North/East)   #Angle measured clockwise from due east to the point on the horizon underneath the sun, 0 radians is due east
	Theta_deg = Theta_raw*180/PI
	
	#Correcting Theta depending on the unit circle "quadrant" the sun is in, and calculating circular angle from due north
	if North > 0 and East > 0:
		Theta_from_North = 90 - Theta_deg
	
	if North > 0 and East < 0:
		Theta_deg = Theta_deg + 180
		Theta_from_North = 450 - Theta_deg
	
	if North < 0 and East < 0:
		Theta_deg = Theta_deg + 180
		Theta_from_North = 450 - Theta_deg

	if North < 0 and East > 0:
		Theta_deg = Theta_deg + 360
		Theta_from_North = 450 - Theta_deg

	Theta = Theta_deg*PI/180
	Theta_from_North = int(Theta_from_North)

	Phi = arccos(Perp/np.sqrt(Perp*Perp + North*North + East*East))  #Angle from the vertical that points to the sun in the reference frame of a person standing on the earth's surface
	Phi_from_Horizon = int(90 - Phi*360/(2*PI))

	return Theta, Phi, Theta_from_North, Phi_from_Horizon


def make_3D_plot(Theta, Phi, Theta_from_North, Phi_from_Horizon, date_time_local, LA, LO, city, save_plot=False):
	'''
	Purpose: Generate 3D plot visualing where the sun is with respect to the cardinal directions from the perspecitve of a person standing on the surface of the earth
	Inputs
		Theta: [radians] Angle measured clockwise from due east to the point on the horizon underneath the sun
		Phi: [radians] Angle from the vertical pointing to the sun from the perspective of a person standing on the surface
		Theta_from_North: [deg] Clockwise angle from due north to the point on the horizon underneath the sun
		Phi_from_Horizon: [deg] Vertical angle from horizon to sun 
		date_time_local: date_time_object with timezone attached
		LA: decimal latitude
		LO: decimal longitude
	Outputs
		3D plot
	''' 

	#3D plot of sun location
	fig = plt.figure(figsize=(10, 8))
	ax = fig.add_subplot(111, projection='3d')
	ax.axis('off')

	# Create the mesh in polar coordinates and compute corresponding Z.
	radPL = 1
	thePL = np.linspace(0, 2*np.pi, 50)
	phiPL = np.linspace(0, 0.5*np.pi, 200)
	ThePL, PhiPL  = np.meshgrid(thePL, phiPL)

	#Plot a dome 
	XD = radPL*cos(ThePL)*sin(PhiPL)
	YD = radPL*sin(ThePL)*sin(PhiPL)
	ZD = radPL*cos(PhiPL)
	ax.plot_surface(XD, YD, ZD, alpha = 0.2)

	#Plot cardinal directions
	ax.plot3D(np.linspace(-1, 1, 50), np.linspace(0, 0, 50), np.linspace(0, 0, 50), color='black')
	ax.plot3D(np.linspace(0, 0, 50), np.linspace(0, 1, 50), np.linspace(0, 0, 50), color='red')
	ax.text(0, 1, 0, "N", color='red', size=14)
	ax.plot3D(np.linspace(0, 0, 50), np.linspace(-1, 0, 50), np.linspace(0, 0, 50), color='black')

	#Plot vector pointing to the current location of the sun
	R = np.linspace(0, 1, 50)
	X = cos(Theta)*sin(Phi)
	Y = sin(Theta)*sin(Phi)
	Z = cos(Phi)

	#Generating single value linspaces for the dashed guide lines
	Xspace = np.linspace(X, X, 50)
	Yspace = np.linspace(Y, Y, 50)
	
	if Phi < np.pi/2: #only plot if sun is above horizon
		ax.plot3D(R*X, R*Y, 0, color='black', dashes=[6, 2]) #dashed line in xy plane
		ax.plot3D(Xspace, Yspace, R*Z, color='black', dashes=[6, 2]) #vertical dashed line
		ax.plot3D(R*X, R*Y, R*Z, color='black') #line from origin to sun
		ax.scatter3D(X, Y, Z, s=1000, color='gold') # sun object itself
	
	
	#Text labels on graph
	time_label = dt.datetime.strftime(date_time_local, '%H:%M %m-%d-%Y')
	city_label = 'City: ' + city
	theta_phi_label = f'Theta: {Theta_from_North} deg\nPhi: {Phi_from_Horizon} deg'
	label = 'Time: ' + time_label + '\n' + city_label + '\n' + theta_phi_label
	ax.text(1.2, 0, 1.2, label,
         size=14,
         color='black',
         horizontalalignment='center',
         verticalalignment='top',
         multialignment='left')

	#Plot arc representing the path of the sun in the sky
	time = date_time_local

	hourspan = range(0,24)
	minutespan = range(0, 60, 20)
	Xspan = []
	Yspan = []
	Zspan = []
	for hour in hourspan:
		for minute in minutespan:
			time = time.replace(minute = minute, hour=hour)
			Theta, Phi, Theta_from_North, Phi_from_horizon = sun_coords(time, LA, LO)
			if Phi < np.pi/2: #only plot if sun is above horizon
				X = cos(Theta)*sin(Phi)
				Y = sin(Theta)*sin(Phi)
				Z = cos(Phi)
				Xspan.append(X)
				Yspan.append(Y)
				Zspan.append(Z)
				if minute == 0:
					ax.text(X, Y, Z, hour, color='black', horizontalalignment='center')
		
	ax.plot3D(Xspan, Yspan, Zspan, color='gold')

	
	# Set Plot Boundaries
	ax.set_xlim(-1, 1)
	ax.set_ylim(-1, 1)
	ax.set_zlim(0, 1)
	ax.set_xlabel('X/West-East')
	ax.set_ylabel('Y/North-South')
	ax.set_zlabel('Z')
	
	plt.subplots_adjust(left=0, bottom=0, right=1, top=0.8)
	plt.show()

	if save_plot:
		fig.savefig('out.png')


def main(args):
	
	# get time, lat, and long from input args or default values
	date_time_local, LA, LO, city = get_inputs(args)

	# get Theta, Phi angles for sun (see documentation for definitions)
	Theta, Phi, Theta_from_North, Phi_from_Horizon = sun_coords(date_time_local, LA, LO)

	print('Theta from North =', Theta_from_North)
	print('Phi from Horizon =', Phi_from_Horizon)

	make_3D_plot(Theta, Phi, Theta_from_North, Phi_from_Horizon, date_time_local, LA, LO, city, args.save_plot)



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--date_time', default=None)
	parser.add_argument('-c', '--city', default=None)
	parser.add_argument('-p', '--save_plot', default=False)
	args = parser.parse_args()
	main(args)


