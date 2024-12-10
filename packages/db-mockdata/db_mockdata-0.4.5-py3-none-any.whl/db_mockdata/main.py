import argparse
import json
import random
import re
import string
import uuid
from datetime import datetime, timedelta

from faker import Faker
from itertools import product, islice
import networkx as nx
import numpy as np
from sqlalchemy import *
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, sessionmaker
from tqdm import tqdm

# --- initialize ORM and random seed ---

Base = declarative_base()
fake = Faker()
seed = random.randint(0, 2 ** 16)
Faker.seed(seed)
random.seed(seed)
print(f"Seed used: {seed}")


# --- initialize ORM and random seed ---


def unique_combinations(fields, created_data, limit):
    """
    Method for generating random combinations of fields, with many FK, used in intermediary tables.
    :param fields: columns which need to be generated
    :param created_data: dictionary of ORM classes with already created objects
    :param limit: determines the number of combinations to generate
    :return: list of values (combinations) for given FK fields
    """
    combination_lists = []
    for field_name, field_type in fields.items():
        if "FK" in field_type:
            foreign_table, foreign_key = field_type.split(' ')[1].split('.')
            combination_lists.append([getattr(x, foreign_key) for x in created_data[foreign_table]])

    for list in combination_lists:
        random.shuffle(list)

    # generate combinations
    combinations = islice(product(*combination_lists), limit)

    return combinations


class EmailGenerator:
    """
    Email generator with capability to keep track of existing emails.
    """

    def __init__(self, local_part_length=10, domain_length=6):
        self.existing_emails = set()
        self.local_part_length = max(local_part_length, 2)
        self.domain_length = domain_length

    def generate_random_email(self, unique=False):
        while True:
            local_part = ''.join(
                random.choices(string.ascii_uppercase, k=1) + random.choices(string.ascii_lowercase + string.digits,
                                                                             k=self.local_part_length - 1))
            domain = ''.join(random.choices(string.ascii_lowercase, k=self.domain_length))
            email = f"{local_part}@{domain}.com"
            if not unique or email not in self.existing_emails:
                self.existing_emails.add(email)
                return email


# --- initialize generators ---

email_generator = EmailGenerator()


# --- initialize generators ---

def create_model(name, fields, intermediary_table):
    attrs = {'__tablename__': name}
    for field_name, field_type_original in fields.items():
        field_type = field_type_original
        is_unique = False
        if "UNIQUE" in field_type:
            is_unique = True
            field_type = field_type_original.strip('UNIQUE').strip()
        if "PK serial" in field_type:
            attrs[field_name] = Column(Integer, primary_key=True, autoincrement=True)
        elif "PK UUID" in field_type:
            attrs[field_name] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        elif "uuid" in field_type:
            attrs[field_name] = Column(UUID(as_uuid=True), primary_key=False, default=uuid.uuid4)
        elif any(x in field_type for x in
                 ["first_name", "last_name", "email", "password", "address", "phone", "long_text",
                  "OPTION IN", "country+city"]):
            attrs[field_name] = Column(String, unique=is_unique)
        elif "timestamp" in field_type:
            attrs[field_name] = Column(TIMESTAMP, unique=is_unique)
        elif "bool" in field_type:
            attrs[field_name] = Column(BOOLEAN, unique=is_unique)
        elif "smallint" in field_type:
            attrs[field_name] = Column(SMALLINT, unique=is_unique)
        elif "integer" in field_type:
            attrs[field_name] = Column(INTEGER, unique=is_unique)
        elif "float" in field_type:
            attrs[field_name] = Column(FLOAT, unique=is_unique)
        elif "jsonb" in field_type:
            attrs[field_name] = Column(JSONB, unique=is_unique)
        elif field_type.startswith("FK_UUID"):
            ref_table, ref_column = field_type.split()[1].split('.')

            attrs[field_name] = Column(UUID, ForeignKey(f"{ref_table}.{ref_column}"),
                                       primary_key=intermediary_table)
        elif field_type.startswith("FK"):
            ref_table, ref_column = field_type.split()[1].split('.')

            attrs[field_name] = Column(Integer, ForeignKey(f"{ref_table}.{ref_column}"),
                                       primary_key=intermediary_table)

        else:
            raise ValueError(f"Unknown field type: {field_type}")

    return type(name, (Base,), attrs)


