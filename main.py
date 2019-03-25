# This is a simple python script for the calculation of the optimal amount of stringers
# for a wing box that is to be designed for the course AE1222-I Design and Construction.
# It was written by Joe Verbist with information from and for Group E6G.

import math
import matplotlib.pyplot as plt

# variables for rivet spacing [in N]
rivet_load = 2500

# These are the variables for the areas of the cross-sections. [in mm**2]
a_stringer_horizontal = 18.5*1.5
a_stringer_vertical = 20*1.5
a_box_horizontal = 400*0.8
a_box_vertical = 150*0.8

# This is a variables that holds all the solutions ( it holds the solution for 1 stringer, for 2 stringers, ...)
variables_list_3 = {}
variables_list_1 = {}


# The following lines of code will create an object that holds all the variables for a specific number of stringers.
class Values:
    def __init__(self):
        print()
        self.stringerNumber = 0
        self.i_x = 0
        self.centroid = 0
        self.stress_max = 0
        self.rivet_spacing = []

    def add_data(self, n):
        values = calculate_centroid_and_moment_of_inertia(n)  # This returns values in mm (done for verifiability)
        text = "I_y for " + str(n) + " stingers: " + leng(str(values[0] * 10**(-12))) + "m^4, the centroid is then at: "
        text = text + leng(str(values[1])) + "mm above the centerline"
        print(text, end="")
        self.stringerNumber = n
        self.i_x = values[0] * 10**(-12)  # Conversion to m**4
        self.centroid = values[1] * 10**(-3)  # conversion to m

# This adds the stress value to object
    def add_stress(self, stress_to_add):
        self.stress_max = stress_to_add

    def add_rivet_spacing(self, rivet_spacing):
        self.rivet_spacing = rivet_spacing
        # print(rivet_spacing)


# This adds whitespaces so it is easy to read the values in the command line
def leng(var):
    return var + " "*(20-len(var))


def i_stringer_up(centroid):  # This is the moment of inertia for a the stringer placed at the top
    i_stringer_vertical = 1/12 * 1.5 * 20**3 + 20 * 1.5 * (75 - 10 - 0.8 - centroid) ** 2
    i_stringer_horizontal = 1/12 * 18.5 * 1.5**3 + 18.5 * 1.5 * (75 - 0.75 - 0.8 - centroid) ** 2
    i_total = i_stringer_horizontal + i_stringer_vertical
    return i_total


def i_stringer_down(centroid):  # This is the moment of inertia for a the stringer placed at the bottom
    i_stringer_vertical = 1 / 12 * 1.5 * 20 ** 3 + 20 * 1.5 * (75 - 10 - 0.8 + centroid) ** 2
    i_stringer_horizontal = 1 / 12 * 18.5 * 1.5 ** 3 + 18.5 * 1.5 * (75 - 0.75 - 0.8 + centroid) ** 2
    i_total = i_stringer_horizontal + i_stringer_vertical
    return i_total


def calculate_centroid_and_moment_of_inertia(n):  # All values are in mm (or mm**4 for i)
    sum_area_distance = a_box_horizontal*(75-0.4)*(top_plate-1)+(n-bottom_stringers)*a_stringer_horizontal*(75.0-0.8-0.75)
    sum_area_distance += (n-bottom_stringers)*a_stringer_vertical*(75-10-0.8)
    sum_area = (n+bottom_stringers+4)*a_stringer_horizontal+(n+4+bottom_stringers)*a_stringer_vertical
    sum_area += 2*a_box_horizontal + 2*a_box_vertical

    centroid = sum_area_distance / sum_area

    i_box_vertical = 1 / 12 * 0.8 * 150 ** 3
    i_box_horizontal = 1 / 12 * 400 * 0.8 ** 3 + 400 * 0.8 * (75 - 0.4) ** 2
    i_box = (1+top_plate) * i_box_horizontal + 2 * i_box_vertical

    i_stringers_bottom = i_stringer_down(centroid) * (bottom_stringers+2)
    i_stringers_top = i_stringer_up(centroid) * (2+n)

    i_total = i_stringers_top + i_stringers_bottom + i_box
    return [i_total, centroid]


def calculate_stress(data_given):
    stress = 3450 * (0.075 - data_given.centroid) / data_given.i_x
    print(", the stress is then " + str(stress*10**(-6)) + " MPa")
    return stress


