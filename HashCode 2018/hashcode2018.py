import sys
import math
from heapq import heappush, heappop


class Car:
    def __init__(self):
        self.position = [0,0]
        self.finishTime = 0

    
    def getPosition(self):
        """
            Posizione corrente
        """
        return self.position

    def distance(self, p):
        """
            Calcola la distanza: p deve essere una tupla (x, y)    
        """
        return abs(self.position[0]-p[0]) + abs(self.position[1]-p[1])

   
    def assignRide(self, r, time):
        """
            Aggiorna le variabile della car quando prende una corsa
        """
        self.position = r.getDestination()
        self.finishTime = max(time + self.distance(r.origin), r.getStart()) + r.distance()

    def getFinishTime(self):
        """
            Ritorna il tempo di fine corsa: quando la car sarà di nuovo avaible
        """
        return self.finishTime
    

class Ride():
    def __init__(self, data):
        self.origin = data[0][:2]
        self.destination = data[0][2:4]
        self.start = data[1]
        self.finish = data[2] #The latest
        self.endTime = self.start + self.distance()


    def getOrigin(self):
        """
            Get della posizione di inizio della corsa.
            Ritorna una tupla (x, y)
        """
        return self.origin

    def getDestination(self):
        """
            Get della posizione di fine della corsa.
            Ritorna una tupla (x, y)
        """
        return self.destination

    def getStart(self):
        """
            Get del tempo di inizio della corsa.
            Ritorna un intero x
        """
        return self.start

    def getEnd(self):
        """
            Get del tempo di fine della corsa.
            Ritorna un intero x
        """
        return self.endTime   
    
    def distance(self):
        """
            Distanza tra i due punti: inizio e fine corsa.
            Metrica lineare, specifica della challenge.
            Ritorna un intero x
        """
        return abs(self.origin[0] - self.destination[0]) + abs(self.origin[1] - self.destination[1])


        
        
    def obsolete(self, currentTime):
        """
            Valuta se una corsa è ancora "avaible_pending" o è "obsolete".
        """
        return currentTime + self.distance() >= self.finish
    

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def parse_input(filename):

    with open(filename, 'r') as f:
        #   First line of the input:
        """
            R - Rows of the map
            C - Columns of the map
            F - Vehicles in the fleet
            N - Number of rides
            B - Per-ride bonus: ride starts on time
            T - Steps of the simulation
        """
        params = list(map(int, f.readline().split()))

        #   List with all the rides
        rides = []
        
        for line in f:

            #   Get values from ride line
            ride = list(map(int, line.split()))

            #   4-uple with origin and destination in that order
            coordenates = tuple(ride[:4])

            #   Earliest step to pick
            earliest = ride[-2]

            #   Latest tick to arrive at destination
            latest = ride[-1]

            #   List of all rides
            rides.append((coordenates, earliest, latest))


        return params, rides

#       TBD
"""
def score_ride(x, rides):
    #x indice di corsa completata
    time = 0
    pos = [0, 0]
    score = 0
    for n in x:
        time += distance(pos, rides[n].getOrigin())
        pos = rides[n].getDestination()
        if time <= rides[n].getStart():
            time = rides[n].getStart()
        if time + rides[n].distance() < rides[n].getEnd():
            score += rides[n].distance()
            else score += rides[n].distance() + rides[n].bonus()
        time += rides[n].distance()

    return score
"""

def evaluate(rides, cars, TIME, maxDistance):
    time = 0
    pending_rides = [x for x in range(len(rides))]
    #   Best performance for inputs A and C
    #pending_rides.sort(key = lambda x: rides[x].distance(), reverse = True)
    available_cars = [x for x in range(len(cars))]
    taken = []  #   List of cars engaged in a ride

    evaluation = [[] for _ in cars]
    while time < TIME and pending_rides:

        while taken:
            car = taken.pop(0)
            if car[0] != time:
                taken.append(car)
                break
            available_cars.append(car[1])

        #   Best performance for the rest of inputs
        pending_rides.sort(key = lambda x: maxDistance if (rides[x].getEnd() == time) else 1 / (rides[x].getEnd() - time), reverse = True)
        while pending_rides and available_cars:
   
            min_d = maxDistance
            assigned_car = 0
            for car in available_cars:
                if min_d > distance(cars[car].getPosition(), rides[pending_rides[0]].getOrigin()):
                    min_d = distance(cars[car].getPosition(), rides[pending_rides[0]].getOrigin())
                    assigned_car = car

            cars[assigned_car].assignRide(rides[pending_rides[0]], time)
            
            evaluation[assigned_car].append(pending_rides[0])
            pending_rides.pop(0)
            taken.append((cars[assigned_car].getFinishTime(), assigned_car))
            available_cars.remove(assigned_car)

            while pending_rides and rides[pending_rides[0]].obsolete(time):
                pending_rides.pop(0)
            
        time = min(taken)[0]

    return evaluation


def main():
    data, rides_ = parse_input(sys.argv[1])
    rows, cols, n_vehicles, n_Rides, bonus, TIME = data
    
    cars = [Car() for _ in range(n_vehicles)]
    rides = [Ride(elem) for elem in rides_]
    maxDistance = rows + cols

    evaluation = evaluate(rides, cars, TIME, maxDistance)
    
    with open(sys.argv[2], 'w') as f:    
        for l in evaluation:
            l = list(map(str, l))
            line = str(len(l)) + ' ' + ' '.join(l) + '\n'
            f.write(line)


if __name__ == "__main__":
    main()