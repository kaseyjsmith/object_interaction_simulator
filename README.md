# Object Interaction Simulator

I've had an urge to make something tangible. I figured an object collision simulator would be a fun thing to make in Pygame and could be a (potentially endless) iterative optimization problem. 

# Features

- Gravity, air friction, and ground friction on objects
- Object collision
- Reflexive edge detection when window is resized during simulation
- Frame-by-frame mode for analyzing interactions

# Optimization Problems Solved

## Checking Collisions

### Improving iteration
Initially I had thought I'd enumerate the list of balls for a bit simpler readablility:

```python
for i, ball1 in enumerate(balls):
    for j, ball2 in enumerate(balls):
        # Then I can call ball1 and ball2 from here easily
```

However, the simulation starts to lag heavily over ~200 balls. Since I'm not really using indexes with this, it seemed wasteful. Modifying the code to iterate using `range(len(balls))` improved performance by about 1 ms per 100 balls.

```python
    for i in range(len(balls)):
        for j in range(len(balls[:i+1])):
            ball1, ball2 = balls[i], balls[j]
            ...
```

### Threading