def calculate_spacing(data_given):
    n = 12  # The number of section designed
    spacing_bottom = []  # Empty variable that is declared to place data from the calculations into.
    spacing_top = []
    for i in range(0, n-1):
        s = 162088 * math.sqrt(data_given.i_x / ((0.075 + data_given.centroid) * rivet_load * (1.385 - i*1.385/n)))
        spacing_bottom.append(s)
    for i in range(0, n-1):
        s = 162088 * math.sqrt(data_given.i_x / ((0.075 - data_given.centroid) * rivet_load * (1.385 - i * 1.385 / n)))
        spacing_top.append(s)
    return [spacing_bottom, spacing_top]


# This is the number of stringers which EXCLUDES the corners
# For code simplicity I opted to only iterate on the top number of stringers, taking the bottom stringers
# as a constant that can easily be change by hand. The number of top plate is also placed here for easy changing.
# We were not considering adding a second one, but this is present for the moment of inertia calculations after
# buckling.
bottom_stringers = 3
top_plate = 1


# Loop that starts the calculations for stringers between 0 and 9
moment_of_inertia = []

# All the calculations for 3 stringers at the bottom
for x in range(2, 6):
    variables_list_3[x] = Values()
    variables_list_3[x].add_data(x)
    variables_list_3[x].add_stress(calculate_stress(variables_list_3[x]))
    spacing = calculate_spacing(variables_list_3[x])
    variables_list_3[x].add_rivet_spacing(spacing)
    moment_of_inertia.append(variables_list_3[x].stress_max)

# Moment of Inertia change for stringer number
n = range(2, 6)
moment_of_inertia = []
moment_of_inertia.append(variables_list_3[2].i_x)
moment_of_inertia.append(variables_list_3[3].i_x)
moment_of_inertia.append(variables_list_3[4].i_x)
moment_of_inertia.append(variables_list_3[5].i_x)
plt.plot(n, moment_of_inertia)
plt.title('Change of moment of inertia for stringer number')
plt.xlabel('Stringer number')
plt.ylabel('Moment of Inertia [m^4]')
plt.grid(True)
plt.show()

# Centroid change for stringer number
n = range(2, 6)
centroid = []
centroid.append(variables_list_3[2].centroid)
centroid.append(variables_list_3[3].centroid)
centroid.append(variables_list_3[4].centroid)
centroid.append(variables_list_3[5].centroid)
plt.plot(n, centroid)
plt.title('Change of centroid for stringer number')
plt.xlabel('Stringer number')
plt.ylabel('Centroid distance to centerline [m]')
plt.grid(True)
plt.show()


# All the calculations for 1 stringer at the bottom
for x in range(2, 6):
    bottom_stringers = 1
    variables_list_1[x] = Values()
    variables_list_1[x].add_data(x)
    variables_list_1[x].add_stress(calculate_stress(variables_list_1[x]))
    spacing = calculate_spacing(variables_list_1[x])
    variables_list_1[x].add_rivet_spacing(spacing)
    moment_of_inertia.append(variables_list_1[x].stress_max)


# PLOT WITHOUT THE CUT OFF   PLOT WITHOUT THE CUT OFF   PLOT WITHOUT THE CUT OFF   PLOT WITHOUT THE CUT OFF
n = range(0, 110, 10)

title = 'Optimal inter-rivet spacing variation for ' + str(variables_list_3[5].stringerNumber) + " stringers"
plt.figure(title)

plt.subplot(121)  # approx 20 % of the length [highest moment]
plt.plot(n, variables_list_3[5].rivet_spacing[0], label="5 top & 3 bottom")

plt.subplot(122)
plt.plot(n, variables_list_3[5].rivet_spacing[1], label="5 top & 3 bottom")


plt.subplot(121)  # approx 50% of the length
plt.plot(n, variables_list_1[5].rivet_spacing[0], label="5 top & 1 bottom")

plt.subplot(122)
plt.plot(n, variables_list_1[5].rivet_spacing[1], label="5 top & 1 bottom")


plt.subplot(121)  # approx 30% of the length [smallest moment]
plt.plot(n, variables_list_1[2].rivet_spacing[0], label="2 top & 1 bottom")
plt.title('Bottom plate)')
plt.xlabel('distance from root [%]')
plt.ylabel('inter rivet spacing [mm]')
plt.grid(True)
plt.legend()

