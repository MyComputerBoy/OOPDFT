# OOPDFT
 OOP Discrete Fourier Transform

 My plain python implementation of Discrete Fourier Transformation

 dft.py -> Main python file
 Main user classes:

 Complex() -> My own complex number implementation with extra functions for ease of use
 Sample() -> Class to store samples for cleaner implementation of DFT
 TimeSpan() -> Class to store full time spans of Sample()s for complete input and transformations

 
 Main user functions:

 DiscreteFourierTransFormTimeSpan(
		TimeSpanInput: "TimeSpan", #TimeSpan input for analysation
		StartFrequency: float = 0, #Frequency to start analyse 
		EndFrequency: float = 10,  #Frequency to stop analyse
		Resolution: float = 10,    #Resolution of frequencies to analyse
		Inverse: bool=False,       #False: Forward Fourier; True: Inverse Fourier
		PercentageThreshholdDigits: float=3 #Digits to show for percentage through analysation
  ) -> "TimeSpan"            #Returns TimeSpan where Frequency is set to TimeCode and Complex output is set to Amplitude
  CreateSineWaveTimeSpan(
   StartTime: float,         #Start time to create sinewave
   EndTime: float,           #End time to create sinewave
   Resolution: float,        #Resolution of TimeCode
   Freq: float               #Frequency of sinewave
   ) -> list["Sample"]       #Outputs a list["Sample"] for easier input for TimeSpan
  CreateSquareWaveTimeSpan(
   StartTime: float,         #Start time to create squarewave
   EndTime: float,           #End time to create squarewave
   Resolution: float,        #Resolution of TimeCode
   Freq: float               #Frequency of squarewave
   ) -> list["Sample"]:      #Outputs a list["Sample"] for easier input for TimeSpan
   __main__(
    StartTime: float = 0,    #Start time for Forward and Inverse Fourier Transformations
    EndTime: float = 100,    #End time for Forward and Inverse Fourier Transformations
    Resolution: float = 50   #Resolution for frequencies analysed
    ) -> list["TimeSpan"]:   #Outputs Forward Fourier, Inverse Fourier
