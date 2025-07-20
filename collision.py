from Ball import Ball
import math

# PERF: see if enumerate() has an impact or if just range(len(balls)) is more efficient 
def check_collision(balls: list[Ball]):
    for i, ball1 in enumerate(balls):
        for j, ball2 in enumerate(balls):
            # ball1, ball2 = balls[i], balls[j]
            dx = ball1.x_pos - ball2.x_pos
            dy = ball1.y_pos - ball2.y_pos
            distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

            # TODO: Make balls bounce apart at proper deflection angles
            # Right now they are changin gdirections at unnatural angles
            if distance < (ball1.radius + ball2.radius):
                # Simple elastic collision response
                # Separate the balls
                # FIX: balls are overlapping to the center (edges interact with ball centerpoints)
                # Calculate distance between each center and if less than ball1.radius + ball2.radius
                # bounce them MFers
                overlap = (ball1.radius + ball2.radius) - distance
                dx_norm = dx / distance if distance > 0 else 1
                dy_norm = dy / distance if distance > 0 else 0
                
                ball1.x_pos += dx_norm * overlap * 0.5
                ball1.y_pos += dy_norm * overlap * 0.5
                ball2.x_pos -= dx_norm * overlap * 0.5
                ball2.y_pos -= dy_norm * overlap * 0.5
                
                # Exchange velocities (simple elastic collision)
                ball1.x_vel, ball2.x_vel = ball2.x_vel, ball1.x_vel
                ball1.y_vel, ball2.y_vel = ball2.y_vel, ball1.y_vel

            


