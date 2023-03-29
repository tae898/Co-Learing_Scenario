from matrx.agents.agent_types.human_agent import HumanAgentBrain
from matrx.agents.agent_types.patrolling_agent import PatrollingAgentBrain
from matrx.logger.log_agent_actions import LogActions
from matrx.logger.log_idle_agents import LogIdleAgents
from loggers.learning_logger import LearningLogger
from loggers.action_logger import ActionLogger
from matrx.world_builder import WorldBuilder
from matrx.actions.move_actions import *
from matrx.actions.object_actions import *
from matrx.actions.door_actions import *
from matrx.world_builder import RandomProperty
from matrx.objects.standard_objects import *
from USAR_Goal import USAR_Goal
from custom_objects import *
from custom_agents import *
from robot_partner import *
from ontology_god import *
from custom_actions import *
import random
import os
from datetime import datetime

block_size = 1
block_colors = ['#DCDDDC', '#D3D2D2', '#A9A9A9']
rock_imgs = ['/images/rock1.png', '/images/rock2.png', '/images/rock3.png']
long_rock_imgs = ['/images/longrock1.png', '/images/longrock2.png', '/images/longrock3.png']
vert_rock_imgs = ['/images/vertrock1.png', '/images/vertrock2.png', '/images/vertrock3.png']
brownlong_imgs = ['/images/brownlong1.png', '/images/brownlong2.png', '/images/brownlong3.png']
brownvert_imgs = ['/images/brownvert1.png', '/images/brownvert2.png', '/images/brownvert3.png']
lower_bound = 11
left_bound = 5
right_bound = 15
upper_bound = 1

rock_img_property = RandomProperty(values=rock_imgs)
long_rock_img_property = RandomProperty(values=long_rock_imgs)
vert_rock_img_property = RandomProperty(values=vert_rock_imgs)
brownlong_img_property = RandomProperty(values=brownlong_imgs)
brownvert_img_property = RandomProperty(values=brownvert_imgs)

rubble_locations = []
for y_loc in range(upper_bound, lower_bound):
    for x_loc in range(left_bound, right_bound):
        rubble_locations.append((x_loc, y_loc))


