import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,  
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)
cv2.namedWindow("AI Virtual Keyboard", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("AI Virtual Keyboard", cv2.WINDOW_NORMAL, cv2.WINDOW_NORMAL)

keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', 'Space'],
        ['Shift', 'Enter', 'Backspace']]

key_boxes = []
last_key_time = time.time()
key_pressed = None
key_press_time = 0


def draw_keyboard(img, window_width):
    key_boxes.clear()
    h, w, _ = img.shape
    key_w, key_h = 60, 60 
    start_y = h - 300 
    
    for row_index, row in enumerate(keys):
       
        row_width = sum(
            key_w * 3 if key in ['Space'] 
            else key_w * 2 if key in ['Enter', 'Backspace', 'Shift'] 
            else key_w 
            for key in row
        ) + (len(row)-1)*10
        
        row_start_x = int((window_width - row_width) / 2)  
        
        for col_index, key in enumerate(row):
            
            if key == 'Space':
                kw = key_w * 4
            elif key in ['Enter', 'Backspace', 'Shift']:
                kw = key_w * 2
            else:
                kw = key_w
                
            x = row_start_x
            y = start_y + row_index * (key_h + 15) 
            
           
            color = (100, 255, 100) if key == key_pressed and (time.time() - key_press_time) < 0.3 else (200, 0, 0)
            cv2.rectangle(img, (x, y), (x + kw, y + key_h), color, -1)  
            cv2.rectangle(img, (x, y), (x + kw, y + key_h), (255, 255, 255), 2) 
            
           
            label = {
                'Space': 'SPACE',
                'Enter': 'ENTER',
                'Backspace': 'backspace',
                'Shift': 'caps',
                ',': ',',
                '.': '.'
            }.get(key, key)
            
            font_scale = 0.7 if key in ['Space', 'Enter', 'Backspace', 'Shift'] else 0.9
            thickness = 2 if len(label) == 1 else 1
            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
            
            cv2.putText(img, label, 
                       (x + int((kw - text_size[0])/2), y + int((key_h + text_size[1])/2)), 
                       cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
            
            key_boxes.append((key, x, y, x + kw, y + key_h))
            row_start_x += kw + 10
            
    return img


def is_touching_thumb(hand_landmarks):
    index_tip = hand_landmarks.landmark[8] 
    thumb_tip = hand_landmarks.landmark[4]  
    
    
    distance = ((index_tip.x - thumb_tip.x)**2 + (index_tip.y - thumb_tip.y)**2)**0.5
    
   
    return distance < 0.03  


def get_key_pressed(x, y):
    for key, x1, y1, x2, y2 in key_boxes:
        if x1 < x < x2 and y1 < y < y2:
            return key
    return None

text = ""
caps_lock = False
window_width = 1000  

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (window_width, 800)) 
    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    h, w, _ = frame.shape  
    frame = draw_keyboard(frame, window_width)  
    current_time = time.time()

    if result.multi_hand_landmarks:
        for hand_idx, handLms in enumerate(result.multi_hand_landmarks):
            mp_drawing.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            
           
            index_finger_tip = handLms.landmark[8]
            x = int(index_finger_tip.x * w)
            y = int(index_finger_tip.y * h)
            
            
            cv2.circle(frame, (x, y), 15, (0, 255, 0), -1)
            
            
            if is_touching_thumb(handLms):
                key = get_key_pressed(x, y)
                if key and current_time - last_key_time > 0.5: 
                    if key == 'Space':
                        pyautogui.press('space')
                        text += ' '
                    elif key == 'Enter':
                        pyautogui.press('enter')
                        text += '\n'
                    elif key == 'Backspace':
                        pyautogui.press('backspace')
                        text = text[:-1] if text else text
                    elif key == 'Shift':
                        caps_lock = not caps_lock
                    elif key in [',', '.']:
                        pyautogui.press(key)
                        text += key
                    else:
                        char = key.upper() if caps_lock else key.lower()
                        pyautogui.press(char)
                        text += char
                    
                    key_pressed = key
                    key_press_time = current_time
                    last_key_time = current_time

   
    cv2.rectangle(frame, (50, 50), (window_width - 50, 150), (50, 50, 50), -1)
    cv2.putText(frame, "Typed Text:", (60, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, text[-50:], (60, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
   
    caps_status = "ON" if caps_lock else "OFF"
    cv2.putText(frame, f"Caps Lock: {caps_status}", (window_width - 200, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("AI Virtual Keyboard", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()