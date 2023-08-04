class Pose:

    def __init__(self,name,height,leg,direction,slider,angle):
        self._name = [ "Collected", "Corssed forward", "Forward", "Backward", "In air forward", "In air backward", "Slide out side", "Wrapped around", "Collected high", "Crossed backward" ]
        self._height = ["straight", "bent", "tiptoe"]
        self._leg = ["right", "left"]
        self._direction = ["north", "northwest", "northeast"]
        self._angle = [0, 30, 60, 90, 120, 150, 180, 270, 360]
        self._slider = [0,1,2,3,4,5,6,7]
        self._p = self._name.index(name)
        self._h = self._height.index(height)
        self._w = self._leg.index(leg)
        self._d = self._direction.index(direction)
        self._r = self._angle.index(angle)
        self._t = self._slider.index(slider)

    @property
    def get_name(self):
        return self._name[self._p]
    
    @property
    def get_height(self):
        return self._height[self._h]
    
    @property
    def get_leg(self):
        return self._leg[self._w]
    
    @property
    def get_direction(self):
        return self._direction[self._d]
    
    @property
    def get_angle(self):
        return self._angle[self._r]
    
    @property
    def get_slider(self):
        return self._slider[self._t]
    
    @property
    def get_name_ind(self):
        return self._p
    
    @property
    def get_height_ind(self):
        return self._h
        
    @property
    def get_leg_ind(self):
        return self._w
    
    @property
    def get_direction_ind(self):
        return self._d
    
    @property
    def get_angle_ind(self):
        return self._r
    
    @property
    def get_slider_ind(self):
        return self._t