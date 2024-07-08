from flask_login import UserMixin


class User(UserMixin):

  def __init__(self, id, perms, first_name, last_name, email, password,
               secrete_question, secrete_answer):
    self.id = id
    self.perms = perms
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
    self.secrete_question = secrete_question
    self.secrete_answer = secrete_answer
    self.authenticated = False

  # def is_active(self):
  #   return self.is_active()

  # def is_anonymous(self):
  #   return False

  # def is_authenticated(self):
  #   return self.authenticated

  # def is_active(self):
  #   return True

  def get_id(self):
    return self.id

  # def get_first_name(self):
  #   return self.first_name
  # def get_last_name(self):
  #   return self.last_name
  # def get_full_name():
  #   return f'{get_first_name()} {get_last_name()}'
