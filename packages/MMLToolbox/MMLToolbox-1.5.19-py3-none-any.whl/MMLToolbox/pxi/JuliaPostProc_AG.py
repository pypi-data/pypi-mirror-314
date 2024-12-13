import h5py 
import numpy as np
import scipy.signal._savitzky_golay
import numpy as np

from .StoreSetup import StoreSetup
from math import factorial
from scipy.interpolate import interp1d
from scipy.optimize import root


class JuliaPostProc_AG():
    def __init__(self, h5Folder):
        self.h5Folder = h5Folder
        self.info = {}
        self.B_meas = None        # Measured B
        self.H_meas = None        # Measured H
        self.B_smooth = None      # Filtered B
        self.H_smooth = None      # Filtered H
        self.B_correct = None     # Correct B by using Function correctHystCurveInterpolateAnhystereticCurve
        self.H_correct = None     # Correct H by using Function correctHystCurveInterpolateAnhystereticCurve
        self.B_an = None          # Anhysterese B by using Function origHystCurveInterpolateAnhystereticCurve
        self.H_an = None          # Anhysterese H by using Function origHystCurveInterpolateAnhystereticCurve
        self.B_an_correct = None  # Anhysterese B by using Function correctHystCurveInterpolateAnhystereticCurve
        self.H_an_correct = None  # Anhysterese H by using Function correctHystCurveInterpolateAnhystereticCurve
        self.B_commutation = None # B of commutation curve by using max(B)
        self.H_commutation = None # H of commutation curve by using max(H)
    

    ################################
    # User Functions
    ################################
    def readBHResults(self,filename,B_dir,H_dir,increment=1,startlevel=0,endlevel=None) -> None:
        ss = StoreSetup(f"./{self.h5Folder}/{filename}")
        
        B_dic = ss.readPostProc("all", B_dir)
        H_dic = ss.readPostProc("all", H_dir)
        levels = list(B_dic.keys())

        B_values = np.transpose(np.array(list(B_dic.values())))
        H_values = np.transpose(np.array(list(H_dic.values())))   
        B_values = B_values[:,startlevel:endlevel:increment]
        H_values = H_values[:,startlevel:endlevel:increment]

        H_values = self.__correctOrientation(B_values,H_values)
        self.B_meas = B_values
        self.H_meas = H_values

        self.info["levels"] = levels[startlevel:endlevel:increment]
        self.info["B_dir"] = B_dir
        self.info["H_dir"] = H_dir

    def filterMeasurements(self,windowsize,order):
        #TODO: Implement twostepfilter wie in julia --> gibt es das in Python überhaupt?
        B_smooth = np.zeros(self.B_meas.shape)
        H_smooth = np.zeros(self.H_meas.shape)

        for i in range(self.H_meas.shape[1]):
            H_smooth[:,i] = scipy.signal.savgol_filter(self.H_meas[:,i],windowsize, order)
        
        for i in range(self.B_meas.shape[1]):
            B_smooth[:,i] = scipy.signal.savgol_filter(self.B_meas[:,i],windowsize, order)
        
        self.B_smooth = B_smooth
        self.H_smooth = H_smooth

    def correctHystCurveInterpolateAnhystereticCurve(self,B,H,numSamplePoints):      
        # Get Anhysterese from Data
        B_an,H_an,B_an_itp_of_H,B_asc,H_asc,B_desc,H_desc = self.__interpolateAnhystereticCurve(B,H,numSamplePoints)
        self.B_an = B_an
        self.H_an = H_an
        self.info["B_asc"] = B_asc
        self.info["H_asc"] = H_asc
        self.info["B_desc"] = B_desc
        self.info["H_desc"] = H_desc

        # Correct Hysterese based on computed Anhysterse
        delta_H, H_correct = self.__correctHystCurve(H,B_an_itp_of_H)
        B_an,H_an,B_an_itp_of_H,B_asc,H_asc,B_desc,H_desc = self.__interpolateAnhystereticCurve(B,H_correct,numSamplePoints)

        self.B_an_correct = B_an
        self.H_an_correct = H_an
        self.B_correct = B
        self.H_correct = H_correct
        self.info["B_asc_correct"] = B_asc
        self.info["H_asc_correct"] = H_asc
        self.info["B_desc_correct"] = B_desc
        self.info["H_desc_correct"] = H_desc
        self.info["delta_H"] = delta_H
        return B_an_itp_of_H
    
    def getCommutationCurve(self,B,H):
        numLevels = B.shape[1]
        H_comm = []
        B_comm = []
        for i in range(numLevels):
            B_comm.append(max(B[:,i]))
            H_comm.append(max(H[:,i]))
        return np.array(B_comm), np.array(H_comm)

    ################################
    # Internal Functions
    ################################
    @staticmethod
    def __correctOrientation(B,H):
        H_corr = np.array(H)
        Bt = B[:,0]
        Ht = H[:,0]
        max_index_B = np.argmax(Bt)
        if Ht[max_index_B] < 0.0:
            H_corr = H_corr * -1
        return H_corr
    
    @staticmethod
    def __findAscendingDescendingIndices(H, M):
        ind_ascending = []
        ind_descending = []
        for n in range(len(H)): 
            if not np.any((H > H[n]) & (M < M[n])): 
                ind_ascending.append(n) 
            elif not np.any((H < H[n]) & (M > M[n])): 
                ind_descending.append(n)
        return ind_ascending, ind_descending
    
    @staticmethod
    def __uniqueSort(B, H):
        ha = np.sort(H) 
        ba = np.sort(B) 
        b, index = np.unique(ba, return_index=True)
        h = ha[index]
        return b, h


    def __interpolateAnhystereticVector(self,B,H,num_sample_points):
        ind_ascending, ind_descending = self.__findAscendingDescendingIndices(H,B)

        B_asc, H_asc = self.__uniqueSort(B[ind_ascending], H[ind_ascending])
        B_desc, H_desc = self.__uniqueSort(B[ind_descending], H[ind_descending])

        Ba = np.linspace(min(np.min(B_asc), np.min(B_desc)), max(np.max(B_asc), np.max(B_desc)), num_sample_points)
      
        H_asc_of_M = interp1d(B_asc, H_asc, fill_value="extrapolate")
        H_desc_of_M = interp1d(B_desc, H_desc, fill_value="extrapolate")
     
        H_asc_itp = H_asc_of_M(Ba)
        H_desc_itp = H_desc_of_M(Ba)
        H_avg = (H_asc_itp + H_desc_itp) / 2
        B_of_H = interp1d(H_avg, Ba, fill_value="extrapolate")
        return H_avg,Ba,B_of_H,H_asc_itp,H_desc_itp
      
    def __interpolateAnhystereticCurve(self,B, H, numSamplePoints):
        H_an = []
        B_an = []
        H_asc = []
        H_desc = []
        B_asc = []
        B_desc = []
        B_an_itp_of_H = []
        
        for i in range(B.shape[1]):
            H_an_vector,Ba,B_an_itp_of_H_vector,H_asc_vector, H_desc_vector = self.__interpolateAnhystereticVector(B[:,i], H[:,i],numSamplePoints)
            H_an.append(H_an_vector)
            B_an.append(B_an_itp_of_H_vector(H_an_vector))
            H_asc.append(H_asc_vector)
            H_desc.append(H_desc_vector)
            B_asc.append(Ba)
            B_desc.append(Ba)
            B_an_itp_of_H.append(B_an_itp_of_H_vector)
        
        H_an = np.transpose(np.array(H_an))
        B_an = np.transpose(np.array(B_an))
        H_asc = np.transpose(np.array(H_asc))
        H_desc = np.transpose(np.array(H_desc))
        B_asc = np.transpose(np.array(B_asc))
        B_desc = np.transpose(np.array(B_desc))
        return B_an,H_an,B_an_itp_of_H,B_asc,H_asc,B_desc,H_desc

    def __correctHystCurve(self, H, B_an_itp_of_H):
        number_of_levels = H.shape[1]
        H_correct =[]
        deltaH = []
        for i in range(number_of_levels):
            s = root(B_an_itp_of_H[i], [0.0], method='hybr')
            deltaH.append(s.x[0])
            H_correct.append(H[:,i] - deltaH[i])
        return np.array(deltaH), np.transpose(H_correct)
    
    

    

