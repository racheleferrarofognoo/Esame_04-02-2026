from database.DB_connect import DBConnect
from model.artist import Artist


class DAO:

    @staticmethod
    def get_ruoli():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor()
        query = """ select distinct role 
                    from authorship  """
        cursor.execute(query)

        for row in cursor:
            riga = row[0]
            result.append(riga)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artista(ruolo):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor()
        query = """ 
                        select distinct ar.artist_id as id, ar.name as nome
                from authorship a, artists ar, objects o 
                where ar.artist_id = a.artist_id 
                and a.role = %s
                and a.object_id = o.object_id 
                and o.curator_approved = 1 

         """
        cursor.execute(query,(ruolo,))

        for row in cursor:
            result.append(Artist(row[0],row[1]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessioni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor()
        query = """with artistaVal as( 
                        select a.artist_id as artista, count(o.curator_approved) as num_approvati
                        from authorship a, objects o 
                        where a.object_id = o.object_id 
                        and o.curator_approved = 1
                        group by a.artist_id 
                    )
                    select a1.artista as artista1, a2.artista as artista2, 
                            a1.num_approvati as indice_a1 , a2.num_approvati as indice_a2, 
                            abs(a1.num_approvati - a2.num_approvati ) as peso
                    from artistaVal a1, artistaVal a2
                    where a1.artista < a2.artista
                    and abs(a1.num_approvati - a2.num_approvati ) > 0 """
        cursor.execute(query)

        for row in cursor:
            result.append({
                'artista1': row[0],
                'artista2': row[1],
                'indice_a1': row[2],
                'indice_a2': row[3],
                'peso': row[4]

            })

        cursor.close()
        conn.close()
        return result