def create_builder():
    factory = WorldBuilder(shape=[20, 12], run_matrx_visualizer=False, visualization_bg_clr="#ffffff",
                           visualization_bg_img='/images/background.png', tick_duration=0.05, simulation_goal=USAR_Goal())

    # Add loggers
    current_exp_folder = datetime.now().strftime("exp_at_time_%Hh-%Mm-%Ss_date_%dd-%mm-%Yy")
    logger_save_folder = os.path.join("experiment_logs", current_exp_folder)

    factory.add_logger(logger_class=ActionLogger, save_path=logger_save_folder, file_name_prefix="actions_")
    factory.add_logger(logger_class=LogIdleAgents, save_path=logger_save_folder, file_name_prefix="idle_")
    factory.add_logger(logger_class=LearningLogger, save_path=logger_save_folder, file_name_prefix="qtable_")

    # Link agent names to agent brains
    human_agent = CustomHumanAgentBrain(max_carry_objects=1, grab_range=1)
    autonomous_agent = PatrollingAgentBrain(waypoints=[(0, 0), (0, 7)])
    robot_partner = RobotPartner(move_speed=10)

    human_img = AvatarAgent()
    machine_img = AvatarAgent()
    victim_img = VictimAgent()
    gravity_god = GravityGod()
    reward_god = RewardGod()
    ontology_god = OntologyGod()

    key_action_map = {
        'ArrowUp': MoveNorth.__name__,
        'ArrowRight': MoveEast.__name__,
        'ArrowDown': MoveSouth.__name__,
        'ArrowLeft': MoveWest.__name__,
        'b': GrabObject.__name__,
        'n': DropObject.__name__,
        #'r': RemoveObject.__name__,
        #'l': GrabLargeObject.__name__,
        #'m': DropLargeObject.__name__,
        #'b': BreakObject.__name__
    }

    # Add the selector agent that allows humans to interact
    factory.add_human_agent([3, 4], human_agent, name="Human Selector", key_action_map=key_action_map,
                            visualize_shape='img', img_name="/images/selector.png", visualize_size=1, is_traversable=True, customizable_properties=["img_name"])

    # Add agents that are static and mostly just show the image of the 'actual' agent
    factory.add_agent([1, 7], human_img, name="Human", visualize_shape='img',
                            img_name="/images/human_square.png", visualize_size=4, visualize_from_center=False, is_traversable=True)
    factory.add_agent([15, 7], machine_img, name="Machine", visualize_shape='img',
                            img_name="/images/machine_square.png", visualize_size=4, visualize_from_center=False, is_traversable=True)
    factory.add_agent([8, 7], victim_img, name="Victim", visualize_shape='img',
                            img_name="/images/victim_square.png", visualize_size=4, visualize_from_center=False, is_traversable=True, visualize_depth=0)

    # Add Gravity by adding the GravityGod agent
    factory.add_agent((0, 0), gravity_god, name="GravityGod", visualize_shape='img', img_name="/images/transparent.png", is_traversable=True)

    # Add Reward by adding the RewardGod agent
    #factory.add_agent((0,0), reward_god, name="RewardGod", visualize_shape='img', img_name="/images/transparent.png", is_traversable=True, goal_reached=False, customizable_properties=["goal_reached"])

    # Add Ontology functions by adding the OntologyGod agent
    factory.add_agent((0,0), ontology_god, name="OntologyGod", visualize_shape='img', img_name="/images/transparent.png", is_traversable=True)

    # factory.add_agent([0,2], autonomous_agent, name="Robot", visualize_shape='img',
    #                   img_name="/images/machine_square.png", visualize_size=2)

    # Add the actual Robot Partner
    factory.add_agent((4,4), robot_partner, name="Robot Selector", visualize_shape='img', img_name="/images/selector2.png", visualize_size=1, is_traversable=True, q_table=None, customizable_properties=["q_table", "img_name"])

    #generate_rubble_pile(name="test_pile", locations=rubble_locations, world=factory)

    #create_brownlong_object(name="test_obstr", location=(16,1), world=factory)
    #create_brownvert_object(name="test_obstr2", location=(16, 3), world=factory)

    #lvl_practice(factory)              # Practice scenario


    lvl_dont_break(factory)            # First scenario

    #lvl_dont_break_2(factory)          # Don't break 2

    #lvl_dont_break_3(factory)          # Don't break 3

    #lvl_dont_break_4(factory)          # Don't break 4


    #lvl_building_bridges(factory)      # Third scenario


    #lvl_looming_spike(factory)         # Second scenario

    #lvl_brown_rock_2(factory)          # Brown rock 2

    #lvl_brown_rock_3(factory)          # Brown rock 3

    #lvl_building_bridges_edited(factory)   # Brown rock 4

    factory.add_object([2,0], name="goal_reached_img", img_name="/images/transparent.png", callable_class=GoalReachedObject, visualize_depth=300)

    return factory


def create_large_object(name, location, world):
    x_loc = location[0]
    y_loc = location[1]

    img_part = "/images/transparent.png"
    world.add_object(location, name="Part_tl_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc+1, y_loc), name="Part_tr_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc, y_loc+1), name="Part_bl_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc+1, y_loc+1), name="Part_br_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)

    world.add_object(location, name=name, img_name=rock_img_property, callable_class=LargeObject)


def create_long_object(name, location, world):
    x_loc = location[0]
    y_loc = location[1]

    img_part = "/images/transparent.png"

    world.add_object(location, name="Part_t1_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc + 1, y_loc), name="Part_t2_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc + 2, y_loc), name="Part_t3_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc + 3, y_loc), name="Part_t4_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)

    world.add_object(location, name=name, img_name=long_rock_img_property, callable_class=LargeObject, visualize_size=4, long=True)


def create_vert_object(name, location, world):
    x_loc = location[0]
    y_loc = location[1]

    img_part = "/images/transparent.png"

    world.add_object(location, name="Part_t1_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc, y_loc + 1), name="Part_t2_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc, y_loc + 2), name="Part_t3_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc, y_loc + 3), name="Part_t4_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)

    world.add_object(location, name=name, img_name=vert_rock_img_property, callable_class=LargeObject, visualize_size=4, vert=True)


def create_brownlong_object(name, location, world):
    x_loc = location[0]
    y_loc = location[1]

    img_part = "/images/transparent.png"

    world.add_object(location, name="Part_t1_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc + 1, y_loc), name="Part_t2_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc + 2, y_loc), name="Part_t3_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc + 3, y_loc), name="Part_t4_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)

    world.add_object(location, name=name, img_name=brownlong_img_property, callable_class=ObstructionObject, visualize_size=4, long=True)


