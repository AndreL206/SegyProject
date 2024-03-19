import matplotlib.pyplot as plt

def printLine (Data, name) : 
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title('Line '+ name)
    Line = ax.imshow(Data, cmap ='grey', vmin = Data.min(), vmax = Data.max(), 
                     extent =[0, Data.shape[0], 0, Data.shape[1]], 
                        interpolation ='nearest', origin ='lower', aspect = 'auto')  
    
    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    plt.colorbar(Line, location = "bottom", pad = 0.01, aspect = 40) 
    # plt.title(Segy_Structure["Name"], fontweight ="bold", y = -0.20) 
    
    plt.ylabel("A.U.")
    plt.xlabel("Shotpoints")
    plt.tight_layout()
    plt.show() 

