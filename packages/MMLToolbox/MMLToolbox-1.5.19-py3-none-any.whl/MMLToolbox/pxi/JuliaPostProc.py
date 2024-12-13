import h5py 
import numpy as np
import scipy.signal._savitzky_golay
import numpy as np
from math import factorial
from scipy.interpolate import interp1d
from scipy.optimize import root


class PostProc:


    def __init__(self):
        pass

    def readBHResults(self, filename, increment, endlevel, startlevel, h5folder, direction, useHallsensor):
        h = []
        b = []

        with h5py.File(filename, "r") as file:
            
            if useHallsensor == True:
                for i in range(endlevel):
                    h.append(file["data"]["step-"+str(i)]["Hx"])
                
            else:                
                for i in range(endlevel):                    
                    h.append(file["data"]["step-"+str(i)]["Hx"])
                
            h = np.transpose(h)
            
            for i in range(endlevel):                    
                    b.append(file["data"]["step-"+str(i)]["Bx"])
            
            b = np.transpose(b)
            
            
            

        return b[0:len(b):increment,startlevel:endlevel+1],h[0:len(h):increment,startlevel:endlevel+1]
    

    def correctOrientation(self, B, H):
        B_transposed = np.transpose(B)
        max_index_B = np.argmax(B_transposed[0])
        Htransposed = np.transpose(H)
        if Htransposed[0][max_index_B] < 0.0:

            H = H * -1
        return H
    
    def filterMeasurements(self, B, H, windowsize, order):
        
        for i in range(len(H[0])):
            H[:,i] = scipy.signal.savgol_filter(H[:,i],windowsize, order)
        
        for i in range(len(B[0])):
            B[:,i] = scipy.signal.savgol_filter(B[:,i],windowsize, order)
        
        
        return H, B
    

    def findAscendingDescendingIndices(self, H, M):
        ind_ascending = []
        ind_descending = []
        for n in range(len(H)):
            if not any(H[n] > H[i] and M[n] < M[i] for i in range(len(H))):
                ind_ascending.append(n)
            elif not any(H[n] < H[i] and M[n] > M[i] for i in range(len(H))):
                ind_descending.append(n)
        return ind_ascending, ind_descending

    def uniqueSort(self, M, H, indices):
        M_sorted = [M[i] for i in indices]
        H_sorted = [H[i] for i in indices]
        sorted_pairs = sorted(zip(M_sorted, H_sorted))
        M_unique, H_unique = zip(*sorted_pairs)

        return np.array(M_unique), np.array(H_unique)


    def interpolateAnhystereticVector(self,M, H, num_sample_points):
       
        
        ind_ascending, ind_descending = self.findAscendingDescendingIndices(H, M)

        M_asc, H_asc = self.uniqueSort(M, H, ind_ascending)
        M_desc, H_desc = self.uniqueSort(M, H, ind_descending)

        Ma = np.linspace(max(min(M_asc), min(M_desc)), min(max(M_asc), max(M_desc)), num_sample_points)
      
        H_asc_of_M = interp1d(M_asc, H_asc, fill_value="extrapolate")
        H_desc_of_M = interp1d(M_desc, H_desc, fill_value="extrapolate")

        # H_asc_of_M = interp1d(M_asc, H_asc)
        # H_desc_of_M = interp1d(M_desc, H_desc)
        
        
      
        Ha = H_asc_of_M(Ma)
        
        Hd = H_desc_of_M(Ma)
        Hm = (Ha + Hd) / 2

        
        return Hm, Ma, interp1d(Hm, Ma, fill_value="extrapolate"), Hd,Ha
      
    def interpolateAnhystereticCurve(self,B, H, numSamplePoints):
        
        H_an = []
        B_an = []
        Ha = []
        Hd = []
        B_an_itp_of_H = []
        
        for i in range(0,len(B[0])):
            H_an_vector, B_an_vectore,B_an_itp_of_H_vector, Ha_vector, Hd_vector = self.interpolateAnhystereticVector(B[:,i], H[:,i],numSamplePoints)
            Ha.append(H_an_vector)
            B_an.append(B_an_vectore)
            Ha.append(Ha_vector)
            Hd.append(Hd_vector)
            B_an_itp_of_H.append(B_an_itp_of_H_vector)
        
        H_an = np.transpose(np.array(Ha))
        B_an = np.transpose(np.array(Ha))
        Ha = np.transpose(np.array(Ha))
        Hd = np.transpose(np.array(Ha))
        return H_an, B_an, B_an_itp_of_H, Ha, Hd

    def correctHystCurve(self, H, B_an_itp_of_H):
        time_steps = len(H)
        number_of_levels = len(H[0])
        H_correct =[]
        deltaH = []
        for i in range(number_of_levels):
            s = root(B_an_itp_of_H[i], [0.0], method='hybr')
            deltaH.append(s.x[0])
            H_correct.append(H[:,i] - deltaH[i])

        return np.array(deltaH), np.transpose(H_correct)
    

    def getCommutationCurve(self, B,H):
        numLevels = len(B[0])
        numTimeSteps = len(B)

        H_comm = []
        B_comm = []

        for i in range(numLevels):
            B_comm.append(max(B[:,i]))
            H_comm.append(max(H[:,i]))
        return np.array(B_comm), np.array(H_comm)
