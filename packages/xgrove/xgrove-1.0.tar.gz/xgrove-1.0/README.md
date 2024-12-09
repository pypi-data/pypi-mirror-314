# xGrove Python Package

Das `xgrove`-Paket bietet eine Klasse zur Berechnung von "Surrogate Groves", um Entscheidungsbäume zu interpretieren. Es ist inspiriert von Methoden aus dem Bereich der Interpretable Machine Learning (IML) und bietet eine Reihe von Funktionen zur Analyse und Visualisierung von Entscheidungsbaumstrukturen.

## Installation

Stelle sicher, dass die erforderlichen Abhängigkeiten installiert sind:

```bash
pip install -r requirements.txt
```

## Klassen und Methoden

### Klasse: `xgrove`

Die Hauptklasse `xgrove` wird verwendet, um "Surrogate Groves" zu erstellen und statistische Analysen durchzuführen.

#### Konstruktor

```python
xgrove(
    model, 
    data: pd.DataFrame, 
    ntrees: np.array = np.array([4, 8, 16, 32, 64, 128]), 
    pfun = None, 
    shrink: int = 1, 
    b_frac: int = 1, 
    seed: int = 42, 
    grove_rate: float = 1
)
```

##### Parameter:
- **model**: Das zu analysierende Modell, typischerweise ein beliebiges ML-Modell.
- **data**: Ein `pandas.DataFrame`, das die Eingabedaten enthält.
- **ntrees**: Ein `np.array`, das die Anzahl der Bäume im Grove angibt.
- **pfun**: Eine Funktion zur Erstellung des Surrogate-Ziels. Falls `None`, wird das Modell zur Vorhersage genutzt.
- **shrink**: Der Shrinkage-Faktor für das Gradient Boosting.
- **b_frac**: Die Fraktion der Stichprobe, die verwendet wird.
- **seed**: Der Seed für die Reproduzierbarkeit.
- **grove_rate**: Die Lernrate für das Grove.

### Methode: `getSurrogateTarget()`

Erzeugt das Surrogate-Ziel basierend auf den Eingabedaten und dem Modell oder der benutzerdefinierten `pfun`.

```python
def getSurrogateTarget(self, pfun):
    if self.pfun is None:
        target = self.model.predict(self.data)
    else:
        target = pfun(model=self.model, data=self.data)
    return target
```

### Methode: `getGBM()`

Erzeugt ein Gradient Boosting Modell (GBM) mit den angegebenen Parametern.

```python
def getGBM(self):
    grove = GradientBoostingRegressor(
        n_estimators=self.ntrees,
        learning_rate=self.shrink,
        subsample=self.b_frac
    )
    return grove
```

### Methode: `encodeCategorical()`

Codiert kategoriale Variablen mithilfe von One-Hot-Encoding (OHE).

```python
def encodeCategorical(self):
    categorical_columns = self.data.select_dtypes(include=['object', 'category']).columns
    data_encoded = pd.get_dummies(data, columns=categorical_columns)
    return data_encoded
```

### Methode: `upsilon()`

Berechnet die Upsilon-Statistik, die das Verhältnis zwischen erklärtem und unerklärtem Fehler angibt, sowie die Korrelation zwischen den Vorhersagen des Modells und den echten Werten.

```python
def upsilon(self, pexp):
    ASE = statistics.mean((self.surrTar - pexp) ** 2)
    ASE0 = statistics.mean((self.surrTar - statistics.mean(self.surrTar)) ** 2)
    ups = 1 - ASE / ASE0
    rho = statistics.correlation(self.surrTar, pexp)
    return ups, rho
```

### Methode: `get_result()`

Gibt eine Liste der zentralen Ergebnisse zurück: Erklärung, Regeln, Groves und Modell.

```python
def get_result(self):
    res = [self.explanation, self.rules, self.groves, self.model]
    return res
```

### Methode: `plot()`

Eine Methode zur Erstellung eines Upsilon-Rules-Plots für den Surrogate Grove. Diese Methode funktioniert ähnlich wie die Plotfunktion in R.

```python
def plot(self, abs="rules", ord="upsilon"):
    i = self.explanation.columns.get_loc(abs)
    j = self.explanation.columns.get_loc(ord)
    plt.plot(self.explanation.iloc[:, i], self.explanation.iloc[:, j], label=f"{abs} vs {ord}", marker="o")
    plt.xlabel(abs)
    plt.ylabel(ord)
    plt.title("Upsilon-Rules Curve")
    plt.show()
```

### Methode: `calculateGrove()`

Berechnet die Performance des Modells und extrahiert Groves sowie die dazugehörigen Regeln. Diese Methode füllt die Erklärungs- und Interpretationsdaten und ruft am Ende die `upsilon`-Methode auf, um den Upsilon-Wert zu berechnen.

```python
def calculateGrove(self):
    explanation = []
    groves = []
    interpretation = []

    # Für jede Anzahl an Bäumen
    for nt in self.ntrees:
        predictions = self.surrGrove.staged_predict(self.data)
        predictions = [next(predictions) for _ in range(nt)][-1]
        rules = []
        
        # Extrahiere Regeln aus den Entscheidungsbäumen
        for tid in range(nt):
            tree = self.surrGrove.estimators_[tid, 0].tree_
            for node_id in range(tree.node_count):
                if tree.children_left[node_id] != tree.children_right[node_id]:  # Splitsnode
                    rule = {
                        'feature': tree.feature[node_id],
                        'threshold': tree.threshold[node_id],
                        'pleft': tree.value[tree.children_left[node_id]][0][0],
                        'pright': tree.value[tree.children_right[node_id]][0][0]
                    }
                    rules.append(rule)
            rules_df = pd.DataFrame(rules)
            groves.append(rules_df)

        # Berechne Upsilon und Korrelation
        upsilon, rho = self.upsilon(predictions)

        # Ergebnisse speichern
        explanation.append([nt, len(rules_df), upsilon, rho])

    # Ergebnisdaten aufbereiten
    groves = pd.DataFrame(groves)
    explanation = pd.DataFrame(explanation, columns=["trees", "rules", "upsilon", "cor"])
    
    self.explanation = explanation
    self.rules = groves
    self.model = self.surrGrove

    self.result = self.get_result()
    return self.result
```
