import math
from typing import Any

Tau = math.pi * 2

class Sample():
	def __init__(self, TimeCode: float, Amplitude) -> None:
		self.TimeCode = TimeCode
		self.Amplitude = Amplitude
	
	def __add__(self, other: "Sample") -> "Sample":
		if self.TimeCode != other.TimeCode:
			raise AttributeError
		return Sample(self.TimeCode, self.Amplitude + other.Amplitude)

	def ScaleAmplitude(self, Scalar: float) -> "Sample":
		return Sample(self.TimeCode, self.Amplitude * Scalar)
	
	def __repr__(self) -> str:
		return "Sample(%s, %s)" % (self.TimeCode, self.Amplitude)
	
	def __str__(self) -> str:
		return "%sunits@%s" % (self.Amplitude, self.TimeCode)
	
	def __graph__(self, Scalar: float = 1, Offset: float = 0) -> str:
		if type(self.TimeCode) is not float:
			raise TypeError
		if type(self.Amplitude) is float:
			q = str(self.TimeCode) + " | " + math.floor(self.Amplitude * Scalar + Offset) * " " + "|" 
		elif type(self.Amplitude) is Complex:
			q = str(self.TimeCode) + " | " + math.floor(self.Amplitude.GetMagnitude() * Scalar + Offset) * " " + "|" 
		else:
			print(self.Amplitude)
			raise TypeError
		return q

class TimeSpan():
	def __init__(self) -> None:
		self.Samples: list[Sample] = []
	
	def AppendSample(self, SampleSample: "Sample") -> None:
		self.Samples.append(SampleSample)
	
	def AppendMultipleSamples(self, Samples: list[Sample]) -> None:
		for SampleSample in Samples:
			self.Samples.append(SampleSample)
	
	def GetAmplitudeFromTimeCode(self, Time: float) -> float:
		Index = self.GetTimeCodes().index(Time)
		return self.GetAmplitudes()[Index]

	def __get_dx__(self):
		return self.Samples[1].TimeCode-self.Samples[0].TimeCode

	def __add__(self, other: "TimeSpan") -> "TimeSpan":
		TimeSpanHandler = TimeSpan()
		for Time, Amp in self.GetZippedSamples():
			TimeSpanHandler.AppendSample(Sample(Time, Amp + other.GetAmplitudeFromTimeCode(Time)))
		return TimeSpanHandler

	def __repr__(self) -> str:
		return "TimeSpan() #%s Samples" % (len(self.Samples))
	
	def __graph__(self, Scalar: float = 1, Offset: float = 0) -> str:
		print("--------------------------")
		for SamplesSample in self.Samples:
			print(SamplesSample.__graph__(Scalar, Offset))
		print("--------------------------")
	
	def GetTimeCodes(self):
		TimeCodes = []
		for TimeCodeSample in self.Samples:
			TimeCodes.append(TimeCodeSample.TimeCode)
		return TimeCodes
	
	def GetAmplitudes(self):
		Amplitudes = []
		for AmplitudeSample in self.Samples:
			Amplitudes.append(AmplitudeSample.Amplitude)
		return Amplitudes
	
	def GetZippedSamples(self):
		return zip(self.GetTimeCodes(), self.GetAmplitudes())

class Complex():
	"""Complex() -> My own implementation of complex numbers with extra functions for ease of use

	Main Functions:
	__init__(self, Real: float = 0, Imaginary: float = 0) -> Creates new Complex number defaults to 0 + 0i
	__add__(self, other: "Complex") -> Add overload, adds Complex numbers
	__mul__(self, other: "Complex") -> Mul overload, multiplies Complex numbers
	PolarToComplex(self, Angle: float, Amplitude: float) -> Converts polar coordinates to Complex number
	GetMagnitude(self) -> Gets the magnitude of self (sqrt(Real**2*Imaginary**2))
	__repr__(self) -> Basic representation of self
	__str__(self) -> Basic string convertion of self
	"""
	def __init__(self, Real: float = 0, Imaginary: float = 0):
		self.Real = Real
		self.Imaginary = Imaginary
	
	def __add__(self, other: "Complex") -> "Complex":
		return Complex(	self.Real + other.Real, 
				 		self.Imaginary + other.Imaginary)

	def __mul__(self, other: "Complex") -> "Complex":
		return Complex(	self.Real * other.Real - self.Imaginary * other.Imaginary,
						self.Real * other.Imaginary + self.Imaginary * other.Real)
	
	def PolarToComplex(self, Angle: float, Amplitude: float) -> "Complex":
		if type(Amplitude) is Complex:
			return Complex(math.cos(Angle), math.sin(Angle)) * Amplitude
		elif type(Amplitude) is float or type(Amplitude) is int:
			return Complex(math.cos(Angle) * Amplitude, math.sin(Angle) * Amplitude)
		else:
			raise TypeError
	
	def GetMagnitude(self) -> float:
		if type(self.Real) is not float and type(self.Real) is not int:
			print(self.Real, self.Imaginary)
			raise TypeError
		return math.sqrt((self.Real ** 2) + (self.Imaginary ** 2))

	def __repr__(self) -> str:
		return "Complex(%s, %s)" % (self.Real, self.Imaginary)
	
	def __str__(self) -> str:
		return "%s + %si |%s|" % (self.Real, self.Imaginary, self.GetMagnitude())

