from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    
    def create_user(self, phone_number, first_name, last_name, email, role, password=None):
        if not phone_number:
            raise ValueError("User must have a phone number.")
        
        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        user.set_password(password)
        user.is_active= True
        return user
    
    def create_superuser(self, phone_number, first_name=None, last_name=None, email=None, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            role='Admin',
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
