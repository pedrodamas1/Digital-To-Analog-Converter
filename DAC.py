# Digital-to-analog converter

import numpy as np
import matplotlib.pyplot as plt


class customADC:

	def __init__(self, channels):
		# Channels are the values of the resistances in parallel
		self.channels = channels
		print('Custom ADC initiated successfully.')

		# Now, we reverse engineer this problem
		# We calculate all 2**n possible combinations of any resistances
		self.calculate_combinations()
		# And we order them by value
		self.order_values()
		# Uncomment this if you wish to plot the equivalent resistance values
		# self.plot_values() 
		
	def calculate_combinations(self):
		# Get the numbers of resistances in parallel
		self.N_channels = len(self.channels)
		# The number of possible combinations with those resistances
		self.N_combinations = 2**self.N_channels
		# Create list of integers from 0 to 2**n
		self.combinations_dec = np.arange(self.N_combinations)

		# Convert each decimal number to its binary form
		# The binary numbers will have all possible combinations of resistances in parallel
		self.combinations_bin = []
		for decimal in self.combinations_dec:
			decFormat = '{0:0' + str(self.N_channels) +'b}'
			self.combinations_bin.append(decFormat.format(decimal))

		# Convert the binary number strings into integers
		self.combinations_array = []
		for binary in self.combinations_bin:
			var = [int(i) for i in binary]
			self.combinations_array.append(var)

		# Convert the list to a numpy array
		self.combinations_array = np.asarray(self.combinations_array)
		self.channels = np.asarray(self.channels)

		# Now, calculate the values of resistance
		self.resistance_combinations = []
		for i in range(self.N_combinations):
			bite_resistance = 0
			for j in range(self.N_channels):
				if self.combinations_array[i][j] == 1:
					bite_resistance = bite_resistance + 1/self.channels[j]

			# Case in open-circuit
			if bite_resistance == 0:
				bite_resistance = 1

			self.resistance_combinations.append(1/bite_resistance)

		print('Combinations successfully calculated.')
		print('\t Maximum resistance value is {0:.1f}'.format(max(self.resistance_combinations)))
		print('\t Minimum resistance value is {0:.1f} \n'.format(min(self.resistance_combinations[1:])))

	def plot_values(self):
		x = self.combinations_dec
		y = self.ordered_resistance
		plt.plot(x, y, linestyle="",marker=".") # , . 
		plt.xlabel('Combination number')
		plt.ylabel('Resistance value')
		plt.grid(True)
		plt.title('Possible combinations of resistance')
		plt.show()


	def order_values(self):
		# 

		X = self.resistance_combinations
		Y = self.combinations_dec

		X,Y = zip(*sorted(zip(X,Y)))

		self.ordered_resistance = np.asarray(X)
		self.ordered_dec = np.asarray(Y)

		print('Resistance values successfully ordered. \n')


	def get_resistance(self, desired_binary):
		# Get the resistance corresponding to a given binary combination

		desired_binary = '0b' + desired_binary
		desired_decimal = int(desired_binary, 2)
		desired_resistance = self.resistance_combinations[desired_decimal]
		
		print('For the binary number {0:} the corresponding resistance is {1:.1f} Ohm.'.format(desired_binary, desired_resistance))


	def get_binary(self, desired_resistance):
		# Find the combination of resistances that gives the closest resistance to the requested value

		# Subtract the desired resistance to all resistances
		error = abs(self.ordered_resistance - desired_resistance)

		# Now, find the index of the smallest difference
		closest_value_index = np.argmin(error)

		# Use that index to identify the decimal position of the best match
		requested_dec = self.ordered_dec[closest_value_index]
		decFormat = '{0:0' + str(self.N_channels) +'b}'
		binFormat = decFormat.format(requested_dec)

		print('For the desired resistance {0:} Ohm, the required binary is {1:}'.format(desired_resistance, binFormat))
		
		# Calculate the relative error of the approximation
		rel_error = min(error)/desired_resistance * 100
		print('\t The error of the approximation is {0:.2f} %'.format(rel_error))

		return binFormat


if __name__ == '__main__':

###########		REQUIRED  	 ###########

	myResistances = [470, 330, 270, 250, 220, 200, 150, 120]
	myADC = customADC(myResistances)

###########		OPTIONAL  	 ###########

	myADC.get_resistance('00010001') 	# Calculates the output resistance depending on which channels are open
	myADC.get_binary(205.4) 				# Calculates which channels have to be open/closed to produce the best approximation resistance