class JsonGeneration:
    @staticmethod
    def generate_field(field_spec):
        """Generate a field value based on its specification."""
        field_type = field_spec.get("type")
        if field_type == "string":
            return random.choice(field_spec.get("options", []))
        elif field_type == "integer":
            start, end = field_spec.get("range", [0, 100])
            return random.randint(start, end)
        elif field_type == "float":
            start, end = field_spec.get("range", [0.0, 1.0])
            return random.uniform(start, end)
        return None

    @staticmethod
    def generate_object(object_spec):
        """Generate an object based on its specification."""
        result = {}
        for field, spec in object_spec["fields"].items():
            result[field] = JsonGeneration.generate_field(spec)
        return result

    @staticmethod
    def generate_custom_json(custom_json_spec):
        """Generate custom JSON from a list of field specifications."""
        result = {}
        for field_obj in custom_json_spec["fields"]:
            for field_name, field_spec in field_obj.items():
                if field_spec["type"] == "array":
                    result[field_name] = JsonGeneration.generate_array(field_spec)
                elif field_spec["type"] == "object":
                    result[field_name] = JsonGeneration.generate_object(field_spec)
        return result

    @staticmethod
    def generate_array(array_spec):
        """Generate an array based on its specification."""
        item_count = array_spec.get("item_count", 1)
        if isinstance(item_count, str) and item_count.startswith("RANGE"):
            start, end = map(int, item_count[6:-1].split(","))
            item_count = random.randint(start, end)
        return [JsonGeneration.generate_object(array_spec["content"]) for _ in range(item_count)]


