
import xml.etree.ElementTree as ET
import math

def modify_sdf(rbt_def, sdp_x_std, frame_names = [], filename='psm.sdf'):
    frame_num = rbt_def.frame_num

    x = sdp_x_std

    if len(frame_names) == 0:
        return

    tree = ET.parse(filename)
    root = tree.getroot()
    model = root[0]

    fric_num = len(rbt_def.friction_type)

    g = 0

    for i in range(frame_num):
        for link in model.findall('link'):
            if frame_names[i] == link.get('name'):
                inertial = link.find('inertial')
                pose = inertial.find('pose')
                inertia = inertial.find('inertia')
                mass = inertial.find('mass')

                # Input Inertia
                if rbt_def.use_inertia[i]:
                    for j in range(6):
                        inertia[j].text = str(math.fabs(sdp_x_std[g]))
                        g += 1

                    # Input Pose
                    text = pose.text
                    w, y, z, rot1, rot2, rot3 = text.split()
                    string = "{} {} {} {} {} {}".format(x[g], x[g+1], x[g+2], rot1, rot2, rot3)
                    pose.text = string
                    g = g + 3

                    # Input Mass
                    mass.text = str(sdp_x_std[g])
                    g += 1

                # If Friction Increment
                if rbt_def.use_friction[i]:
                    g = g + fric_num

                if rbt_def.use_Ia[i]:
                    g += 1

    tree.write('psm_new.sdf')