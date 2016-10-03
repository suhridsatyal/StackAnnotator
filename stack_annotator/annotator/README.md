#API Documentation

##End Points

###GET
```
/api/annotations/{id}
```
Gets a set of annotations based on the id. The options are by question id or answer id

Example:
```
/api/annotations?answer_id=3
``` 
Will search for all annotations where the answer_id is 3
```
/api/annotation/{id}
```
Gets a specific annotation with particular id

###POST
```
/api/annotation
```
Posts an annotation
