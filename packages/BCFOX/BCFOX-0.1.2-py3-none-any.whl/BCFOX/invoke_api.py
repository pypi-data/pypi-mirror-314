import requests

def invoke_api_list(link, uf):
    url = f"https://api-4.bcfox.com.br/bcjur/views/{parametros}{uf}"

    payload = ""
    headers = {"x-access-token": token}

    response = requests.request("GET", url, data=payload, headers=headers)

    response_api_list = response.json()
    print(f"Response API List: {response_api_list}")

    return response_api_list

# ToDo: Continuar dps q validar as outras
# def invoke_depara_cliente():
#     """
#     Formato:
#         invoke_depara_cliente(parametros, )
#         - Parametros: https://api-4.bcfox.com.br/bcjur/views/depara/ { PARAMETROS/VAI/AQUI }
#     """

#     url = f"https://api-4.bcfox.com.br/bcjur/views/depara/{parametros}"

#     payload = {}
#     headers = {"x-access-token": token}
#     max_attempts = 5
#     for attempt in range(1, max_attempts + 1):
#         try:
#             response = requests.request("GET", url, json=payload, headers=headers)
#             print(response.json())

#             try:
#                 print(response.json()[0])
#                 gi.cliente = response.json()[0]['CLIENTE_BB']
#                 break
#             except BaseException:
#                 gi.obs = "Cliente Invalido ou não configurado"
#                 self.exibir_messagebox("Atenção", f'Atenção! Cliente Invalido ou não configurado para gerar as custas \n cliente:{gi.cliente} idcliente: {gi.id_cliente} \n cnpj: {gi.cnpj_autor}')
#                 break
#         except Exception as e:
#             print(f"Tentativa {attempt} falhou: {e}")
#             if attempt < max_attempts:
#                 print("Tentando novamente em 5 segundos...")
#                 time.sleep(5)
#                 continue
#             else:
#                 raise ValueError("Error no depara cliente")

# def invoke_delete_guias():
#     if gi.status != 3:

#         url = f'https://api-4.bcfox.com.br/bcjur/{self.url}'

#         payload = {"idguia": gi.id_tabela}

#         headers = {"x-access-token": token}

#         max_attempts = 5
#         for attempt in range(1, max_attempts + 1):
#             try:
#                 response = requests.delete(url, json=payload, headers=headers)
#                 # Lança uma exceção se a resposta não for bem-sucedida
#                 response.raise_for_status()
#                 print(response.json())
#                 print(f'{payload}, JSON: {response.json()}')
#                 status = response.json()[0]['STATUS']

#                 if status != 200:
#                     print('Erro ao deletar guias!')
#                     self.invoke_delete_guias()

#                 break

#             except Exception as e:
#                 print(f"Tentativa {attempt} falhou: {e}")

#                 if attempt < max_attempts:
#                     print("Tentando novamente em 5 segundos...")
#                     time.sleep(5)
#                     continue

#                 else:
#                     raise ValueError("Erro no delete guias")

# def invoke_insere_guias():

#     url = f'https://api-4.bcfox.com.br/bcjur/{self.url}'
#     # gi.link_servidor = 'https://bcfiles.bcfox.com.br/docs/arquivos/'

#     # ToDo: Ajustar variáveis quando tiver todas
#     payload = {
#         "idguia": gi.id_tabela,
#         "numseq": 1,
#         "status": gi.status,
#         "nomearquivo": gi.nome_arquivo,
#         "linkarquivo": f'{gi.link_servidor}{gi.nome_arquivo}',
#         "linhadigitavel": gi.linha_digitavel
#     }

#     headers = {"x-access-token": token}

#     max_attempts = 5
#     for attempt in range(1, max_attempts + 1):
#         try:
#             response_insert = requests.post(url, json=payload, headers=headers)
#             # Lança uma exceção se a resposta não for bem-sucedida
#             response_insert.raise_for_status()
#             print(f'Response.json: {response_insert.json()}')
#             print(f'Payload: {payload}')
#             status = response_insert.json()[0]['STATUS']

#             if status != 200:
#                 print('Erro ao inserir guias!')
#                 self.invoke_insere_guias()