def create_brownvert_object(name, location, world):
    x_loc = location[0]
    y_loc = location[1]

    img_part = "/images/transparent.png"

    world.add_object(location, name="Part_t1_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc, y_loc + 1), name="Part_t2_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc, y_loc + 2), name="Part_t3_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)
    world.add_object((x_loc, y_loc + 3), name="Part_t4_" + name, img_name=img_part, callable_class=PartLargeObject,
                     bound_to=name)

    world.add_object(location, name=name, img_name=brownvert_img_property, callable_class=ObstructionObject, visualize_size=4,
                     vert=True)


def generate_rubble_pile(name, locations, world):
    possible_locations = locations[:]
    random.shuffle(possible_locations)
    for items in range(0, 3):
        initial_loc = possible_locations[0]
        ix_loc = initial_loc[0]
        iy_loc = initial_loc[1]
        loc_to_check = {initial_loc, (ix_loc + 1, iy_loc), (ix_loc + 2, iy_loc), (ix_loc + 3, iy_loc)}
        if loc_to_check <= set(possible_locations):
            create_long_object(name="long_" + str(items), location=initial_loc, world=world)
        for locs in loc_to_check:
            if locs in possible_locations:
                possible_locations.remove(locs)
    for items in range(0, 3):
        initial_loc = possible_locations[0]
        ix_loc = initial_loc[0]
        iy_loc = initial_loc[1]
        loc_to_check = {initial_loc, (ix_loc, iy_loc + 1), (ix_loc, iy_loc + 2), (ix_loc, iy_loc + 3)}
        if loc_to_check <= set(possible_locations):
            create_vert_object(name="vert_" + str(items), location=initial_loc, world=world)
        for locs in loc_to_check:
            if locs in possible_locations:
                possible_locations.remove(locs)
    for items in range(0, 8):
        initial_loc = possible_locations[0]
        ix_loc = initial_loc[0]
        iy_loc = initial_loc[1]
        loc_to_check = {initial_loc, (ix_loc+1, iy_loc), (ix_loc, iy_loc+1), (ix_loc+1, iy_loc+1)}
        if loc_to_check <= set(possible_locations):
            create_large_object(name="large_"+str(items), location=initial_loc, world=world)
        for locs in loc_to_check:
            if locs in possible_locations:
                possible_locations.remove(locs)
    for items in range(0, 30):
        loc = possible_locations.pop()
        world.add_object(loc, name=name, visualize_shape='img', img_name=rock_img_property,
                         is_traversable=True, is_movable=True)


