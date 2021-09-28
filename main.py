from random import choice, randint
from ursina import *   
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.frame_animation_3d import FrameAnimation3d
from ursina.prefabs.health_bar import HealthBar


app = Ursina(fullscreen=True)
window.title = 'Simple Game'

Sky()
ground = Entity(model= 'plane', texture='grass', collider='mesh', scale=(100, 0, 100))
player = FirstPersonController(cursor_scale=.002)
sword = Entity(model='blade', texture='sky_sunset', rotation=(30,-40),
		position=(0.6,-0.6), parent=camera.ui, scale=(0.09,0.15))
enemies = []
"""
enemy = Entity(
	model='cube',
	texture='white_cube',
	parent=scene,
	collider='box',
	y=0.5,
	highlight_color=color.red
	) 


def new_enemy():
	new = Entity(
	model='cube',
	texture='white_cube',
	parent=scene,
	collider='box',
	x=randint(0,50),
	y=0.5,
	z=randint(0,50))
	enemies.append(new)
	invoke(new_enemy, delay=2)
new_enemy() """
health=HealthBar(bar_color=color.green, text_color=color.black,scale_y=0.03, roundness=.5, value=50)

enemy1= FrameAnimation3d('Wolf_One_obj',
	fps=12,
	texture='Wolf_body',
	color=Color(0, 0, 0, 0),
	position=(1,0.5,0),
	)
score = 0
def new_wolf():
	new=Entity(
		model='Wolf_obj',
		texture='Wolf_body',
		collider='box',
		parent=enemy1,

		x=randint(0,50)* choice((-1,1)),
		z=randint(0,50)* choice((-1,1))
	)
	enemies.append(new)
	invoke(new_wolf, delay=2)

new_wolf()

def update():
	for en in enemies:
		en.lookAt(player)
		dist = distance(en,player)
		if dist > 1:
			diff_x = player.x - en.x
			diff_z = player.z - en.z
			en.x += 2*time.dt*diff_x/abs(diff_x)
			en.z += 3*time.dt*diff_z/abs(diff_z)
		elif dist < 1 and dist > 0:
			health.value -=5
			player.z -= 3
			player.x -= 3
			player.jump()
			en.x -= player.x + 0.2
	if health.value == 0:
		for tr in enemies:
			enemies.remove(tr)
			destroy(tr)
		fim=Text(text=f'GAME OVER\n SCORE:{score}\n\nShift + Q to exit', color=color.black)

def input(key):
	global score
	if key == Keys.left_mouse_down:
		sword.position = (0.4, -0.5)
	elif key == Keys.left_mouse_up:
		sword.position = (0.6,-0.6)
	for tr in enemies:
		if tr.hovered:
			if key == 'left mouse down':
				score +=1
				enemies.remove(tr)
				destroy(tr)

app.run()
