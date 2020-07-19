import cv2 
import pytesseract

def tesseract ():
	#Reading the image
	img = cv2.imread('cropped.jpg')

	# Adding custom options
	custom_config = r'-l eng --psm 4'
	text = pytesseract.image_to_string(img, config=custom_config).split()
	if 'Government' in text or 'India' in text:
		for i in range(0, len(text)):
			if text[i] == 'India':
				print("Name:", text[i+3], text[i+4])
				break
	else:
		print("Name:", text[2], text[3])

	for i in range(0, len(text)):
		if text[i] == 'DOB:':
		    print("DOB:", text[i+1])
		    break
		elif text[i] == 'Year' and text[i+1] == 'of' and text[i+2] == 'Birth':
		    print("Year of Birth:", text[i+4])
		    break
    
