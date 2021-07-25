from flask import Flask, flash 
from flask_app import app
import re
from flask_app.config.mysqlconnection import connectToMySQL


class Recipes():

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.under30 = data['under30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.made_on = data['made_on']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']

    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, under30, description, instructions, made_on, users_id) VALUES (%(name)s, %(under30)s, %(description)s, %(instructions)s, %(made_on)s , %(user_id)s);"

        results = connectToMySQL('recipes_schema').query_db(query, data)

        return results

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"

        results = connectToMySQL('recipes_schema').query_db(query)

        table = []

        for item in results:
            table.append(cls(item))

        return table


    @classmethod
    def show_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"

        results = connectToMySQL('recipes_schema').query_db(query, data)

        return cls(results[0])

    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET  name = %(name)s, under30 = %(under30)s, description = %(description)s, instructions = %(instructions)s, made_on = %(made_on)s WHERE id = %(id)s"

        results = connectToMySQL('recipes_schema').query_db(query, data)

        return results

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"

        results = connectToMySQL('recipes_schema').query_db(query, data)

        return results




















    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 3:
            flash("Name needs to be more than 3 characters")
            is_valid = False

        if len(data['description']) < 3:
            flash("Description needs to more than 3 characters")
            is_valid = False

        if len(data['instructions']) < 3:
            flash("Instructions needs to more than 3 characters")
            is_valid = False
        return is_valid


