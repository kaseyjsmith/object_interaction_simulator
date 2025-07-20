from Ball import Ball
import math

# FIXME: remove after testing performance
import time

def check_collision(balls: list[Ball]):
    start_time = time.perf_counter()
    for i in range(len(balls)):
        for j in range(len(balls[:i+1])):
            # ball1, ball2 = balls[i], balls[j]
            ball1, ball2 = balls[i], balls[j]
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

    end_time = time.perf_counter()
    print(f"Time to check {len(balls)} balls is: {end_time - start_time}")
            
def spacial_partitioned_collisions(balls: list[Ball], grid_size: int = 100):
    """
    Only check for collisions for other balls in nearby grid cells. 
    Improves performance for large number of objects.
    """

    start_time = time.perf_counter()
    # Setup a grid
    grid = {}
    
    for i, ball in enumerate(balls):
        # Assign the ball a grid x and y coordinate
        grid_x = int(ball.x_pos // grid_size)
        grid_y = int(ball.y_pos // grid_size)

        # Since we don't need to know every possible grid position
        # Only account for one's that have a ball in it
        if (grid_x, grid_y) not in grid:
            grid[(grid_x, grid_y)] = []
        grid[(grid_x, grid_y)].append(i)

    checked_pairs = set()

    for (gx, gy), ball_indicies in grid.items():
        for i in range(len(ball_indicies)):
            for j in range(i + 1, len(ball_indicies)):
                # ball1, ball2 = balls[i], balls[j]
                ball1, ball2 = balls[i], balls[j]
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

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                adjacent_cell = (gx + dx, gy + dy)
                if adjacent_cell in grid:
                    for idx1 in ball_indicies:
                        for idx2 in grid[adjacent_cell]:
                            pair = (min(idx1, idx2), max(idx1, idx2))
                            if pair in checked_pairs:
                                continue
                            checked_pairs.add(pair)

                            # TODO: compress this logic and the logic above into one function
                            ball1, ball2 = balls[idx1], balls[idx2]
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

    end_time = time.perf_counter()
    print(f"Spacially partitioned time to check {len(balls)} balls: {end_time - start_time}")









