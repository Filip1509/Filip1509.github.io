from metrology_functions import *

if __name__ == '__main__':

    #script_corner_hybrid_r011.py

    plt.ion()
    xyz_file=sys.argv[1]
    measurement_file=sys.argv[2]
    print("#Z measurenent: ",xyz_file)
    print("#SNR measurment: ",measurement_file)

            

    df = pd.read_csv(xyz_file, delimiter="\t", names=["x", "y", "z","nul1","nul2","nul3","nul4"])
    df2 = pd.read_csv(measurement_file, delimiter="\t")

    #print(df2)
    #print(df)
    #print(df2)

    #df.round(1)
    #df2.round(1)

    x=df["x"]
    y=df["y"]
    z=df2["Snr"]
    z_r=df["z"]

    X,Y,Z,Z2 = plot_contour(x,y,z,z_r,resolution = 1000,contour_method='linear')
    #print(X)
    #print(np.round(X))

    with plt.style.context("bmh"):
        fig = plt.figure()
        ax2 = fig.add_subplot(122)
        ax2.set_aspect('equal')
        ax2.grid(False)
        
        ax2.scatter(x,y, color="black", linewidth=1, edgecolor="ivory", s=2)
        CS = ax2.contourf(X,Y,Z,levels=5)
        plt.colorbar(CS)
        
        working=False
        index=0
        a=30
        while not working:
            try:
                p = CS.collections[a].get_paths()[index] #3 working, with 5 levels, 15 working with 20 levels
                v = p.vertices
                #print(v)
                x2 = v[:,0]
                y2 = v[:,1]
                if abs(max(x2)-min(x2))>1:
                    print("#{}".format(abs(max(x2)-min(x2))))
                    working=True
                else:
                    index=index+1
            except Exception as e:
                a=a-1
                index=0
                print("#{}".format(e))
                continue
        if mean(x2) > ((max(df["x"])+min(df["x"]))/2):
            LEFT=True
        else:
            LEFT=True
        print('#Left?',LEFT)

        ## needed this printed, can be removed later
        #np.savetxt("collection7_2.txt", x2)

        # end of removable section







        if LEFT:
            Lcorner = min(v, key=lambda x: (x[1], x[0]))
        else:
            Lcorner = max(v, key=lambda x: (-x[0], -x[1]))

        print("#SNR Corner found at ",Lcorner)

        #ax2.set_title("SNR\nMeasurement\n%s" % (xyz_file))
        ax2.set_title("SNR\nMeasurement R13")

        plt.scatter(x2,y2, s=5, color='white')
        plt.scatter(Lcorner[0], Lcorner[1], s=15, color='black', marker="x")
        plt.xlim(min(x), max(x))
        plt.ylim(min(y), max(y))

        if LEFT:
            SNR_CORNER=max(enumerate(v), key=lambda x: (-x[1][1], x[1][0]))
        else:
            SNR_CORNER=max(enumerate(v), key=lambda x: (-x[1][1], -x[1][0]))
        #print("enumerate snr corner=",SNR_CORNER)
    
        if LEFT:
            idx, maxval = max(enumerate(v), key=lambda x: (-x[1][1], -x[1][0]))
        else:
            idx, maxval = max(enumerate(v), key=lambda x: (-x[1][1], -x[1][0]))



        points = [i for i in zip(x2, y2)]
        CORNER_PROTO = max(points, key=lambda point: math.hypot(maxval[1]-5-point[1], maxval[0]+5-point[0]))  #0.1,0.3 ,0.4,0.4 
        plt.scatter(maxval[0],maxval[1], s=15, color='orange')



        #POINT_FROM_SNR=CS.find_nearest_contour(maxval[0],maxval[1],indices=10)
        #print(POINT_FROM_SNR)
        #for i in range(100,0):
        #    try:
        #        p = CS.collections[5].get_paths()[i] #7-0
        #        v = p.vertices
        #        x2 = v[:,0]
        #        y2 = v[:,1]
        #        ax2.scatter(x2,y2, s=5, color='white')
        #    except:
        #        continue
        
    df_r = df
    df2_r = df2

            #zmask = df_r["z"]<(1.1*mean(df_r["z"])) 
        #print(mean)
        #df_r = df_r[zmask]
        #zmask2 = df_r["z"]>0.1
        #df_r = df_r[zmask2]

        #df_r = df_r.query('z < 0.4')
        #df_r = df_r.query('z > 0.1')

    with plt.style.context("bmh"):
        ax = fig.add_subplot(121)
        ax.set_aspect('equal')
        ax.grid(False)
        
        ax.scatter(x,y, color="black", linewidth=1, edgecolor="ivory", s=2)
        CS = ax.contourf(X,Y,Z2, levels=10)

        #POINT_FROM_SNR=CS.find_nearest_contour(maxval[0],maxval[1],indices=2)
        #print(POINT_FROM_SNR)

        plt.colorbar(CS)
        #ax.set_title("Z\nMeasurement\n%s" % (xyz_file))
        ax.set_title("Z\nMeasurement R13")
        size=0
        valid=False
        a=0 #formerly 0, try different numbers for a fix
        while not valid:
            for i in range(0,10000):
                try:
                    p = CS.collections[a].get_paths()[i] #7-0


                    v = p.vertices
                    x1 = v[:,0]
                    y1 = v[:,1]
                    #print(max(x1))
                    #print(min(x1))
                    #print(max(x1)-min(x1))
                    sizenew=abs(max(x1)-min(x1))
                    if sizenew > size:
                        size=sizenew
                        print("#{}".format(size))
                    #requirement between 1 and 2
                    if abs(max(x1)-min(x1))<1.1:
                    
                        #print(i)
                        continue
                    else:
                        ax.scatter(x1,y1, s=5, color='red')
                        
                        print("#I ADDED A SCATTER")


                        #former corner - cornermost point from raw edge
                        if LEFT:
                            Rcorner = max(v, key=lambda x: (x[1], -x[0]))  # -1, 0 works well
                        else:
                            Rcorner = max(v, key=lambda x: (-x[1], -x[0]))  # -1, 0 works well
                        ax.scatter(x2,y2, s=5, color='white')
                        ax.scatter(Rcorner[0], Rcorner[1], s=15, color='black', marker="x")


                        valid=True
                        break
                except:
                    continue

                        #print("some path found x1,y1")
                        #print(x1)
                        #print(y1)
            a=a+1
            #************ uncomment this if el problemo *************** print(a)      

        # max
        # 0, -1 bottom left cornermost
        # 0, 1
        # -0, 1 top left cornermost
        # -0, -1 top left cornermost
        # 1, 0
        # 1, -0 top left cornermost
        # -1, 0 corner from bottom
        # -1, -0 corner from bottom
        try:    
            points = [i for i in zip(x1, y1)]
            if LEFT:
                target = (maxval[0]+0.7,maxval[1]-0.36)
            else:
                target = (maxval[0]-0.7,maxval[1]-0.36)
            #print(points)
            #print(target)
            #print("points zipped, target set")
            Rcorner2 = min(points, key=lambda point: math.hypot(target[1]-point[1], target[0]-point[0]))
            #print(Rcorner2)
            ax.scatter(Rcorner2[0], Rcorner2[1], s=15, color='black', marker="o")

        except:
            print("#finding corner2 failed")

            #print(Rcorner)
            #print("iteration ended")
            
            #print("we are out of loop now")
            #plt.scatter(x1,y1, s=5, color='white')
        
        #plt.axline(Rcorner, Lcorner, linewidth=1, linestyle='dashed', color='r')
        #plt.xlim(min(x), max(x))
        #plt.ylim(min(y), max(y))

        df_r = df.query('z < 0.27')
        x_r=df_r["x"]
        y_r=df_r["y"]
            #plt.scatter(x_r,y_r, s=0.1, c="white")

            #ax2.axline(Rcorner, Lcorner, linewidth=1, linestyle='dashed', color='r')
            

        #ig = plt.figure()
        #ax = fig.add_subplot(111, projection='3d')
        #ax.plot_surface(x_r, y_r, z_r)
        #ax.scatter(Rcorner2,s=15,c='green')

        #module_width = math.dist(Lcorner, Rcorner)

    #slope, intercept, r_value, p_value, std_err = linregress(Lcorner,Rcorner)
    #inv_slope = -1/slope
    #inv_intercept = Lcorner[1] - inv_slope*Lcorner[0]

    #commented until i fix this
    #print(slope,intercept)
    #print(module_width)
    #print(exec_time)

    #plt.figtext(0.5, 0.01, "Module width is: %.3f, exec time is: %.3f\nxAxis: y = %.3fx + %.3f\nyAxis: y = %.3fx + %.3f" % (module_width, exec_time, slope, intercept, inv_slope, inv_intercept), ha="center", fontsize=+11, bbox={"facecolor":"gray", "alpha":0.5, "pad":5})
    
    #with plt.style.context("bmh"):
        #x = np.linspace(130,138,100)
        #ax2.plot(x, inv_slope*x+inv_intercept, linewidth=1, linestyle='dashed', color='r')



    # SCATTER AROUND THE CORNER
    switch=1 #to turn this of
    if switch == 1:

        HEIGHT_PROTO=profile_selector(CORNER_PROTO[0]-0.5,1.3,verbose=0,plot=0,dataframe=df,z_params=z)
        print("#determined height limit is ",HEIGHT_PROTO)
        CORNER_PROTO_2=[CORNER_PROTO[0]+0.03,CORNER_PROTO[1]+0.035]

        #df = df.query("z < @HEIGHT_PROTO")

        x = df["x"]
        y = df["y"]
        z = df["z"]

        fig, ax = plt.subplots()
        
        im = plt.scatter(x, y, c=z, s=15, cmap="viridis")
        
        lst = list(CORNER_PROTO)
        lst[0] = CORNER_PROTO[0]+0.024
        lst[1] = CORNER_PROTO[1]-0.897
        CORNER_PROTO = tuple(lst)

        points = [i for i in zip(x, y)]
        #LATEST_CORNER = min(points, key=lambda point: math.hypot(CORNER_PROTO_2[1]-point[1], CORNER_PROTO_2[0]-point[0]))
        print("#Success. Corner found at: ",CORNER_PROTO)
        print("{0},{1}".format(CORNER_PROTO[0],CORNER_PROTO[1]))
        plt.scatter(CORNER_PROTO[0], CORNER_PROTO[1], s=25, color='red', marker="o") #tuto bol Lcorner nvm preco ???
        #plt.scatter(CORNER_PROTO_2[0], CORNER_PROTO_2[1], s=25, color='red', marker="o")
        #plt.scatter(LATEST_CORNER[0], LATEST_CORNER[1], s=25, color='red', marker="o")
        fig.colorbar(im, ax=ax)
        '''
        f=open("metrology_results.txt","a")
        f.write("%s\n" % (xyz_file))
        f.write("Upper-right sensor corner: [%s, %s]\n" % (Lcorner[0],Lcorner[1]))
        f.close()
        '''
        #plt.show()

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d') 

        #print(df3d)
        ax.scatter(df['x'], df['y'], df['z'],s=0.8,c=df['z'])
        for i in range(0,30):
            ax.scatter(Lcorner[0],Lcorner[1],i*(0.8/20),c='green',s=15)
        #plt.show()


