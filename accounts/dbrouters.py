class DBRouter(object):

    appname = 'accounts'

    def db_for_read(self, model, **hints):
        """
        Attempts to read self.appname models go to model.db.
        """
        if model._meta.app_label == self.appname:
            return model.db
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write self.appname models go to model.db.
        """
        if model._meta.app_label == self.appname:
            return model.db
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the self.appname app is involved.
        """
        if obj1._meta.app_label == self.appname or \
           obj2._meta.app_label == self.appname:
           return True
        return None

    # This is possibly the new way, for beyond 1.8.
    ''' 
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the self.appname app only appears in the self.appname
        database.
        """
        if app_label == self.appname:
            return db == self.appname
        return None
    '''

    # Contrary to Djano docs this one works with 1.8, not the one above.
    def allow_migrate(self, db, model):
            """
            Make sure the self.appname app only appears in the self.appname
            database.
            """
            if db == self.appname:
                return model._meta.app_label == self.appname
            elif model._meta.app_label == self.appname:
                return False
            return None