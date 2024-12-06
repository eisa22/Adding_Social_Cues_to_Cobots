import math

# Format: (j1, j2, j3, j4, j5, j6, hovering, gripper_state (True = closed, False = open))

# Define all the positions as variables
home = (
    math.radians(-180), math.radians(-45), math.radians(-120), 
    math.radians(-105), math.radians(90), math.radians(357), False, True
)
home_go = (
    math.radians(-180), math.radians(-45), math.radians(-120), 
    math.radians(-105), math.radians(90), math.radians(357), False, False
)
home_go_hover = (
    math.radians(-180), math.radians(-45), math.radians(-120), 
    math.radians(-105), math.radians(90), math.radians(357), True, False
)

pos_pick_body = (
    math.radians(-249.05), math.radians(-80.15), math.radians(-132.07), 
    math.radians(-55.4), math.radians(89.07), math.radians(20.45), False, True
)
pos_pick_body_go = (
    math.radians(-249.05), math.radians(-80.15), math.radians(-132.07), 
    math.radians(-55.4), math.radians(89.07), math.radians(20.45), False, False
)

pos_pick_body_h = (
    math.radians(-249.02), math.radians(-72.33), math.radians(-111.54), 
    math.radians(-83.76), math.radians(89.07), math.radians(20.4), False, True
)
pos_pick_body_h_go = (
    math.radians(-249.02), math.radians(-72.33), math.radians(-111.54), 
    math.radians(-83.76), math.radians(89.07), math.radians(20.4), False, False
)


pos_pick_body_app = (
    math.radians(-145.67), math.radians(-56), math.radians(-110), 
    math.radians(-104), math.radians(89), math.radians(124), False, True
)
pos_pick_body_app_go = (
    math.radians(-145.67), math.radians(-56), math.radians(-110), 
    math.radians(-104), math.radians(89), math.radians(124), False, False
)


pos_place_body = (
    math.radians(-92.44), math.radians(-102.8), math.radians(-124.9), 
    math.radians(-41.1), math.radians(37), math.radians(180), False, True
)
pos_place_body_go = (
    math.radians(-92.44), math.radians(-102.8), math.radians(-124.9), 
    math.radians(-41.1), math.radians(37), math.radians(180), False, False
)

pos_place_body_h = (
    math.radians(-95), math.radians(-97.6), math.radians(-119), 
    math.radians(-49), math.radians(34), math.radians(172), False, True
)
pos_place_body_h_go = (
    math.radians(-95), math.radians(-97.6), math.radians(-119), 
    math.radians(-49), math.radians(34), math.radians(172), False, False
)

pos_place_body_rem = (
    math.radians(-83.58), math.radians(-89.22), math.radians(-125.34), 
    math.radians(-62.8), math.radians(39.6), math.radians(189), False, True
)
pos_place_body_rem_go = (
    math.radians(-83.58), math.radians(-89.22), math.radians(-125.34), 
    math.radians(-62.8), math.radians(39.6), math.radians(189), False, False
)






pos_pick_top = (
    math.radians(-277.48), math.radians(-94.38), math.radians(-111.22), 
    math.radians(-66.13), math.radians(89.41), math.radians(353.27), False, True
)
pos_pick_top_go = (
    math.radians(-277.48), math.radians(-94.38), math.radians(-111.22), 
    math.radians(-66.13), math.radians(89.41), math.radians(353.27), False, False
)

pos_pick_top_h = (
    math.radians(-277.45), math.radians(-89.46), math.radians(-90.7), 
    math.radians(-91.6), math.radians(89.4), math.radians(353.2), False, True
)
pos_pick_top_h_go = (
    math.radians(-277.45), math.radians(-89.46), math.radians(-90.7), 
    math.radians(-91.6), math.radians(89.4), math.radians(353.2), False, False
)

pos_place_top = (
    math.radians(-96.33), math.radians(-95.18), math.radians(-122.0), 
    math.radians(-42.91), math.radians(46.72), math.radians(168.51), False, True
)
pos_place_top_go = (
    math.radians(-96.33), math.radians(-95.18), math.radians(-122.0), 
    math.radians(-42.91), math.radians(46.72), math.radians(168.51), False, False
)

pos_place_top_h_go = (
    math.radians(-97.23), math.radians(-92.34), math.radians(-118.2), 
    math.radians(-46), math.radians(39), math.radians(165), False, False
)
pos_place_top_h = (
    math.radians(-97.23), math.radians(-92.34), math.radians(-118.2), 
    math.radians(-46), math.radians(39), math.radians(165), False, True
)



pos_place_top_rem = (
    math.radians(-79.20), math.radians(-82.76), math.radians(-126.7), 
    math.radians(-67.05), math.radians(46.28), math.radians(192.16), False, True
)

pos_place_top_rem_go = (
    math.radians(-79.20), math.radians(-82.76), math.radians(-126.7), 
    math.radians(-67.05), math.radians(46.28), math.radians(192.16), False, False
)