#--------------------------------------------- Level Configurations ----------------------------------------------------
def lvl_practice(factory):
    create_vert_object(name="vert1", location=(7, 7), world=factory)

    create_long_object(name="long1", location=(8, 7), world=factory)

    create_large_object(name="large1", location=(9, 3), world=factory)
    create_large_object(name="large2", location=(12, 6), world=factory)
    create_large_object(name="large3", location=(10, 8), world=factory)
    create_large_object(name="large4", location=(8, 9), world=factory)

    factory.add_object((9, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 6), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 6), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 6), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((11, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((13, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)

def lvl_dont_break(factory):
    create_vert_object(name="vert1", location=(7, 2), world=factory)

    create_long_object(name="long1", location=(5, 6), world=factory)
    create_long_object(name="long2", location=(9, 6), world=factory)
    create_long_object(name="long3", location=(11, 7), world=factory)

    create_large_object(name="large1", location=(8, 4), world=factory)
    create_large_object(name="large2", location=(11, 4), world=factory)
    create_large_object(name="large3", location=(12, 9), world=factory)

    factory.add_object((8, 3), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 4), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((13, 6), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((6, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((6, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((5, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((11, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)

# Don't break 1
def lvl_dont_break_2(factory):
    create_vert_object(name="vert1", location=(10, 4), world=factory)

    create_long_object(name="long1", location=(8, 9), world=factory)

    create_large_object(name="large1", location=(12, 9), world=factory)

    factory.add_object((10, 3), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((11, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((6, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((14, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)

def lvl_dont_break_3(factory):
    create_long_object(name="long1", location=(5, 6), world=factory)
    create_long_object(name="long2", location=(10, 8), world=factory)

    create_large_object(name="large1", location=(8, 4), world=factory)
    create_large_object(name="large2", location=(9, 6), world=factory)
    create_large_object(name="large3", location=(11, 9), world=factory)

    factory.add_object((8, 2), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 3), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 3), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 4), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 4), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((5, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((6, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((11, 6), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((11, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((13, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((6, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((6, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((5, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((6, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((13, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)

def lvl_dont_break_4(factory):
    create_vert_object(name="vert1", location=(8, 4), world=factory)
    create_vert_object(name="vert2", location=(11, 1), world=factory)

    create_long_object(name="long1", location=(6, 8), world=factory)

    create_large_object(name="large1", location=(6, 6), world=factory)
    create_large_object(name="large2", location=(11, 5), world=factory)
    create_large_object(name="large3", location=(12, 9), world=factory)

    factory.add_object((7, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 4), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((6, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((14, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)

# Brown rock 1
def lvl_looming_spike(factory):
    create_brownvert_object(name="brownvert1", location=(11, 1), world=factory)

    create_long_object(name="long1", location=(7, 6), world=factory)
    create_long_object(name="long2", location=(10, 5), world=factory)

    create_vert_object(name="vert1", location=(7, 7), world=factory)

    create_large_object(name="large1", location=(9, 3), world=factory)
    create_large_object(name="large2", location=(11, 6), world=factory)
    create_large_object(name="large3", location=(9, 9), world=factory)

    factory.add_object((8, 4), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((5, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((6, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((6, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((11, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)

def lvl_brown_rock_2(factory):
    create_brownlong_object(name="brownlong1", location=(9, 8), world=factory)

    create_large_object(name="large1", location=(9, 6), world=factory)
    create_large_object(name="large2", location=(5, 9), world=factory)
    create_large_object(name="large3", location=(7, 9), world=factory)

    factory.add_object((9, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((11, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((13, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)

def lvl_brown_rock_3(factory):
    create_brownlong_object(name="brownlong1", location=(7, 2), world=factory)

    create_brownvert_object(name="brownvert1", location=(11, 1), world=factory)

    create_vert_object(name="vert1", location=(7, 7), world=factory)

    create_long_object(name="long1", location=(10, 5), world=factory)
    create_long_object(name="long2", location=(7, 6), world=factory)

    create_large_object(name="large1", location=(9, 3), world=factory)
    create_large_object(name="large2", location=(11, 6), world=factory)
    create_large_object(name="large3", location=(9, 9), world=factory)

    factory.add_object((8, 3), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 4), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((6, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 9), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((5, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((6, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((11, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((12, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)

# Brown rock 4
def lvl_building_bridges_edited(factory):
    create_brownlong_object(name="brownlong1", location=(6, 2), world=factory)
    create_brownlong_object(name="brownlong2", location=(10, 4), world=factory)

    create_long_object(name="long1", location=(9, 10), world=factory)

    create_large_object(name="large2", location=(8, 3), world=factory)
    create_large_object(name="large3", location=(6, 9), world=factory)
    create_large_object(name="large4", location=(8, 8), world=factory)
    create_large_object(name="large5", location=(12, 8), world=factory)

    factory.add_object((8, 1), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((10, 3), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((11, 3), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((13, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((13, 6), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((13, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 6), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((13, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)

def lvl_building_bridges(factory):
    create_brownlong_object(name="brownlong1", location=(6, 3), world=factory)
    create_brownlong_object(name="brownlong2", location=(10, 4), world=factory)

    create_long_object(name="long1", location=(9, 10), world=factory)

    create_large_object(name="large1", location=(7, 1), world=factory)
    create_large_object(name="large2", location=(8, 4), world=factory)
    create_large_object(name="large3", location=(6, 9), world=factory)
    create_large_object(name="large4", location=(8, 8), world=factory)
    create_large_object(name="large5", location=(11, 8), world=factory)

    factory.add_object((10, 3), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((11, 3), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((11, 5), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((11, 6), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((11, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 6), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((9, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 7), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((7, 8), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)
    factory.add_object((8, 10), name="rock1", visualize_shape='img', img_name=rock_img_property, is_traversable=True,
                       is_movable=True)


