class Shooter(object):
    def aim(self, coords):
        '''aims at the tuple coords; returns true if coords are within the range'''
        return False

    def shoot(self):
        '''pulls the trigger'''
        pass

    def aim_and_shoot(self, coords):
        if self.aim(coords):
            self.shoot()
