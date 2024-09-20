# boid_sim
Simulates boids that follow a set of rules that is called each frame.  The boids are meant to push away from one another but it does not seem like that is happening here.

The boid that is outlined in black is the player who can control themselves using WASD the camera will remain focused on them.  You can see a red line coming out from the player that represents the players velocity and will grow the faster the player is moving.

Each boid has it's own position as well as velocity and rotation.  The rotation is called each frame from the base model (each entity is assigned and index that goes to a pygame surface) which takes up a lot of the processing time.  In the future I plan on pre rendering maybe 360 of these images that are already rotated and then just grabbing the closest one to their current rotation or even limit the rotation to only those degrees, it depends on how noticable it is (this could be decreased to less images depending on how much the percision matters).

The biggest thing I am having a hard time implementing is the rebounding of the boids off each other, I want them to push away from each other but it largely depends on their rotation as their velocity is not based on x_vel and y_vel but rather just a single float that is added and removed from.  A better way of doing this would probably be to have a seperate x_vel and y_vel for each boid.

I plan on reimplementing this as a project in a more challanging language when I figure out how all the math behind it will work (more challanging language meaning C).

If you have any questions feel free to message me.  I also have a similar project with python astroids but that one doesn't have as correct math in it's implementation.

### Simple Demo
Showing off a few boids doing mostly normal things.
![boidsim_0](https://user-images.githubusercontent.com/95717625/223926924-647b931e-6e20-4a58-99e8-d82e7b6963c1.PNG)
### A few more boids
Seems the code for them pushing each other away doesn't work all that well.
![boidsim_1](https://user-images.githubusercontent.com/95717625/223926926-99dd0221-45d5-4363-ac95-c64e64ba5276.PNG)
### Too many boids
Can handle over 1000 boids.
![boidsim_2](https://user-images.githubusercontent.com/95717625/223926923-a9b62343-376f-4a5e-a535-3b42931f134e.PNG)
