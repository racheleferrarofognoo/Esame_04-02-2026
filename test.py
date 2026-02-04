from database.dao import DAO
from model.model import Model

dao = DAO()
model = Model()

print(dao.get_connessioni())

print(model.get_ruoli())

model.build_graph('Maker')
print(model.num_archi_nodi())