## Self-supervised elimination of non-independent noise in hyperspectral imaging

## Graphical abstract

![](_page_0_Picture_4.jpeg)

## Highlights

- Statistical analysis of non-independent noise
- Self-supervised deep learning method to remove nonindependent noise
- High fidelity chemical imaging to provide quantitative biomarker distribution
- Robust to other imaging modalities and noise styles

## Authors

Guangrui Ding, Chang Liu, Jiaze Yin, ..., Haonan Lin, Lei Tian, Ji-Xin Cheng

## Correspondence

[hnlin@bu.edu](mailto:hnlin@bu.edu) (H.L.), [leitian@bu.edu](mailto:leitian@bu.edu) (L.T.), [jxcheng@bu.edu](mailto:jxcheng@bu.edu) (J.-X.C.)

## In brief

Denoising improves the sensitivity of optical imaging systems. It remains challenging to handle non-independent noise, which is prevalent yet often overlooked. Ding et al. systematically analyzed its behavior and physical origins. By leveraging the physical nature difference of signal and noise, a selfpermutation Noise2Noise denoiser is proposed to handle correlated noise without requiring ground truth. This approach offers high fidelity across various modalities, enhancing the capability of current imaging systems.

![](_page_0_Picture_16.jpeg)

![](_page_0_Picture_17.jpeg)

![](_page_1_Picture_1.jpeg)

## Article

## **Self-supervised elimination of non-independent noise in hyperspectral imaging**

Guangrui Ding,1,4 Chang Liu,2,4 Jiaze Yin,1,4 Xinyan Teng,3,4 Yuying Tan,2,4 Hongjian He,1,4 Haonan Lin,1,4,\* Lei Tian,1,2,4,\* and Ji-Xin Cheng1,2,3,4,5,\*

ACCESSIBLE OVERVIEW Denoising is a fundamental task in optical microscopy. However, it remains a challenge to remove non-independent noise, which commonly appears due to parasite physical processes or imperfect measurement system. To address this issue, we introduce SPEND (self-permutation Noise2Noise denoiser), a self-supervised deep learning framework to remove non-independent noise. SPEND exploits the following physical signal noise correlation principle: real signals exhibit correlations across all domains (such as space, frequency, or time), whereas noise remains uncorrelated in at least one domain. SPEND permutes the data along the axes of minimal noise correlation to generate a replica with decorrelated noise, allowing the network to learn the signals by minimizing the difference between the prediction and those two noisy pairs. We demonstrate the performance of SPEND on hyperspectral-stimulated Raman scattering imaging and hyperspectral mid-infrared photothermal imaging, which achieves high-fidelity chemical imaging of metabolic biomarkers in the fingerprint and silent regions. SPEND is also broadly applicable for removing structured noise in various imaging modalities. Along the direction of pushing the sensitivity limits, techniques like SPEND, which build upon physical understanding of noise statistics rather than assuming ideal conditions, are crucial for uncovering faint physical phenomena otherwise buried in complex backgrounds.

### SUMMARY

Hyperspectral imaging has been widely used for spectral and spatial identification of target molecules, yet it is often contaminated by sophisticated noise. Current denoising methods generally rely on independent and identically distributed noise statistics, showing corrupted performance for non-independent noise removal. Here, we demonstrate SPEND (*s*elf-*pe*rmutation *N*oise2Noise *d*enoiser), a deep learning denoising architecture tailor-made for removing non-independent noise from a single hyperspectral image stack. We utilize hyperspectral stimulated Raman scattering and mid-infrared photothermal microscopy as the testbeds, where the noise is spatially correlated and spectrally varied. Based on single hyperspectral images, SPEND permutates odd and even spectral frames to generate two stacks with identical noise properties and uses the pairs for efficient self-supervised noise-to-noise training. SPEND achieved an 8-fold signal-to-noise improvement without having access to the ground truth data. SPEND enabled accurate mapping of low-concentration biomolecules in both the fingerprint and silent regions, demonstrating its robustness in sophisticated cellular environments.

#### INTRODUCTION

