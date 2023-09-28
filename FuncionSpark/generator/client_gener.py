'''
Modulo para crear un csv de n clientes con los datos:
    - Nombre
    - Direccion
    - Telefono
    - Email
usando la libreria Faker
El csv se guardara en la carpeta FuncionSpark/data
'''

import os

from faker import Faker
import pandas as pd

class Client():
    def __init__(self, faker_obj):
        self.name = faker_obj.name()
        self.phone = faker_obj.phone_number()
        self.email = faker_obj.email()

    
    def __repr__(self) -> str:
        return f"""
                Name: {self.name}
                Phone: {self.phone}
                Email: {self.email}
                """


def gen_a_client(faker_obj) -> Client:
    return Client(faker_obj)
    
    
def gen_clients_df(faker_obj, clients_number:int) -> pd.DataFrame:
    clients:list[dict] = [vars(Client(faker_obj)) for _ in range(0,clients_number)]
    df_clients = pd.DataFrame(data=clients)
    return df_clients


def df_2_csv(df:pd.DataFrame, path = '../data/clients.csv') -> None:
    if not os.path.exists(path):
        df.to_csv(
            index = False,
            path_or_buf= path
        )
    else:
        #dataframe de clientes ya existe
        existing_clients_df = pd.read_csv(path)
        pd.concat([existing_clients_df, df], ignore_index=True)\
            .to_csv(index=False, path_or_buf= path)


if __name__ == "__main__":
    fake = Faker('es_ES') #Crear un objeto Faker en Español
    #new_client:Client = gen_a_client(fake)
    df_clients = gen_clients_df(fake, 2)
    df_2_csv(df_clients)
    
    
    