#             gi.id_guia = response_insert.json()
#             break

#         except Exception as e:
#             print(f"Tentativa {attempt} falhou: {e}")

#             if attempt < max_attempts:
#                 print("Tentando novamente em 5 segundos...")
#                 time.sleep(5)
#                 continue

#             else:
#                 raise ValueError("Erro no insere guias")

# def valida_qtd_itens():
#     base_api_url = "https://api-4.bcfox.com.br/bcjur"
#     url = f"{base_api_url}/views/guias/iniciais/valida/itens"
#     self.tipo_guia = 'POS'

#     payload = {
#         "id": gi.id_tabela,
#         "uf": self.uf,
#         "tipo": self.tipo_guia,
#         "tipoguia": 0
#     }

#     headers = {
#         "x-access-token": token
#     }

#     max_attempts = 5

#     for attempt in range(1, max_attempts + 1):
#         try:
#             response = requests.request("PATCH", url, headers=headers, data=payload)
#             response_data = response.json()

#             # Exibe o retorno da API
#             print(response_data)

#             # Trata o retorno da API
#             status = response_data[0].get("STATUS")
#             if status == 200:
#                 print("Validação OK!")
#                 print(f"Quantidade Real: {response_data[0].get('QUANTIDADE_REAL')}")
#                 print(f"Quantidade Atual: {response_data[0].get('QUANTIDADE_ATUAL')}")
#                 return status
#             elif status == 400:
#                 print("Quantidade de arquivos no banco incorreta!")
#                 print("")
#                 self.exibir_messagebox(
#                     None, f"Quantidade que deveria ter: {
#                         response_data[0].get('QUANTIDADE_REAL')}\nQuantidade que possui: {
#                         response_data[0].get('QUANTIDADE_ATUAL')}\n")
#             else:
#                 print("Resposta inesperada da API.")
#                 self.exibir_messagebox(None, "Resposta inesperada da API.")

#             return response_data[0]

#         except Exception as e:
#             print(f"Tentativa {attempt} falhou: {e}")

#             if attempt < max_attempts:
#                 print("Tentando novamente em 5 segundos...")
#                 time.sleep(5)
#             else:
#                 print("Máximo de tentativas atingido. Falha ao validar quantidade de itens.")
#                 # Aqui pode ser adicionada uma ação caso o erro persista
#                 break

def invoke_api_proc_final(parametros, payload_vars, token):
    """
    As suas variaveis vão dentro dos '{}' como nos exemplos abaixos:

    Modelo:
        invoke_api_proc_final({parametros}, {payload}, {token})

        - Parametros:
            https://api-4.bcfox.com.br/bcjur/{parametros}  (Passar só o parametro)

        - Payload:
            {"var1": self.var1}
            {"var2": self.var2}
            {"var3": self.var3}
            ...
    """
    # PROC PARA FINALIZAR PROCESSO
    url = f'https://api-4.bcfox.com.br/bcjur/{parametros}'

    payload = {payload_vars}

    print(f'payload: {payload}')

    headers = {"x-access-token": token}

    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            response_insert = requests.put(url, json=payload, headers=headers)
            # Lança uma exceção se a resposta não for bem-sucedida
            response_insert.raise_for_status()
            print(response_insert.json())
            print(payload)

            status = response_insert.json()[0]['STATUS']
            print(status)

            if status != 200:
                print('Erro ao atualizar caso!')
                self.invoke_api_proc_final()

            return status

        except Exception as e:
            print(f"Tentativa {attempt} falhou: {e}")

            if attempt < max_attempts:
                print("Tentando novamente em 5 segundos...")
                time.sleep(5)
                continue

            else:
                raise ValueError("Api proc FINAL falhou")

def invoke_api_proc_log(id_robo, token):
    """Só colocar o ID do robo e o Token direto """

    url = "https://api-4.bcfox.com.br/bcjur/log"

    payload = {
        "id": id_robo
    }

    print(payload)

    headers = {
        "x-access-token": token}

    responseinsert = requests.request(
        "POST", url, json=payload, headers=headers)
    print(responseinsert.json())