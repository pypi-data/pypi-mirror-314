import algebraic_immunity_utils



m = algebraic_immunity_utils.Matrix([[1,1], [1,0]])
m1 = m.echelon_form_last_row()[0]
print(m1)
print(m1.rank())


m = algebraic_immunity_utils.Matrix([[1,1], [1,1]])
m1 = m.echelon_form_last_row()[0]
print(m1)
print(m1.rank())


m.append_row([1,0])
print(m)

m.append_column([1,0,1])

print(m)

m = algebraic_immunity_utils.Matrix([[1,1], [0,0]])
print(m.kernel())

m = algebraic_immunity_utils.Matrix([[1,0], [0,0]])
print(m.kernel())

print()
m = algebraic_immunity_utils.Matrix([[1,1,0], [0,1,1]])
print(m.kernel())