
import kivy
kivy.require('1.10.0')

from kivy.config import Config
Config.set('graphics', 'resizable', False)
 
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock

import time
import random
from random import randint

class PongPaddle(Widget):
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

class Background(Widget):
	ball = ObjectProperty()
	player1 = ObjectProperty()
	player2 = ObjectProperty()
	p1label = StringProperty()
	p2label = StringProperty()

	def serve_ball(self):
		self.ball.center = self.center
		self.ball.velocity = Vector(0, 9).rotate(randint(-90, 90)) or Vector(0, -9).rotate(randint(-90, 90))
	
	def reset(self):
		self.player1.center = self.center_x, self.height - 10
		self.player2.center = self.center_x, 10
		self.ball.center = self.center
		time.sleep(1)

	def update(self, dt):
	    self.ball.move()

	    # bounce off bottom paddle
	    if (self.ball.x >= self.player2.x) and (self.ball.x <= self.player2.x + self.player2.width) and (self.ball.y <= self.player2.y):
	        self.ball.velocity_y *= -1

	    # bounce off top paddle
	    if (self.ball.x >= self.player1.x) and (self.ball.x <= self.player1.x + self.player1.width) and (self.ball.y >= self.player1.y - self.player1.height):
	        self.ball.velocity_y *= -1

	    # bounce off left and right
	    if (self.ball.x < 0) or (self.ball.right > self.width):
	        self.ball.velocity_x *= -1

	    # concede a goal
	    if self.ball.center_y < 0:
	        self.p1label = str(int(self.p1label) + 1)
	        self.ball.velocity = Vector(0, -9).rotate(randint(-45, 45))
	        self.reset()
	    if self.ball.center_y > self.height:
	        self.p2label = str(int(self.p2label) + 1)
	        self.ball.velocity = Vector(0, 9).rotate(randint(-45, 45))
	        self.reset()
	        
	    #test if game ended
	    if self.p1label == "5":
	    	time.sleep(2)
	    	print("Player 1 won")
	    	time.sleep(2)

	    	self.p1label = "0"
	    	self.p2label = "0"
	    	self.serve_ball()

	    if self.p2label == "5":
	    	time.sleep(2)
	    	print("Player 2 won")
	    	time.sleep(2)

	    	self.p1label = "0"
	    	self.p2label = "0"
	    	self.serve_ball()


	def on_touch_move(self, touch):
	    if touch.y < self.height / 2:
	        self.player2.center_x = touch.x
	    if touch.y > self.height / 2:
	        self.player1.center_x = touch.x

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
 
class PongApp(App):
    def build(self):
        game = Background()

        Clock.schedule_interval(game.update, 1.0 / 180.0)
        game.serve_ball()

        return game

Window.size = (350, 600)
Window.clearcolor = (1,1,1,1)

Pong = PongApp()
Pong.run()

