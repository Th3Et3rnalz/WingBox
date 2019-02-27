i_stringer = 1/12 * 18.5 * 1.5**3 + 18.5*1.5*(75-0.75-0.8)**2 + 1/12*1.5*20**3 + 20*1.5*(75-10-0.8)**2
i_box_vertical = 1/12*0.8*150**3
i_box_horizontal = 1/12*400*0.8**3 + 400*0.8*(75-0.4)**2
i_box = 2*i_box_horizontal + 2*i_box_vertical

a_stringer_horizontal = 18.5*1.5
a_stringer_vertical = 20*1.5
a_box_horizontal = 400*0.8
a_box_vertical = 150*0.8


def calculate_centroid(n):
    i_total = i_box + i_stringer*(n+5)

    sum_area_distance = (n-1)*a_stringer_horizontal*(75.0-0.8-0.75)+(n-1)*a_stringer_vertical*(75-10-0.8)
    sum_area = (n+5)*a_stringer_horizontal+(n+5)*a_stringer_vertical + 2*a_box_horizontal + 2*a_box_vertical

    centroid = sum_area_distance / sum_area
    return [i_total, centroid]


def mass(n):
    sum_area = (n+5) * a_stringer_horizontal + (n+5) * a_stringer_vertical + 2 * a_box_horizontal + 2 * a_box_vertical
    return sum_area

def leng(var):
    return var + " "*(20-len(var))


for x in range(0, 10):
    values = calculate_centroid(x)
    text = "I_y for " + str(x) + " stingers: " + leng(str(values[0])) + ", the centroid is then at: " + leng(str(values[1]))
    text = text + ", with a relative mass: " + leng(str(mass(x)/mass(0)))
    print(text)
