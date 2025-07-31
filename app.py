from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

def isbis(anno):
    return (anno % 4 == 0 and anno % 100 != 0) or (anno % 400 == 0)

@app.route('/', methods=['GET', 'POST'])
def calcolo_date():
    risultato = None
    errore = None

    if request.method == 'POST':
        try:
            giornoi = int(request.form['giornoi'])
            mesei = int(request.form['mesei'])
            annoi = int(request.form['annoi'])
            giornof = int(request.form['giornof'])
            mesef = int(request.form['mesef'])
            annof = int(request.form['annof'])

            mesi = {1:30,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
            mesib = mesi.copy()
            mesib[2] = 29

            # controlli iniziali
            if not (1800 <= annoi <= 2500) or not (1800 <= annof <= 2500):
                errore = "Inserisci anni compresi tra 1800 e 2500"
            elif mesei > 12 or mesef > 12:
                errore = "I mesi devono essere compresi tra 1 e 12"
            elif giornoi < 1 or giornof < 1:
                errore = "I giorni devono essere maggiori di zero"
            elif isbis(annoi) and giornoi > mesib[mesei]:
                errore = "Giorno iniziale non valido"
            elif not isbis(annoi) and giornoi > mesi[mesei]:
                errore = "Giorno iniziale non valido"
            elif isbis(annof) and giornof > mesib[mesef]:
                errore = "Giorno finale non valido"
            elif not isbis(annof) and giornof > mesi[mesef]:
                errore = "Giorno finale non valido"
            elif (annof < annoi or
                  (annof == annoi and mesef < mesei) or
                  (annof == annoi and mesef == mesei and giornof < giornoi)):
                errore = "La data iniziale deve essere precedente a quella finale"
            else:
                # tutto valido, calcolo giorni
                ris = 1
                if annoi == annof:
                    if mesei == mesef:
                        ris = giornof - giornoi + 1
                    else:
                        ris += (mesib if isbis(annoi) else mesi)[mesei] - giornoi
                        ris += giornof
                        for i in range(mesei + 1, mesef):
                            ris += (mesib if isbis(annoi) else mesi)[i]
                else:
                    primo_anno = mesib if isbis(annoi) else mesi
                    ultimo_anno = mesib if isbis(annof) else mesi
                    ris += primo_anno[mesei] - giornoi
                    for i in range(mesei + 1, 13):
                        ris += primo_anno[i]
                    ris += giornof
                    for i in range(1, mesef):
                        ris += ultimo_anno[i]
                    for i in range(annoi + 1, annof):
                        ris += 366 if isbis(i) else 365
                risultato = f"Numero di giorni trascorsi: {ris}"

        except Exception as e:
            errore = "Errore nei dati inseriti. Controlla che tutti i campi siano numeri validi."

    return render_template("index.html", risultato=risultato, errore=errore)

if __name__ == "__main__":
    app.run(debug=True)

