import math

# Format: (j1, j2, j3, j4, j5, j6, hovering, gripper_state (True = closed, False = open))

# Define all the positions as variables
home = (
    math.radians(-180), math.radians(-57), math.radians(-115), 
    math.radians(-90), math.radians(90), math.radians(360), False, True
)
home_go = (
    math.radians(-180), math.radians(-57), math.radians(-115), 
    math.radians(-90), math.radians(90), math.radians(360), False, False
)
home_go_hover = (
    math.radians(-216), math.radians(-70), math.radians(-115), 
    math.radians(-35), math.radians(90), math.radians(358), True, False
)

pos_pick_body = (
    math.radians(-250.72), math.radians(-80.11), math.radians(-131.58), 
    math.radians(-55.62), math.radians(90.93), math.radians(21.03), False, True
)
pos_pick_body_go = (
    math.radians(-250.72), math.radians(-80.11), math.radians(-131.58), 
    math.radians(-55.62), math.radians(90.93), math.radians(21.03), False, False
)

pos_pick_body_h = (
    math.radians(-161.11), math.radians(-80.25), math.radians(88.73), 
    math.radians(-96.03), math.radians(-88.74), math.radians(17.36), False, True
)
pos_pick_body_h_go = (
    math.radians(-161.11), math.radians(-80.25), math.radians(88.73), 
    math.radians(-96.03), math.radians(-88.74), math.radians(17.36), False, False
)


pos_pick_body_app = (
    math.radians(-160), math.radians(-60), math.radians(-105), 
    math.radians(-100), math.radians(88), math.radians(15), False, True
)
pos_pick_body_app_go = (
    math.radians(-160), math.radians(-60), math.radians(-105), 
    math.radians(-100), math.radians(88), math.radians(15), False, False
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
    math.radians(-159.96), math.radians(-75.8), math.radians(97.96), 
    math.radians(-109.73), math.radians(-88.74), math.radians(18.52), False, True
)
pos_pick_top_go = (
    math.radians(-159.96), math.radians(-75.8), math.radians(97.96), 
    math.radians(-109.73), math.radians(-88.74), math.radians(18.52), False, False
)

pos_pick_top_h = (
    math.radians(-159.98), math.radians(-79.29), math.radians(85.76), 
    math.radians(-94.04), math.radians(-88.7), math.radians(18.5), False, True
)
pos_pick_top_h_go = (
    math.radians(-159.98), math.radians(-79.29), math.radians(85.76), 
    math.radians(-94.04), math.radians(-88.7), math.radians(18.5), False, False
)

pos_place_top = (
    math.radians(37.49), math.radians(-63.67), math.radians(130.51), 
    math.radians(-205.46), math.radians(-120.62), math.radians(293.30), False, True
)
pos_place_top_go = (
    math.radians(37.49), math.radians(-63.67), math.radians(130.51), 
    math.radians(-205.46), math.radians(-120.62), math.radians(293.30), False, False
)

pos_place_top_h_go = (
    math.radians(32.26), math.radians(-80.92), math.radians(113.95), 
    math.radians(-168.1), math.radians(-114.37), math.radians(289.86), False, False
)
pos_place_top_h = (
    math.radians(32.26), math.radians(-80.92), math.radians(113.95), 
    math.radians(-168.1), math.radians(-114.37), math.radians(289.86), False, True
)



pos_place_top_rem = (
    math.radians(43.01), math.radians(-64.38), math.radians(140.24), 
    math.radians(-220.2), math.radians(-123.5), math.radians(291.3), False, True
)

pos_place_top_rem_go = (
    math.radians(43.01), math.radians(-64.38), math.radians(140.24), 
    math.radians(-220.2), math.radians(-123.5), math.radians(291.3), False, False
)

