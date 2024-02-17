user_join_schema = {'real_name': {'type': 'string', 'minlength': 1},
                    'real_email': {'type': 'string', 'minlength': 1,
                                   'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'},
                    'user_password': {'type': 'string', 'minlength': 4},
                    'post_code': {'type': 'string', 'minlength': 5, 'maxlength': 5},
                    'phone': {'type': 'string', 'minlength': 11, 'maxlength': 13},
                    'addresses': {'type': 'string', 'minlength': 5},
                    'detail_address': {'type': 'string', 'minlength': 5}}

login_schema = {'username': {'type': 'string', 'minlength': 1},
                'password': {'type': 'string', 'minlength': 1}}

goods_schema = {'goods_name': {'type': 'string', 'minlength': 1, 'required': True},
                'price': {'type': 'number', 'min': 3, 'required': True},
                'goods_cnt': {'type': 'number', 'min': 0, 'required': True},
                'goods_description': {'type': 'string', 'minlength': 1, 'required': True}}

cart_add_schema = {'goods_code': {'type': 'string', 'minlength': 1, 'required': True},
                   'goods_cnt': {'type': 'number', 'min': 1, 'required': True}}

cart_modify_schema = {'goods_cnt': {'type': 'number', 'min': 1, 'required': True}}

user_modify_schema = {'real_name': {'type': 'string', 'minlength': 2, 'required': True},
                      'real_email': {'type': 'string', 'minlength': 1,
                                     'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'},
                      'user_current_password': {'type': 'string', 'minlength': 4},
                      'user_new_password': {'type': 'string', 'minlength': 4},
                      'user_new_password_confirm': {'type': 'string', 'minlength': 4},
                      'post_code': {'type': 'string', 'minlength': 5, 'maxlength': 5},
                      'real_phone': {'type': 'string', 'minlength': 11, 'maxlength': 13},
                      'addresses': {'type': 'string', 'minlength': 5},
                      'detail_address': {'type': 'string', 'minlength': 5}
                      }

order_schema = {
    'items': {
        'type': 'list',
        'required': True,
        'minlength': 1,
        'schema': {
            'type': 'dict',
            'required': True,
            'schema': {
                'goods_code': {'type': 'string', 'minlength': 3, 'required': True},
                'goods_cnt': {'type': 'number', 'min': 1, 'required': True},
                'goods_price': {'type': 'number', 'min': 100, 'required': True}
            }
        }
    },
    'ship_to': {
        'type': 'dict',
        'required': True,
        'schema': {
            'name': {'type': 'string', 'minlength': 2, 'required': True},
            'phone': {'type': 'string', 'minlength': 9, 'required': True},
            'addresses': {'type': 'string', 'minlength': 8, 'required': True},
            'post_code': {'type': 'string', 'minlength': 5, 'required': True}
        }
    }
}
