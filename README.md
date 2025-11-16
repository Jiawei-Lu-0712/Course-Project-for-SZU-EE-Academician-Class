# Outline

## Machine Learning

### Regression
Use Boston House Dataset (506 samples and 13 feature variables), predict the value of prices of the house using the given features.  
Split input data into training and testing sets (the testing set includes 10% of the samples).  
The output of the algorithm should include the model learned from the whole training set, the average mean squared error on training set via 10-fold cross validation.  
For ridge regression model, determine the value of hyper-parameter via 10-fold cross validation.

### Classification
Use logistic regression & LDA & KNN & Naive Bayes & SVM to implement the classification on the Seeds dataset respectively.

### Clustering
Load 5 datasets. Drawing scatterplots to visualize data sets.  
Use K-means Clustering on all the data sets separately, and visualize the clustering results.  
Use DBScan on all the data sets separately, adjust the parameter eps for different datasets, and visualize the clustering results.

### Deep Learning
1. Use MLP for image classification on the MINST dataset. Revise the MLP architecture if any.  
2. Use Transformer for natural language learning on cmn-eng dataset. Revise the transformer architecture if any.

In each experiment, set the seed value to the last 4 numbers of your student ID in  
```

np.random.seed(seed=1)
torch.manual_seed(1)

```
or  
```

set_seed(seed)

```

In each experiment, report the classification results including quantitative results and intermediate visualization results.  
Report the figure of training loss, feature maps of intermediate layers.

### Reinforcement Learning
1. **Q-Learning**  
   Choose an environment, Blackjack or Cliff Walking:  
   https://gymnasium.farama.org/environments/toy_text/  
   Train an agent in the environment you chose.

2. **PPO**  
   Debug the code to run smoothly and train an agent.  
   Revise the parameter clip-coef to different values. Report and analyse the results. You may need to fix the seed when you compare different clip-coef values.

### Final Lab
Research on multi-channel fusion perception interaction including gesture, somatosensory, voice, etc.  
Design an end-to-end multi-task learning model to process gesture recognition, voice recognition and somatosensory analysis at the same time, and output the user's comprehensive intention.  
Demonstrate the practical application of virtual-reality fusion terminals in education, cultural tourism, industry and other scenarios.  
**Requirements:** The accuracy of gesture, somatosensory and voice fusion interaction is ≥ 96%.

---

## Blockchain
Textbook：《Mastering Blockchain: Second Edition》

### sha256_hash
Design a standard hash algorithm and verify it.

### EllipticCurve-Signature
Design a standard elliptic curve signature algorithm and verify it.

### ETH_Wallet
Design a blockchain wallet and verify it.

### contracts
Design a smart contract to mint and auction NFTs.

---

## Computer Architecture
Textbook：《Computer Organization and Design: RISC-V Edition》

### Final_lab
1. Conduct preliminary testing on the Tang Nano 20K FPGA development board, and install and verify the Gowin FPGA IDE on their system.  
2. Write Verilog code to implement an LED blinking experiment on the Tang Nano 20K development board.  
3. Compile and deploy the NES simulator on the FPGA board, set up peripherals (game controller, HDMI monitor, TF card), and achieve complete compilation and execution.  
4. Compile the SparrowRV design and program it onto the FPGA, and execute the "Hello World" test on the running processor.

---

## Computer Network
Textbook：《Computer Networking A Top-Down Approach: Eighth Edition》

### Application Layer
1. Developing a simple Web server in Python that is capable of processing only one request.  
2. Developing a simple DNS resolution program  
3. Developing a simple FTP based on TCP

### Data link layer
Wireshark experiments  
1. Ethernet  
2. Address Resolution Protocol (ARP)

### Network Layer
Implement Routing algorithm  
1. Link State algorithm  
2. Distance-Vector algorithm

### Physical layer
WiFi platform experiments

### Transport Layer
Implement reliable data transfer protocol reliable transport layer protocol  
1. stop-and-wait  
2. Go-back-N  
3. Selective repeat

---

## Digital Image Processing
Textbook：《Digital Image Processing: fourth edition》

### Digital Image Fundamentals
1. **Display Three Individual Color Components of RGB Image.**  
   Load an image with OpenCV. Display the R, G, and B color component of image, respectively. Display them in the same figure with sub-figures.

2. **Convert Color Image to Grayscale.**  
   Display the original Lena image and the grayscale images obtained by three grayscaling methods in the same figure. Add the corresponding title.  
   a1) Maximum of the three components;  
   a2) The average of the three components;  
   a3) gray = 0.30r + 0.59g + 0.11b.

3. **Image Cropping.**  
   Load a RGB image. Select the 128x128 central region of the image. Display the full image and its central part. Save the central part as an image file in the same format as the full image.

4. **Adding Noise to Image.**  
   Load an RGB image with Scikit-Image. Add Gaussian additive noise, salt noise, pepper noise, salt and pepper noise, or speckle noise to it.The parameters can be chosen freely.Display these six images in the same figure and add the corresponding title.