def Faculty(x: int) -> float:
	q = 1
	for i in range(2, x):
		q *= i
	return q

def DiscreteFourierTransFormTimeSpan(
		TimeSpanInput: "TimeSpan", 
		StartFrequency: float = 0, 
		EndFrequency: float = 10, 
		Resolution: float = 10, 
		Inverse: bool=False, 
		PercentageThreshholdDigits: float=2) -> "TimeSpan":
	"""_summary_

	Args:
		TimeSpanInput (TimeSpan): Input of TimeSpan for transformation
		StartFrequency (float, optional): Starting frequency to analyse. Defaults to 0.
		EndFrequency (float, optional): Ending frequency to analyse. Defaults to 10.
		Resolution (float, optional): Resolution of analysation. Defaults to 10.
		Inverse (bool, optional): False: Forward Fourier; True: Inverse Fourier. Defaults to False.
		PercentageThreshholdDigits (float, optional): Digits to show for percentage through transformation. Defaults to 3.

	Raises:
		TypeError: If Amplitude of Sample is not of typee int|float|Complex

	Returns:
		TimeSpan: Creates TTimeSpan of transformed TimeSpan where frequency is set to TimeCode and Amplitude is the full Complex output
	"""

	#Create class handlers for clearer handling
	TimeSpanHandler = TimeSpan()	#The final output TimeSpan
	ComplexHandler = Complex()

	if Inverse:	#Inverse Fourier
		sign = 1
		Multiplier = 1/math.sqrt(Tau)
	else:		#Forward Fourier
		sign = -1
		Multiplier = 1
	
	ComplexMultiplier = Complex(Multiplier, Multiplier)

	TotalIterations = (EndFrequency-StartFrequency)*Resolution

	#Main Fourier loop through every frequency
	for ScaledFrequency in range(math.floor((TotalIterations))):
		Frequency = (ScaledFrequency-StartFrequency)/Resolution
		WorkingPoint = Complex()

		# ScaledPercentageThreshhold = math.floor(TotalIterations/(10**PercentageThreshholdDigits))
		# if ScaledFrequency %  ScaledPercentageThreshhold == 0:
		# 	PercentageThrough = 100*Frequency/(EndFrequency-StartFrequency)
		# 	print("%s%s" % (str(PercentageThrough), "%"))

		#Integral part of Fourier
		for Time, Amp in TimeSpanInput.GetZippedSamples():
			Angle = sign * Tau * Time * Frequency
			WorkingPoint += ComplexHandler.PolarToComplex(Angle, Amp)
		
		OutputAmplitude = WorkingPoint * ComplexMultiplier
		if Inverse:
			WorkingSample = Sample(Frequency, OutputAmplitude.GetMagnitude())
		else:
			WorkingSample = Sample(Frequency, OutputAmplitude)
		TimeSpanHandler.AppendSample(WorkingSample)
	
	return TimeSpanHandler

def CreateSineWaveTimeSpan(StartTime: float, EndTime: float, Resolution: float, Freq: float, Amp: float = 1) -> list["Sample"]:
	TimeSpanHandler = []
	for ScaledTimeCode in range(math.floor((EndTime-StartTime)*Resolution)):
		TimeCode = (ScaledTimeCode-StartTime)/Resolution

		Amplitude = math.sin(TimeCode * Tau * Freq)
		TemporarySample = Sample(TimeCode, Amplitude * Amp)
		TimeSpanHandler.append(TemporarySample)
	return TimeSpanHandler

def CreateSquareWaveTimeSpan(StartTime: float, EndTime: float, Resolution: float, Freq: float) -> list["Sample"]:
	TimeSpanHandler = []
	for ScaledTimeCode in range(math.floor((EndTime-StartTime)*Resolution)):
		TimeCode = (ScaledTimeCode-StartTime)/Resolution

		if (TimeCode*Freq) % 1 < .5:
			Amplitude = Complex(1, 1)
		else:
			Amplitude = Complex(0, 0)
		
		TemporarySample = Sample(TimeCode, Amplitude)
		TimeSpanHandler.append(TemporarySample)
	return TimeSpanHandler

def __main__(StartTime: float = 0, EndTime: float = 50, Resolution: float = 10) -> list["TimeSpan"]:
	"""_summary_

	Args:
		StartTime (float, optional): Start frequency of Fourier and Inverse Fourier. Defaults to 0.
		EndTime (float, optional): End frequency of Fourier and Inverse Fourier. Defaults to 100.
		Resolution (float, optional): Resolution of frequencies analysed. Defaults to 50.

	Returns:
		list["TimeSpan"]: Returns Input, Forward Fourier, Inverse Fourier
	"""
	print("Creating input.")
	WorkingSineTimeSpan = TimeSpan()
	WorkingSineList = CreateSquareWaveTimeSpan(0, 50, 50, 1)
	WorkingSineTimeSpan.AppendMultipleSamples(WorkingSineList)
	
	# return WorkingSineTimeSpan

	print("Squarewave created.")

	Fourier = DiscreteFourierTransFormTimeSpan(WorkingSineTimeSpan, StartTime, EndTime, Resolution)
	print("Fourier Done.")

	# return WorkingSineTimeSpan, Fourier

	InverseFourier = DiscreteFourierTransFormTimeSpan(Fourier, StartTime, EndTime, Resolution, True)

	print("Inverse Fourier Done.")

	return WorkingSineTimeSpan, Fourier, InverseFourier
