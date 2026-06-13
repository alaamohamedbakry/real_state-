from odoo import models, fields, api
from odoo.exceptions import ValidationError
class Crm_Lead(models.Model):
    _inherit="crm.lead"

    phone = fields.Char(string="phone",required=True)
    phone2 = fields.Char(string="phone2",required=True)

    def action_set_won_rainbowman(self):
         #self.return_phone_number()
         #self.validation_user()
         #self.set_revenue()
         #self.check_revenue()
         

         return super(Crm_Lead,self).action_set_won_rainbowman()
     
      
    # this function to print phone and name who won deal in crm lead


    # def return_phone_number(self):
    #      print(f"opportunity_name:{self.name} , phone number:{self.phone}")

    #this function to make a valdiate when click the deal for user has no premission 
    
    # def validation_user(self):
    #      raise ValidationError("you dont have premission")
    

    #this function to set 1000 for revenue in ui when click won in crm lead 
    # def set_revenue(self):
                
    #   self.expected_revenue = 1000


    # this function to check revenue for who has less than 2000 has a valdiate msg and more than 2000 pass 

    # def check_revenue(self):
          
    #       if self.expected_revenue <2000:
    #           raise ValidationError("you can not allow to deal win ")
          
    #       if  not self.email_from:
    #            raise ValidationError("Email is required")
             
    #       else:
    #           print(f"opportunity_name:{self.name} , phone number:{self.phone}")
    # def write(self, vals):
    #     res = super().write(vals)

    #     if 'email_from' in vals:
    #         new_email = (f"Email has been changed to: {vals['email_from']}")
    #         print(new_email)
    #         return res
      
    # @api.model
    # def create(self, vals):
    #    vals['expected_revenue'] = 0
       
    #    if 'expected_revenue' not in vals:
    #     vals['expected_revenue'] = 1500

    #    res= super().create(vals)
       
    #    print("product revenue updated")

    #    return res
    
    # def unlink(self):
    #     for lead in self:
    #         if lead.stage_id.id == 4 :
    #             raise ValidationError("you can not delte this lead because it is alredy in stage won")
    #         else:
    #             return super(Crm_Lead,self).unlink()

    # def unlink(self):
    #     for lead in self:
    #         if lead.stage_id.fold == True:
    #             raise ValidationError("you can not delte this opportunity")

    #     return super(Crm_Lead,self).unlink()


    # def unlink(self):
    #      for lead in self:
    #         if lead.user_id.id == 2:
    #              raise ValidationError("you have no access ")
    #         else:

    #          return super(Crm_Lead,self).unlink()


    # def unlink(self):
    #      for lead in self: 
    #         if 2 in lead.tag_ids.ids :
    #              raise ValidationError("you can not delete this tag ")
    #         else:

    #          return super(Crm_Lead,self).unlink()


    # def unlink(self):
    #      for lead in self: 
    #         if  not lead.partner_id :
    #             raise ValidationError("you must choose customer ")

    #         if 2  in lead.partner_id.category_id.ids :
    #              raise ValidationError("you can not delete this ")
           






   
 