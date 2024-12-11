# Functional Programming Utilities
"Functional Programming"  unterscheidet zwischen:

1. Daten
2. Funktionen
3. Aktionen

## Arbeiten mit Daten
Daten sollten als unveränderlich behandelt werden. 
Wird beispielsweise zu einer Liste ein Element hinzugefügt,
so entsteht ein neues "list" Objekt. Die Quelle bleibt
unverändert. Das entspricht dem Verhalten von Strings in Python.
Anders sieht es bei den "Collection" Objekten in Python aus.
Die Klassen:
- list
- dict

können "in place" geaendert werden. "tuple" und "set" hingegen nicht.
Das Modul "collection.py" stellt die Funktionen:
- append_element
- append_collection
- remove_element

bereit mit denen sich:
- list
- dict
- tuple

gleichermassen bearbeiten lassen. Die Quelle bleibt jeweils
unverändert. Das Ergebnis ist immer ein neue Objekt von
der selben Klasse wie die Quelle.  

## Arbeiten mit Funktionen und Iteratoren
Funktionen - oder "pure functions" werden für die Implementierung
der Geschäftsregeln verwendet. Das Ergbnis ist nur von den
Eingangsparaemetern der Funktion abhängig. Die ebenfalls im Rahmen
von "functional programming" häufig verwendeten Iteratoren führen
dabei allerdings zu überraschenden Effekten. 

Beispiel:
```
def get_even_num(list_of_numbers):
    return filter(lambda x: x % 2 == 0, list_of_numbers)

# Create iterator; return even numbers only
coll_even_num = get_even_num([1,2,3,4,5,6,7,8])
# get sum; sum is a "pure function"
print(sum(coll_even_num))
print(sum(coll_even_num))
```
Die Ausgabe ist:
```
        20
        0
```

Das Ergebnis ist schnell erklärt: die Funktion "sum" hat mit dem ersten
Aufruf den Iterator "coll_even_num" aufgebraucht. Beim zweiten Aufruf liefert
diese Iterator dann keine Werte mehr - das Ergebnis ist "0" . 
Führt man das oben gezeigte Beispiel mit einem Objekt der Klasse "list"
aus, so wird ein anderes Ergebnis geliefert:

```
def get_even_num_as_list(list_of_numbers):
    return list(filter(lambda x: x % 2 == 0, list_of_numbers))

# Create iterator; return even numbers only
coll_even_num = get_even_num([1,2,3,4,5,6,7,8])
# get sum; sum is a "pure function"
print(sum(coll_even_num))
print(sum(coll_even_num))
```
Die Ausgabe ist:
```
        20
        20
```

Eine wichtigen Eigenschaften von Python sind generische Algorithmen. 
Diese (so wie die Funktion "sum") können mit verschiedenen Eingangsdaten
arbeiten wie:
- tuple
- list
- iterator



Das Modul "iterator.py" stellt die "Decorators":
- restartable_t
- restartable_m

bereit. Diese lassen sich auf Funktionen anwenden die "Iteratoren" zurückliefern.
Mit dem "Decorator" wird der "Iterator" in eine Klasse verpackt die bei
jedem Aufruf den Funktion ``__iter__()`` einen neuen "Iterator" zurueckliefert.
Dabei verwenden "restartable_t" und "restartable_m" verschiedene Methoden um
jeweils einen neuen "Iterator" zu bekommen:
- "restartable_t" ruft die Funktion die den urspünglichen "Iterator" erzeugt hatte erneut auf.
- "restartable_m" verwendet intern die Funktion "itertools.tee".

Die "restartable_t" und "restartable_m" können natürlich keine Wunder
vollbringen - sie kompensieren lediglich das unerwartete Verhalten des
"Iterators". "restartable_t" tut das auf Kosten der Laufzeit - "restartable_m" auf
Kosten des Speicherplatzes. 

Beispiel:
```
from  klfuncutil.iterator import restartable_t

@restartable_t
def get_even_num(list_of_numbers):
    return filter(lambda x: x % 2 == 0, list_of_numbers)

# Create iterator; return even numbers only
coll_even_num = get_even_num([1,2,3,4,5,6,7,8])
# get sum; sum is a "pure function"
print(sum(coll_even_num))
print(sum(coll_even_num))
```
Die Ausgabe ist:
```
        20
        20
```

