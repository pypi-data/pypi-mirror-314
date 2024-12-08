"""
Este modulo incluye la clase de reproductorMusica()
"""

class Player:
    """
    Esta clase crea un reproductor
    de musica
    """
    def play(self, song):
        """
        Reproduce la cancion que recibio en el constructor

        Parameters:
        song (str): Este es un string que recibio como parametro

        Returns:
        int: devuelve 1 si reproduce con exito, 0 si es lo contrario
        """
        print("Reproduciendo cancion: {}".format(song))

    def stop(self, song):
        """
        Detiene la cancion que recibio en el constructor
        """
        print("Deteniendo cancion: {}".format(song))

    

    
