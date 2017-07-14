Input:
cloud point ros message

Logic:
1. Perform detection on every frame
2. If obstacle detected, perform clustering to determine location and size of obstacle starting from the next frame
3. Path planning (undergoing)

Output:
Publish ros topic /detect_result and costumized msg containing flag, distance and turning_angle