def create_random_model_object(model, fields, existing_objects, json_schemas:dict, self_referential=False):
    field_data = {}
    for field_name, field_type_original in fields.items():
        field_type = field_type_original
        is_unique = False
        const = False
        if "UNIQUE" in field_type:
            is_unique = True
            field_type = field_type_original.split('UNIQUE')[0].strip()
        if "CONST" in field_type:
            const = True
            const_value = field_type_original.split('CONST')[-1].strip()
            if const_value == "None": const_value = None
        if "PK" in field_type:
            continue
        elif "bool" in field_type:
            field_data[field_name] = bool(const_value) if const else fake.random_element([True, False])
        elif "uuid" in field_type:
            field_data[field_name] = const_value if const else uuid.uuid4()
        elif "smallint" in field_type:
            if const:
                field_data[field_name] = const_value
            else:
                if "RANGE" in field_type:
                    min_val = int(field_type.split("RANGE(")[1].split(",")[0])
                    max_val = int(field_type.split("RANGE(")[1].split(",")[1].split(")")[0])
                else:
                    min_val, max_val = 0, 10
                field_data[field_name] = random.randint(min_val, max_val)
        elif "float" in field_type:
            if const:
                field_data[field_name] = const_value
            else:
                if "RANGE" in field_type:
                    min_val = int(field_type.split("RANGE(")[1].split(",")[0])
                    max_val = int(field_type.split("RANGE(")[1].split(",")[1].split(")")[0])
                else:
                    min_val, max_val = None, None

                if "DISTRIBUTION(normal," in field_type:
                    mean = float(field_type.split("mean=")[1].split(",")[0])
                    std = float(field_type.split("std=")[1].split(")")[0])
                    new_value = np.random.normal(mean, std)
                    if min_val:
                        # problematic part, better not combine
                        loop_limit=25
                        while (min_val > new_value or new_value > max_val) and loop_limit >0:
                            new_value = np.random.normal(mean, std)
                            loop_limit -=1
                    else:
                        field_data[field_name] = new_value

                elif "DISTRIBUTION(beta," in field_type:
                    alpha = float(field_type.split("alfa=")[1].split(",")[0])
                    beta = float(field_type.split("beta=")[1].split(")")[0])
                    new_value = np.random.beta(alpha, beta)
                    if min_val:
                        field_data[field_name] = min_val + (max_val - min_val) * new_value
                    else:
                        field_data[field_name] = new_value

                else:
                    # just uniform distribution
                    if min_val:
                        field_data[field_name] = fake.random_int(min=min_val, max=max_val)
                    else:
                        field_data[field_name] = random.random()

        elif "integer" in field_type:
            if const:
                field_data[field_name] = const_value
            else:
                if "RANGE" in field_type:
                    min_val = int(field_type.split("RANGE(")[1].split(",")[0])
                    max_val = int(field_type.split("RANGE(")[1].split(",")[1].split(")")[0])
                else:
                    min_val, max_val = None, None

                # just uniform distribution
                if min_val:
                    field_data[field_name] = fake.random_int(min=min_val, max=max_val)
                else:
                    field_data[field_name] = fake.random_int()

        elif "jsonb" in field_type:
            json_spec_key = field_type.split("jsonb:")[1].split(' ')[0]
            result = JsonGeneration.generate_custom_json(json_schemas[json_spec_key])
            json_subfield_value = field_type.split("value:")[1]
            field_data[field_name] = result[json_subfield_value]

        elif "first_name" in field_type:
            field_data[field_name] = const_value if const else (
                fake.unique.first_name() if is_unique else fake.first_name())
        elif "last_name" in field_type:
            field_data[field_name] = const_value if const else fake.last_name()
        elif "email" in field_type:
            field_data[field_name] = const_value if const else email_generator.generate_random_email(is_unique)
        elif "password" in field_type:
            field_data[field_name] = const_value if const else fake.password()
        elif "address" in field_type:
            field_data[field_name] = const_value if const else fake.address()
        elif "country+city" in field_type:

            if const:
                field_data[field_name] = const_value if const else fake.city()
            else:
                country_codes = eval(field_type.split("city(")[1].split(')')[0])
                rand_locale = country_codes[random.randint(0,len(country_codes)-1)]
                field_data[field_name] = f"{Faker(locale=rand_locale).current_country()}, {Faker(locale=rand_locale).city()}"

        elif "timestamp" in field_type:
            if "RANGE" in field_type:
                start_date = datetime.strptime(field_type.split("RANGE(")[1].split(",")[0], '%Y-%m-%d %H:%M:%S')
                end_date = datetime.strptime(field_type.split("RANGE(")[1].split(",")[1].split(")")[0], '%Y-%m-%d %H:%M:%S')
            else:
                start_date, end_date = None, None
            if start_date:
                delta = end_date - start_date
                random_second = random.randint(0, int(delta.total_seconds()))
                random_datetime = start_date + timedelta(seconds=random_second)
                field_data[field_name] = random_datetime
            else:
                field_data[field_name] = const_value if const else fake.date_time()
        elif "phone" in field_type:
            field_data[field_name] = const_value if const else fake.phone_number()
        elif "long_text" in field_type:
            nb_sentences = 5
            if "RANGE" in field_type:
                min_paragraphs = int(field_type.split('RANGE(')[1].split(',')[0])
                max_paragraphs = int(field_type.split('RANGE(')[1].split(',')[1][:-1])
                nb_sentences = random.randint(min_paragraphs, max_paragraphs)

            field_data[field_name] = const_value if const else (
                fake.unique.paragraph() if is_unique else fake.paragraph(
                    nb_sentences=nb_sentences,
                    variable_nb_sentences=False
                ))
        elif "OPTION IN" in field_type:
            options = field_type.split('(')[1].strip(')').split(',')
            field_data[field_name] = fake.random_element(elements=options)
        elif "FK" in field_type:
            foreign_table, foreign_key = field_type.split(' ')[1].split('.')
            if foreign_table == model.__table__.name and not self_referential:
                field_data[field_name] = None
            else:
                get_data = getattr(fake.random_element(existing_objects[foreign_table]), foreign_key)
                field_data[field_name] = get_data
        else:
            raise ValueError(f"Unknown field type: {field_type}")

    return model(**field_data)


