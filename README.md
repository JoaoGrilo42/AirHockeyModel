# AirHockeyModel
The goal of this project is to eventually design and build a robotic air hockey opponent.  The idea being that I will first develop a software model that I can use not only to prove the concept, but primarily as a platform to develop the control algorithms.  As a bonus, I will use this chance to learn python.

# The Table Model
The air hockey table model will be fairly ideal.  I will be modeling perfect elastic collisions with uniform dynamic friciton and no static friction.  
I will be modeling the puck as an object with the following attributes
* radius (42 mm)
* mass (42 g)
* Position (x, y) 
* Velocity (dx, dy) (mm/s)
* Theta (heading rad)
* Coefficient of Friction (mu_F)
* g (gravity 9.8 m/s/s)
* dt_impact (duration of impacts)

The puck will also have the following methods 
* collsion
* friction
* update
Each of these methods will be used to interact with the puck.
## collision
This function takes as arguments the position (x,y) of the other object, the vector angle of the force, and the magnitude of the force.  The position is used to calculate the direction of the vector normal to the tangent collision point ie the direction that force will act on the puck.  
This function first calculates the angles that will be used, namely theta_n (the angle of the force normal to the tangent of the collision point) and theta_puch (the direction of motion of the puck).
Next the puck velocity and colision force multiplied by dt_impact and divided by mass of puck are projected onto the theta_n vector and added together to give V_n.
The projection of the puck velocity perpendicular to the theta_n vector is also calculated to give V_p (The force is not included in this equations because it doesn't act perpendicular to the normal vector)
Finally V_n and V_p are projected back on the x-y plane and added together to give the new x-y velocity of the puck.

There are two types of collisions that use this function.  The first is the collision with the wall.  In this case the the point of impact is calculated based on the puck position and the direction of the wall being impacted.  Theta 0, pi/2, pi, or 3pi/2, and is chosen to be in the direction to the puck from the wall.  And finaly F is selected as 2*m_puck*V/dt_impact where m_puck is the mass of the puck, V is the magnitude of the current puck velocity and dt_impact is the duration of the impact where the force is applied.  This force will result in lossless reflection.

The second type of collision is with the paddle.  In this case the position of the paddle and puck will be used to determine the impact point and a control algorithm will be used to select the force direction and magnitude.

## friction
This simple function applies a frictional force in the direction opposite the velocity of the puck.  The ammount that the puck slows due to friction is calculated by multiplying the coefficient of friction with gravity and the update interval (dt) subtracting that from the current velocity.

## update
As of right now the update function is called by the main loop to update the state of the puck by applying friction and collisions with the table walls.  It also handles drawing the puck.

# Player Model