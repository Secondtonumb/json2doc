import pickle as pkl

with open('dataset.pkl', 'rb') as f_d:
    data = pkl.load(f_d)

a, b, c, d, e, f, g, h = data
print(e)
