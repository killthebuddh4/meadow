# import the opencv library 
import cv2 
import boto3
import json

textract = boto3.client('textract')
  
  
# define a video capture object 
vid = cv2.VideoCapture(0) 
  
has_sent = False
while(True): 
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 

    # Display the resulting frame 
    cv2.imshow('window', cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE))
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

    if has_sent == False and cv2.waitKey(1) & 0xFF == ord('c'): 
        has_sent = True
        print("Encoding image as png")
        bytes = cv2.imencode('.png', frame)[1].tobytes()
        print("Sending image to textract")
        response = textract.detect_document_text(Document={'Bytes': bytes})
        print("Response from textract received")
        with open('./response.json', 'w') as f:
            f.write(json.dumps(response, indent=4))
        
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
