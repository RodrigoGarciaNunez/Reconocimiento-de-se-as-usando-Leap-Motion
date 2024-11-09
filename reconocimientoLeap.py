import Leap
from Leap import KeyTapGesture
import math

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print ("Initialized")

    def on_connect(self, controller):
        print ("Connected")

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print ("Disconnected")

    def on_exit(self, controller):
        print ("Exited")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        print ("Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures())))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            #print ("  %s, id %d, position: %s" % (
            #    handType, hand.id, hand.palm_position))

            # Get the hand's normal vector and direction
            normal = hand.palm_normal   #la normal!!!!
            direction = hand.direction 

            # Calculate the hand's pitch, roll, and yaw angles
            #print ("  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
            #    direction.pitch * Leap.RAD_TO_DEG,
            #    normal.roll * Leap.RAD_TO_DEG,
            #    direction.yaw * Leap.RAD_TO_DEG))

            # Get arm bone
            arm = hand.arm
            #print ("  Arm direction: %s, wrist position: %s, elbow position: %s" % (
            #    arm.direction,
            #    arm.wrist_position,
            #    arm.elbow_position))

            
            # Get fingers
            for finger in hand.fingers:

                #print ("    %s finger, id: %d, length: %fmm, width: %fmm" % (
                #    self.finger_names[finger.type],
                #    finger.id,
                #    finger.length,
                #    finger.width))

                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    #print ("      Bone: %s, start: %s, end: %s, direction: %s" % (
                    #    self.bone_names[bone.type],
                    #    bone.prev_joint,
                    #    bone.next_joint,
                    #    bone.direction))

        # Get tools
        for tool in frame.tools:

            print ("  Tool id: %d, position: %s, direction: %s" % (
                tool.id, tool.tip_position, tool.direction))

        # Get gestures
        for gesture in frame.gestures():

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                print ("  Key Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state],
                        keytap.position, keytap.direction ))
                
                #angulos
                # Get hands
                for hand in frame.hands:

                    handType = "Left hand" if hand.is_left else "Right hand"

                    if hand.is_left:
                        
                        print ("  %s, id %d, position: %s" % (
                        handType, hand.id, hand.palm_position))

                        # Get the hand's normal vector and direction
                        normal = hand.palm_normal #la normal!
                        direction = hand.direction

                        # Calculate the hand's pitch, roll, and yaw angles
                        print ("  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                        direction.pitch * Leap.RAD_TO_DEG,
                        normal.roll * Leap.RAD_TO_DEG,
                        direction.yaw * Leap.RAD_TO_DEG))

                        # Get arm bone
                        arm = hand.arm
                        print ("  Arm direction: %s, wrist position: %s, elbow position: %s" % (
                        arm.direction,
                        arm.wrist_position,
                        arm.elbow_position))

                        angulosregistro=[]
                    # Get fingers
                    
                        for finger in hand.fingers:

                            print ("    %s finger, id: %d, length: %fmm, width: %fmm" % (
                                self.finger_names[finger.type],
                                finger.id,
                                finger.length,
                                finger.width))

                            # Get bones
                            for b in range(0, 4):
                                bone = finger.bone(b)
                                print ("      Bone: %s, start: %s, end: %s, direction: %s" % (
                                self.bone_names[bone.type],
                                bone.prev_joint,
                                bone.next_joint,
                                bone.direction))

                                angulo = normal.angle_to(bone.direction)
                                angulo *= (180/math.pi)
                                print(angulo)
                                angulosregistro.append(angulo)

                
                        f = open('senas.txt', 'a')
                    #f.write('Hola, senal registrada: ')
                        for angulo in angulosregistro:
                            f.write("%s, " % angulo)
                
                        sena = input("Por favor, ingresa la etiqueta de la senal (1-piedra, 2- papel, 3- tijera): ")
                        f.write("%s\n" % sena)
                    #f.write(angulosregistro)
                        f.close()

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ("")

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"