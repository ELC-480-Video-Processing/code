% normxcorr2 based object tracker

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

% Extract ROI from original frame
grey = rgb2gray(roiFrame);
template = imcrop(grey, x); 

while (video.hasFrame())
    
    
    currFrame = video.readFrame(); 
    currFrame_grey = rgb2gray(currFrame);
    
    p = gpuArray(template); 
    t = gpuArray(currFrame_grey);
    
    c = normxcorr2(p, t);
    cpu_c = gather(c);
    [dy,dx] = find(cpu_c==max(cpu_c(:)));
    
    yoff = dy - size(template,1);
    xoff = dx - size(template,2);
    updatedFrame = insertShape(currFrame, 'Rectangle',[xoff, yoff, size(template,2), size(template,1)],'Color','magenta'); 
    playback(updatedFrame);

end 





