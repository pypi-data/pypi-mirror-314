import matplotlib.pyplot as plt

def plot_binary(
  df,
  cols = ['x1', 'x2', 'y'],
  markers = ['s','o'],
  fills = ['#ddf', '#fdd'],
  strokes = ['b', 'r'],
  labels = [0, 1],
):
    x1 = df[cols[0]].tolist() 
    x2 = df[cols[1]].tolist()
    y = df[cols[2]].tolist()
    
    plt.figure(figsize=(4, 4))
    for i in range(len(y)):
        m = markers[labels.index(y[i])]
        mec = strokes[labels.index(y[i])]
        mfc = fills[labels.index(y[i])]
        plt.plot(x1[i], x2[i], marker=m, mec=mec, mfc=mfc)
    
    plt.xlabel(cols[0])
    plt.ylabel(cols[1])
    plt.grid();
