"""
from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route("/dsi/<word>", methods=["GET"])
def procesar(word):
    try:
        print(word)
        # Ejecutamos el script externo con el parámetro de la URL
        result = subprocess.run(['python', 'getInterface.py', word], capture_output=True, text=True)
        print(result)
        output = result.stdout  # Capturamos la salida del script
    except Exception as e:
        output = f"Error: {str(e)}"
    
    return render_template("result.html", output=output)

if __name__ == "__main__":
    app.run(debug=False)
"""

from flask import Flask, render_template, request, redirect, url_for
import subprocess
import json
from .transformation import json_compound_unit_validation


app = Flask(__name__)

@app.route("/api/si/unit", methods=["GET"])

def process():
    
    unit = request.args.get('input')
    
    if unit:
        
        try:
            
            info=json_compound_unit_validation(unit)
            result=info.json_message_response()
            
        except Exception as e:
            output = f"Error: {str(e)}"
            
        return render_template("result.html", data=result)
        
    
    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
