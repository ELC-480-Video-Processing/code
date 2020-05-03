
%%%
% Phase Correlation Object Tracking 

% Steps: 
%     - Determine ROI through user input
%     - Create Search Region that encapsulates ROI, must be at least 2x bigger than ROI
%       than object to account for potential motion
%     - Partition search region into a set of square blocks 
%     - Draw a search region on a second frame, and break into respective square blocks
%     - Perform phase plane correlation on each of the corresponding blocks between the two frames
%     - Deliver a set of candidate vectors, the greatest of which corresponds to the most probable object translation
%     - Redraw the bounding box according to the translation determined by the peak vector
%     - if the peak vector is at the boundary of the search region, shift the search region linearly by where the edge is 
%         
        
%%%
clear 
clc

    
%%% 
%     Runtime Parameters
    
    SEARCH_BLOCK_SIZE = 63; 
    OFFSET = 16;
%%%

% Load Video and create VideoPlayer objects
video = VideoReader('DJI_0003.MP4');
playback = vision.VideoPlayer(); 

% Select ROI through user input
roiFrame = video.readFrame(); 
figure; imshow(roiFrame); 
roi = drawrectangle;
x = roi.Position;
close;

% Display video frame with embedded ROI 
objectImage = insertShape(roiFrame,'Rectangle',x,'Color','red');
figure; imshow(objectImage);
pause(1); 
close; 

% Draw 128x128 Region of Interest
search_x = x(1)-OFFSET; 
search_y = x(2)-OFFSET; 
search_hgt = SEARCH_BLOCK_SIZE; 
search_wid = SEARCH_BLOCK_SIZE; 
return


figure; objectImage = insertShape(roiFrame, 'Rectangle', [search_x, search_y, search_hgt, search_wid],'Color','green'); 
imshow(objectImage); 
pause(2); 
close

% Extract search region from input frame (after converting to greyscale)
roi_grey = rgb2gray(roiFrame); 
searchRegion_F1 = imcrop(roi_grey, [search_x, search_y, search_hgt, search_wid]);  
searchRegionOld = searchRegion_F1; 

threshold = 0.05; 
while (video.hasFrame)
    secondFrame = video.readFrame(); 
    
    % Extract search region from frame
    roigrey_2 = rgb2gray(secondFrame);
    searchRegion_F2 = imcrop(roigrey_2, [search_x, search_y, search_hgt, search_wid]); 
    
    % Correlate with search region of old frame
    corr = phase_corr(searchRegionOld, searchRegion_F2,64); 
    corr(1:5, 1:5) = 0; 
    corr(end-5:end, end-5:end) = 0; 
    corr(1:5, end-5:end) = 0; 
    corr(end-5:end, 1:5) = 0; 
    
    
    [peak, idx] = max( corr(:)); 
    
    if (peak >= threshold)
        [dx, dy] = ind2sub(size(corr), peak); 
    else
        dx = 0; dy = 0; 
    end 
   
    % update search box parameters
    search_x = search_x + dx; 
    search_y = search_y + dy; 
    updatedFrame = insertShape(secondFrame, 'Rectangle',[search_x, search_y, search_hgt, search_wid],'Color','magenta'); 
    playback(updatedFrame); 
    
    searchRegionOld = searchRegion_F2; 
end




% exit; 
% 
% frame1 = read(x,1); 
% frame2= read(x,10); 
% 
% frame1 = rgb2gray(frame1); 
% frame2 = rgb2gray(frame2); 
% corr = phase_corr(frame1, frame2); 
% 
% corr(1:5, 1:5) = 0; 
% corr(end-5:end, end-5:end) = 0; 
% corr(1:5, end-5:end) = 0; 
% corr(end-5:end, 1:5) = 0; 
% 
% 

%%% OLD Code for testing
% % Compute phase correlation and draw new bounding box
% corr = phase_corr(searchRegion_F1, searchRegion_F2,SEARCH_BLOCK_SIZE+1);
% % corr(1:5, 1:5) = 0; 
% % corr(end-5:end, end-5:end) = 0; 
% % corr(1:5, end-5:end) = 0; 
% % corr(end-5:end, 1:5) = 0; 
% 
% subplot(313); 
% mesh(real(corr));
% [peak, translation] = max(max(corr));
% x(1) = x(1)-translation; 
% 
% figure; objectImage = insertShape(roiFrame, 'Rectangle', x ,'Color','green'); 
% imshow(objectImage); 
% pause(2); 
% close

% % Extract search region from second frame
% secondFrame = read(video,300);
% roigrey_2 = rgb2gray(secondFrame);
% searchRegion_F2 = imcrop(roigrey_2, [search_x, search_y, search_hgt, search_wid]); 
% 
% subplot(311); 
% imshow(searchRegion_F1); 
% subplot(312); 
% imshow(searchRegion_F2); 
% 
