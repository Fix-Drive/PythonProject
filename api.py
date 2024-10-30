import requests

url = 'https://api.infosimples.com/api/v2/consultas/sinesp/veiculo'
args = {
  "placa":       "EUX8543",
  "login_cpf":   "44954401879",
  "login_senha": "Marley@gabi02",
  "token":       "VWgA6SlnN2ffE5d64JwlTuTf79uSVTWN9zw4PxU_",
  "timeout":     300
}

response = requests.post(url, args)
response_json = response.json()
response.close()

if response_json['code'] == 200:
  print("Retorno com sucesso: ", response_json['data'])
elif response_json['code'] in range(600, 799):
  mensagem = "Resultado sem sucesso. Leia para saber mais: \n"
  mensagem += "Código: {} ({})\n".format(response_json['code'], response_json['code_message'])
  mensagem += "; ".join(response_json['errors'])
  print(mensagem)

print("Cabeçalho da consulta: ", response_json['header'])
print("URLs com arquivos de visualização (HTML/PDF): ", response_json['site_receipts'])