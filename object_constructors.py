import random

def draw_cuboid(x1, x2, z1, z2, y1, y2 ,t ):
	return '<DrawCuboid x1="{x1}" x2="{x2}" z1="{z1}" z2="{z2}" y1="{y1}" y2="{y2}" type="{t}"/>'.format(
	  x1= x1,
	  x2= x2,
	  z1= z1,
	  z2= z2,
	  y1= y1,
	  y2= y2,
	  t=t)

def gen_tree(x,z):

	tree_length = random.randint(3,6)
		
	start = float(random.randint(1,3))
	tree_foliage_start = int( round( (start / (start+1)) * float(tree_length) ) )
	leaves = random.choice(['leaves','leaves2'])
	log = random.choice(['log','log2'])

	#Make top foliage
	generatorString = '<DrawBlock x="{0}" z="{1}" y="{2}" type="{3}"/>'.format(x, z, tree_length+6, leaves)
	generatorString += draw_cuboid(x-1,x+2,z-1,z+1,tree_length+5,tree_length+5,leaves)
	
	foliage_around_trunk = tree_length - tree_foliage_start + 1
	for i in range(foliage_around_trunk):
		#max reach
		s = 1 #Can change this to create wider foliage.
		generatorString += draw_cuboid(x-s-i,x+s+i,z-s-i,z+s+i,tree_length-i+4,tree_length-i+4,leaves)

	#I'm putting this here because I think later entries override earlier ones, and I want a stem instead of foliage.
	generatorString += draw_cuboid(x,x,z,z,4,tree_length+4,log)
	return generatorString

def gen_house(x, z, small=False):
	
	generatorString= ''

	#There is no logic to the choices. Just picked a few.
	door = random.choice(['acacia_door','jungle_door', 'spruce_door', 'dark_oak_door'])
	wall = 'brick_block' #random.choice(['glass','ice','cobblestone','mossy_cobblestone','brick_block','stonebrick']) 
	roof = 'glass' #random.choice(['glass','brick_block', 'clay'])
	
	if small:
		w = random.randint(1,3)
		l = random.randint(2,4)
		h = random.randint(2,3)
	else:
		w = random.randint(4,10)
		l = random.randint(5,10)
		h = random.randint(3,7)

	house_has_fence = random.choice([True,False])
	if house_has_fence:
		fence = random.choice(['spruce_fence', 'jungle_fence', 'birch_fence', 'dark_oak_fence' ])
		fence_gate = '{0}_{1}'.format(fence,'gate')
		d = random.randint(2,3)
		#Front fence, back fence, left fence right fence
		generatorString += draw_cuboid(x-w-d, x+w+d, z+d,   z+d,   4,4, fence)
		generatorString += draw_cuboid(x-w-d, x+w+d, z-l-d, z-l-d, 4,4, fence)
		generatorString += draw_cuboid(x-w-d, x-w-d, z+d,   z-l-d, 4,4, fence)
		generatorString += draw_cuboid(x+w+d, x+w+d, z+d,   z-l-d, 4,4, fence)
		#Add fence door
		generatorString += '<DrawBlock x="{0}" z="{1}" y="4" type="{2}"/>'.format(x,z+d,fence_gate)
	#Draw walls
	#Front wall, back wall, side wall left, side wall right:
	generatorString += draw_cuboid(x-w, x+w, z,   z,   4, h+4, wall)
	generatorString += draw_cuboid(x-w, x+w, z-l, z-l, 4, h+4, wall) 
	generatorString += draw_cuboid(x-w, x-w, z,   z-l, 4, h+4, wall)
	generatorString += draw_cuboid(x+w, x+w, z,   z-l, 4, h+4, wall)

	#Add some sort of roof 
	if small:
		r = 2
	else:
		r = 5
	for i in range(r):
		generatorString += draw_cuboid(x+w-i,x-w+i,z,z-l+i,h+4+i,h+4+i,roof)
	#Draw door at the x,z
	generatorString += '<DrawBlock x="{0}" z="{1}" y="4" type="{2}"/>'.format(x,z,door)
	generatorString += '<DrawBlock x="{0}" z="{1}" y="5" type="{2}"/>'.format(x,z,door)

	#Draw windows on the side opposite to the roof
	if wall != 'glass': 
		generatorString += '<DrawBlock x="{0}" z="{1}" y="5" type="{2}"/>'.format(x+1,z-l,'glass')
		generatorString += '<DrawBlock x="{0}" z="{1}" y="5" type="{2}"/>'.format(x-1,z-l,'glass')

	#Add some NPCs
	people = [random.choice(['Cow','Chicken','Villager','Sheep']) for i in range( random.randint(2,4) )]
	for i in people:
		generatorString += '<DrawEntity x="{0}" z="{1}" y="{2}" type="{3}"/>'.format(x-2,z+4,4,i)
	return generatorString

def gen_sapling(x,y):
	return '<DrawBlock x="{0}" z="{1}" y="{2}" type="{3}"/>'.format(x,y,4,'sapling')

def gen_art_sphere(x,z):
	w = random.randint(1,3)
	h = random.randint(1,3)
	o = ['obsidian'] #, 'ice', 'wool', 'diamond_block']
	stuff = random.choice(o)
	stuff2 = random.choice(o)
	generatorString = draw_cuboid(x-w,x+w,z-w,z+w,4,4+h,stuff)
	generatorString += '<DrawSphere x="{0}" z="{1}" y="{2}" radius="{3}" type="{4}" />'.format(x,z,10+h,w*2,stuff2)
	return generatorString

def gen_something_that_is_not_a_tree_but_is_similar_for_foolings():
	pass