Hyperspectral imaging offers rich spectral and spatial information in complex environments.[1–4](#page-15-0) Advanced vibrational spectroscopic imaging methods, such as stimulated Raman scattering (SRS)[5](#page-15-0) and mid-infrared photothermal (MIP)[6](#page-15-0) microscopy, provide high spatial resolution to resolve overlapped vibrational bands in biological systems. However, for low-concentration molecules, the raw hyperspectral SRS or MIP images are often heavily contaminated by noise, undermining the effectiveness

![](_page_1_Picture_17.jpeg)

<sup>1</sup>Department of Electrical and Computer Engineering, Boston University, Boston, MA 02215, USA

<sup>2</sup>Department of Biomedical Engineering, Boston University, Boston, MA 02215, USA

<sup>3</sup>Department of Chemistry, Boston University, Boston, MA 02215, USA

<sup>4</sup>Photonics Center, Boston University, Boston, MA 02215, USA

<sup>5</sup>Lead contact

<sup>\*</sup>Correspondence: [hnlin@bu.edu](mailto:hnlin@bu.edu) (H.L.), [leitian@bu.edu](mailto:leitian@bu.edu) (L.T.), [jxcheng@bu.edu](mailto:jxcheng@bu.edu) (J.-X.C.) <https://doi.org/10.1016/j.newton.2025.100195>

![](_page_2_Picture_0.jpeg)

![](_page_2_Picture_1.jpeg)

of subsequent spectral segmentation or quantification. Computation-based image denoising presents a viable solution to circumvent these hardware-imposed limitations.[7–10](#page-15-0) Notably, denoising algorithms that do not rely on ground truth are particularly valuable, given the challenges associated with obtaining higher-SNR (signal-to-noise ratio) images.

Model-based hyperspectral denoising algorithms rely on prior knowledge of the targets across the spatial and spectral domains. Harnessing the spectral feature variance difference between signal and noise, principal component analysis (PCA) combined with the 2D spatial and 1D spectral wavelet shrinkage effectively reduces noise in low-energy principal components while preserving important spectral information.[11](#page-15-0) Additionally, spectral total variation incorporates spatial and spectral smoothing constraints to mitigate noise.[12](#page-15-0) 3D non-local mean[s13](#page-15-0) and block-matching and 4D filtering (BM4D)[14](#page-15-0) group the similar pixel blocks together to enhance feature recognition in denoising. Despite these innovations, the performance of model-based denoisers often falls short in low-SNR environments due to the complexity of physical systems and challenges in deriving closed-form expressions.

To overcome these challenges, self-supervised deep learning denoising algorithms have been developed. Leveraging the premise that adjacent pixels follow the same receptive fields, Noise2Void (N2V) and Noise2Self have been developed.[15](#page-15-0),[16](#page-15-0) Noise2Noise (N2N), on the other hand, utilizes pairs of independent low-SNR measurements, treating them as both input and output to directly learn noise statistics and object priors.[17](#page-15-0) Multiple variants of N2V and N2N have been tailored for 3D image stack denoising. For example, DeepInterpolation[18](#page-15-0) voids the central frame entirely, relying on the continuity of adjacent frames for signal interpolation. DeepVI[D19](#page-15-0) further introduces the N2V strategy to enhance spatial signal correlations. Techniques like Noise2Stack[20](#page-15-0) and DeepCAD[21](#page-16-0) construct a pair of identically distributed signal and noise stacks through oddand-even frame splitting, thereby facilitating N2N-based denoising. These state-of-art self-supervised denoising methods have successfully pushed the limits of 3D imaging systems where noise in each frame is statistically independent with an identical mean. However, neither N2N nor N2V is valid for spatially or spectrally correlated noise.

Meanwhile, advanced hyperspectral imaging systems often contend with non-independent noise [\(Figure 1](#page-3-0)A) due to complex signal generation, acquisition, and amplification processes. Multiple pump-probe hyperspectral imaging systems, including the aforementioned SRS and MIP, rely on demodulation of subtle intensity variance. Heterodyne detection, facilitated by a lock-in amplifier (LIA)[,22](#page-16-0) is essential for extracting weak modulation signals. However, the delayed response of the electronic circuit in the low pass filter of LIA, coupled with mismatches of signal generation frequency and extraction frequency, causes information leaking between two adjacent pixels. Besides, perturbation of the sample's local environment leads to a correlation between adjacent measurements. Additionally, spectral absorption variations among samples and inhomogeneous input energy at different wavenumbers contribute to spectral varied noise.

To address these issues, we introduce self-permutation Noise2Noise denoiser (SPEND), a self-supervised learningbased denoiser that operates without explicit noise modeling. SPEND harnesses a stack permutation strategy, where the permutation direction is determined to break the correlation of the noise. After selecting the appropriate axis, the raw stack is split into two substacks, which are then recombined in alternating sequences (odd + even, even + odd). This configuration treats adjacent frames as two independent measurements of the same sample. With the input spatial SNR greater than 9 and spectral SNR greater than 3, our approach enhances the signal-to-noise ratio by more than eight-fold. Moreover, SPEND is compatible with various spectral unmixing tools, including least absolute shrinkage and selection operator (LASSO),[23](#page-16-0) multivariate curve resolution (MCR),[24](#page-16-0) and phasor analysis.[25](#page-16-0) Together, SPEND enables high-fidelity chemical imaging in both the fingerprint window and the silent window.

#### RESULTS

#### Noise in hyperspectral SRS displays spatial correlation and spectral variation

Our study begins with an elucidation of the process for acquiring SRS images. In our SRS system, two pulse trains, pump, and Stokes are collinearly focused on the sample, with the Stokes beam being modulated at 2.4 MHz. After interacting with the sample, the pump power loss occurs at the modulation frequency. After acquiring single-color SRS images, we utilized spectral focusing to generate 3D hyperspectral SRS images [\(Figures 1B](#page-3-0) and [S1\)](#page-15-0). The intensity of the modulation is extracted using an LIA, which functions as a mixer and low-pass filter. Due to the complexity of LIA signal processing, noise in the LIA output is non-independent, as detailed below.

We observed heterogeneous noise statistics along the two spatial axes. As depicted in [Figure 1C](#page-3-0), the noise power spectral density (PSD), which is the Fourier transform of the autocorrelation function of the noise, along the fast and slow axes of the laser scanning differs significantly. The noise PSD along the fast axis shows a notable decreasing trend from lower frequencies to higher frequencies, indicative of a patterned noise behavior. This conflicts with the independent and identical noise condition, which would exhibit identical uniform PSD along both axes, as demonstrated in two-photon fluorescence imaging [\(Figure S2\)](#page-15-0). To delve deeper into the spatial properties, we conducted a Pearson cross-correlation (PCC) analysis of noise among neighboring pixels [\(Figure 1](#page-3-0)D). At a fixed time constant of 70% of pixel dwell time, increasing the scanning speed (i.e., reducing the pixel dwell time) invariably increases the noise correlation level. As suggested in [Figure 1](#page-3-0)E, reducing the time constant does not remove noise correlation. The first order filter of lock-in was used, which is closest to a sharp cut off. Therefore, the system retains a portion of the correlated noise despite changes in the time constant. In addition to photodiode (PD)[26](#page-16-0) detection with a narrowband amplifier, similar correlation using broadband PD was found [\(Figure S3\)](#page-15-0). In addition, PCC is positively correlated with the laser power on the sample. We also found that the fast axis noise correlation is positively related to the Raman intensity [\(Figure S4\)](#page-15-0), suggesting that the stimulated Raman photothermal effect[27](#page-16-0) contributes to the thermal convection-induced correlation. Together, these observations suggest

![](_page_2_Picture_12.jpeg)

![](_page_2_Picture_13.jpeg)

![](_page_2_Picture_14.jpeg)

![](_page_2_Picture_15.jpeg)

![](_page_2_Picture_16.jpeg)

What

![](_page_3_Picture_1.jpeg)

<span id="page-3-0"></span>![](_page_3_Figure_2.jpeg)

**Figure 1. Noise characteristics and analysis of hyperspectral SRS spatial and spectral noise** 

- (A) Zero mean noise (*E*[*n*] = 0) and non-zero mean noise (*E*[*n*]∕= 0) characteristics.
- (B) Illustration of hyperspectral SRS laser scanning process.
- (C) Noise PSD is measured along different axes. The shaded region represents variance.
- (D) Correlation analysis of the noise spatial correlation to pixel dwell time. PCC, Pearson cross-correlation.
- (E) Comparison of noise spatial correlation across different axes under varying power settings.
- (F) Spectral varied noise. Noise and signal intensity distribution via the wavenumber.
- (G) Comparison of Poisson noise with spectrally varied SRS noise.
- (H) Comparison of photothermal convection-induced noise and other noise in the hyperspectral SRS system. The widely studied noise contains laser noise, thermal noise, and Poisson noise. Int.: intensity.
- (I) Physical diagram depicting the generation of photothermal convection induce noise. *ωp*and *ωs*are the frequency of pump and stokes photon.

<span id="page-4-0"></span>![](_page_4_Picture_0.jpeg)

![](_page_4_Picture_1.jpeg)

![](_page_4_Figure_2.jpeg)

the complexity of the underlying physical processes, which frustrates the efforts to experimentally eliminate the spatial noise correlation.

Besides spatial correlation, noise in SRS is spectrally heterogeneous and correlates with signal levels. For SRS spectroscopic imaging, the constant noise hypothesis in the spectral domain no longer holds. Commonly, the well-known 1/f laser noise, detector thermal noise, and Poisson shot noise,[28](#page-16-0) which are identically and independently distributed in the spatial and spectral domains, are widely studied in SRS systems. In addition to these established noises, our investigation revealed a new type of noise that deviates from uniform distribution in a spectral domain. [Figure 1F](#page-3-0) shows the spectral variation of the noise based on hyperspectral SRS of dimethyl sulfoxide (DMSO) solution. This spectrally varied noise is distinct from the Gaussian noise, which has a uniform distribution, or the Poisson noise.[29](#page-16-0) Adjustment to the detector power on the photodiode allows for

#### **Figure 2. SPEND workflow**

(A) Axis selection. Directions of the least correlation axis will be chosen as the permutation axis. (B) Permutation. Upon selecting the axis (i.e., spectral axis *ω*), the data cube is rearranged into two different sequences, which make the training pairs for the next step. Blue slices represent odd frames; red slices represent even frames.

(C and D) Training and prediction phase. In training, the input and result dataset are generated from permutation. In prediction, the input data will maintain the original sequence without additional process. Unet is selected as a neural network model (blue box: maxpooling layer; yellow box: convolution layer; green box: upsampling layer).

fitting the Poisson noise distribution. [Figure 1G](#page-3-0) demonstrates significant discrepancies in the statistical behavior between Raman on-off resonance noise and Poisson noise. These findings indicate that conventional transformations from Poisson to Gaussian noise are ineffective in hyperspectral SRS systems.

We attribute the spectral varied noise to the stimulated Raman photothermal effect[27](#page-16-0) [\(Figures 1](#page-3-0)H and 1I). When the frequency difference of the pump and probe matches the vibrational frequency of chemical bonds, photon emissions occur, leading to Raman gain and loss. Meanwhile, vibrational excitation occurs and is followed by non-radiative decay. This effect heats the local environment and leads to higher thermal fluctuation. The photothermally induced noise performs differently from the white noise, featuring a peak at the Raman resonance. Together, our results highlight the complex nature of noise characteris-

tics in these systems, underscoring the necessity for developing a new denoising framework tailored to these nuanced dynamics. [Figure S5](#page-15-0) and [methods](#page-13-0) section summarize the way to the noise characteristic analysis.

#### SPEND

To remove the spatially correlated and spectrally varied noise in a hyperspectral SRS image, we propose a SPEND framework, depicted schematically in Figure 2. We first select the permutation axis, which is determined based on the noise characteristics along different axes. In Figure 2A, we choose *ω* axis as the permutation direction due to its least correlation.

For self-supervised N2N-based deep learning denoising, the key is to learn the noise statistics and characteristics using two independent measurements of the same field of view (FOV). The purpose of the permutation operation is to create two independent image stacks using only one input image. Besides the **Newton** Article

![](_page_5_Picture_1.jpeg)

general i.i.d. noise part, our images contain strong correlated noise that needs to be separated as independently as possible in the permutation step. Permutation along the less correlated axes (the slow scanning or spectral tuning axes) guarantees the measurement independence.

Furthermore, as a frame-by-frame, point-scanning imaging system, 1/f noise levels along the three axes are different and are proportional to the scanning frequency of the axes. Permutation along the slowest axis could maximize the 1/f contribution during N2N learning.

The variated noise poses additional challenges for single-image N2N methods. Since the underlying assumption is that adjacent frames along the permutation axis follows the same noise statistics and thus can be treated as two independent measurements N2N learning, permuting along the axis (the spectral tuning axis) with the lowest noise level difference could maximize the learning performance (concept illustrated in Figure S6). In contrast, permuting along the correlated axis (the spatial scanning axis) can artificially reduce the noise level because the noise correlation is falsely learned as part of the true signals. This leads to a higher noise level difference, thereby degrading the denoising performance. Considering these factors, we choose the spectral tuning axis (as depicted in Figure 2) in our  $x-y-\omega$  system for permutation to optimize the model's ability to learn all types of noise characteristics in an N2N manner.

To emphasize the importance of choice of the permutation axis, we compared the results of multiple hyperspectral SRS data collection strategies. The Noise correlation properties are decided by scanning modalities. For instance, in the  $\omega-y-x$  scanning modality (Figure S7A), significant noise correlation exists in the spectral domain, suggesting that permutating along the spatial axis yields optimal results (Figure S7C and S7E). Conversely, in the commonly used  $x-y-\omega$  scanning modality (Figure S7B), where spatial noise is more prevalent, permutating along the  $\omega$  axis preserves essential high-frequency noise features for effective denoising (Figures S7D and S7F).

The permutation process is illustrated in Figure 2B, which involves dividing the raw data stack into odd and even slices along the chosen axis. These slices are then alternately concatenated to form the input and target datasets for the training phase, illustrated in Figure 2C. The concatenation sequences provide the fundamental support for N2N, i.e., independent measurements of the same FOV. Through recombination, we can utilize the entire signal and noise information within the input data and deliver an unbiased estimation of noise. For the network architecture, we employ a U-Net structure, <sup>31</sup> detailed in Figure S8. During the training phase, the two concatenated stacks generated from the permutation step are used as the input and target of the neural network. During the prediction phase (Figure 2D), the input data ARE fed into the model in its original sequence, maintaining the continuity and integrity of the spectral and spatial information.

To demonstrate the broad applicability of SPEND, we integrate it with several published chemical unmixing methods, including Phasor, LASSO, and MCR. In Figure S9, we illustrate the typical process of chemical unmixing with and without reference spectra, showcasing SPEND's ability to enhance the signal-to-noise ratio (SNR) significantly. This enhancement en-

ables more reliable chemical unmixing, providing deeper insights into biological systems. Subsequently, we use chemical unmixing to provide comprehensive compositional information from the hyperspectral SRS stacks. Here, we demonstrate the whole process and compare the results of different permutation strategies for comprehensive study, shown in Figure S10 and Video S1. Figure S10A demonstrates that spatial permutation significantly reduces noise, although it may blur some features, suggesting potential improvements through expanded training datasets or oversampling in the spatial domain during imaging. Figure S10B shows the impact of permutation choice on chemical unmixing results, emphasizing the importance of appropriate axis selection. By optimizing the selection, although the spatial information is blurred, the spectral resolution is maintained, allowing us to achieve good unmixing results. Figure S10C calculates the spectral error of different permutation strategies. Figure S10D shows the correlation level of each axis. The correlation along the spatial axis is lower than that along the spectral axis. Hence, permutation along the spatial axis is preferred. Wrong permutation strategies will impair the performance of the denoiser, Figures S10E and S10F demonstrate the improvement comparison between the spectral domain and the spatial domain. The mean intensity value and standard deviations are also provided.

## Validation of SPEND's performance in the spectral and spatial domains

The validation of SPEND's efficacy in enhancing hyperspectral SRS image quality is crucial, particularly as this self-supervised denoiser aims to improve sensitivity in label-free chemical imaging modalities that lack ground truth data. The SNR in SRS imaging, which is proportional to the product of the intensity of the Stokes beam and the square root of the intensity of the pump beam  $SNR \propto I_{stokes} \sqrt{I_{pump}}$ , serves as a fundamental indicator of image quality.<sup>32</sup> To quantitatively evaluate SPEND's performance, we manipulated the intensity of the Stokes beam and pixel dwell time to create a testing set. By increasing the average power of both beams, we can create high SNR references. Conversely, by decreasing the power, we achieve low SNR images as the testing set to be denoised. After denoising, the noise can be reduced 8.5 times, while the signal remains same level. Consequently, the SNR can be increased by approximately 8.5 times. We employ the structural similarity index (SSIM), peak SNR (PSNR), Fourier ring correlation<sup>33</sup> (FRC), and Fréchet distance<sup>34</sup> as metrics to gauge the spatial and spectral performance.

The low laser power group and denoised single-color SRS images are presented in Figure 3A. The performance of SPEND is benchmarked against that of BM4D, a golden standard denoising algorithm. Chemical unmixing was pursued (in Figure 3B) using LASSO, with references shown in Figure S11, alongside their unmixed hyperspectral SRS counterparts for lipid, cholesterol, and protein channels. We further recorded an image of the same sample at high laser power as a reference to validate the accuracy. Figure S12 shows the high SNR group and its unmixing result, which are used as the reference to calculate the spectrum error and SSIM. The spectral error was evaluated by calculating the Fréchet distance based on the single-pixel spectrum

<span id="page-6-0"></span>![](_page_6_Picture_0.jpeg)

![](_page_6_Figure_2.jpeg)

**Figure 3. Spatial and spectral fidelity analysis of SPEND. SPEND is compared with BM4D. Using maximum power to generate high SNR reference to validate denoising result** 

- (A) Single-color SRS of OVCAR5 cancer cell taken at 2935.2 cm<sup>−</sup> <sup>1</sup> .
- (B) Chemical unmixing map. The hyperspectral SRS data stacks are divided into three chemical channels, including lipid, cholesterol, and protein.
- (C) Spectrum error respectively. The value indicates the difference compared with the ground truth dataset.
- (D and E) SSIM and PSNR analysis of each chemical channel. The error bars represent the variance of SSIM and PSNR.
- (F) Pinpoint small ROI.
- (G) Dashed line intensity plot.
- (H) Resolution calibration by FRC. Dashed line, 1/7; low power, 612 nm; BM4D, 575 nm; SPEND, 406 nm; high power, 414 nm.

(Figures 3C; [S13](#page-15-0) and [methods\)](#page-13-0). SPEND exhibited less spectral distortion compared with both BM4D and low power data. In Figures 3D and 3E, SSIM and PSNR are conducted on each chemical channel evaluating the spectral and spatial performance of SPEND. SPEND shows better performance over BM4D. In Figures 3F and 3G, A line in the region of interest Article

![](_page_7_Picture_1.jpeg)

(ROI) is highlighted. There are no discernible features in the low power and BM4D groups. However, after applying SPEND, the 1-*μm* diameter spot at the 2-*μm* position can be identified. Next, we quantified the resolution by FRC. FRC provides a measure of the consistency of the spatial frequency information. As shown in [Figure 3](#page-6-0)H, the resolution achieved by SPEND approached 400 nm, which closely matches that of the high laser power group and significantly surpasses the approximately 600 nm resolution in the low laser power and BM4D groups. Linear relationship between the SRS intensity and the molecule concentration are well maintained after denoising [\(Figure S14\)](#page-15-0). Overall, SPEND outperforms BM4D in SNR and spatial resolution improvement.

The denoising performance depends on both the SNR of input images and the complexity of the structure being analyzed, which represents one of the most structurally complex scenarios in biomedical imaging. Based on our validation dataset, SPEND is effective when the input spatial SNR of the Raman on-resonance is greater than 9. For spectral SNR, the requirement is lower due to spatial continuity aiding spectral domain reconstruction. We find that SNR ≈3 is typically sufficient. If the target structure is less intricate than cellular data (e.g., fungal structures, pure chemical distributions), the minimum required SNR can be lower. The minimum SNR threshold for successful denoising is spatial SNR >3 and spectral SNR >1.

#### SPEND enables high-fidelity SRS imaging in the fingerprint region

The spectrally crowded SRS signals in the carbon-hydrogen (C-H) stretching vibration region (2800–3100 cm<sup>−</sup> <sup>1</sup> ), where strong Raman bands reside, have limited chemical specificity in a complex biological environment. Instead, fingerprint SRS offers a significant advantage in enhancing specificity by providing distinct Raman peaks for each biological component. Major chemicals such as protein, fatty acid, and cholesterol can be distinguished in this region, shown in [Figure 4](#page-8-0)A. However, the fingerprint region presents challenges due to the inherently weak Raman cross-sections, which tend to reduce the SNR, posing difficulties for chemical analysis.

As shown in [Figure 4](#page-8-0)B and [Video S2,](#page-15-0) applying SPEND to a hyperspectral SRS image stack significantly enhances the SNR within the fingerprint window. The input SNR is 15, higher than the input SNR limitation, meaning that the denoised results are reliable for further analysis. A representative single-frame image illustrates the enhancement in [Figure S15](#page-15-0)A, which provides a detailed comparison of spectral noise reduction in regions enriched with fatty acids, cholesterol, and proteins ([Figures S15](#page-15-0)B– S15D). The co-plotted spectra further highlight SPEND's ability to reduce spectral noise.

To validate the improvement and robustness, we cross-reference the results with the C-H region. MCR [\(methods\)](#page-13-0) is a well-established method to unmix chemical distribution within the hyperspectral stacks, which effectively retrieves chemical spectra in the cellular environment, allowing for robustness analysis by comparing the differences between reference from standard sample and retrieved spectra. We perform MCR on raw fingerprint data, SPEND-processed data, and the C-H region, as displayed in [Figure 4C](#page-8-0). To quantify the similarity between the unmixing results of the fingerprint and C-H regions, we use SSIM [\(Figure 4D](#page-8-0)). In raw data, separating the fatty acid, cholesterol, and protein components is challenging due to the highlevel noise, which contaminates the fatty acid and protein channels. The boxplot SSIM analysis shows values close to zero for raw fingerprint data, indicating minimal similarity with the high-SNR C-H data. However, after denoising with SPEND, the chemical components become distinctly separable, and the high SSIM values confirm strong similarity between fingerprint and C-H chemical maps.

Despite these improvements, some differences between the unmixing results of the fingerprint and C-H regions persist, as indicated by arrows in [Figure 4C](#page-8-0). Notably, in the C-H unmixing results, diffused cholesterol appears as concentrated dots, suggesting crosstalk among chemical components. To assess the accuracy of unmixing, we compare the global difference between retrieved spectra from MCR with pure chemical spectra [\(Figure 4E](#page-8-0)). MCR requires an initial input of the spectral references and can update the spectral references in the results. Here, the data are a known system, namely, the species of chemical components is known. In this case, the input spectral references can be treated as the ground truth. The difference between the input and output spectral references can therefore be a quantitative metric on the fidelity of the denoised hyperspectral image along the spectral axis.

Based on [Figure 4E](#page-8-0), we observe that the global difference between the input (reference) and output (MCR-retrieved) spectrum in the C-H region is higher than that in the fingerprint region after denoising. This suggests that the chemical unmixing process in the C-H region is not as stable as that in the denoised fingerprint region. This is due to the dense clustering of chemical peaks in the C-H region, where many biomolecules exhibit strong C-H and O-H vibration bands[.35–38](#page-16-0) The whole process demonstrates that SPEND enables high-fidelity chemical imaging in the fingerprint region.

A minor shoulder appears around 1600 cm<sup>−</sup> 1 in [Figure S15.](#page-15-0) For the fatty acid-rich ROI, the 1600 cm<sup>−</sup> 1 peak is significantly stronger than a shoulder peak in protein and therefore should be contributed by some other metabolites. Further analysis revealed that this peak aligns with retinyl ester,[39](#page-16-0) a storage form of vitamin A commonly found within intracellular lipid droplets. To confirm this, we performed the peak fitting analysis [\(Figure S16](#page-15-0)), which showed an FWHM of around 20 cm<sup>−</sup> <sup>1</sup> , consistent with literature reported value of retinyl ester. Additionally, chemical unmixing map [\(Figure S17](#page-15-0)) demonstrated that retinyl ester is localized in the lipid droplets, which match with the physiological distributions. This further supports its presence as a real spectral feature rather than artifacts.

Further comparisons in [Figure S18](#page-15-0) reveal that in the fingerprint region, MCR preserves the spectral peaks of each component at their original wavenumbers. In contrast, in the C-H region, the spectral shapes of fatty acids and cholesterol are notably distorted. The fatty acid peak around 2850 cm<sup>−</sup> 1 and the cholesterol peak around 2860 cm<sup>−</sup> 1 are buried in the background noise.

Overall, applying SPEND in the fingerprint region effectively mitigates the weak signal issue and enhances the chemical unmixing accuracy, making it a valuable tool for hyperspectral SRS imaging.

<span id="page-8-0"></span>![](_page_8_Picture_0.jpeg)

![](_page_8_Figure_2.jpeg)

**Figure 4. SPEND enables high-fidelity SRS imaging in the fingerprint window** 

- (A) SRS spectra of fatty acid, cholesterol, and protein in the fingerprint and C-H vibration regions, respectively. Spectra in the fingerprint region are magnified by 10 times for clarity. The references are also used for MCR unmixing.
- (B) Single-color SRS imaging of U87 cell in the fingerprint region at 1649 cm<sup>−</sup> 1 and the C-H region at 2936 cm<sup>−</sup> <sup>1</sup> .
- (C) Chemical map unmixing result. SRS data were divided into three channels, including lipid, cholesterol, and protein. We cross-validate with the unmixing result from both the fingerprint and C-H regions.
- (D) SSIM boxplot of SPEND in the denoising fingerprint hyperspectral SRS dataset. Error bars represent the SSIM variance.
- (E) Difference between the retrieved spectra after MCR and the input chemical spectra from pure chemicals. Error bars represent the variance of the retrieved difference. Raw data were published.[23](#page-16-0)

Article

![](_page_9_Picture_1.jpeg)

#### SPEND enables high-fidelity SRS imaging of lowconcentration molecules in the silent window

SRS has been extensively used for click-free imaging of alkynetagged small molecules in the silent window[.40](#page-16-0) For example, homopropargylglycine (HPG), as a biorthogonal precursor, is widely used to study protein synthesis via click chemistry.[41,42](#page-16-0) In click chemistry, a copper-catalyzed azide-alkyne cycloaddition reaction is used to link HPG to fluorescent dyes or affinity tags for the visualization of protein synthesis.[43](#page-16-0) However, this type of reaction prohibits live cell imaging due to the cell fixation requirement.

HPG exhibits a Raman peak at around 2125 cm<sup>−</sup> <sup>1</sup> , which enables SRS visualization of protein synthesis in live cells in a clickfree manner.[44](#page-16-0) While previous single-color SRS can visualize concentrated HPG, it remains difficult to provide quantitative HPG distribution due to the cross-phase modulation background[.44](#page-16-0) In addition, the low SNR prevents unmixing to quantitatively isolate the HPG signals and the background. Here, we show that SPEND and subsequent unmixing can overcome the SNR issue and enable accurate mapping of HPG distribution inside a cell.

By applying SPEND, we markedly improved the fidelity of SRS images within the silent region ([Video S3\)](#page-15-0). To facilitate quantitative chemical unmixing, the accurate reference spectra for each component, including HPG and XPM, are essential. We derived the HPG spectrum from the hyperspectral SRS of a pure HPG solution. Next, we used spectral phasor analysis to obtain other references for unmixing [\(Figures 5A](#page-10-0)–5F). Phasor analysis identified three distinct clusters, representing HPG, XPM in the cell body, and XPM in lipids. We found that the alkyne signals were absent in lipids and were distributed in the non-lipid cytoplasm, indicating that after treatment, newly synthesized protein was distributed throughout the cell. The clarity is significantly enhanced in both HPG-treated and control samples, confirming the robustness of SPEND. [Figure S19](#page-15-0) showcases the noise reduction effect by plotting the spectrum from selected ROIs, confirming the suppression of frame-toframe noise across all pixels. Using asymmetrically reweighted penalized least squares (arPLS),[45](#page-16-0) we extract the HPG peak for each ROI ([methods](#page-13-0)). Without SPEND, extracting such peaks was unfeasible in such regions due to the variable XPM spectrum among samples. Surprisingly, XPM for each component within the cell was found to be different, leading to uncertainty in traditional chemical unmixing methods. The clarity required for unmixing was unachievable with raw data, underscoring SPEND's efficacy in distinguishing these components. Phasor-retrieved spectrum served as references for LASSO unmixing, detailed in [Figure S20](#page-15-0).

Through SPEND and unmixing, we differentiated major components in the hyperspectral SRS stack, including HPG, XPM of lipids, and cell bodies [\(Figures 5G](#page-10-0) and 5H). Frame-to-frame variation analysis revealed substantial noise reduction in both HPG-treated and control groups [\(Figure 5](#page-10-0)I). In [Figure 5J](#page-10-0), we calculate the HPG intensity of 12 cells to confirm the stability of this method. In the HPG-treated group, the intensity in the HPG channel is significantly higher than that in the control group, with a *p* value of 1.58e− 7, affirming the effectiveness of SPEND.

#### SPEND enables high-fidelity hyperspectral MIP imaging in the fingerprint region

Besides the SRS modality, MIP imaging[46–49](#page-16-0) is another potent tool for revealing chemical distribution in a label-free manner. [Figure 6](#page-11-0) showcases the complex noise distribution in an MIP syste[m50](#page-16-0) and demonstrates the improvements that SPEND brings to a hyperspectral MIP dataset. [Figure 6](#page-11-0)A illustrates the physical concept of MIP, where a mid-infrared beam excites the chemical bonds and arouses temperature in the sample. This heat alters the refractive index, affecting the redistribution of the visible probe beam intensity, which can be used to generate chemical maps. [Figure S21](#page-15-0) shows the diagram of an MIP microscope.

One key criterion for assessing the correlation strength is the cut-off frequency of the noise PSD. We analyzed noise correlation in MIP images of PMMA beads in [Figure 6](#page-11-0)B. For the two scanning axes, we identified the cut-off spatial frequencies, after which the noise PSD remains constant. The cut-off frequency for the fast axis is higher than that for the slow axis, indicating the non-independent nature of noise along the fast-scanning axis in MIP microscopy. Further, 2D noise PSD is shown in [Figure S22](#page-15-0). The noise exhibits similar properties compared with the SRS modalities, showing that conventional denoising methods are not applicable to MIP images. Compared with SRS [\(Figures 1C](#page-3-0) and [S2C](#page-15-0)), we observed less correlation in an MIP system, likely because the pixel dwell time of 10 μs in MIP is longer than that of 1 μs in SRS. [Figure 6](#page-11-0)C shows noise spectral variation, supporting the universality of spectrally varied noise across all pump-probe imaging modalities and underscoring the necessity of our method.

Next, we demonstrate SPEND's effectiveness for MIP images taken in the fingerprint region. In [Figure 6](#page-11-0)D and [Video S4,](#page-15-0) SNR improvements in the hyperspectral MIP image of *Candida albicans* fungal cells in the fingerprint region are displayed. After SPEND, the SNR improved by 13 times. Three single wavenumbers from the hyperspectral MIP data stack are presented, including 952 cm<sup>−</sup> <sup>1</sup> , 1070 cm<sup>−</sup> <sup>1</sup> , and 1162cm<sup>−</sup> <sup>1</sup> . The first two wavenumbers correspond to the O-H and C-O bond in carbohydrates, crucial fungal cell wall components. The concentrations of O-H and C-O are different. O-H band originated from polygalacturonase acid, commonly found in the plant cell wall,[51](#page-16-0) and is less common in the fungal cell wall. In the raw data, it is hard to distinguish individual fungal cells due to the low SNR. After SPEND, the differential distribution of O-H and C-O becomes clear. 1162 cm<sup>−</sup> 1 corresponds to the C-O bond in lipids. After SPEND, several lipid droplets can be resolved. Temporal color encoding is then employed to show the three-layer structure of the cell wall [\(Figures 6E](#page-11-0) and 6F). In the raw data, the low SNR obscured continuous layer structures. However, after denoising, the structure delineation appears smoother and more distinct. Due to the insufficient resolution in MIP, the distinctive threelayer structure is not achievable. However, the high chemical selectivity and spectral discrimination help to reveal these structures in the hyperspectral images. The intensity cross-section plot is shown in [Figure S23.](#page-15-0) The spectrum is shown in [Figure 6](#page-11-0)G, further validating the accuracy along the spectral dimension. In summary, SPEND significantly enhances SNR in

<span id="page-10-0"></span>![](_page_10_Picture_0.jpeg)

![](_page_10_Picture_1.jpeg)

![](_page_10_Figure_2.jpeg)

**Figure 5. Quantitative HPG mapping via hyperspectral SRS and SPEND in the silent window** 

(A–C) Phasor analysis of raw HPG-treated SJSA-1 cell.

(D–F) Phasor analysis of HPG-treated SJSA-1 cell after SPEND denoising. Three clusters show up in spectral phasor after denoising. Avg, average; Seg, segmentation.

- (G) HPG-treated group LASSO unmixing result.
- (H) Control group LASSO unmixing result.
- (I) Frame-to-frame noise reduction analysis.
- (J) Statistical analysis of HPG intensity in treated and control groups. Error bars represent the variance of the HPG intensity. *p* = 1.58e-7 < 0.005. \*\*\*\* means extremely significant.

![](_page_11_Picture_1.jpeg)

<span id="page-11-0"></span>![](_page_11_Figure_2.jpeg)

**Figure 6. SPEND performance for hyperspectral MIP imaging** 

(A) MIP diagram. Pulsed mid-infrared pulses are used to excite molecules to the vibrational state. Non-radioactive decay in the process leads to temperature rise in the local environment. The continuous visible probe beam is used to detect the thermal effect.

- (B) Noise PSD along different axes. The shaded region represents variance.
- (C) Noise spectral variation in MIP. Noise in oil is imaged in the fingerprint region.
- (D) Hyperspectral MIP image of fungal cells in the fingerprint region and the SPEND result at 952 cm<sup>−</sup> <sup>1</sup> , 1070 cm<sup>−</sup> <sup>1</sup> , and 1162 cm<sup>−</sup> <sup>1</sup> .
- (E) Temporal color-coding result.
- (F) Zoom-in image of three-layer fungal wall structures. I, inner; M, middle; O, outer.
- (G) MIP spectrum of each layer. Raw data were published.[50](#page-16-0)

![](_page_12_Picture_0.jpeg)

![](_page_12_Picture_1.jpeg)

MIP imaging within the fingerprint region, enabling clearer differentiation and visualization of complex biochemical structures.

#### Broad applicability of SPEND

SPEND offers a broadly applicable solution for denoising nonzero mean noise in high-dimensional datasets [\(Figure 1A](#page-3-0)). Non-zero mean is prevalent across various imaging modalities and, in our case, manifests primarily as correlation and variation. Besides, non-zero mean noise can originate from structure noise by uneven gain of the detector or electronics turbulence ([Figure S24A](#page-15-0)), striping noise caused by non-uniform illumination or sample scattering ([Figure S24](#page-15-0)B), or reconstruction artifacts in computational imaging caused by model mismatch.[52](#page-16-0) To demonstrate the effectiveness of SPEND, we tested its performance on structure noise ([Figure S25](#page-15-0)A) and striping noise ([Figure S25](#page-15-0)B). The same datasets were proceeded with two common self-supervised denoisers, BM4D and N2V. Moreover, SPEND can achieve similar performance compared with the supervised denoising strategy [\(Figure S26\)](#page-15-0). Since the noise statistics violate the mathematical assumptions of the conventional denoiser, the artifacts are significant. In comparison, SPEND does not require noise modeling, and all the noise statistics are directly learned via permutation and N2N training. As a result, SPEND effectively suppresses artifacts while preserving structural integrity. The source data and code are from public datasets (data availability).

Additionally, SPEND can boost the denoising efficiency for non-identical, shot noise-limited 3D dataset, i.e., volumetric imaging or fluorescence lifetime imaging. In these cases, due to scattering of the incident beam or relaxation of the fluorophore, the shot noise is not identically distributed along the third dimension (depth axis or spectral axis), as shown in [Figure S24](#page-15-0)C. Existing self-supervised denoisers (e.g., BM4D and N2V) suffer from SNR mismatch. To address this, SPEND applies permutation along the highest fluctuation axis, ensuring that the input and target datasets maintain identical noise statistics, thereby resolving the SNR mismatch issues. Here, we take the FLIM dataset as an example ([Figure S25C](#page-15-0)). BM4D fails to handle regions with varying noise levels, leading to over-smoothing in low-noise areas and insufficient denoising in high-noise areas. N2V struggles with anisotropic noise in high-dimensional data, producing noticeable artifacts in central regions. Both SSIM and PSNR demonstrate the preferable performance of SPEND.

In summary, non-zero mean noise and non-identical zero mean noise are widespread across imaging modalities and often compromise the performance of conventional denoiser such as BM4D and N2V. SPEND provides a robust solution for handling complex noise distributions, reducing artifacts and improving overall denoising performance, making it well suited for highdimensional imaging applications.

#### DISCUSSION

Denoising is essential to improve sensitivity across all kinds of microscopy. In this work, based on hyperspectral SRS microscopy and MIP microscopy, we provide an in-depth analysis of the sophisticated noise distribution. Spatially, noise correlation arises from signal leakage in the LIA and perturbation diffusion in the sample, predominantly along the fast-scanning axis. An effective way to reduce this correlation is by increasing the pixel dwell time, though this concurrently reduces scanning speed. The heat accumulation may contribute to the correlation as well, thus corrupting the effect of longer pixel dwell time. Spectrally, the on-off resonance status induces noise variation nearly proportional to the SRS signal intensity.

To mitigate the complicated noise issues, we developed SPEND, a self-supervised framework. We demonstrate the necessity of permutation to improve the accuracy and efficiency. SPEND enhances the sensitivity by up to eight times and proves compatibility with various chemical unmixing tools, thus facilitating high-fidelity SRS and MIP imaging in both the fingerprint and silent regions. In the fingerprint region, SPEND enables quantitative analysis of lipids, proteins, and cholesterol, which are hard to distinguish in the CH region. By suppressing spectral noise and enhancing the precision of chemical channel separation, SPEND refines chemical unmixing in the fingerprint region, even in the absence of high SNR reference. In the silent region, SPEND enables quantitative distribution analysis of HPG, which cannot be accomplished by single-color SRS. Furthermore, the application of SPEND to MIP microscopy demonstrates its versatility across other kinds of imaging modalities. Compared with SRS imaging modalities, MIP is more sensitive in the fingerprint region benefiting from the large infrared absorption crosssection. SPEND further boosts the performance enabling better SNR of MIP images.

Beyond SRS and MIP imaging, SPEND has the potential to assist other lock-in-based 3D imaging modalities that suffer from complex noise challenges. Techniques like stimulated Raman photothermal microscopy,[27](#page-16-0) Brillouin scattering microscopy[,53](#page-16-0) and transient absorption microscopy,[54](#page-16-0) which encounter similar sophisticated noise issues, could benefit from the improved SNR without necessitating additional hardware expenses. Moreover, the application of SPEND extends beyond hyperspectral imaging; it could also enhance SNR in videos ([Figure S27](#page-15-0)), providing a convenient solution to suppress noise issues in dynamic imaging scenarios. Different imaging systems exhibit distinct noise characteristics, which can significantly impact the performance of deep-learning-based denoisers. Integrating prior knowledge of noise statistics into deep learning models can enhance denoising effectiveness by enabling more accurate noise modeling and adaptive filtering. By incorporating system-specific noise priors, deep-learning denoisers can achieve improved generalization and robustness across various imaging modalities.

While SPEND demonstrates robust denoising capabilities, it is also possible to encounter misfitting problems. These challenges can be addressed by expanding the training dataset's size and complexity, which helps refine the model's accuracy and generalizability. However, achieving the independent measurements required by the N2N framework poses specific demands on data acquisition strategies in both spatial and spectral domains. To optimize the effectiveness of SPEND, we recommend adhering to the Nyquist sampling rate during data acquisition, where the spatial step size should be half the resolution, which should be tailored according to the specific features of interest in the post-denoising analysis. Thus, a strategic approach

## <span id="page-13-0"></span>**Newton** Article

![](_page_13_Picture_1.jpeg)

to data acquisition is crucial to fully leverage SPEND's denoising capabilities and ensure high-quality imaging outcomes.

Due to the complexity and variability of noise in real-world imaging scenarios, developing a universal denoising algorithm that achieves optimal performance across all imaging modalities remains a challenge. SPEND serves as an example of how denoiser models can be tailored to specific imaging modalities by leveraging system-specific noise characteristics, demonstrating the advantages of customized denoising strategies over generic approaches.

#### **METHODS**

#### **SRS** microscope

A lab-built hSRS microscope (Figure S1), previously reported,<sup>55</sup> is used to perform hyperspectral SRS imaging. A femtosecond pulse laser (Insight, DeepSee+, spectra-Physics) operating at 80 MHz with two synchronized beams, a tunable pump beam ranging from 680 nm to 1,300 nm and a fixed Stokes beam at 1,040 nm is used. The pump beam is tuned to 800 nm for the C-H region, 852 nm for the CC triple bond in the silent region, and 890 nm for the fingerprint region. The Stokes beam is modulated at 2.5 MHz by an acoustic optical modulator (1205-C, Isomet) and chirped by a 15-cm glass rod (SF57, Schott) before merging the two beams. The combined two beams were chirped by five glass rods to picosecond pulse. A motorized linear stage is used to tune the time delay between the pump and Stokes pulse, which corresponds to the Raman shift of chemical bonds. A 2D Galvo scanner (GVS102, Thorlabs) is used for laser scanning. The combined beam is sent to the sample through a  $60\times$ water immersion objective (NA = 1.2, UPlanApo/IR, Olympus). After interacting with the sample, the beam is collected by an oil condenser (NA = 1.4, U-AAC, Olympus). A photodiode (S3994-01, Hamamatsu) is used to collect signals after filtering the Stokes beam. The LIA (UHFLI, Zurich Instruments) is used to extract high-frequency signals.

#### **Power settings**

For DMSO imaging, the pump power is set at 30 mW, and the Stokes power is set at 50 mW. The IR power for MIP bead imaging is set in the range of 10 mW to 30 mW, due to the uneven laser profile. The visible probe beam is set at 50 mW. The power settings for other public dataset can be found in the original papers.

#### Spectral and spatial analysis of noise

The evaluation of noise property was performed in Figure S3. To simplify the process, we conducted all analyses on pure chemical samples. For analyzing spectral variation, we measured standard deviation within a small area to quantify the noise level. Then, the average intensity of the same area was calculated to represent the signal level. We then plotted the relationship between noise and signal to elucidate their dependency. Spatial correlation analysis was conducted using videos of pure chemical samples. Due to objective drift issues, we used the average intensity to represent the signal. The individual frame was then subtracted from this average to isolate the noise distribution. PCC analysis was then performed between adjacent rows or columns to assess the spatial correlation of noise.

#### **Training and interference**

To enhance the robustness of our model, we implemented data augmentation such as flipping and rotating at 180°. This was done to avoid distorting the inherent noise patterns, which are non-uniformly distributed. Such a cautious approach is essential as traditional data augmentation methods can potentially exacerbate noise issues if not aligned with the noise structures. This augmentation ensures that the integrity of the augmented datasets is maintained, accurately reflecting the characteristics of the original data.

After augmentation, the size of the training set increased four-fold. The training set comprised 24 stacks, with 10% for validation and 90% for training. Each stack contains  $400 \times 400$  pixels and 100 frames. We employed a four-layer Unet architecture based on the CSBDeep framework. The training was conducted on a commercial graphics processing unit (GPU, RTX 4090, Nvidia), taking 2 h to complete. For interference, it will take 14 s to denoise an entire image stack.

#### **Chemical unmixing**

In this paper, we utilized three established methods for chemical unmixing, MCR, LASSO, and phasor. The dimensions of the hyperspectral data, x, y, and  $\lambda$ , dissected as  $N_x$ ,  $N_y$ , and  $N_\lambda$ , respectively.

For spectral phasor analysis, we interpreted the spectrum of each pixel through the discrete Fourier transform of first-order harmonics. This analysis was facilitated by scattering the pixels of the entire image across the complex plane, allowing us to identify specific clusters representing target chemical channels. The phasor was performed by the ImageJ plugin (Spechron Phasor)

For MCR and LASSO, we first reshape the 3D hyperspectral stack into a 2D matrix ( $D \in R^{N_x N_y \times N_z}$ ) by arranging the pixels in the raster order. Assuming that the number of interested chemical channels is K, a model is used to decompose the data matrix into the multiplication of concentration maps  $C \in R^{N_x N_y \times K}$  and spectral profiles of pure chemicals  $S \in R^{K \times N_z}$ :

$$D = CS^T + E$$
, (Equation 1)

where E is the error. MCR-ALS is an algorithm that solves the bilinear model using a constrained alternating least-squares algorithm, which improves the interpretability of the profile in both C and  $S^T$ . In LASSO, we add an L1-norm regularization to each row of the concentration matrix and solve the original inverse problem in a row-by-row manner through LASSO regression:

$$\widehat{C_{i,:}} = argmin_{C_{i,:} \ge 0} \left\{ \frac{1}{2} ||D_{i,:} - C_{i,:}S^{T}||_{2}^{2} + \lambda ||C_{i,:}||_{1} \right\},$$
(Equation 2)

where  $C_{i::}$  is a k-element non-negative vector representing the  $i_{th}$  row of the concentration matrix,  $\widehat{C_{i::}}$  is the output of LASSO regression,  $D_{i::}$  is the  $i_{th}$  row of the data matrix, and  $\lambda$  is the hyperparameter that tunes the level of sparsity. MCR was

![](_page_14_Picture_0.jpeg)

![](_page_14_Picture_1.jpeg)

implemented by a Python library, pyMCR. LASSO was achieved by a GitHub project (github.com/buchenglab/LASSO-spectral-unmixing).

#### Quantitation of spectrum distortion

We employed the Fréchet distance of the input spectrum and reference spectrum to quantify spectrum distortion in a pixel, shown in Figure S10A. In mathematics, the Fréchet distance measures the similarity between two curves by calculating the minimum distance of each point. Let A and B be two curves represented by continuous functions  $a:[0,1] \rightarrow R^n$  and  $b:[0,1] \rightarrow R^n$ , where  $R^n$  is an n-dimensional Euclidian space. The Fréchet distance between A and B is given by  $d_F(A, B) = \inf_{\alpha,\beta t \in [0,1]} \|a(\alpha(t)) - b(\beta(t))\|$ , where  $\alpha$  and  $\beta$  range over all continuous functions.

uous, non-decreasing surjective functions from [0,1] to [0,1], ensuring that both curves are traversed from start to finish. The norm  $\|\ \|$  typically represents the Euclidean distance between points on the two curves.

In the spectrum distortion part, we calculate the Fréchet distance of each pixel. Figures S10B and S10C show an example of calculating spectral distortion. Parallel computing was used to improve time consumption.

#### **Spatial resolution calibration**

We use Fourier ring correlation<sup>33</sup> to benchmark the resolution and by accounting for both the PSF and SNR of the image. It can calculate the normalized cross-correlation between the Fourier image pairs (input and reference) at different spatial frequencies and find the cut-off spatial frequency as the cross-correlation reduces to 1/7.

## Asymmetrically reweighted penalized least squares smoothing for peak extraction

The arPLS is a numerical method for baseline correction. With a high tolerance of noise in the input spectrum, it performs well to remove the cross-phase background in hyperspectral SRS data. Assuming x is the input signal vector and z is the underlining background, z must keep the trend of x with smoothness, expressed by the regularized least-square function:

$$R(z) = (x - z)^{T} (x - z) + \lambda z^{T} D^{T} Dz,$$
 (Equation 3)

where D is the difference matrix. Putting weights term in Equation 3, it was modified into a penalized least-square function:

$$P(z) = (x - z)^{T}W(x - z) + \lambda z^{T}D^{T}Dz$$
 (Equation 4)

Pushing the partial derivative  $\frac{\partial P}{\partial z^T}=0$ , the result of z can be expressed as

$$z = (W + \lambda D^T D)^{-1} Wx$$
 (Equation 5)

The PLS algorithm changes weights iteratively, comparing each estimated baseline  $z_i$  and signal  $x_i$ . To eliminate noise interference, in arPLS algorithms, the asymmetric weighting mechanism was incorporated by a logic function:

$$w_i = \begin{cases} logistic(d_i, m, \sigma) = \frac{1}{\frac{2(d_i - (-m+2\sigma))}{\sigma}}, x_i > z_i \\ 1 + e & \sigma \end{cases},$$

$$1 \cdot x_i < z_i$$

(Equation 6)

where  $d_i = x_i - z_i$  and  $m, \sigma$  are the mean and standard deviation of the negative d region. The algorithm iterates until convergence, that is, when it reaches the maximum number of iterations or weights change smaller than  $\frac{|w_t - w_{t+1}|}{|w_t|} < r$ , where r is the ratio parameter, and  $w_t$  and  $w_{t+1}$  are weights at t and t+1 iteration.

#### Sample preparation

#### **OVCAR5** cells

OVCAR5 cells were cultured in the PRMI 1640 medium supplemented with 2 mM L-glutamine, 10% fetal bovine serum (FBS; v/v), and 1% penicillin/streptomycin (P/S; v/v). Then, they were cultured at  $37^{\circ}$ C in a humidified incubator with 5% CO<sub>2</sub> supply.

#### **U87** cancer cells

After seeding the U87 cells in a 35-mm glass-bottom dish overnight, the original culture medium was replaced with media containing PhDY-Chol. Cells were incubated within the medium that contains analogs at a concentration of 20  $\mu$ M for 48 h. Cells were fixed with 10% neutral buffered formalin for 30 min and then washed with phosphate-buffered saline (PBS) three times.

#### **HPG-treated SJSA-1 cancer cells**

SJSA-1 cells were cultured in RPMI-1640 medium, supplemented with 10% (v/v) FBS and 1% (v/v) P/S.

HPG-treated cells were incubated with methionine-deficient medium with 2 mM HPG supplied in the medium for 24 h, and the HPG Ctrl group were incubated in a methionine-deficient medium only.

All the cells were cultured in a humidified incubator with  $37^{\circ}$ C and 5% CO<sub>2</sub> supply. Finally, all the cells were fixed with 10% neutral-buffered formalin for 30 min, followed by PBS washes before microscopic imaging.

#### C. albicans fungal cells

C. albicans isolates were cultured using yeast extract peptone dextrose medium. The culture was incubated overnight at 37°C with continuous shaking at 250 revolutions per minute. Following incubation, a 500- $\mu$ L suspension of Candida was centrifuged, and the pellet obtained was washed three times with PBS to remove any residual medium. The washed cells were then resuspended in PBS. Approximately 15  $\mu$ L of the Candida suspension was carefully placed onto the surface of a 0.2-mm-thick calcium fluoride (CaF $_2$ ) substrate. This setup was then covered with a 0.15-mm-thick coverslip to create a sandwiched structure, optimizing the optical path and minimizing cell movement during imaging. Photothermal imaging was conducted by detecting the signal from forward scattering.

#### RESOURCE AVAILABILITY

#### Lead contact

Further information and requests for resources and reagents should be directed to and will be fulfilled by the lead contact, Ji-Xin Cheng (jxcheng@bu.edu).

<span id="page-15-0"></span>Article

![](_page_15_Picture_1.jpeg)

#### Materials availability

This study did not generate new, unique materials.

#### Data and code availability

The dataset for SRS and MIP and the code have been made publicly available on [https://github.com/buchenglab.](https://github.com/buchenglab) Noise2Void is available on [https://github.](https://github.com/juglab/n2v) [com/juglab/n2v.](https://github.com/juglab/n2v) BM4D is available on [https://webpages.tuni.fi/foi/GCF-](https://webpages.tuni.fi/foi/GCF-BM3D/index.html)[BM3D/index.html.](https://webpages.tuni.fi/foi/GCF-BM3D/index.html) Fluo-C2DL-MSC dataset is available on [https://](https://celltrackingchallenge.net/) [celltrackingchallenge.net/.](https://celltrackingchallenge.net/) Light sheet fluorescence microscopy dataset is available.[57](#page-16-0) Striping noise simulation is available.[58](#page-17-0) Intensity diffraction tomography dataset is available.[59](#page-17-0) Fluorescence lifetime imaging dataset is available.[60](#page-17-0) RGB video datasets are available.[61](#page-17-0) White Gaussian noise (*σ* = 40) was added to the grayscale videos.

#### ACKNOWLEDGMENTS

The authors thank Zhongyue Guo for discussion in writing process. This work is supported by the NIH grants R35GM136223, R01 EB032391, and R01 EB035429 to J.-X.C.

#### AUTHOR CONTRIBUTIONS

G.D. built the SPEND network, conducted hyperspectral SRS experiments, and analyzed the data. H.L. provided the OVCAR-5 dataset. Y.T. provided the U87 hyperspectral SRS dataset. X.T. and H.H. prepared HPG-treated SJSA-1 cells. J.Y. conducted the MIP experiment. C.L. helped with data discussion. H.L., L.T., and J.-X.C. supervised the project. G.D., H.L., and J.-X. C. co-wrote the manuscript. All authors read the manuscript.

#### DECLARATION OF INTERESTS

The authors declare no competing interests.

#### DECLARATION OF GENERATIVE AI AND AI-ASSISTED TECHNOLOGIES

During the preparation of this work, the authors used ChatGPT in order to polish the manuscript. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication.

#### SUPPLEMENTAL INFORMATION

Supplemental information can be found online at [https://doi.org/10.1016/j.](https://doi.org/10.1016/j.newton.2025.100195) [newton.2025.100195.](https://doi.org/10.1016/j.newton.2025.100195)

Received: October 22, 2024 Revised: March 31, 2025 Accepted: July 3, 2025 Published: July 24, 2025

#### REFERENCES

- 1. [Gao, L., and Smith, R.T. \(2015\). Optical hyperspectral imaging in micro](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref1)[scopy and spectroscopy – a review of data acquisition. J. Biophotonics](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref1) *8*[, 441–456](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref1).
- 2. [Karim, S., Qadir, A., Farooq, U., Shaikh, S., and Laghari, A. \(2022\).](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref2) [Hyperspectral Imaging: A Review and Trends towards Medical Imaging.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref2) [Current Medical Imaging Formerly Current Medical Imaging Reviews](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref2) *18*, [417–427.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref2)
- 3. [Li, Q., He, X., Wang, Y., Liu, H., Xu, D., and Guo, F. \(2013\). Review of spec](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref3)[tral imaging technology in biomedical engineering: achievements and](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref3) [challenges. J. Biomed. Opt.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref3) *18*, 100901.
- 4. [Lu, G., and Fei, B. \(2014\). Medical hyperspectral imaging: a review.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref4) [J. Biomed. Opt.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref4) *19*, 010901.
- 5. [Freudiger, C.W., Min, W., Saar, B.G., Lu, S., Holtom, G.R., He, C., Tsai, J.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref5) [C., Kang, J.X., and Xie, X.S. \(2008\). Label-Free Biomedical Imaging with](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref5)

- [High Sensitivity by Stimulated Raman Scattering Microscopy. Science](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref5) *322*[, 1857–1861.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref5)
- 6. [Zhang, D., Li, C., Zhang, C., Slipchenko, M.N., Eakins, G., and Cheng, J.-](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref6) [X. \(2016\). Depth-resolved mid-infrared photothermal imaging of living cells](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref6) [and organisms with submicrometer spatial resolution. Sci. Adv.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref6) *2*, [e1600521.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref6)
- 7. [Manifold, B., Men, S., Hu, R., and Fu, D. \(2021\). A Versatile Deep Learning](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref7) [Architecture for Classification and Label-Free Prediction of Hyperspectral](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref7) [Images. Nat. Mach. Intell.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref7) *3*, 306–315.
- 8. [Manifold, B., Thomas, E., Francis, A.T., Hill, A.H., and Fu, D. \(2019\).](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref8) [Denoising of stimulated Raman scattering microscopy images via deep](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref8) [learning. Biomed. Opt. Express](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref8) *10*, 3860–3874.
- 9. [Tang, X., Zhang, Y., Huang, X., Lee, H.J., and Zhang, D. \(2024\). Enhanced](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref9) [stimulated Raman and fluorescence imaging by single-frame trained BDN.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref9) Opt. Express *32*[, 40593–40604](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref9).
- 10. [Abdolghader, P., Ridsdale, A., Grammatikopoulos, T., Resch, G., Le´](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref10) gare´ , [F., Stolow, A., Pegoraro, A.F., and Tamblyn, I. \(2021\). Unsupervised hyper](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref10)[spectral stimulated Raman microscopy image enhancement: denoising](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref10) [and segmentation via one-shot deep learning. Opt. Express](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref10) *29*, 34205– [34219](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref10).
- 11. [Chen, G., and Qian, S.E. \(2011\). Denoising of Hyperspectral Imagery Using](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref11) [Principal Component Analysis and Wavelet Shrinkage. IEEE Trans. Geo](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref11)[sci. Remote Sens.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref11) *49*, 973–980.
- 12. [Liao, C.-S., Choi, J.H., Zhang, D., Chan, S.H., and Cheng, J.-X. \(2015\).](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref12) [Denoising Stimulated Raman Spectroscopic Images by Total Variation](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref12) [Minimization. J. Phys. Chem. C Nanomater. Interfaces](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref12) *119*, 19397– [19403](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref12).
- 13. [Coupe, P., Yger, P., Prima, S., Hellier, P., Kervrann, C., and Barillot,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref13) [C. \(2008\). An optimized blockwise nonlocal means denoising filter for](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref13) [3-D magnetic resonance images. IEEE Trans. Med. Imaging](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref13) *27*, [425–441.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref13)
- 14. Dabov, K., Foi, A., Katkovnik, V., and Egiazarian, K. (2008). Image restoration by sparse 3D transform-domain collaborative filtering, Image Processing: Algorithms and Systems VI Vol 6812 (SPIE) [https://doi.org/10.](https://doi.org/10.1117/12.766355) [1117/12.766355](https://doi.org/10.1117/12.766355).
- 15. Krull, A., Buchholz, T.O., and Jug, F. (2019). Noise2Void Learning Denoising From Single Noisy Images. Paper presented at: 2019 IEEE/ CVF Conference on Computer Vision and Pattern Recognition (CVPR) [https://openaccess.thecvf.com/content\\_CVPR\\_2019/papers/Krull\\_](https://openaccess.thecvf.com/content_CVPR_2019/papers/Krull_Noise2Void_-_Learning_Denoising_From_Single_Noisy_Images_CVPR_2019_paper.pdf) [Noise2Void\\_-\\_Learning\\_Denoising\\_From\\_Single\\_Noisy\\_Images\\_CVPR\\_](https://openaccess.thecvf.com/content_CVPR_2019/papers/Krull_Noise2Void_-_Learning_Denoising_From_Single_Noisy_Images_CVPR_2019_paper.pdf)  [2019\\_paper.pdf](https://openaccess.thecvf.com/content_CVPR_2019/papers/Krull_Noise2Void_-_Learning_Denoising_From_Single_Noisy_Images_CVPR_2019_paper.pdf).
- 16. [Batson, J., and Royer, L. \(2019\). Noise2Self: Blind Denoising by Self-](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref16)[Supervision. In Proceedings of the 36th International Conference on](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref16) [Machine Learning, C. Kamalika and S. Ruslan, eds. \(PMLR\)\),](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref16) [pp. 524-–533.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref16)
- 17. [Lehtinen, J., Munkberg, J., Hasselgren, J., Laine, S., Karras, T., Aittala, M.,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref17) [and Aila, T. \(2018\). Noise2Noise: Learning Image Restoration without](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref17) [Clean Data. In Proceedings of the 35th International Conference on Ma](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref17)[chine Learning, D. Jennifer and K. Andreas, eds., pp. 2965-–2974.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref17)
- 18. [Lecoq, J., Oliver, M., Siegle, J.H., Orlova, N., Ledochowitsch, P., and](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref18) [Koch, C. \(2021\). Removing independent noise in systems neuroscience](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref18) [data using DeepInterpolation. Nat. Methods](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref18) *18*, 1401–1408.
- 19. [Liu, C., Lu, J., Wu, Y., Ye, X., Ahrens, A.M., Platisa, J., Pieribone, V.A.,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref19) [Chen, J.L., and Tian, L. \(2024\). DeepVID v2: Self-Supervised Denoising](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref19) [with Decoupled Spatiotemporal Enhancement for Low-Photon Voltage](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref19) [Imaging. bioRxiv : the preprint server for biology](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref19) *11*, 045007.
- 20. [Papkov, M., Roberts, K., Madissoon, L.A., Shilts, J., Bayraktar, O., Fish](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref20)[man, D., Palo, K., and Parts, L. \(2021\). Noise2Stack: improving image](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref20) [restoration by learning from volumetric data. Paper Presented at: Machine](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref20) [Learning for Medical Image Reconstruction: 4th International Workshop,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref20) [MLMIR 2021, Held in Conjunction with MICCAI 2021, Strasbourg, France,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref20) [October 1, 2021, Proceedings 4 \(Springer\)](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref20).

<span id="page-16-0"></span>![](_page_16_Picture_0.jpeg)

![](_page_16_Picture_1.jpeg)

- 21. [Li, X., Zhang, G., Wu, J., Zhang, Y., Zhao, Z., Lin, X., Qiao, H., Xie, H.,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref21)  [Wang, H., Fang, L., and Dai, Q. \(2021\). Reinforcing neuron extraction](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref21)  [and spike inference in calcium imaging using deep self-supervised denois](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref21)[ing. Nat. Methods](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref21) *18*, 1395–1400.
- 22. [Michels, W.C., and Curtis, N.L. \(1941\). A Pentode Lock](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref22)-In Amplifier of High [Frequency Selectivity. Rev. Sci. Instrum.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref22) *12*, 444–447.
- 23. [Tan, Y., Lin, H., and Cheng, J.-X. \(2023\). Profiling single cancer cell meta](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref23)[bolism via high-content SRS imaging with chemical sparsity. Sci. Adv.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref23) *9*, [eadg6061.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref23)
- 24. [Zhang, D., Wang, P., Slipchenko, M.N., Ben-Amotz, D., Weiner, A.M., and](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref24)  [Cheng, J.-X. \(2013\). Quantitative Vibrational Imaging by Hyperspectral](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref24)  [Stimulated Raman Scattering Microscopy and Multivariate Curve Resolu](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref24)[tion Analysis. Anal. Chem.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref24) *85*, 98–106.
- 25. [Fereidouni, F., Bader, A.N., and Gerritsen, H.C. \(2012\). Spectral phasor](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref25)  [analysis allows rapid and reliable unmixing of fluorescence microscopy](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref25)  [spectral images. Opt. Express](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref25) *20*, 12729–12741.
- 26. [Slipchenko, M.N., Oglesbee, R.A., Zhang, D., Wu, W., and Cheng, J.-X.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref26)  [\(2012\). Heterodyne detected nonlinear optical imaging in a lock-in free](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref26)  [manner. J. Biophotonics](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref26) *5*, 801–807.
- 27. [Zhu, Y., Ge, X., Ni, H., Yin, J., Lin, H., Wang, L., Tan, Y., Prabhu Dessai, C.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref27)  [V., Li, Y., Teng, X., and Cheng, J.X. \(2023\). Stimulated Raman photother](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref27)[mal microscopy toward ultrasensitive chemical imaging. Sci. Adv.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref27) *9*, [eadi2181](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref27).
- 28. [Cheng, J.-X., Min, W., Ozeki, Y., and Polli, D. \(2021\). Stimulated Raman](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref28)  [Scattering Microscopy: Techniques and Applications \(Elsevier\).](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref28)
- 29. [Audier, X., Heuke, S., Volz, P., Rimke, I., and Rigneault, H. \(2020\). Noise in](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref29)  [stimulated Raman scattering measurement: From basics to practice. APL](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref29)  [Photonics](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref29) *5*, 011101.
- 30. [Lin, H., and Cheng, J.-X. \(2023\). Computational coherent Raman scat](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref30)[tering imaging: breaking physical barriers by fusion of advanced instru](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref30)[mentation and data science. eLight](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref30) *3*, 6.
- 31. [Ronneberger, O., Fischer, P., and Brox, T. \(2015\). U-net: Convolutional](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref31)  [networks for biomedical image segmentation. Paper Presented at: Medi](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref31)[cal Image Computing and Computer-Assisted Intervention–MICCAI 2015:](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref31)  [18th International Conference, Munich, Germany, October 5-9, 2015, Pro](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref31)[ceedings, Part III 18 \(Springer\).](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref31)
- 32. [Ozeki, Y., Dake, F., Kajiyama, S., Fukui, K., and Itoh, K. \(2009\). Analysis](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref32)  [and experimental assessment of the sensitivity of stimulated Raman scat](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref32)[tering microscopy. Opt. Express](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref32) *17*, 3651–3658.
- 33. [Koho, S., Tortarolo, G., Castello, M., Deguchi, T., Diaspro, A., and Vicido](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref33)[mini, G. \(2019\). Fourier ring correlation simplifies image restoration in fluo](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref33)[rescence microscopy. Nat. Commun.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref33) *10*, 3103.
- 34. [Alt, H., and Godau, M. \(1995\). Computing the Fre´](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref34) chet Distance between [Two Polygonal Curves. Int. J. Comput. Geom. Appl.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref34) *05*, 75–91.
- 35. [Howell, N.K., Arteaga, G., Nakai, S., and Li-Chan, E.C. \(1999\). Raman](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref35)  Spectral Analysis in the C− [H Stretching Region of Proteins and Amino](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref35)  [Acids for Investigation of Hydrophobic Interactions. J. Agric. Food](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref35)  Chem. *47*[, 924–933](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref35).
- 36. [Marble, C.B., Marble, K.S., Keene, E.B., Petrov, G.I., and Yakovlev, V.V.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref36)  [\(2024\). Hyper-Raman spectroscopy of biomolecules. Analyst](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref36) *149*, [528–536](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref36).
- 37. [Yue, S., and Cheng, J.X. \(2016\). Deciphering single cell metabolism by](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref37)  [coherent Raman scattering microscopy. Curr. Opin. Chem. Biol.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref37)  *33*[, 46–57.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref37)
- 38. [Huang, K.C., Li, J., Zhang, C., Tan, Y., and Cheng, J.X. \(2020\). Multiplex](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref38)  [Stimulated Raman Scattering Imaging Cytometry Reveals Lipid-Rich Pro](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref38)[trusions in Cancer Cells under Stress Condition. iScience](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref38) *23*, 100953.
- 39. [Zhuge, M., Huang, K.-C., Lee, H.J., Jiang, Y., Tan, Y., Lin, H., Dong, P.-T.,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref39)  [Zhao, G., Matei, D., Yang, Q., and Cheng, J.X. \(2021\). Ultrasensitive Vibra](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref39)[tional Imaging of Retinoids by Visible Preresonance Stimulated Raman](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref39)  [Scattering Microscopy. Adv. Sci.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref39) *8*, 2003136.

- 40. [Wei, L., Yu, Y., Shen, Y., Wang, M.C., and Min, W. \(2013\). Vibrational im](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref40)[aging of newly synthesized proteins in live cells by stimulated Raman scat](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref40)[tering microscopy. Proc. Natl. Acad. Sci. USA](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref40) *110*, 11226–11231.
- 41. [Su Hui Teo, C., Serwa, R.A., and O'Hare, P. \(2016\). Spatial and Temporal](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref41)  [Resolution of Global Protein Synthesis during HSV Infection Using Bio](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref41)[orthogonal Precursors and Click Chemistry. PLoS Pathog.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref41) *12*, e1005927.
- 42. [Dieterich, D.C., Hodas, J.J.L., Gouzer, G., Shadrin, I.Y., Ngo, J.T., Triller,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref42)  [A., Tirrell, D.A., and Schuman, E.M. \(2010\). In situ visualization and dy](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref42)[namics of newly synthesized proteins in rat hippocampal neurons. Nat.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref42)  [Neurosci.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref42) *13*, 897–905.
- 43. [Liu, J., Xu, Y., Stoleru, D., and Salic, A. \(2012\). Imaging protein synthesis in](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref43)  [cells and tissues with an alkyne analog of puromycin. Proc. Natl. Acad. Sci.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref43)  USA *109*[, 413–418.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref43)
- 44. [Wei, L., Hu, F., Shen, Y., Chen, Z., Yu, Y., Lin, C.-C., Wang, M.C., and Min,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref44)  [W. \(2014\). Live-cell imaging of alkyne-tagged small biomolecules by stim](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref44)[ulated Raman scattering. Nat. Methods](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref44) *11*, 410–412.
- 45. [Baek, S.-J., Park, A., Ahn, Y.-J., and Choo, J. \(2015\). Baseline correction](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref45)  [using asymmetrically reweighted penalized least squares smoothing. An](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref45)alyst *140*[, 250–257.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref45)
- 46. [He, H., Yin, J., Li, M., Dessai, C.V.P., Yi, M., Teng, X., Zhang, M., Li, Y., Du,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref46)  [Z., Xu, B., and Cheng, J.X. \(2024\). Mapping enzyme activity in living sys](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref46)[tems by real-time mid-infrared photothermal imaging of nitrile chame](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref46)[leons. Nat. Methods](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref46) *21*, 342–352.
- 47. [Ishigane, G., Toda, K., Tamamitsu, M., Shimada, H., Badarla, V.R., and](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref47)  [Ideguchi, T. \(2023\). Label-free mid-infrared photothermal live-cell imaging](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref47)  [beyond video rate. Light Sci. Appl.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref47) *12*, 174.
- 48. [Li, M., Razumtcev, A., Yang, R., Liu, Y., Rong, J., Geiger, A.C., Blanchard,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref48)  [R., Pfluegl, C., Taylor, L.S., and Simpson, G.J. \(2021\). Fluorescence-De](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref48)[tected Mid-Infrared Photothermal Microscopy. J. Am. Chem. Soc.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref48) *143*, [10809–10815.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref48)
- 49. [Yin, J., Lan, L., Zhang, Y., Ni, H., Tan, Y., Zhang, M., Bai, Y., and Cheng, J.-](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref49)  [X. \(2021\). Nanosecond-resolution photothermal dynamic imaging via MHZ](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref49)  [digitization and match filtering. Nat. Commun.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref49) *12*, 7097.
- 50. [Yin, J., Zhang, M., Tan, Y., Guo, Z., He, H., Lan, L., and Cheng, J.-X. \(2023\).](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref50)  [Video-rate mid-infrared photothermal imaging by single-pulse photother](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref50)[mal detection per pixel. Sci. Adv.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref50) *9*, eadg8814.
- 51. [Karunakaran, C., Christensen, C.R., Gaillard, C., Lahlali, R., Blair, L.M., Pe](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref51)[rumal, V., Miller, S.S., and Hitchcock, A.P. \(2015\). Introduction of Soft](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref51)  [X-Ray Spectromicroscopy as an Advanced Technique for Plant Biopoly](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref51)[mers Research. PLoS One](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref51) *10*, e0122959.
- 52. [Tang, X., Ren, Y., and Xie, H. \(2023\). Noise correlation and its impact on](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref52)  [the performance of multi-material decomposition-based spectral imaging](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref52)  [in photon-counting CT. J. Appl. Clin. Med. Phys.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref52) *24*, e13830.
- 53. [Palombo, F., and Fioretto, D. \(2019\). Brillouin Light Scattering: Applica](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref53)[tions in Biomedical Sciences. Chem. Rev.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref53) *119*, 7833–7847.
- 54. [Davydova, D., de la Cadena, A., Akimov, D., and Dietzek, B. \(2016\). Tran](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref54)[sient absorption microscopy: advances in chemical imaging of photoin](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref54)[duced dynamics. Laser Photon. Rev.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref54) *10*, 62–81.
- 55. [Lin, H., Lee, H.J., Tague, N., Lugagne, J.-B., Zong, C., Deng, F., Shin, J.,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref55)  [Tian, L., Wong, W., Dunlop, M.J., and Cheng, J.X. \(2021\). Microsecond](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref55)  [fingerprint stimulated Raman spectroscopic imaging by ultrafast tuning](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref55)  [and spatial-spectral learning. Nat. Commun.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref55) *12*, 3052.
- 56. [Weigert, M., Schmidt, U., Boothe, T., Mu¨](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref56) ller, A., Dibrov, A., Jain, A., Wil[helm, B., Schmidt, D., Broaddus, C., Culley, S., et al. \(2018\). Content](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref56)[aware image restoration: pushing the limits of fluorescence microscopy.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref56)  [Nat. Methods](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref56) *15*, 1090–1097.
- 57. [Li, C., Li, Y., Zhao, H., and Ding, L. \(2024\). Enhancing brain image quality](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref57)  [with 3D U-net for stripe removal in light sheet fluorescence microscopy.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref57)  [Brain Inform.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref57) *11*, 24.

# <span id="page-17-0"></span>Article

![](_page_17_Picture_1.jpeg)

- 58. [Kim, N., Han, S.S., and Jeong, C.S. \(2023\). ADOM: ADMM-Based Optimi](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref58)[zation Model for Stripe Noise Removal in Remote Sensing Image. IEEE Ac](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref58)cess *11*[, 106587–106606.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref58)
- 59. [Zhao, J., Matlock, A., Zhu, H., Song, Z., Zhu, J., Wang, B., Chen, F., Zhan,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref59) [Y., Chen, Z., Xu, Y., et al. \(2022\). Bond-selective intensity diffraction to](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref59)[mography. Nat. Commun.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref59) *13*, 7767.
- 60. Kapsiani, S., La¨ [ubli, N.F., Ward, E.N., Shehata, M., Kaminski, C.F., and](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref60) [Kaminski Schierle, G.S. \(2024\). FLIMPA: A versatile software for Fluores-](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref60)
- [cence Lifetime Imaging Microscopy Phasor Analysis. Preprint at bioRxiv,](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref60) [612802.](http://refhub.elsevier.com/S2950-6360(25)00187-2/sref60)
- 61. Tassano, M., Delon, J., and Veit, T. (2020). Fastdvdnet: Towards realtime deep video denoising without flow estimation. Paper presented at: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition [https://openaccess.thecvf.com/content\\_CVPR\\_](https://openaccess.thecvf.com/content_CVPR_2020/papers/Tassano_FastDVDnet_Towards_Real-Time_Deep_Video_Denoising_Without_Flow_Estimation_CVPR_2020_paper.pdf) [2020/papers/Tassano\\_FastDVDnet\\_Towards\\_Real-Time\\_Deep\\_Video\\_](https://openaccess.thecvf.com/content_CVPR_2020/papers/Tassano_FastDVDnet_Towards_Real-Time_Deep_Video_Denoising_Without_Flow_Estimation_CVPR_2020_paper.pdf) [Denoising\\_Without\\_Flow\\_Estimation\\_CVPR\\_2020\\_paper.pdf.](https://openaccess.thecvf.com/content_CVPR_2020/papers/Tassano_FastDVDnet_Towards_Real-Time_Deep_Video_Denoising_Without_Flow_Estimation_CVPR_2020_paper.pdf)

**NEWTON, Volume** *1* 

## **Supplemental information**

**Self-supervised elimination of** 

**non-independent noise in hyperspectral imaging** 

**Guangrui Ding, Chang Liu, Jiaze Yin, Xinyan Teng, Yuying Tan, Hongjian He, Haonan Lin, Lei Tian, and Ji-Xin Cheng** 

![](_page_19_Picture_2.jpeg)

**Figure S1. Hyperspectral Stimulated Raman Scattering imaging setup.** (a) Spectral focusing. Two femtosecond laser pulses are chirped to picosecond and delayed in the time domain. The wavenumber difference of two pulses corresponds to the vibrational state of chemical bonds. (b) Lab-build hyperspectral SRS setup. AOM: acoustic optical modulator; DM: dichroic mirror; GM: Galvo mirror; Obj: Objective; C: sample; F: filter; PD: photodiode; LIA: lock-in amplifier.

![](_page_20_Figure_0.jpeg)

**Figure S2. Spatial noise comparison in fluorescence and SRS images.** (a) Single color SRS image of OVCAR5. (b) Fluorescence image of OVCAR5. (c) Noise PSD of SRS image. (d) Noise PSD of fluorescence imaging.

![](_page_21_Figure_0.jpeg)

![](_page_21_Figure_1.jpeg)

**Figure S3. Noise Characteristic of hyperspectral data by a broadband photodiode detector**. (a) 2D noise Power Spectral Density distribution. (b) Pearson Cross Correlation analysis vs Time Constant.

![](_page_21_Figure_3.jpeg)

**Figure S4. Pearson Cross Correlation coefficient vs Raman resonance frequency on DMSO sample.** (a) PCC analysis of fast axis. (b) PCC analysis of slow axis.

![](_page_22_Figure_1.jpeg)

**Figure S5. Noise analysis workflow.** (a) Spectral variation analysis. (b) Spatial correlation analysis.

![](_page_23_Figure_0.jpeg)

![](_page_23_Figure_1.jpeg)

**Figure S6. Permutation for 2D anisotropic noise.** (a) 2D input image with different noise levels at different pixels. (b) Permutation of two adjacent columns along the x axis. (c) Permutation of two adjacent rows along the y axis.

![](_page_24_Figure_0.jpeg)

**Figure S7. Different permutation strategies to handle data from different scanning modalities.** It is shown that two scanning modalities lead to two different permutation strategies. (a) − − scanning. (b) − − scanning. (c-d) Choose the corresponding axis as the permutation axis according to the correlation level. (e-f) Permutation based on the chosen axis.

![](_page_25_Figure_0.jpeg)

**Figure S8. Network architecture of SPEND.** The whole network is based on a three-layer Unet architecture.

![](_page_26_Figure_1.jpeg)

**Figure S9. Chemical unmixing methods.** (a) Unsupervised chemical unmixing methods. No chemical reference is needed. The outputs are segmentation of each component based on the spectral difference. (b) Supervised chemical unmixing methods. Chemical references are needed. The outputs are quantitative chemical concentration maps.

![](_page_27_Figure_0.jpeg)

**Figure S10. Performance of permutation along different axes.** (a) Single color SRS (1650cm-1 ) Mean intensities and standard deviations are calculated within ROI. Raw: mean = 31672, std = 334. Spectral axis permutation: mean = 31653, std = 331. Spatial axis permutation: mean = 31719, std = 54. High SNR: mean = 31714, std = 69. (b) Chemical unmixing map. (c) Spectrum error respectively. (d) Correlation of each axis. (e) Spectrum of ROI. (f) Chemical map SSIM.

![](_page_28_Figure_0.jpeg)

**Figure S11. Chemical references for OVCAR5 spectral unmixing.**

![](_page_28_Figure_2.jpeg)

**Figure S12. OVCAR5 cells imaged by SRS under high laser power condition.** (a) Single color SRS image of OVCAR5 cell @2935.2cm-1 . (b) Chemical unmixing map of OVCAR5 hyperspectral SRS stack.

![](_page_29_Figure_0.jpeg)

![](_page_29_Figure_1.jpeg)

**Figure S13. Spectral distortion calculation diagram.** (a) Fréchet distance diagram. (b)-(c) ROI spectrum plot. Spectrum from ground truth is utilized as the reference. The same ROI spectrums of different groups are input to calculate freshet distance to calculate spectral distortion.

![](_page_30_Figure_0.jpeg)

**Figure S14. Single pixel analysis of linear relationship on DMSO SRS intensity after denoising.**  (a) Raw single pixel DMSO intensity. (b) Linear fitting of raw spectrum intensity. (c) Single pixel DMSO intensity after SPEND. (d) Linear fitting of denoised spectrum intensity.

![](_page_31_Figure_0.jpeg)

**Figure S15. SRS spectra of different chemical rich ROIs in the fingerprint region.** (a) Single color SRS image of a U87 cell at 1648.6cm-1 . (b)-(d) Raw and denoised spectrum in (b) fatty acid rich, (c)cholesterol rich, and (d) protein rich ROIs.

![](_page_32_Figure_0.jpeg)

**Figure S16. The peak fitting of fatty acid rich region spectrum.**

![](_page_33_Figure_0.jpeg)

**Figure S17. The chemical map unmixing results.** (a) Fatty acid distribution. (b) Cholesterol distribution. (c) Retinyl ester distribution. (d) Protein distribution.

![](_page_34_Figure_0.jpeg)

**Figure S18. Comparison of Input chemical references and MCR retrieved references.** (a) Input chemical references in the fingerprint region. (b) Retrieved chemical references in the fingerprint region. (c) Input chemical references in the C-H region. (d) Retrieved chemical references in C-H region.

![](_page_35_Figure_0.jpeg)

**Figure S19. Spectra in different ROIs.** (a)-(b) Raw and denoising result of single-color SRS of the treated group. Raman shift: 2125cm-1 . (c)-(d) Raw and denoising result of single-color SRS of control group at 2125cm-1 . (e)-(f) spectrum of ROI of raw and denoising treated group respectively. (g)-(h) spectrum of ROI of raw and denoising control groups respectively. (i)-(j) Normalized spectrum after arPLS baseline correction of HPG treated Group. (k)-(l) Normalized spectrum after arPLS baseline correction of the control group.

![](_page_36_Figure_0.jpeg)

**Figure S20. Reference spectrum generated for lasso unmixing by the retrieval of phasor segmentation result.**

![](_page_36_Figure_2.jpeg)

**Figure S21. Mid-infrared photothermal microscopy setup.** DM: Dichroic mirror; CM1: concave mirror f=150 mm; CM2: concave mirror f=250 mm; IR obj: reflective objective lens 40X 0.5NA; Vis Obj: visible objective lens 60X 1.2NA; SL: scan lens f=75 mm; TL: tube lens f=180mm; GV: Galvo mirrors.

![](_page_37_Figure_0.jpeg)

**Figure S22. 2D Noise Power Spectral Density of a mid-infrared photothermal imaging system.**

![](_page_37_Figure_4.jpeg)

**Figure S23. Three-layer structure intensity cross-section plot.**

![](_page_38_Figure_0.jpeg)

**Figure S24. Examples of non i.i.d. noise in different imaging modalities**. (a) Structure noise in confocal fluorescence imaging. Whole video average is shown. (b) Striping noise in light sheet fluorescence microscopy. (c) Noise Analysis of Fluorescence Lifetime Imaging.

![](_page_39_Figure_0.jpeg)

**Figure S25. Denoising performance of SPEND on different modalities.** (a) Raw data, BM4D, Noise2Void and SPEND result on confocal fluorescence dataset. (b) Raw data, BM4D, Noise2Void and SPEND result of light sheet fluorescence microscopy dataset. (c) Raw data, BM4D, Noise2Void and SPEND result of FLIM dataset. The raw stack average is used to calculate the SSIM and PSNR of each denoised results.

![](_page_40_Figure_0.jpeg)

**Figure S26. Performance comparison between SPEND and supervised training on striping noise dataset.**

![](_page_41_Figure_0.jpeg)

**Figure S27. Denoising performance of SPEND on videos.**