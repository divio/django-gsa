# -*- coding: utf-8 -*-
import time
import datetime
from gsa import GSA

def run_test():
    phrase_set = "peperoncini  ligne le site culinaire de haute hackbraten Vous y trouverez tout un choix d'excellentes recettes, de Kondensmilch, Eier und Sauerrahm glatt Mehl, Backpulver und Salz mischen. Zur Milch-Eier".split(" ")
    
    c = 0
    while True:
        phrase = phrase_set[c]
        
        now = datetime.datetime.now()
        result = GSA("94.230.210.4").query(phrase)
        print ">> OK", datetime.datetime.now() - now, result.count(), phrase
        time.sleep(1)
        c += 1
        if c >= len(phrase_set):
            c = 0
            
        
if __name__ == "__main__":
    run_test()