5. **Image Denoising by Averaging.**
   Load an RGB image.Add Gaussian noise with a mean value of 0 and a variance of 0.1 to it.Display and compare the images before and after adding noise.Use the for loop to add 3, 30, and 300 images with random Gaussian noise and find their average value, respectively. 

6. **Image Algebraic Operations.**
   Download two pictures by yourself, and load these two pictures with OpenCV.Perform algebraic operations of addition and subtraction.Display the images before and after processing.

7. **Text adding**
   Load the Lena image with OpenCV.Employ a red rectangle to mark the 64x64 rectangle in the middle of image.Adding some black text on it.

8. **Adding image mask.**
   Load the Lena image with OpenCV.Adding a circular mask on the Lena image.

### Intensity Transformations and Spatial Filtering
1. **Perform Contrast Adjustment.**  
   Load the image 'beans.png'.Stretch its graysacle to the range of [0,1].Shrink its grayscale to the range of [0.2,0.8].Obtain the negative image.Perform log transformation.Perform Gamma transformation with 𝛾=0.5 and 𝛾=1.5, respectively.

2. **Compute and Display Image Histogram.**  
   Compute the histogram of the original image and the histograms of the adjusted images above.Display the histogram of the original image and the histograms of the adjusted images above.

3. **Image Histogram Equalization.**  
   Load the image 'beans.png'.Perform histogram equalization of the image.Display the original image, the equalized image, the histogram of the original image, and the equalized image.

4. **Smoothing Linear Filtering.**  
   Load the image 'mandrill.jpg'.Add salt&Pepper noise with different intensities (at least 3 kinds).Perform smoothing linear filtering to smooth these noised images respectively.

5. **Gaussian Smoothing Filtering.**
   Load the image 'mandrill.jpg'.Add Gaussian noise to image.Perform Gaussian Smoothing Filtering to smooth the noised image. Select kernels with different radius values (at least 3 kinds).

6. **Median Filtering.**
   Load the image 'mandrill.jpg'.Add salt&Pepper noise with different intensities (at least 3 kinds).Perform median filtering to smooth these noised images respectively. Select kernels with different radius parameter values (at least 3 kinds).

7. **Sharpening Filtering.**
   Load the image 'lena.jpg', convert it to grayscale.Perform sharpening spatial filtering to enhance the image with different parameters (at least 3 kinds).

8. **Face Detection and Processing with OpenCV.**
   Load the image 'exp2_7.jpg'.The face region is detected and marked with a green rectangle.Perform Gaussian smoothing filtering for the background region.

9. **Face Detection with Laptop Camera.**
   Load video stream from the laptop camera.Use a face detection model to detect images captured by the camera.Mark the face region with a green rectangle to achieve real-time detection as good as possible.Perform Gaussian smoothing filtering for the background region.

### Filtering in the Frequency Domain
1. **FFT and IFFT.**  
   Load the image rhino.jpg, convert it to grayscale.Perform FFT. Shift the DC component to the center, and show the phase angles and the magnitudes.Perform IFFT and show the reconstructed image (Tips: remember to shift the DC component back).

2. **Ideal Lowpass Filtering.**  
   Load the image rhino.jpg. Convert it to grayscale.Perform FFT.Design an ideal lowpass filter.Perform frequency domain filtering with the ideal lowpass filter.

3. **Gaussian Lowpass Filter.**  
   Load the image lena.jpg. Convert it to grayscale.Perform FFT.Perform Gaussian lowpass filtering.

4. **Butterworth Lowpass Filter.**  
   Load the RGB image lena.jpg.Perform FFT. (Note that when using color images, pay attention to the parameter axes of functions such as fft, ifft, fftshift and ifftshift).Design three Butterworth lowpass filters with different cutoff frequencies D0 and orders n (cut-off frequency D0 and order n are free to choose).Perform frequency domain filtering with the designed Butterworth lowpass filters.Obtain filtered images with IFFT.

5. **Butterworth Highpass Filter.**
   Load the RGB image lena.jpg.Perform FFT.Design three Butterworth highpass filters with different cutoff frequencies and orders.Perform frequency domain filtering with the designed Butterworth highpass filters.Obtain filtered images with IFFT.

6. **Motion Blur, Inverse filtering and Wiener filtering.**
   Load the RGB image lena.jpg.Apply motion blur to it.Recovering images by using inverse filtering and Wiener filtering, respectively.Add noise to the blurred image, and then use Inverse filtering and Wiener filtering to recovere the image, respectively.

7. **Homomorphic Filtering.**
   Load the RGB image forest.jpg.Write a function to enhance a color image with homomorphic filtering to each of its color channels.

### Image Compression
1. **Compression Ratio and Relative Coding Redundancy.**  
   Load the image bunny.png. Save it as a JPEG image with a quality factor of 90, 60, 10, respectively. Name the images as b90.jpg, b60.jpg, b10.jpg, respectively.Display the original image and the compressed images.Calculate the Compression Ratio and Relative Data Redundancy between the PNG image and JPEG images according to the file sizes.

2. **Fidelity Criteria.**  
   Load the saved JPEG images. Use functions from skimage.metrics to calculate MSE, PSNR, and SSIM values between the PNG image and JPEG images. Implement a SSIM function according to [1].  
