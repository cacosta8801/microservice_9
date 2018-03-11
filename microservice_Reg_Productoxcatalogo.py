#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request #import main Flask class and request object
import pika
import MySQLdb
import json
import sys
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs
import cgi


class Microservice:
   
    @staticmethod
    def microserviceLogic (id_producto,id_catalogo,cantidad,estado):

        try:

            db = MySQLdb.connect(host="35.199.86.113", user="root", passwd="root2018", db="microservice")        
            cur = db.cursor()
            fechaCreacion= time.strftime('%Y-%m-%d')
            cur.execute("INSERT INTO `microservice`.`productoxcatalogo` VALUES (null,'"+id_producto+"','"+id_catalogo+"','"+cantidad+"','"+estado+"','"+fechaCreacion+"')")
            db.commit()
            
        except IOError as e:
            db.rollback()
            db.close()
            return "Error BD: ".format(e.errno, e.strerror)
            
        db.close() 

        return {"id":str(cur.lastrowid)  ,"id_producto": id_producto} 

		
app = Flask(__name__)
@app.route('/microservicio/reg_productoxcatalogo',methods=['GET', 'POST'])

def registrar_provedor ():

    if request.method == "POST":

      req_data = request.get_json()
      id_producto = req_data['id_producto']
      id_catalogo = req_data['id_catalogo']
      cantidad = req_data['cantidad']
      estado = req_data['estado']

      
      data = Microservice.microserviceLogic(id_producto,id_catalogo,cantidad,estado)
      
      response = {} 
      response['productoxcatalogo_info'] = "producto x catalogo "+data["id_producto"]+" persistido."
      response['msg'] = 'Hecho'

      return json.dumps(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5008)