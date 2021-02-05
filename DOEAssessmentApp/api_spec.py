"""OpenAPI v3 Specification"""

# apispec via OpenAPI
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields

# Create an APISpec
spec = APISpec(
    title="DOE Assessment App",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


# Define schemas


class InputSchema(Schema):
    id = fields.Int(description="An integer.", required=True)


class OutputSchema(Schema):
    msg = fields.String(description="A message.", required=True)


# register schemas with spec


spec.components.schema("Input", schema=InputSchema)
spec.components.schema("Output", schema=OutputSchema)

# add swagger tags that are used for endpoint annotation
tags = [
    {'name': 'login',
     'description': 'Login & Logout.'
     },
    {'name': 'getcreateproject',
     'description': 'Fetch and create project(s).'
     },
    {'name': 'updatedeleteproject',
     'description': 'Fetch, update and delete a project.'
     },
    {'name': 'getcreatearea',
     'description': 'Fetch and create area(s).'
     },
    {'name': 'updatedeletearea',
     'description': 'Fetch, update and delete a area.'
     },
    {'name': 'fetchareabyprojectid',
     'description': 'Fetch areas by project id.'
     },
    {'name': 'getcreatefunctionality',
     'description': 'Fetch and create functionality(s).'
     },
    {'name': 'updatedeletefunctionality',
     'description': 'Fetch, update and delete a functionality.'
     },
    {'name': 'fetchfunctionalitiesbyareaid',
     'description': 'Fetch functionalities by area id.'
     },
    {'name': 'getcreatesubfunctionality',
     'description': 'Fetch and create sub-functionality(s).'
     },
    {'name': 'updatedeletesubfunctionality',
     'description': 'Fetch, update and delete a sub-functionality.'
     },
    {'name': 'fetchsubfunctionalitiesbyfunctionalityid',
     'description': 'Fetch sub-functionalities by functionality id.'
     },
    {'name': 'getcreateemailconfig',
     'description': 'Fetch and create email configuration(s).'
     },
    {'name': 'updatedeleteemailconfig',
     'description': 'Fetch, update an email configuration.'
     },
    {'name': 'getcreaterole',
     'description': 'Fetch and create role(s).'
     },
    {'name': 'deleterole',
     'description': 'Delete role.'
     },
    {'name': 'getcreaterbac',
     'description': 'Fetch and create RBAC(s).'
     },
    {'name': 'updatedeleterbac',
     'description': 'Fetch and update a RBAC.'
     },
    {'name': 'fetchfeaturesbyrole',
     'description': 'Fetch features by role.'
     },
    {'name': 'getcreatequestion',
     'description': 'Fetch and create question(s).'
     },
    {'name': 'updatedeletequestion',
     'description': 'Fetch, update and delete a question.'
     },
    {'name': 'viewquestions',
     'description': 'View question(s) using required filters.'
     },
    {'name': 'getcreateuser',
     'description': 'Fetch and create users(s).'
     },
    {'name': 'updatedeleteuser',
     'description': 'Fetch, update and delete an user.'
     },
    {'name': 'fetchusersbyrole',
     'description': 'Fetch users by role.'
     },
    {'name': 'getcreateprojectmanagerassignment',
     'description': 'Fetch project manager(s) assigned to project(s) and assign a project to a project manager.'
     },
    {'name': 'associateprojectmanager',
     'description': 'Associate/Disassociate a project manager.'
     },
    {'name': 'getcreatecompanydetails',
     'description': 'Fetch all registered company details and register a company into the app.'
     }
]

for tag in tags:
    print(f"Adding tag: {tag['name']}")
    spec.tag(tag)
