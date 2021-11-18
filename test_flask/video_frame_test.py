import cv2
vidcap = cv2.VideoCapture("/Users/selvaganapathyt/Documents/personal/Selvaganapathy Thirugnanam/ms-datascience/cs-410-text-info-systems/final_project/courseera-dl/cs-410/01_week-1/04_module-1-lessons/01_lesson-1-1-natural-language-content-analysis.mp4")
vidcap.set(cv2.CAP_PROP_POS_MSEC,(300*1000))
success,image = vidcap.read()
cv2.imwrite("frame%d.jpg" % 0, image)