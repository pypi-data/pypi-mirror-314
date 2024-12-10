class OneClickManager:
    def __init__(self):
        self.clicked = False
        self.hovering = False

    def update(self):
        self.clicked = False
        self.hovering = False

    def get_clicked(self):
        return self.clicked

    def get_hovering(self):
        return self.hovering
    
    def set_clicked(self, status=True):
        self.clicked = bool(status)

    def set_hovering(self, status=True):
        self.hovering = bool(status)