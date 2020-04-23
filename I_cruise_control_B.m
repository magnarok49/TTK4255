function u = I_cruise_control_B(desired_speed, measured_speed, time_step, reset_integral)
    ki = 0.3;
    kp = 0;
    persistent integral
    if isempty(integral)
        integral = 0;
    end
    if reset_integral
        integral = 0;
    end
    integral = integral + (desired_speed - measured_speed)*time_step
    proportional = desired_speed - measured_speed;
    u = ki*integral + proportional*kp;
end

