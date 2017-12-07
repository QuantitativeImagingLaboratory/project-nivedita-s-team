1. Implementation of fft
to compute fft run fftsymmetry.py file which gives the desired output. As time taken to compile  fft written by us is more when compared to inbuilt fft, we used inbuilt fft for our computation.

2. Implementation of frequency filtering
Steps to apply filter:
Compile Home.py
- click Browse image to import image.
- First select filter you want to apply i.e
	- Normal Filter
	- Band Filter
- Then Select type of filter you want to apply.
	-ideal
	-gaussian
	-butterworth
 	you may choose high pass or low pass for band filter - Low pass represents band reject and high pass represents band pass filter.
-click on 'click here to convert button' for the output.
-output will be filtered image and mask image.

3. Implementation of notch filter
- click on browse button  to import image(There are few images with noise: lena2.jpg, periodic.png, noise.png).
 - click on 'band notch' button .
- dft of the image is displayed. Drag and cover noise in the image.
- then press 'x' to exit dft image and compile band notch.
- output will be noise reduced image and mask image.
 