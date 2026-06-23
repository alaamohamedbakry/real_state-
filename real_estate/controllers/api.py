from odoo import http, fields
from odoo.http import request
from functools import wraps
import json
import odoo


class RealEstateAPI(http.Controller):


    
    @http.route('/api/properties/create', type='json', auth='user', methods=['POST'], csrf=False)
    def create_property(self, **kwargs):
        try:
            params = kwargs

            
            # Validate required fields
            if not params.get('name') or not params.get('price'):
                return {
                    'status': 'error',
                    'message': 'Name and price are required'
                }
            
            if not params.get('available'):
                return {
                    'status': 'error',
                    'message': 'Property must be available'
                }
            
            crm_obj = request.env['crm.lead'].sudo().create({
                'name':params.get('name'),
                'property_type':params.get('property_type'),
              })
            
            # Create property
            property_obj = request.env['real_estate.property'].sudo().create({
                'name': params.get('name'),
                'price': params.get('price'),
                'bed_rooms': params.get('bed_rooms', 0),
                'property_type': params.get('property_type', 'house'),
                'deposit_required': params.get('deposit_required', 0),
                'available': params.get('available', False),
                'created_from_api':True,
                'lead_id':crm_obj.id


            })

           
            
            return {
                'status': 'success',
                'message': 'Property created successfully',
                'data': {
                    'property_id': property_obj.id,
                    'crm_obj':crm_obj.id
                    
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    @http.route('/api/properties/update', type='json', auth='public', methods=['POST'], csrf=False)
    def update_property_price(self,**kwargs):
        try:
          
          

           
          
          property_id = kwargs.get('property_id')

          
          property_obj = request.env['real_estate.property'].sudo().browse(property_id)
          monthly_rent = kwargs.get('price')
          property_obj.sudo().write({
              'price':monthly_rent
          })

          return {
              'status':'success',
              'message':'property updated success',
              'data':{
                  'propert_id':property_obj.id,
                  'monthly_rent':property_obj.price
              }
          }
       

          
        except Exception as e:

             return {
                'status': 'error',
                'message': str(e)
            }

          

    
    
        

    @http.route('/api/tenant/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_tenant(self, **kwargs):
        try:
            params = kwargs
            
            # Validate required fields
            if not params.get('name') or not params.get('email'):
                return {
                    'status': 'error',
                    'message': 'Name and email are required'
                }
            
    
            
            # Create tenant
            tenant_obj = request.env['real_estate.tenant'].sudo().create({
                'name': params.get('name'),
                'email': params.get('email'),
                'phone': params.get('phone'),
                'mobile': params.get('mobile'),
                'created_from_api':True
                
                

            })
            
            return {
                'status': 'success',
                'message': 'tenant created successfully',
                'data': {
                    'tenant_id': tenant_obj.id,
                 

                    
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    @http.route('/api/tenant/update', type='json', auth='public', methods=['POST'], csrf=False)

    def update_tenant_email(self,**kwargs):
        try:
            tenant_id = kwargs.get('tenant_id')
            tenant_obj = request.env['real_estate.tenant'].sudo().browse(tenant_id)
            email = kwargs.get('email')
            old_email = tenant_obj.email
            tenant_obj.sudo().write({
                'email':email

            })
            return{
                'state':'success',
                'massege':'update tenant success',
                'data':{
                    'old_email':old_email,
                    'email':tenant_obj.email,
                    'tenant_id':tenant_obj.id
                }
            }
        except Exception as e:

            return {
                'status': 'error',
                'message': str(e)
            }
        
    @http.route('/api/tenant/<int:tenant_id>', type='http', auth='public', methods=['GET'], csrf=False)

    def get_tenant(self,tenant_id):
        try:
            tenant = request.env['real_estate.tenant'].sudo().browse(tenant_id)
            
            if not tenant.exists():
                return request.make_response(
                    json.dumps({'status': 'error', 'message': 'tenant not found'}),
                    headers={'Content-Type': 'application/json'}
                )
            data = {
                'status': 'success',
                'data': {
                    'id': tenant.id,
                    'name': tenant.name,
                    'email': tenant.email,
                    'phone': tenant.phone,
                    'city': tenant.city,
                    'related user':tenant.user_id.name
                }
            }
            return request.make_response(
                json.dumps(data),
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}),
                headers={'Content-Type': 'application/json'}
            )
        
    @http.route('/api/tenant/list', type='json', auth='public', methods=['POST'], csrf=False)
    def tenant_list(self,**kwargs):
        try:
            params = kwargs
            domain =[]
            if params.get('name'):
                # domain.append(('property_type','=',params['property_type']))
                domain.append(('name','ilike' ,params['name']))

            tenants = request.env['real_estate.tenant'].sudo().search(
                domain,
                limit = params.get('limit',30)
            )
            data = []
            for ten in tenants:
                data.append({
                    'id':ten.id,
                    'name':ten.name,
                    'email':ten.email,
                    'phone':ten.phone
                })
            return{
                'state':'success',
                'tenant_list':len(data),
                'data':data
            }
        except Exception as e:
              return {
                'status': 'error',
                'message': str(e)
            }









    
    @http.route('/api/create/lead', type='json', auth='user', methods=['POST'], csrf=False)
    def create_lead_crm(self, **kwargs):

        try:
            params = kwargs
            
            # Validate required fields
            if not params.get('name') :
                return {
                    'status': 'error',
                    'message': 'Name  are required'
                }
            
    
            
            # Create tenant
            lead_obj = request.env['crm.lead'].sudo().create({
                'name': params.get('name'),
                'created_from_api':True
                
                

            })
            
            return {
                'status': 'success',
                'message': 'Lead created successfully',
                'data': {
                    'lead_id': lead_obj.id,
                    'name': lead_obj.name,
                
                    
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
        

    @http.route('/api/properties/<int:property_id>', type='http', auth='public', methods=['GET'], csrf=False)
    # @validate_token
    def get_property(self, property_id):
        """
        GET http://localhost:8017/api/properties/23
        """
        try:
            prop = request.env['real_estate.property'].sudo().browse(property_id)
            
            if not prop.exists():
                return request.make_response(
                    json.dumps({'status': 'error', 'message': 'Property not found'}),
                    headers={'Content-Type': 'application/json'}
                )
            data = {
                'status': 'success',
                'data': {
                    'id': prop.id,
                    'name': prop.name,
                    'description': prop.description,
                    'price': prop.price,
                    'state': prop.state if hasattr(prop, 'state') else ('available' if prop.available else 'rented')
                }
            }
            return request.make_response(
                json.dumps(data),
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}),
                headers={'Content-Type': 'application/json'}
            )

    @http.route('/api/properties/list', type='json', auth='public', methods=['POST'], csrf=False)
    # @validate_token
    def list_properties(self, **kwargs):
        """
        POST http://localhost:8017/api/properties/list
        Body: {
            "params": {
                "state": "available",
                "min_price": 2500,
                "max_price": 5000,
                "limit": 10
            }
        }
        """
        try:
            params = kwargs
            
            # Build domain
            domain = []
            if params.get('min_price'):
                domain.append(('price', '>=', params['min_price']))
            if params.get('max_price'):
                domain.append(('price', '<=', params['max_price']))
            if params.get('property_type'):
                domain.append(('property_type', '=', params['property_type']))                
            
            # Search properties
            properties = request.env['real_estate.property'].sudo().search(
                domain, 
                limit=params.get('limit', 50)
            )
            
            # Format response
            data = []
            for prop in properties:
                data.append({
                    'id': prop.id,
                    'name': prop.name,
                    'price': prop.price,
                    'bed_rooms': prop.bed_rooms,
                    'property_type': prop.property_type,
                    'available': prop.available,
                })
            
            return {
                'status': 'success',
                'count': len(data),
                'data': data
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }


    @http.route('/api/login', type='json', auth='public', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        """
        POST http://localhost:8017/api/login
        Body: {
            "db": "your_db",
            "login": "admin",
            "password": "admin"
        }
        """
        try:
            params = kwargs.get('params', kwargs) if kwargs else {}
            db = params.get('db') or request.db
            login = params.get('login')
            password = params.get('password')

            if not db or not login or password is None:
                return {
                    'status': 'error',
                    'message': 'db, login and password are required'
                }

            request.session.authenticate(db, login, password)
            if request.session.uid is None:
                return {
                    'status': 'error',
                    'message': 'Authentication failed'
                }
            print("request.session.uid:", request.session.uid)
            request.session.db = db
            registry = odoo.modules.registry.Registry(db)
            with registry.cursor() as cr:
                # env = odoo.api.Environment(cr, request.session.uid, request.session.context)
                # if not request.db:
                #     http.root.session_store.rotate(request.session, env)
                #     request.future_response.set_cookie(
                #         'session_id', request.session.sid,
                #         max_age=http.get_session_max_inactivity(env), httponly=True
                #     )
                # print("session_id:", request.session.sid)
                return {
                    'status': 'success',
                    'session_id': request.session.sid
                    # 'data': env['ir.http'].session_info()
                }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }


    



