from roksana.attack_methods.base_attack import BaseAttack


'''
This is an example of how to write custom attack algorithm. Your custom routine should inherit from BaseAttack class.
The main routine should be implemented in the execute method. The execute method should take two arguments: data and params.
Execute metho return the modified data as the only output.

Example:
----------------------------------------------------------------------
from custom_attack import MyCustomAttack

attack = MyCustomAttack()
result = attack.execute(data, params={'custom_param': 'value'})
----------------------------------------------------------------------
'''


class MyCustomAttack(BaseAttack):
    def execute(self, data, params):
        # Implement custom attack logic
        modified_data = data  # Modify data as needed
        return modified_data
