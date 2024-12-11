# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Server Analysis Report',
    'version': '18.0.1.0.0',
    'summary': 'Server Analysis Report',
    'description': """
This module helps to monitor and understand the server-side of odoo.
""",
    'depends': ['base'],
    'data': [
        'data/cpu_scheduled_action.xml',
        'security/ir.model.access.csv',
        'views/server_monitor.xml',
        'views/disk_view.xml'
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
