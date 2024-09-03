# import math

# from Constants import SCREEN_HEIGHT

# class Camera:
# 	def __init__(self, player):
# 		self.y = 0
# 		self.player = player

# 	def update(self, score):
# 		if self.player.y - self.y <= SCREEN_HEIGHT / 2:
# 			self.y = self.player.y - SCREEN_HEIGHT/2
# 		if self.player.y < SCREEN_HEIGHT / 2:
# 			change = int(math.sqrt(score))/10
# 			if not change:
# 				self.y += 1
# 			if(change<4):
# 				self.y += change
# 			else:
# 				self.y += 4

import math
import time
from Constants import SCREEN_HEIGHT

class Camera:
    def __init__(self, player):
        self.y = 0
        self.player = player
        self.start_time = time.time()  # Record the time when the camera is initialized

    def update(self, score):
        # Check if 5 seconds have passed
        elapsed_time = time.time() - self.start_time
        if elapsed_time < 5:
            return  # Do not move the camera if 5 seconds haven't passed

        # Ensure the score is non-negative before taking the square root
        safe_score = max(score, 0)

        # Move the camera downwards when the player is in the lower half of the screen
        if self.player.y - self.y >= SCREEN_HEIGHT / 2:
            self.y = self.player.y - SCREEN_HEIGHT / 2
        
        change = int(math.sqrt(safe_score)) / 10

        # If the change is zero, move the camera by 1 unit
        if not change:
            self.y += 1
        elif change < 4:
            self.y += change
        else:
            self.y += 4


