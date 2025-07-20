import pygame

class Ball:
    def __init__(
            self, 
            surface: pygame.Surface, 
            center,
            color: pygame.Color, 
            image = None,
            init_x_vel = [5.0, 1],      # [magnitude, direction]
            init_y_vel = [5.0, 1],      # [magnitude, direction]
            radius: int = 20):
        self.surface = surface
        self.color = color
        self.center = center
        self.radius = radius

        if image is not None:
            self.image = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(self.image, (radius*2, radius*2))
        else:
            self.image = None

        self.x_pos = self.center[0]
        self.y_pos = self.center[1]
        self.x_vel = init_x_vel
        self.y_vel = init_y_vel

        self.WINDOW_SIZE = None
        # self.WINDOW_SIZE = pygame.display.get_window_size()

    def get_x_pos(self):
        """
        Returns the current x position of the center of the ball
        """
        return self.x_pos

    def get_y_pos(self):
        """
        Returns the current y position of the center of the ball
        """
        return self.y_pos

    def get_x_vel(self):
        """
        Returns the current x velocity of the center of the ball
        """
        return self.x_vel

    def get_y_vel(self):
        """
        Returns the current y velocity of the center of the ball
        """
        return self.y_vel

    def draw(self):
        """
        Draws the ball, optionally with an image if the object has been created with one
        """
        pygame.draw.circle(
            self.surface,
            self.color,
            (self.x_pos, self.y_pos),
            self.radius
        )
        if self.image is not None:
            self.surface.blit(self.image, (self.x_pos - self.radius, self.y_pos - self.radius))

    # TODO: make gravity and friction global in the main simulation, not local to this
    def get_next_pos(self):
        """
        Handles calculating the next position of the ball. 

        Considers gravity, air and ground friction, and velocity.
        """
        # if self.WINDOW_SIZE == None:
        self.WINDOW_SIZE = pygame.display.get_window_size()
        
        # Add gravity to y-velocity (increase downward velocity each frame)
        gravity = 0.5  # Adjust this value to make gravity stronger/weaker
        self.y_vel[0] += gravity

        # # Reduces speed in x-direction all the time
        # TODO: the velocity asymptotically approaches 0. Cut it off as it gets negligibly close to 0
        ground_friction = 0.99
        air_friction = 0.9999

        if self.y_pos + self.radius >= self.WINDOW_SIZE[1] - 5:  # Near ground
            self.x_vel[0] *= ground_friction
        else:  # In the air
            self.x_vel[0] *= air_friction      

        # Update positions
        self.x_pos += self.x_vel[0]
        self.y_pos += self.y_vel[0]
        
        # X-direction bouncing (no change needed)
        if self.x_pos + self.radius >= self.WINDOW_SIZE[0] or self.x_pos - self.radius <= 0:
            self.x_vel[0] *= -1
            self.x_pos = max(self.radius, min(self.WINDOW_SIZE[0] - self.radius, self.x_pos))
        
        # Y-direction bouncing with energy loss (makes it more realistic)
        if self.y_pos + self.radius >= self.WINDOW_SIZE[1]:
            self.y_vel[0] *= -0.8  # Bounce back but lose some energy (80% of velocity retained)
            self.y_pos = self.WINDOW_SIZE[1] - self.radius  # Keep ball above ground
        
        # Optional: bounce off ceiling too
        if self.y_pos - self.radius <= 0:
            self.y_vel[0] *= -0.8
            self.y_pos = self.radius

    def move(self):
        """
        Performs the action of getting the next position and drawing the ball in the new position
        """
        self.get_next_pos()
        self.draw()
        pygame.display.update()