def main():
    parser = argparse.ArgumentParser(
        description="Script to populate database according to specified schema.")

    parser.add_argument('-f', '--file',
                        type=str,
                        help='Configuration file with mock data schema.',
                        required=False,
                        default='mock-data.json')

    args = parser.parse_args()

    with open(args.file, 'r') as f:
        json_data = json.load(f)

    # added timeout for 2min, in case the specified connection string is not specified
    engine = create_engine(json_data['connection'], connect_args={"connect_timeout": 10})

    objects_counts = {}
    for table_name in json_data['objects_count']:
        objects_counts[table_name] = json_data['objects_count'][table_name]

    # parse jsons schemas

    json_schemas = {}
    if 'json_schemas' in json_data:
        for json_schema in json_data['json_schemas']:
            for schema_key, inner_schema in json_schema.items():
                json_schemas[schema_key] = inner_schema

    # while loop for generating data
    tables = {}
    models = {}
    special_tables = {}
    print("Processing order of filling tables...")
    pbar = tqdm([x for x in json_data['tables']])
    for table in pbar:
        table_name = table
        intermediary_table = False
        if len(table.split(' ')) > 1:
            table_name = table.split(' ')[1]
            special_tables[table.split(' ')[1]] = table.split(' ')[0]
            if table.split(' ')[0] == 'IntermediaryTable:':
                intermediary_table = True
        tables[table_name] = json_data['tables'][table]
        models[table_name] = create_model(table_name, json_data['tables'][table], intermediary_table=intermediary_table)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()

    # --- order the table creation according to FK constraints ---
    tables_dependencies = []
    for table_name, table in models.items():
        for fk in list(table.__table__.foreign_keys):
            fk_table = fk.target_fullname.split('.')[0]
            if fk_table != table_name:
                tables_dependencies.append((fk_table, table_name))

    directed_graph = nx.DiGraph()
    directed_graph.add_edges_from(tables_dependencies)
    # Perform a topological sort to get the order of processing
    ordered_tables = list(nx.topological_sort(directed_graph))
    for table in tables:
        if table not in ordered_tables:
            ordered_tables.append(table)
    print("\nOrder of creation of the tables: ")
    print("\t" + ' --> '.join(ordered_tables))
    # --- order the table creation according to FK constraints ---

    new_objects = {}
    pbar = tqdm(ordered_tables)
    for table_name in pbar:
        pbar.set_description(f"Processing {table_name}")

        # generate objects
        if table_name in special_tables:
            if 'IntermediaryTable:' in special_tables[table_name]:
                continue
            if re.match(r'SelfReferential\((\d+)%\):', special_tables[table_name]):
                percentage = float(re.match(r'SelfReferential\((\d+)%\):', special_tables[table_name]).group(1))
                for i in range(round(objects_counts[table_name] * (100 - percentage) / 100)):
                    new_obj = create_random_model_object(models[table_name], tables[table_name], new_objects, json_schemas,
                                                         self_referential=False)
                    if table_name not in new_objects:
                        new_objects[table_name] = [new_obj]
                    else:
                        new_objects[table_name].append(new_obj)
                    session.add(new_obj)
                # get new_objects id's for further self references
                session.commit()
                for _ in range(round(objects_counts[table_name] * percentage / 100)):
                    new_obj = create_random_model_object(models[table_name], tables[table_name], new_objects, json_schemas,
                                                         self_referential=True)
                    if table_name not in new_objects:
                        new_objects[table_name] = [new_obj]
                    else:
                        new_objects[table_name].append(new_obj)
                    session.add(new_obj)

        for i in tqdm(range(objects_counts[table_name])):
            new_obj = create_random_model_object(models[table_name], tables[table_name], new_objects, json_schemas)
            if table_name not in new_objects:
                new_objects[table_name] = [new_obj]
            else:
                new_objects[table_name].append(new_obj)
            session.add(new_obj)
        session.commit()

    # -- processing Intermediary Tables ---
    pbar = tqdm([x for x in special_tables if special_tables[x] == "IntermediaryTable:"])
    for table_name in pbar:
        pbar.set_description("Processing %s" % table_name)
        combinations = unique_combinations(tables[table_name], new_objects, objects_counts[table_name])
        i = 0
        for combination in combinations:
            new_obj = models[table_name](
                **{label: integer for integer, label in zip(combination, list(tables[table_name].keys()))})
            if table_name not in new_objects:
                new_objects[table_name] = [new_obj]
            else:
                new_objects[table_name].append(new_obj)
            session.add(new_obj)
        session.commit()
    # -- processing Intermediary Tables ---

    print("\n\n\t\tEXAMPLE ROW FROM EACH TABLE:")
    for example_column in new_objects.keys():
        print(example_column)
        for i in range(1):
            for field in new_objects[example_column][i].__table__.columns.keys():
                print(f"\t{field}: {getattr(new_objects[example_column][i], field)}")
            print('\n')
        print('\n')

    session.close()


if __name__ == "__main__":
    main()
