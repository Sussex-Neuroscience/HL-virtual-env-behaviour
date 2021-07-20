function code = shortTrack
% spatialNavigation_linearTrack   Code for the ViRMEn experiment spatialNavigation_linearTrack.
%   code = spatialNavigation_linearTrack   Returns handles to the functions that ViRMEn
%   executes during engine initialization, runtime and termination.


% Begin header code - DO NOT EDIT
code.initialization = @initializationCodeFun;
code.runtime = @runtimeCodeFun;
code.termination = @terminationCodeFun;
% End header code - DO NOT EDIT

%cd('C:\Users\kira\Documents\MATLAB');

% --- INITIALIZATION code: executes before the ViRMEn engine starts.
function vr = initializationCodeFun(vr)


% how many times to run along linear track...
TOT_NUM = 100;
vr.labjack = 1;
vr.REST_LENGTH = 10;
%%%%% initialises lab jack
try
    
    vr.ljmAsm = NET.addAssembly('LabJack.LJM'); %Make the LJM .NET assembly visible in MATLAB
    
    vr.t = vr.ljmAsm.AssemblyHandle.GetType('LabJack.LJM+CONSTANTS');
    vr.LJM_CONSTANTS = System.Activator.CreateInstance(vr.t); %creating an object to nested class LabJack.LJM.CONSTANTS
    
    vr.labjackhandle = 0;
    %
    %     Open first found LabJack
    %     register lab jack
    [vr.ljmError, vr.labjackhandle] = LabJack.LJM.OpenS('T7', 'USB', '470014150', vr.labjackhandle);
    %
    %     set lab jack channels in matlab
    vr.numFrames = 2;
    vr.aNames = NET.createArray('System.String', vr.numFrames);
    vr.aNames(1) = 'DIO0_EF_ENABLE';
    vr.aNames(2) = 'DIO1_EF_ENABLE';
    vr.aValues = NET.createArray('System.Double', vr.numFrames);
    vr.aValues(1) = 0; %disabled
    vr.aValues(2) = 0; %disabled
    LabJack.LJM.eWriteNames(vr.labjackhandle, vr.numFrames, vr.aNames, vr.aValues, 0);
    
    vr.aNames(1) = 'DIO0_EF_INDEX';
    vr.aNames(2) = 'DIO1_EF_INDEX';
    vr.aValues = NET.createArray('System.Double', vr.numFrames);
    vr.aValues(1) = 10; %Set feature index to quadrature.
    vr.aValues(2) = 10; %Set feature index to quadrature.
    LabJack.LJM.eWriteNames(vr.labjackhandle, vr.numFrames, vr.aNames, vr.aValues, 0);
    
    vr.aNames(1) = 'DIO0_EF_ENABLE';
    vr.aNames(2) = 'DIO1_EF_ENABLE';
    vr.aValues = NET.createArray('System.Double', vr.numFrames);
    vr.aValues(1) = 1; %Set feature index to quadrature.
    vr.aValues(2) = 1; %Set feature index to quadrature.
    LabJack.LJM.eWriteNames(vr.labjackhandle, vr.numFrames, vr.aNames, vr.aValues, 0);
    %
catch
    disp('No labjack');
    vr.labjack = 0;
end
%just want to set counter to 1 for first run of loop
dataDir = fullfile(pwd, 'data');
if exist(dataDir) ~= 7
    mkdir(dataDir)
end
logName = sprintf('%s/%s_t%d_%s.dat', dataDir, vr.mouse, vr.trial, datestr(now, 'yyyymmddHHMM'));
vr.fid = fopen(logName, 'w');
vr.counter=1;
vr.rewarded = 0;
vr.worldLength = 295;
vr.TOT_NUM = TOT_NUM;
vr.curLength = 0;
vr.novel = randi(2)==1;
vr.startmeasure = 0;
vr.stime = 0;
vr.rewardName = 'FIO2';
vr.x = 0;
vr.y = 0;

