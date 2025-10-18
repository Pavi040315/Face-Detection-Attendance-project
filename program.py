import face_recognition            # add capture image from webcam, 
import cv2 #webcam
import numpy as np #array
import csv
import os
from datetime import datetime
import time

video_capture = cv2.VideoCapture(0) #input from default webcam

'''
pavi_image = face_recognition.load_image_file("images/pavi.jpg")
pavi_encoding = face_recognition.face_encodings(pavi_image)[0]

walter_image = face_recognition.load_image_file("images/walter.webp")
walter_encoding = face_recognition.face_encodings(walter_image)[0]  

brad_image = face_recognition.load_image_file("images/brad.webp")
brad_encoding = face_recognition.face_encodings(brad_image)[0] 


known_face_encodings = [
    pavi_encoding,
    walter_encoding,
    brad_encoding   
]

known_face_names = [
    "Pavithran",
    "Walter White",
    "Brad Pitt"
]

#OR Can use this method to load multiple images from a directory
# path = 'images'
# known_face_encodings = []
# for filename in os.listdir(path):
#     if filename.endswith(".jpg") or filename.endswith(".webp"):
#         image = face_recognition.load_image_file(os.path.join(path, filename))
#         encoding = face_recognition.face_encodings(image)[0]
#         known_face_encodings.append(encoding)

students = known_face_names.copy()
'''

path = "images"
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

        if len(encodings) > 0:
            encoding = encodings[0]  # Use the first face found
            known_face_encodings.append(encoding)

            # Use the file name (without extension) as the person's name
            name = os.path.splitext(filename)[0]
            known_face_names.append(name)
            print(f"Loaded encoding for: {name}")
        else:
            print(f"No face found in {filename}, skipping...")

# Copy list if you need a separate 'students' list
students = known_face_names.copy()
 
face_locations = []
face_encodings = []
face_names = []
s=True 

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

while True: 

        _, frame = video_capture.read() #read the frame from webcam
        small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25) #resize frame to 1/4th size for faster processing
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
                
                if name in known_face_names:
                    if name not in existing_names:  # Only add if not already marked today
                        existing_names.add(name)
                        print(f"Marked attendance for {name}")
                        current_time = datetime.now().strftime("%I:%M:%S %p")
                        lnwriter.writerow([name, current_time])
                    else: 
                        if name not in recently_logged:
                            print(f"Attendance already marked for {name.upper()} at {datetime.now():%I:%M %p}.")
                            recently_logged.add(name)
        
        
        for (top, right, bottom, left), name in zip(face_locations, face_names): 
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
    
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)  
            cv2.rectangle(frame, (left, bottom), (right, bottom), (0,255,0), cv2.FILLED) 
            font = cv2.FONT_HERSHEY_SIMPLEX 
            cv2.putText(frame, name, (left, bottom), font, 1.0, (255,255,255),1)
            color = (0, 255, 0) 
            
            if name in known_face_names: 
                color = (0, 255, 0)
            else: 
                color = (0, 0, 255)
                           
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2) 
               
        cv2.imshow("Attendance System", frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    

video_capture.release() 
cv2.destroyAllWindows()
file.close()