clear all
mylego = legoev3('usb');
motorA = motor(mylego, 'A');
motorB = motor(mylego, 'B');
sonic_sensor = sonicSensor(mylego,1);
gyro_sensor = gyroSensor(mylego, 2);
resetRotationAngle(gyro_sensor);
gyro_data = [];
gyro_data(1) = 0;
gyro_rate_data = [];
gyro_rate_data(1) = readRotationRate(gyro_sensor)-5;
start(motorA);
start(motorB);
encoder_A_data = [];
encoder_B_data = [];
encoder_A_data(1) = readRotation(motorA);
encoder_B_data(1) = readRotation(motorB);
speed_A_vector = [];
speed_B_vector = [];
speed_A_vector(1) = 0;
speed_B_vectorr(1) = 0;
time_step = 0.1;
x = [0];
y = [0];
state = 'None';
turn_numbers = 100;
elapsedTime = [0];
for i = 2:700
    elapsedTime(i) = elapsedTime(i-1) + time_step;
    tic;
    pause(0.07)
    gyro_rate_data(i) = readRotationRate(gyro_sensor)-5;
    gyro_data(i) = gyro_data(i-1) + gyro_rate_data(i)*time_step;
    encoder_A_data(i) = readRotation(motorA);
    encoder_B_data(i) = readRotation(motorB);
    prev_state = state;
    if readDistance(sonic_sensor) > 0.5 && turn_numbers > 25
        state = 'Drive';
    else 
        state = 'Turn';
        if turn_numbers > 25
            turn_numbers = 0;
            random_turn_number = rand - 0.5
        else 
            turn_numbers = turn_numbers + 1;
        end
    end
    switched_state = ~strcmp(state,prev_state);
    speed_A = (encoder_A_data(i) - encoder_A_data(i-1))/time_step;
    speed_A_vector(i) = speed_A;
    speed_B = (encoder_B_data(i) - encoder_B_data(i-1))/time_step;
    speed_B_vector(i) = speed_B;
    if switched_state
        resetRotation(motorA)
        speed_A = 0;
        encoder_A_data(i) = 0;
        resetRotation(motorB)
        speed_B = 0;
        encoder_B_data(i) = 0;
    end
    
    switch state
        case 'Drive'
            %'Driving'
            motorA.Speed = I_cruise_control_A(-150, speed_A, time_step, switched_state);
            motorB.Speed = I_cruise_control_B(-150, speed_B, time_step, switched_state);
            x(i) = x(i-1) + (-(speed_A + speed_B)*pi/180)/2*0.0275*cos(gyro_data(i)*pi/180)*time_step;
            y(i) = y(i-1) + (-(speed_A + speed_B)*pi/180)/2*0.0275*sin(gyro_data(i)*pi/180)*time_step;
        case 'Turn'
            %'Turning'
            motorA.Speed = I_cruise_control_A(sign(random_turn_number)*50, speed_A, time_step, switched_state);
            motorB.Speed = I_cruise_control_B(sign(random_turn_number)-50, speed_B, time_step, switched_state);
            x(i) = x(i-1);
            y(i) = y(i-1);
        case 'None'
            'error, state not set'
    end
    time_step = toc;
end

resetRotation(motorA)
resetRotation(motorB)
stop(motorA)
stop(motorB)

ts = trackingScenario;
wayPoints= [x;y;ones(1,size(x,2))]';
target = platform(ts);
traj = waypointTrajectory('Waypoints',wayPoints,'TimeOfArrival',elapsedTime);
target.Trajectory = traj;
r = record(ts);
pposes = [r(:).Poses];
pposition = vertcat(pposes.Position);
tp = theaterPlot('XLim',[min(x)-0.5 max(x)+0.5],'YLim',[min(y)-0.5 max(y)+0.5]);
trajPlotter = trajectoryPlotter(tp,'DisplayName','Trajectory');
plotTrajectory(trajPlotter,{pposition})

restart(ts);
trajPlotter = platformPlotter(tp,'DisplayName','Platform');

while advance(ts)
    p = pose(target,'true');
    plotPlatform(trajPlotter, p.Position);
    pause(0.1)

end


    