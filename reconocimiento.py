## NOtA: PARA CORRER LA PARTE DE LA TOMA DE MEUSTRAS, CORRER EL CODIGO CON PYTHON2. PARA LA PARTE DEL ENTRENAMIENTO, CORRER CON PYTHON3

import sys, time
import math
import numpy as np  
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

if sys.version_info.major == 2:
    from reconocimientoLeap import SampleListener
    from reconocimientoLeap import Leap


def main():

    if sys.version_info.major == 2:
        print("se ejecuta python2")
    # Create a sample listener and controller
        listener = SampleListener()
        controller = Leap.Controller()

    # Have the sample listener receive events from the controller
        controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    #print ("Press Enter to quit...")
        try:
        #sys.stdin.readline()
            while True:
                pass
        except KeyboardInterrupt:
            pass
        finally:
            # Remove the sample listener when done
            controller.remove_listener(listener)

    else:

        print("se ejecuta python3")
        f= open('senas.txt', 'r')
    
        #datos = iris.data[:,:2]
        datos = f.readlines()

        datos = [muestra.strip().split(',') for muestra in datos] #para quitar el '\n' de las muestras y, de paso, con split dividimos las muestras 
                                                                # para que datos sea una matriz


        etiquetas = []

        for muestra in datos:
            etiquetas.append(muestra[-1])  #pone la etiqueta de la muestra en 'etiquetas'
            muestra.pop(-1)                   #elimina la etiqueta de 'datos'


        datos = np.array(datos)
        etiquetas = np.array(etiquetas)

    #print("%s" % etiquetas)

    #print("%s" %  datos)
    
        datasets = train_test_split(datos, 
                            etiquetas,
                            test_size=0.2)

        train_data, test_data, train_labels, test_labels = datasets


        mlp = MLPClassifier(hidden_layer_sizes=(20, 20), #capas ocultas de n neuronas
                    solver='adam', ## que entrene la red con el metodo llamado "adam"
                    learning_rate='constant') # se pone constant porque si esta cerca va a dar pasos cortos, si esta lejos, pasos

        mlp.max_iter=1000000
        #  Realizar el entrenamiento del perceptron con nuestros datos
        train_data=train_data.astype(np.float64)
        train_labels=train_labels.astype(np.float64)   #esto es para que python2 no chille con la seguridad y para que las listas sean float
        test_data=test_data.astype(np.float64)
        test_labels=test_labels.astype(np.float64)

        X1=test_data[:,1]
        X2=test_data[:,2]

        print("\nse imprime x1",X1,"\n")
        print("\naqui x2",X2, "\n")

        mlp.fit(train_data, train_labels)


        #print("Peso  w: ", mlp.coefs_)
        #print("Sesgo b: ", mlp.intercepts_)


        # Para predecir la clase de varios puntos de entrada
        y_estimado = mlp.predict( test_data )
        print("\nprediccion         ",y_estimado, "\n")

        print("\netiquetas de prueba",test_labels, "\n")

        total_puntos_prueba = len(test_labels)
        print("Total de puntos en el conjunto de prueba:", total_puntos_prueba)

        puntos_mal_clasificados = total_puntos_prueba * (1 - accuracy_score(test_labels, y_estimado))
        print("Número de puntos mal clasificados:", puntos_mal_clasificados)

        accuracy = accuracy_score(test_labels, y_estimado)
        print("Precision en el conjunto de prueba: %f" % accuracy)

        # Obtener los índices de los puntos mal clasificados
        equivocaciones = np.where(y_estimado != test_labels)

        print("\n equivoaciones", equivocaciones, "\n")

        #total_puntos_prueba = len(test_labels)
        #print("Total de puntos en el conjunto de prueba:", total_puntos_prueba)

        fig, ax = plt.subplots()

             
        contorno= np.where(y_estimado != test_labels, 'black', 'none')

        ax.scatter(X1, X2, s=60, c=y_estimado, cmap='coolwarm', edgecolor=contorno, linewidths=4)

        #for idx in equivocaciones:
        #    circle = plt.Circle((idx)), radius=2, color='red', fill=False)
        #    plt.gca().add_patch(circle)
        #    plt.colorbar()

        plt.xlabel('X1 (x)')
        plt.ylabel('X2 (y)')

        plt.show()


if __name__ == "__main__":
    main()
