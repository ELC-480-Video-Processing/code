function [corr] =  phase_corr(im1,im2,windowSize)
 
DELTA = 0.01;

% Create Hann Window
win = hann(windowSize); 
win = win(:) * win(:)';


fr_im1 = fft2(double(im1).*win);
fr_im2 = fft2(double(im2).*win);
fr_im2 = conj(fr_im2);
prod = fr_im1 .* fr_im2;
prod = prod ./ (abs(prod) + DELTA);
corr = ifft2(prod);


end 