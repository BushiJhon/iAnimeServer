class Address:
    __work_id = None
    __path = None
    __original_image = None
    __colorization_image = None
    __user_id = None
    __receipt = None

    def set_receipt(self, receipt):
        self.__receipt = receipt
        return

    def get_receipt(self):
        return self.__receipt

    def set_work_id(self, work_id):
        self.__work_id = work_id
        return

    def set_path(self, path):
        self.__path = path
        return

    def set_original_image(self, original_image):
        self.__original_image =original_image
        return

    def set_colorization_image(self, colorization_image):
        self.__colorization_image = colorization_image
        return

    def set_user_id(self, user_id):
        self.__user_id = user_id
        return

    def get_work_id(self):
        return self.__work_id

    def get_path(self):
        return self.__path

    def get_original_image(self):
        return self.__original_image

    def get_colorization_image(self):
        return self.__colorization_image

    def get_user_id(self):
        return self.__user_id