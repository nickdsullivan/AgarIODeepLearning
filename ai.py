import neat
class AI:
	def __init__(self):
		self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,config_file)
		local_dir = os.path.dirname(__file__)
    	config_path = os.path.join(local_dir, 'config-feedforward')
    	run(config_path)
