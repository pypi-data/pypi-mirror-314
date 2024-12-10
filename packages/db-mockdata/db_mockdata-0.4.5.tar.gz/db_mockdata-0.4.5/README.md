## Mock data generation

This is small project for generating artificial / mock data, conforming to the specified DB schema.
It can be useful to either generate pseudo-realistic data in the database, or prepare large amounts of mock data for stress testing.


The package allows for generating mock data for specified database schema.

## Simple configuration file schema:

```  
{
  "connection": "postgresql+psycopg2://admin:test@172.17.0.1:5432/ChmielDB",
  "tables": {
        "Projects":{
        "id": "PK serial",
        "project_name": "first_name",
        "project_owner": "FK Users.id"
      },
      "Users": {
        "id": "PK serial",
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "email UNIQUE",
        "password": "password",
        "role": "OPTION IN (USER, ADMIN)",
        "address": "address",
        "birth_date": "timestamp",
        "phone_number": "phone"
      },
      "IntermediaryTable: Projects_Users": {
        "project_id": "FK Projects.id",
        "user_id": "FK Users.id"
      },
  },
  "objects_count": {
    "Users": 25,
    "Projects": 10,
    "Projects_Users": 250,
  }
```

## Advanced configuration file schema:

```
{
  "connection": "postgresql+psycopg2://admin:test@172.22.0.1:5432/JobMarketDB",
  "tables": {
    "app_users": {
      "user_id": "PK UUID",
      "company": "FK_UUID company.company_id",
      "email": "email UNIQUE",
      "first_name": "first_name",
      "last_name": "last_name",
      "phone": "first_name",
      "role": "OPTION IN (USER,ADMIN)",
      "is_blocked": "bool",
      "email_verified": "bool",
      "employee_verified": "bool",
      "created_at": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)",
      "password_hash": "first_name"
    },
    "skills": {
      "skill_id": "PK UUID",
      "profile_id": "FK_UUID user_profiles.profile_id",
      "skill_name": "first_name",
      "proficiency_level": "first_name",
      "updated_at": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)"
    },
    "chat_messages": {
      "message_id": "PK UUID",
      "chat_id": "FK_UUID chats.chat_id",
      "content": "long_text RANGE(6, 20)",
      "created_by": "FK_UUID app_users.user_id",
      "created_by_display": "first_name",
      "read_by": "first_name",
      "deleted_by": "first_name",
      "created_at": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)",
      "updated_at": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)"
    },
    "job": {
      "job_id": "PK UUID",
      "company_id": "FK_UUID company.company_id",
      "job_title": "first_name",
      "job_description": "long_text RANGE(6, 20)",
      "required_skills": "jsonb:json1",
      "required_experience": "long_text RANGE(6, 20)",
      "location": "first_name",
      "salary": "float RANGE(100,12000) DISTRIBUTION(normal,mean=1,std=1)",
      "created_at": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00) RANGE()"
    },
    "experiences": {
      "experience_id": "PK UUID",
      "profile_id": "FK_UUID user_profiles.profile_id",
      "company_name": "FK_UUID company.company_id",
      "role": "first_name",
      "start_date": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)",
      "end_date": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)",
      "updated_at": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)"
    },
    "educations": {
      "education_id": "PK UUID",
      "profile_id": "first_name",
      "institution_name": "first_name",
      "degree": "first_name",
      "location": "country+city(\"en_US\",\"en_GB\",\"fr_FR\",\"de_DE\",\"it_IT\",\"es_ES\",\"pl_PL\",\"nl_NL\",\"pt_PT\",\"sv_SE\",\"da_DK\",\"fi_FI\",\"no_NO\",\"cs_CZ\",\"hu_HU\",\"en_CA\",\"sk_SK\")",
      "start_date": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)",
      "end_date": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)",
      "updated_at": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)"
    },
    "company": {
      "company_id": "PK UUID",
      "company_name": "first_name",
      "location": "first_name",
      "industry": "first_name",
      "description": "first_name",
      "verified": "bool",
      "created_at": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)",
      "updated_at": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)"
    },
    "chats": {
      "chat_id": "PK UUID",
      "name": "first_name",
      "created_by": "first_name",
      "deleted_by": "first_name",
      "last_message": "first_name",
      "tags": "first_name",
      "created_at": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)",
      "updated_at": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)"
    },
    "IntermediaryTable: user_chats":{
      "chat_id": "FK_UUID chats.chat_id",
      "user_id": "FK_UUID app_users.user_id"
    },
    "user_profiles": {
      "profile_id": "PK UUID",
      "user_id": "FK_UUID app_users.user_id",
      "resume_path": "first_name",
      "profile_picture_path": "first_name",
      "updated_at": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)"
    },
    "user_settings": {
      "settings_id": "PK UUID",
      "user_id": "FK_UUID app_users.user_id",
      "offers_notification": "bool",
      "newsletter_notification": "bool",
      "recruiter_messages": "bool",
      "push_notification": "bool",
      "updated_at": "timestamp RANGE(2023-01-01 00:00:00,2024-12-24 22:12:00)"
    }
  },
  "json_schemas": [
    {
      "json1": {
        "fields": [
          {
            "skills": {
               "type": "array",
               "item_count": "RANGE(1, 5)",
               "content": {
                  "type": "object",
                  "fields": {
                    "name": {
                      "type": "string",
                      "options": ["Python", "JavaScript", "Java", "C++", "Go", "Ruby"]
                    },
                    "level": {
                      "type": "integer",
                      "range": [1, 5]
                    }
                  }
               }
            }
          }
        ]
      }
    }
  ],
  "objects_count": {
    "app_users": 200,
    "skills": 500,
    "chat_messages": 8000,
    "job": 250,
    "experiences": 100,
    "educations": 200,
    "company": 20,
    "chats": 50,
    "user_profiles": 500,
    "user_settings": 500,
    "user_chats": 10000
  }
}
```

### Allowed column keywords:

TODO

#### Disclaimer:
The program only checks for uniqueness and integrity withing itself, there can still be error if there's already existing data in the database.