plt.subplot(122)
plt.plot(n, variables_list_1[2].rivet_spacing[1], label="2 top & 1 bottom")

plt.title('Top plate')
plt.xlabel('distance from root [%]')
plt.ylabel('inter rivet spacing [mm]')
plt.grid(True)

plt.subplots_adjust(top=0.90, bottom=0.10, left=0.10, right=0.90, hspace=0.3, wspace=0.35)
plt.legend()
plt.show()


# PLOT WITH CUT OFF  PLOT WITH CUT OFF   PLOT WITH CUT OFF   PLOT WITH CUT OFF   PLOT WITH CUT OFF
title = 'Optimal inter-rivet spacing variation for ' + str(variables_list_3[5].stringerNumber) + " stringers"
plt.figure(title)

plt.subplot(121)  # approx 20 % of the length [highest moment]
n_new = [0, 10, 20]
spacing_new = []
spacing_new.append(variables_list_3[5].rivet_spacing[0][0])
spacing_new.append(variables_list_3[5].rivet_spacing[0][1])
spacing_new.append(variables_list_3[5].rivet_spacing[0][2])
plt.plot(n_new, spacing_new, label="5 top & 3 bottom")

plt.subplot(122)
n_new = [0, 10, 20]
spacing_new = []
spacing_new.append(variables_list_3[5].rivet_spacing[1][0])
spacing_new.append(variables_list_3[5].rivet_spacing[1][1])
spacing_new.append(variables_list_3[5].rivet_spacing[1][2])
plt.plot(n_new, spacing_new, label="5 top & 3 bottom")


plt.subplot(121)  # approx 50% of the length
n_new = [20, 30, 40, 50, 60, 70]
spacing_new = []
spacing_new.append(variables_list_1[5].rivet_spacing[0][2])
spacing_new.append(variables_list_1[5].rivet_spacing[0][3])
spacing_new.append(variables_list_1[5].rivet_spacing[0][4])
spacing_new.append(variables_list_1[5].rivet_spacing[0][5])
spacing_new.append(variables_list_1[5].rivet_spacing[0][6])
spacing_new.append(variables_list_1[5].rivet_spacing[0][7])
plt.plot(n_new, spacing_new, label="5 top & 1 bottom")

plt.subplot(122)
n_new = [20, 30, 40, 50, 60, 70]
spacing_new = []
spacing_new.append(variables_list_1[5].rivet_spacing[0][2])
spacing_new.append(variables_list_1[5].rivet_spacing[0][3])
spacing_new.append(variables_list_1[5].rivet_spacing[0][4])
spacing_new.append(variables_list_1[5].rivet_spacing[0][5])
spacing_new.append(variables_list_1[5].rivet_spacing[0][6])
spacing_new.append(variables_list_1[5].rivet_spacing[0][7])
plt.plot(n_new, spacing_new, label="5 top & 1 bottom")


plt.subplot(121)  # approx 30% of the length [smallest moment]
n_new = [70, 80, 90, 100]
spacing_new = []
spacing_new.append(variables_list_1[2].rivet_spacing[0][7])
spacing_new.append(variables_list_1[2].rivet_spacing[0][8])
spacing_new.append(variables_list_1[2].rivet_spacing[0][9])
spacing_new.append(variables_list_1[2].rivet_spacing[0][10])
plt.plot(n_new, spacing_new, label="2 top & 1 bottom")
plt.title('Bottom plate)')
plt.xlabel('distance from root [%]')
plt.ylabel('inter rivet spacing [mm]')
plt.grid(True)
plt.legend()

plt.subplot(122)
n_new = [70, 80, 90, 100]
spacing_new = []
spacing_new.append(variables_list_1[2].rivet_spacing[1][7])
spacing_new.append(variables_list_1[2].rivet_spacing[1][8])
spacing_new.append(variables_list_1[2].rivet_spacing[1][9])
spacing_new.append(variables_list_1[2].rivet_spacing[1][10])
plt.plot(n_new, spacing_new, label="2 top & 1 bottom")
plt.title('Top plate')
plt.xlabel('distance from root [%]')
plt.ylabel('inter rivet spacing [mm]')
plt.grid(True)

plt.subplots_adjust(top=0.90, bottom=0.10, left=0.10, right=0.90, hspace=0.3, wspace=0.35)
plt.legend()
plt.show()
