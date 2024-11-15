import math

# Format: (j1, j2, j3, j4, j5, j6, hovering, gripper_state (True = closed, False = open))

# Define all the positions as variables
home = (
    math.radians(-216), math.radians(-70), math.radians(-115), 
    math.radians(-35), math.radians(90), math.radians(358), False, True
)
home_go = (
    math.radians(-216), math.radians(-70), math.radians(-115), 
    math.radians(-35), math.radians(90), math.radians(358), False, False
)

pos_pick_body = (
    math.radians(-161.09), math.radians(-74.80), math.radians(102.73), 
    math.radians(-115.48), math.radians(-88.81), math.radians(17.4), False, False
)
pos_pick_body_go = (
    math.radians(-161.09), math.radians(-74.80), math.radians(102.73), 
    math.radians(-115.48), math.radians(-88.81), math.radians(17.4), False, True
)

pos_pick_body_h = (
    math.radians(-159.48), math.radians(-83.09), math.radians(93.52), 
    math.radians(-103.03), math.radians(-90.31), math.radians(19.10), False, True
)
pos_pick_body_h_go = (
    math.radians(-159.48), math.radians(-83.09), math.radians(93.52), 
    math.radians(-103.03), math.radians(-90.31), math.radians(19.10), False, False
)


pos_pick_body_app = (
    math.radians(-19.41), math.radians(-144.94), math.radians(126.34), 
    math.radians(-90.41), math.radians(-84.28), math.radians(252.25), False, True
)
pos_pick_body_app_go = (
    math.radians(-19.41), math.radians(-144.94), math.radians(126.34), 
    math.radians(-90.41), math.radians(-84.28), math.radians(252.25), False, False
)


pos_place_body = (
    math.radians(34.44), math.radians(-64.90), math.radians(88.04), 
    math.radians(14.81), math.radians(116.74), math.radians(108.79), False, True
)
pos_place_body_go = (
    math.radians(34.44), math.radians(-64.90), math.radians(88.04), 
    math.radians(14.81), math.radians(116.74), math.radians(108.79), False, False
)

pos_place_body_h = (
    math.radians(32.55), math.radians(-63.67), math.radians(77.45), 
    math.radians(25.91), math.radians(115.03), math.radians(108.84), False, True
)
pos_place_body_h_go = (
    math.radians(32.55), math.radians(-63.67), math.radians(77.45), 
    math.radians(25.91), math.radians(115.03), math.radians(108.84), False, False
)

pos_place_body_rem = (
    math.radians(41.42), math.radians(-72.37), math.radians(89.07), 
    math.radians(27.2), math.radians(119.7), math.radians(117.0), False, True
)
pos_place_body_rem_go = (
    math.radians(41.42), math.radians(-72.37), math.radians(89.07), 
    math.radians(27.2), math.radians(119.7), math.radians(117.0), False, False
)






pos_pick_top = (
    math.radians(-114), math.radians(-95), math.radians(-104), 
    math.radians(-45), math.radians(91), math.radians(20), False, True
)
pos_pick_top_go = (
    math.radians(-114), math.radians(-95), math.radians(-104), 
    math.radians(-45), math.radians(91), math.radians(20), False, False
)

pos_pick_top_h = (
    math.radians(-114), math.radians(-95), math.radians(-104), 
    math.radians(-45), math.radians(91), math.radians(20), False, True
)
pos_pick_top_h_go = (
    math.radians(-114), math.radians(-95), math.radians(-104), 
    math.radians(-45), math.radians(91), math.radians(20), False, False
)

pos_place_top = (
    math.radians(-30), math.radians(-130), math.radians(-104), 
    math.radians(-45), math.radians(90), math.radians(321), False, True
)
pos_place_top_go = (
    math.radians(-30), math.radians(-130), math.radians(-104), 
    math.radians(-45), math.radians(90), math.radians(321), False, False
)

pos_place_top_h = (
    math.radians(-30), math.radians(-120), math.radians(-104), 
    math.radians(-45), math.radians(90), math.radians(321), False, True
)
pos_place_top_h_go = (
    math.radians(-30), math.radians(-120), math.radians(-104), 
    math.radians(-45), math.radians(90), math.radians(321), False, False
)
