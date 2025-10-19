import face_recognition           
import cv2 #webcam                  
import numpy as np 
import csv
import os
from datetime import datetime
import time
import winsound #audio notification


# ----------Webcam setup----------
video_capture = cv2.VideoCapture(0) 
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# ----------Paths----------
path = "images"
snapshots_path = "snapshots"
os.makedirs(snapshots_path, exist_ok=True)


# ----------Load known faces----------
known_face_encodings = []
known_face_names = []


# Loop through all files in the folder
for filename in os.listdir(path):
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):    #jpg, webp
        # Get the full image path
        image_path = os.path.join(path, filename)

        # Load the image
        image = face_recognition.load_image_file(image_path)

        # Get encodings for the face(s) in the image
        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0: # Check if at least one face encoding is found
            encoding = encodings[0]  # Use the first face found
            known_face_encodings.append(encoding) 

            # Use the file name (without extension) as the person's name
            name = os.path.splitext(filename)[0] 
            known_face_names.append(name) 
            print(f"Loaded encoding for: {name}")
        else:
            print(f"No face found in {filename}, skipping...")


students = known_face_names.copy()  # Copy list if you need a separate 'students' list

 
# ----------Initialize variables---------- 
face_locations = []
face_encodings = []
face_names = []


# ----------Attendance CSV setup----------
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")


file = open(current_date+".csv", "a+", newline="") #write method, newline no value
lnwriter = csv.writer(file) #used when writing into csv file


existing_names = set()
if os.path.exists(current_date + ".csv"):
    with open(current_date + ".csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0:
                existing_names.add(row[0])  # First column is the name


recently_logged = set()
print("Press Q to quit.")


# ----------Main loop----------
s = True
while True: 

        _, frame = video_capture.read() #read the frame from webcam
        small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) #resize frame to 1/4th size for faster processing
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB) #convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        
        
        face_locations = face_recognition.face_locations(rgb_small_frame) #detect all faces in the frame
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) #get the encodings of the detected faces n store data
        face_names = []
        
        if s:    
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding) #compare the detected faces with known faces
                name = ""
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding) #get the distance between the detected face and known faces
                best_match_index = np.argmin(face_distances) #get the index of the best match
                
                if matches[best_match_index]:
                    name = known_face_names[best_match_index] #get the name of the match if exists
                face_names.append(name)
                

                # ----------Attendance marking----------
                if name in known_face_names:
                    if name not in existing_names:  # Only add if not already marked today
                        existing_names.add(name)
                        print(f"Marked attendance for {name}")
                        current_time = datetime.now().strftime("%I:%M:%S %p")

                        top, right, bottom, left = face_locations[face_encodings.index(face_encoding)]

                        top *= 2
                        right *= 2     
                        bottom *= 2
                        left *= 2

                        face_crop = frame[top:bottom, left:right]
                        
                        snapshot_filename = os.path.join(snapshots_path, f"{name}_{current_date}_{current_time.replace(':', '-')}.jpg")
                        cv2.imwrite(snapshot_filename, face_crop)
                        print(f"Saved snapshot for {name} at {snapshot_filename}")
                        snapshot_url = f"file:///{os.path.abspath(snapshot_filename).replace(os.sep, '/')}"
                        lnwriter.writerow([name, current_time, snapshot_url])
                        winsound.PlaySound("Attendance recorded.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) #audio notification without blocking webcam
                
                    else: 
                        if name in existing_names and time.time() % 3 < 2:      # Show message for 2 seconds every 3 seconds
                            cv2.putText(frame, "Attendance recorded", (50, 50), cv2.QT_FONT_NORMAL, 1.0, (0,0,255),2)

                
        # ----------Display box around face----------
        for (top, right, bottom, left), name in zip(face_locations, face_names): 
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)  
            cv2.rectangle(frame, (left, bottom), (right, bottom), (0,255,0), cv2.FILLED) 
            font = cv2.QT_FONT_NORMAL
            cv2.putText(frame, name, (left, top), font, 1.0, (255,255,255),2)
            color = (0, 255, 0) 
            
            if name in known_face_names: 
                color = (0, 255, 0)
            else: 
                color = (0, 0, 255)
                cv2.putText(frame, "Unknown", (left, top), font, 1.0, (255,255,255),2)

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2) 


        cv2.imshow("Attendance System", frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    

# ----------Cleanup----------
video_capture.release() 
cv2.destroyAllWindows()
file.close()