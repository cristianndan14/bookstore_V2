import re
import string

class PasswordValidator:
    def __init__(self):
        self.rules = {
            'min_length': 8,
            'has_uppercase': True,
            'has_lowercase': True,
            'has_digit': True,
            'has_special_character': True,
            'has_no_consecutive_numbers': True,
            'is_different_username': True
        }
        self.error_messages = {
            'min_length': 'La contraseña debe tener al menos 8 caracteres.',
            'has_uppercase': 'La contraseña debe tener al menos una letra mayúscula.',
            'has_lowercase': 'La contraseña debe tener al menos una letra minúscula.',
            'has_digit': 'La contraseña debe tener al menos un dígito.',
            'has_special_character': 'La contraseña debe tener al menos un caracter especial.',
            'check_consecutive_numbers': 'La contraseña no debe contener números consecutivos ni números repetidos en bloque de tres o más.',
            'check_username_difference': 'La contraseña no debe contener el nombre de usuario.'
        }
    
    def set_rule(self, rule, value):
        if rule in self.rules:
            self.rules[rule] = value
        else:
            raise ValueError(f'{rule} is not a valid rule.')

    def set_error_messages(self, messages_dict):
        for key, value in messages_dict.items():
            if key in self.error_messages:
                self.error_messages[key] = value
            else:
                raise ValueError(f'{key} is not a valid error message key.')

    def check_consecutive_numbers(self, password):
        pattern1 = re.compile(r'(\d)\1{2,}')
        pattern2 = re.compile(r'(?:(?<=\d)\d{3}|\d{3}(?=\d))')
        if pattern1.search(password) or pattern2.search(password):
            return False
        return True

    def check_username_difference(self, password, username):
        if username in password:
            return False
        return True
    
    def validate(self, password, username, rules=None):
        if not rules:
            rules = self.rules

        error_msgs = []

        if self.rules['has_no_consecutive_numbers'] and not self.check_consecutive_numbers(password):
            error_msgs.append(self.error_messages['check_consecutive_numbers'])
        
        if self.rules['is_different_username'] and not self.check_username_difference(password, username):
            error_msgs.append(self.error_messages['check_username_difference'])
        
        if len(password) < self.rules['min_length']:
            error_msgs.append(self.error_messages['min_length'])

        if self.rules['has_uppercase'] and not any(c.isupper() for c in password):
            error_msgs.append(self.error_messages['has_uppercase'])

        if self.rules['has_lowercase'] and not any(c.islower() for c in password):
            error_msgs.append(self.error_messages['has_lowercase'])

        if self.rules['has_digit'] and not any(c.isdigit() for c in password):
            error_msgs.append(self.error_messages['has_digit'])

        if self.rules['has_special_character'] and not any(c in string.punctuation for c in password):
            error_msgs.append(self.error_messages['has_special_character'])
        
        if error_msgs:
            return (False, error_msgs)
        return (True, None)