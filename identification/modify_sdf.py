
import xml.etree.ElementTree as ET
import math

def modify_sdf(rbt_def, sdp_x_std, frame_names = [], filename='psm.sdf', namespace = 'dvrk_psm', name = 'PSM1', filename_cfg='psm_friction.yaml'):
    frame_num = rbt_def.frame_num

    x = sdp_x_std

    if len(frame_names) == 0:
        return

    tree = ET.parse(filename)
    root = tree.getroot()
    model = root[0]

    fric_num = len(rbt_def.friction_type)

    g = 0

    myfile = open(filename_cfg, "w")
    myfile.write(namespace + ": \n")
    myfile.write("  " + name + ": \n")
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

                if rbt_def.use_friction[i]:
                    g = g + fric_num

                if rbt_def.use_Ia[i]:
                    g += 1

                #myfile.write("\n")

    tree.write('psm_new.sdf')

def add_trans_config(rbt_def, sdp_x_std, frame_names = [], namespace = 'dvrk_psm', name = 'PSM1', filename='psm_friction.yaml'):
    frame_num = rbt_def.frame_num

    x = sdp_x_std

    if len(frame_names) == 0:
        return

    g = 0
    myfile = open(filename, "w")
    myfile.write(namespace + ": \n")
    myfile.write("  " + name + ": \n")

    for i in range(frame_num):
        if frame_names[i] != ' ':
            if rbt_def.use_inertia[i]:
                g += 10

            # If Friction is modeled
            myfile.write("    " + frame_names[i] + ": \n")
            if 'Coulomb' in rbt_def.friction_type and rbt_def.use_friction[i]:
                z = "%f" % (sdp_x_std[g])
                myfile.write("      " + "Fc: " + z + "\n")
                g += 1
            else:
                myfile.write("      " + "Fc: " + "0\n")

            if 'viscous' in rbt_def.friction_type and rbt_def.use_friction[i]:
                z = "%f" % (sdp_x_std[g])
                myfile.write("      " + "Fv: " + z + "\n")
                g += 1
            else:
                myfile.write("      " + "Fv: " + "0\n")

            if 'offset' in rbt_def.friction_type and rbt_def.use_friction[i]:
                z = "%f" % (sdp_x_std[g])
                myfile.write("      " + "Fo: " + z + "\n")
                g += 1
            else:
                myfile.write("      " + "Fo: " + "0\n")

            # If Motor Inertia is modeled
            if rbt_def.use_Ia[i]:
                z = "%f" % (sdp_x_std[g])
                myfile.write("      " + "Ia: " + z + "\n")
                g += 1

            else:
                myfile.write("      " + "Ia: " + "0\n")


    myfile.close()



