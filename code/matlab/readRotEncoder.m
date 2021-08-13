function readRotEncoder()
    %Read rotary encoder input through LabJack T7. It will output the input
    %onto the DAC1 for direct input into the microscope and will generated a
    %datafile (.dat) with in the first column the timestamp and in the second
    %column the distance.
    dataDir = 'C:\Users\catherine hall\Documents\data';
    if exist(dataDir) ~= 7
        mkdir(dataDir)
    end

    logName = sprintf('%s/%s.dat', dataDir, datestr(now, 'yyyymmddHHMM'));
    fid = fopen(logName, 'w');

    ljmAsm = NET.addAssembly('LabJack.LJM'); %Make the LJM .NET assembly visible in MATLAB

    t =  ljmAsm.AssemblyHandle.GetType('LabJack.LJM+CONSTANTS');
    LJM_CONSTANTS = System.Activator.CreateInstance( t); %creating an object to nested class LabJack.LJM.CONSTANTS

    labjackhandle = 0;
    %
    %     Open first found LabJack
    %     register lab jack
    [ljmError, labjackhandle] = LabJack.LJM.OpenS('T7', 'USB', '470014150',  labjackhandle);
    %
    %     set lab jack channels in matlab
    numFrames = 2;
    aNames = NET.createArray('System.String', numFrames);
    aNames(1) = 'DIO0_EF_ENABLE';
    aNames(2) = 'DIO1_EF_ENABLE';
    aValues = NET.createArray('System.Double',  numFrames);
    aValues(1) = 0; %disabled
    aValues(2) = 0; %disabled
    LabJack.LJM.eWriteNames( labjackhandle,  numFrames,  aNames,  aValues, 0);

    aNames(1) = 'DIO0_EF_INDEX';
    aNames(2) = 'DIO1_EF_INDEX';
    aValues = NET.createArray('System.Double',  numFrames);
    aValues(1) = 10; %Set feature index to quadrature.
    aValues(2) = 10; %Set feature index to quadrature.
    LabJack.LJM.eWriteNames( labjackhandle,  numFrames,  aNames,  aValues, 0);

    aNames(1) = 'DIO0_EF_ENABLE';
    aNames(2) = 'DIO1_EF_ENABLE';
    aValues = NET.createArray('System.Double',  numFrames);
    aValues(1) = 1; %Set feature index to quadrature.
    aValues(2) = 1; %Set feature index to quadrature.
    LabJack.LJM.eWriteNames( labjackhandle,  numFrames,  aNames,  aValues, 0);
    %

    name = 'DIO0_EF_READ_A';
    finishup = onCleanup(@() myCleanupFun(labjackhandle, fid));
    oldPosition = 0;
        LabJack.LJM.eWriteName(labjackhandle, 'DAC0', 5.0);
    pause(0.1);
    LabJack.LJM.eWriteName(labjackhandle, 'DAC0', 0);
    while(true)

        %output value will give a rotary encoder reading (i.e. if this
        %doesn't change, it hasn't moved)
        [ljmError, value] = LabJack.LJM.eReadName(labjackhandle, name, 0);

        if value > 2^31
            value = value-2^32; %everything bigger than 2^31 is negative (matlab default)
        end

        %%%% NB// 1700 is the end of the linear track -- will need a non
        %%%% manual way of getting this
        %%%% will need to update these when know size of ball (i.e. 4096 and 62.8)
        %%%% 62.8 refers to wheel circumference
        %%%% 4096 refers to counts per cycle (Kubler)
        newPosition = (value/4096) * 62.8;
        timestamp = now;
        displacement = abs(newPosition - oldPosition);
        if displacement < 2
            LabJack.LJM.eWriteName(labjackhandle, 'DAC1', (displacement*5)/2);
        else
            LabJack.LJM.eWriteName(labjackhandle, 'DAC1', 5.0);
        end

        oldPosition = newPosition;
        fwrite(fid, [timestamp, newPosition], 'double');
    end
end

function myCleanupFun(labjackhandle, fid)
% Close labjack
    LabJack.LJM.eWriteName(labjackhandle, 'DAC0', 5.0);
    pause(0.1);
    LabJack.LJM.eWriteName(labjackhandle, 'DAC0', 0);
    LabJack.LJM.Close(labjackhandle);
    fclose(fid);
    disp('closed')
end


