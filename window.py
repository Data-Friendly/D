from tkinter import *
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

final_count = 0

# agility score and diet recomendation screen
def score_page(final_count):
        score = Frame()
        score.place(x=0, y=0, width=1000, height=600)
        score.configure(bg = "#ffffff")
        
        def btn_clicked():
            home_page()

        canvas = Canvas(
            score,
            bg = "#ffffff",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)
        
        global background_img_score
        background_img_score = PhotoImage(file = f"background_1.png")
        canvas.create_image(
            506.5, 239.0,
            image=background_img_score)

        canvas.create_text(
            360.0, 112.5,
            text = "YOUR AGILITY SCORE :",
            fill = "#000000",
            font = ("RalewayRoman-ExtraBold", int(35.0)))

        canvas.create_text(
            680, 109.5,
            text = "{}".format(final_count),
            fill = "#fa2121",
            font = ("RalewayRoman-Regular", int(40.0)))

        canvas.create_text(
            600, 191.5,
            text = "22",
            fill = "#fa2121",
            font = ("RalewayRoman-Regular", int(40.0)))

        canvas.create_text(
            320.0, 194.5,
            text = "EXPECTED SCORE :",
            fill = "#000000",
            font = ("RalewayRoman-ExtraBold", int(35.0)))

        canvas.create_text(
            164, 276.5,
            text = "DIET : ",
            fill = "#fa2121",
            font = ("RalewayRoman-ExtraBold", int(35.0)))

        canvas.create_text(
            184, 322.0,
            text = "THIS IS YOUR DIET",
            fill = "#000000",
            font = ("OpenSansRoman-Light", int(15.0)))
        
        global img0_score
        img0_score = PhotoImage(file = f"img0_1.png")
        b0 = Button(
            score,
            image = img0_score,
            borderwidth = 0,
            highlightthickness = 0,
            command = btn_clicked,
            relief = "flat")

        b0.place(
            x = 403, y = 466,
            width = 194,
            height = 57
            )
        

# calculate angles
def calculate_angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    # calculate angle between three points
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle_in_degrees = np.abs(radians*180.0/np.pi)
    
    # if angle is negetive because body movement is restricted to 180
    if angle_in_degrees > 180.0:
        angle_in_degrees = 360 - angle_in_degrees
    
    return angle_in_degrees

# Deep Learning Algo to count Squats
def squat_counter(entry0, entry1):
    cap = cv2.VideoCapture(0)

    # set the frame size
    def make_1080p():
        cap.set(3, 1920)
        cap.set(4, 1080)
        
    make_1080p()

    # get frame height and width
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT )

    # curl counter
    counter = 0
    stage = None
    results = None
    
    
    with mp_pose.Pose(min_detection_confidence = 0.7, min_tracking_confidence = 0.7) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolour image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Make detection
            results = pose.process(image)
            
            # Recolour image to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                    
                # get cordinates 
                # right side
                ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                # caculate angle
                knee_angle = calculate_angle(ankle, knee, hip)
                knee_angle = round(knee_angle , 2)

                hip_angle = calculate_angle(shoulder, hip, knee)
                hip_angle = round(hip_angle, 2)
                
                elbow_angle = calculate_angle(shoulder, elbow, wrist)
                elbow_angle = round(elbow_angle, 2)
                
                # print("Stage ===========> {}".format(stage))
                # print("hip angle {}".format(hip_angle))
                # print("knee angle {}".format(knee_angle))
                # print("elbow angle {}".format(elbow_angle))
                
                # visualize 
                cv2.putText(image, str(round(knee_angle, 1)),
                            tuple(np.multiply(knee, [width, height]).astype(int)),
                            cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255),2 ,cv2.LINE_AA
                        )
                cv2.putText(image, str(round(hip_angle, 1)),
                            tuple(np.multiply(hip, [width, height]).astype(int)),
                            cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255),2 ,cv2.LINE_AA
                        )
                cv2.putText(image, str(round(elbow_angle, 1)),
                            tuple(np.multiply(elbow, [width, height]).astype(int)),
                            cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255),2 ,cv2.LINE_AA
                        )
                
                # squat counter logic
                if knee_angle > 160 and hip_angle > 160:
                    stage = "up"
                if knee_angle < 90 and hip_angle < 90 and stage == 'up':
                    stage = "down"
                    counter += 1
                    print(counter)
            except:
                pass    
            
            # render curl counter 
            cv2.rectangle(image, (0,0), (225,73), (245, 117, 16), -1)
            cv2.putText(image, 'REPS', (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX,  1, (255, 255, 255), 2, cv2.LINE_AA)
            
            cv2.putText(image, 'STAGE', (65, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, (60, 60), cv2.FONT_HERSHEY_SIMPLEX,  1, (255, 255, 255), 2, cv2.LINE_AA)
            
            # render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
                                    ) 
            
            cv2.imshow('Mediapipe Feeed', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                final_count = counter
                break
            
    
            
    cap.release
    cv2.destroyAllWindows()

    print(entry0.get())
    print(entry1.get())
    score_page(final_count=final_count)


root = Tk()
root.geometry("1000x600")

def home_page():
    Home = Frame()
    Home.place(x=0, y=0, width=1000, height=600)
    Home.configure(bg = "#ffffff")
    canvas = Canvas(
        Home,
        bg = "#ffffff",
        height = 600,
        width = 1000,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)
    
    global entry0_img
    entry0_img = PhotoImage(file = f"img_textBox0.png")
    canvas.create_image(
        760.0, 232.0,
        image = entry0_img)

    entry0 = Entry(
        Home,
        bd = 0,
        bg = "#d9d9d9",
        highlightthickness = 0)

    entry0.place(
        x = 617.0, y = 210,
        width = 286.0,
        height = 42)
    
    global entry1_img
    entry1_img = PhotoImage(file = f"img_textBox1.png")
    canvas.create_image(
        760.0, 333.0,
        image = entry1_img)

    entry1 = Entry(
        Home,
        bd = 0,
        bg = "#d9d9d9",
        highlightthickness = 0)

    entry1.place(
        x = 617.0, y = 311,
        width = 286.0,
        height = 42)
    
    global background_img
    background_img = PhotoImage(file = f"background.png")
    canvas.create_image(
        460.0, 300.0,
        image=background_img)
    
    global img0
    img0 = PhotoImage(file = f"img0.png")
    b0 = Button(
        Home,
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = lambda : squat_counter(entry0, entry1),
        relief = "flat")

    b0.place(
        x = 690, y = 421,
        width = 138,
        height = 45)
    
home_page()
root.resizable(False, False)
root.mainloop()