vr.currentWorld = randi(2);
if vr.labjack == 1
    LabJack.LJM.eWriteName(vr.labjackhandle, 'DAC0', 5.0);
    pause(0.1);
    LabJack.LJM.eWriteName(vr.labjackhandle, 'DAC0', 0);
end


% --- RUNTIME code: executes on every iteration of the ViRMEn engine.
function vr = runtimeCodeFun(vr)

%%%% check animal's position on linear track - if at end, teleport back to beginning
if vr.position(2)>vr.worldLength %test to see if animal is at end of linear track in current world
    vr.rewarded = 0;
    vr.counter = vr.counter+1;
    vr.curLength = vr.curLength + vr.worldLength;
    if vr.counter > vr.TOT_NUM
        vr.experimentEnded=1; %end the experiment if has been through the track twice
    else
        vr.position(2)=0; %teleport animal back to beginning
        vr.currentWorld = randi(2);
        % Reset novel object
        
        novel = vr.exper.worlds{vr.currentWorld}.objects{end};
        vr.novel= 0;
        x = -30; %generate randomly left/right
        y = 100; %generate randomly
        vr.x = x;
        vr.y = y;
        novel.x = x;
        novel.y = y;
        vr.worlds{vr.currentWorld} = vr.exper.worlds{vr.currentWorld}.triangulate;
        
        
        if vr.currentWorld ==1
            display('Boring world')
        else
            display('Salient world')
        end
        vr.dp(:)=0; %prevent any additional movement during teleportation
        vr.rewarded = 0;
    end
    
    % Novel object environment 25% of the time
    if randi(4) > 3
        display('Novel object')
        vr.novel =1;
        % Generate novel object
        novel = vr.exper.worlds{vr.currentWorld}.objects{end};
        vr.x = -30;
        vr.y = 75+randi(150); %generate randomly
        while (abs(vr.y-100) < 15)
            vr.y = 75+randi(150); %generate randomly
        end
        novel.x = vr.x;
        novel.y = vr.y;
        vr.worlds{vr.currentWorld} = vr.exper.worlds{vr.currentWorld}.triangulate;
    else
        novel = vr.exper.worlds{vr.currentWorld}.objects{end};
        vr.novel= 0;
        x = -30; %generate randomly left/right
        y = 100; %generate randomly
        vr.x = x;
        vr.y = y;
        novel.x = x;
        novel.y = y;
        vr.worlds{vr.currentWorld} = vr.exper.worlds{vr.currentWorld}.triangulate;
    end
    %% Check if the mouse is in the novel environment and the reward zone
elseif abs(vr.position(2) - 240) < 5 & vr.novel == 1 & vr.rewarded <3
    vr.rewarded = vr.rewarded + 1;
    if vr.labjack == 1
        LabJack.LJM.eWriteName(vr.labjackhandle, vr.rewardName, 1);
        pause(0.01);
        LabJack.LJM.eWriteName(vr.labjackhandle, vr.rewardName, 0);
    end
    
end

if vr.labjack ==1
    LabJack.LJM.eWriteName(vr.labjackhandle, 'DAC1', (vr.position(2)/vr.worldLength*5.0));
end

%Save position to log
timestamp = now;
fwrite(vr.fid, [timestamp, vr.position(1:2), vr.currentWorld, vr.novel, vr.x, vr.y, vr.rewarded], 'double');


% --- TERMINATION code: executes after the ViRMEn engine stops.
function vr = terminationCodeFun(vr)
novel = vr.exper.worlds{1}.objects{end};

x = 70; %generate randomly left/right
y = 150; %generate randomly
novel.x = x;
novel.y = y;
vr.worlds{vr.currentWorld} = vr.exper.worlds{vr.currentWorld}.triangulate;
%delete the temporary log file
if(exist('vr.tempfile')==1)
    delete(vr.tempfile);
end

% Close labjack
if vr.labjack == 1
    LabJack.LJM.eWriteName(vr.labjackhandle, 'DAC0', 5.0);
    pause(0.01);
    LabJack.LJM.eWriteName(vr.labjackhandle, 'DAC0', 0);
    LabJack.LJM.Close(vr.labjackhandle);
    fclose(vr.fid);
end



