import requests , json
import pyodbc

# Paso 1: Obtener los datos de la API JSON
Athorizacion = '2dfd81256bce00dae0dfd47a3a2590e5cfb63d0e'
url = "https://api.cmfchile.cl/api-sbifv3/recursos_api/dolar?apikey=2dfd81256bce00dae0dfd47a3a2590e5cfb63d0e&formato=JSON"  # Reemplaza esto con la URL de tu API JSON
response = requests.get(url)
data = response.json()


with open('./Dolar.json', 'w', encoding='utf8') as f:
        json.dump (data, f, ensure_ascii=False)


with open('Dolar.json') as f:
    data = json.load(f)

Valor = data['Dolares'][0]['Valor']
ValorConvert = format(Valor).replace(',','.')
Fecha = data['Dolares'][0]['Fecha']
# Paso 3: Conectar a la base de datos SQL Server
try:
      conn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.0.1;DATABASE=tpeevo;UID=sa;PWD=gp1433023')
# Paso 4: Crear una tabla para almacenar los datos si aún no existe
      cursor = conn.cursor()
#SQL="INSERT INTO DolarObservado (Dolar, Fecha) VALUES (?, ?)"
      SP='{call Api_DolarObservado (?,?)}'
      #Val=[(853.99,'2023-08-04')]
      Val=(float(ValorConvert),Fecha)
      #print(ValorConvert)
      #print(Val)
      cursor.execute(SP,(Val))
      row = cursor.fetchone()
      while row:
    # Print the row
        print(str(row[0]) + " : " + str(row[1] or '') )
        row = cursor.fetchone()
      conn.commit()
      # Cerrar la conexión
      cursor.close()
      conn.close()

except Exception as e:
 print("Error: %s" % e)