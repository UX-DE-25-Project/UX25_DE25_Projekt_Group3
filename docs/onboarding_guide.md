# Kontrollera att du har rätt versioner installerade:

'''git --version

#### Kom igång:

''' git clone https://github.com/DITT-TEAM/REPO-NAMN.git
cd REPO-NAMN 


#### Skapa en ny branch innan du börjar jobba:

'''git checkout -b featur/ditt-namn-beskrivning

#### Dubbel kolla att du är på rätt branch:

'''git branch


#### Spara dina ändringar:

'''git add .
'''git commit -m "Kort beskrivning av vad du gjort"
'''git push origin feature/ditt-namn-beskrivning


#### Hämta senaste versionen från main:

'''git checkout main
'''git pull origin main


