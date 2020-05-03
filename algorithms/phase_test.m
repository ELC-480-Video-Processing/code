clear clc



video = VideoReader('DJI_0003.MP4'); 

search_x = 574; 
search_y = 367; 
search_wid = 127;
search_hgt = 127; 

% Extract search region from first frame
firstFrame = video.readFrame(); 
roigrey_1 = rgb2gray(firstFrame);
searchRegion_F1 = imcrop(roigrey_1, [search_x, search_y, search_hgt, search_wid]); 

% Extract search region from second frame
secondFrame = read(video,700);
roigrey_2 = rgb2gray(secondFrame);
pause(2); 

montage({roigrey_2, searchRegion_F1});
c = normxcorr2(searchRegion_F1, roigrey_2); 
pause(2); 
surf(c)
shading flat

[dy,dx] = find(c==max(c(:)));
yoff = dy - size(searchRegion_F1,1);
xoff = dx - size(searchRegion_F1,2);
imshow(secondFrame)
drawrectangle(gca,'Position',[xoff,yoff,size(searchRegion_F1,2),size(searchRegion_F1,1)], ...
    'FaceAlpha',0);

% % searchRegion_F2 = imcrop(roigrey_2, [search_x, search_y, search_hgt, search_wid]); 
% 
% % % Compute Phase Correlation
% % corr = phase_corr(searchRegion_F1, searchRegion_F2,64);
% 
% subplot(311); 
% imshow(searchRegion_F1); 
% subplot(312); 
% imshow(searchRegion_F2); 
% subplot(313); 
% mesh(real(corr))


