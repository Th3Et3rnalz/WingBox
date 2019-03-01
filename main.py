a_stringer_horizontal = 18.5*1.5
a_stringer_vertical = 20*1.5
a_box_horizontal = 400*0.8
a_box_vertical = 150*0.8

variables_list = {}


class Values:
    def __init__(self):
        print()
        self.stringerNumber = 0
        self.i_x = 0
        self.centroid = 0
        self.mass_rel = 0
        self.stress_max = 0

    def add_data(self, n):
        values = calculate_centroid(n)
        text = "I_y for " + str(n) + " stingers: " + leng(str(values[0])) + ", the centroid is then at: "
        text = text + leng(str(values[1])) + ", with a relative mass: " + leng(str(mass(n) / mass(0)))
        print(text)
        self.stringerNumber = n
        self.i_x = values[0]
        self.centroid = values[1]
        self.mass_rel = mass(n)/mass(0)

    def add_stress(self, stress_to_add):
        self.stress_max = stress_to_add


def leng(var):
    return var + " "*(20-len(var))


def mass(n):
    sum_area = (n+5) * a_stringer_horizontal + (n+5) * a_stringer_vertical + 2 * a_box_horizontal + 2 * a_box_vertical
    return sum_area


def i_stringer_up(n, centroid):
    i_stringer_vertical = 1 / 12 * 1.5 * 20 ** 3 + 20 * 1.5 * (75 - 10 - 0.8 - centroid) ** 2
    i_stringer_horizontal = 1 / 12 * 18.5 * 1.5 ** 3 + 18.5 * 1.5 * (75 - 0.75 - 0.8 - centroid) ** 2
    i_total = i_stringer_horizontal*n + i_stringer_vertical*n
    return i_total


def i_stringer_down(n, centroid):
    i_stringer_vertical = 1 / 12 * 1.5 * 20 ** 3 + 20 * 1.5 * (75 - 10 - 0.8 + centroid) ** 2
    i_stringer_horizontal = 1 / 12 * 18.5 * 1.5 ** 3 + 18.5 * 1.5 * (75 - 0.75 - 0.8 + centroid) ** 2
    i_total = i_stringer_horizontal*n + i_stringer_vertical*n
    return i_total


def calculate_centroid(n):
    sum_area_distance = (n-1)*a_stringer_horizontal*(75.0-0.8-0.75)+(n-1)*a_stringer_vertical*(75-10-0.8)
    sum_area = (n+5)*a_stringer_horizontal+(n+5)*a_stringer_vertical + 2*a_box_horizontal + 2*a_box_vertical

    centroid = sum_area_distance / sum_area

    i_box_vertical = 1 / 12 * 0.8 * 150 ** 3
    i_box_horizontal = 1 / 12 * 400 * 0.8 ** 3 + 400 * 0.8 * (75 - 0.4) ** 2
    i_box = 2 * i_box_horizontal + 2 * i_box_vertical

    i_stringers_bottom = i_stringer_down(3, centroid)
    i_stringers_top = i_stringer_up(2+n, centroid)

    i_total = i_stringers_top + i_stringers_bottom + i_box
    return [i_total, centroid]


def calculate_stress(data_given):
    stress = 3450 * (75 + data_given.centroid)*10**(-3) / (data_given.i_x*10**(-12))
    print("The stress is then " + str(stress*10**(-6)) + " MPa")
    return stress


for x in range(0, 10):
    variables_list[x] = Values()
    variables_list[x].add_data(x)
    max_stress = calculate_stress(variables_list[x])
    variables_list[x].add_stress(max_stress)