[1] Wang Z, Bovik AC, Sheikh HR, Simoncelli EP. Image quality assessment: from error visibility to structural similarity. IEEE Trans Image Process. 2004 Apr;13(4):600-12.

3. **Simulation of a Part of JPEG Compression.**  
   Load the grayscale image lenagray.tiff.Shift the pixel intensity by -128.Divide the image into non-overlapped 8 ∗ 8 subimages and perform 8 ∗ 8 block DCT on each subimage.Use a quantization table with QF=50 for quantization.Perform lossless predictive coding (difference coding) of DC coefficients by using the coefficient in the previous subimage as reference (a raster scan mannar).Sort 63 AC coefficients in each block in a ZigZag order. Converted them into a one-dimensional vector.Save all the compressed data into a Numpy data format (refered to as NPY/NPZ (.npy or .npz) file).Compress the npy/npz file to a zip file (refered to as NPZzip). Compress the TIFF image to another zip file (refered to as TIFFzip).Calculate the Compression Ratio between the TIFF image and the NPY/NPZ file according to the file sizes. Calculate the Compression Ratio between the TIFF image and the NPZzip file according to the file sizes. Calculate the Compression Ratio between the TIFFZzip and the NPZzip according to the file sizes.Load the above saved file. Decode it to a recovered image.Compute the MSE and PSNR of the recovered image, and display it with the original image side by side.

### Morphological Image Processing & Image Segmentation
1. **Erosion, Dilation, Opening and Closing.**  
   Load the RGB image clock2.jpg. Convert it to grayscale and then convert it into a binary image using a threshold of 0.5. Use an SE as [1 1 1; 1 1 1; 1 1 1] to obtain the binary morphological erosion, dilation, opening and closing of the binary image. Display them in the same figure with sub-figures. Add the corresponding title to the sub-figure.Use an SE as [1 0 0; 0 1 0; 0 0 1] to obtain the binary morphological erosion, dilation, opening and closing of the binary image. Display them in the same figure with sub-figures. Add the corresponding title to the sub-figure. Load the RGB image zebras.jpg. Convert it to grayscale. Use a 3x3 SE to obtain the grayscale morphological erosion, dilation, opening and closing of grayscale image. Display them in the same figure with sub-figures. Add the corresponding title to the sub-figure.Use a 7x7 SE to obtain the grayscale morphological erosion, dilation, opening and closing of grayscale image.

2. **Boundary Extraction and Hole Filling.**  
   Load the image boundary.tif. Convert it into a binary image.Use a 5x5 SE of 1s to obtain the binary morphological erosion of the binary image. Obtian the boundary of the binary image via performing the difference between the binary image and its erosion image.Load the image holefiling.tif. Convert it into a binary image.Fill the holes in binary objects.

3. **Thining and Convex Hull.**  
   Load the image CT.tif. Convert it into a binary image.Perform morphological thinning of a binary image.Compute the convex hull image of a binary image.

4. **Top-hat (white top-hat) and Bottom-hat (black top-hat) Transformation.**  
   Load the grayscale image rice.tif. Convert it into a binary image with a threshold of 0.5. Perform top-hat transformation to the grayscale image. Obtain thresholded top-hat image and convert it into a binary image.Perform bottom-hat transformation to the grayscale image.Obtain thresholded bottom-hat image and convert it into a binary image.

5. **Edge Detection.**
   Load the image building.tif. Find edges in an image using the Roberts' cross operators, Sobel operators, Prewitt operators, and the Canny algorithm.

6. **Edge-Based Segmentation.**
   Load the coins image in skimage.Use Canny algorithm to obtain the edge image.Fill the holes to obtain the segmented image.

7. **Hough transform.**
   Load the image triangle_circle.png. Convert it to grayscale.Perform a straight line Hough transform to the grayscale image.Obtain the peaks in a straight line Hough transform.Highlight the detected lines by red color. 

8. **Thresholding-Based Segmentation.**
   Load the image shade_text1.tif.Perform automatic image thresholding by Otsu's method to get the threshold value. Transform the grayscale image into a binary image using the threshold value obtained by Otsu's method.Compute a moving average threshold.Obtain the result of local thresholding using moving averages.

9. **Segmentation Using Morphological Watersheds.**
   Load the coins image by skimage. Find edges as the elevation map in an image using the Sobel filter. Obtain the segmentation result by morphological Watersheds. 

10. **Image Processing Software with GUI.**
   Use QT or other tools to design an image processing toolbox with GUI. There is no limitation on implementations.The GUI contain at least one basic image processing function, can it can display the input image and the processed image.

---

## Electromagnetism

### Final Lab
1. Design a single-frequency, single-polarized microstrip antenna with a resonant frequency f0 of (1 + student number/10) GHz.  
2. Design a single-frequency, dual-polarized microstrip antenna with a resonant frequency of f0.  
3. Design a single-frequency, circularly polarized microstrip antenna with a reflection coefficient below -10 dB at θ=0 and an axial ratio of less than 3 dB at θ=0 (single-port implementation).
